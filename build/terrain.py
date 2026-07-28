#!/usr/bin/env python3
"""Terrain field for the three views (register A2-d, round 3). Run with venv python:

    ./venv/bin/python3 build/terrain.py            # fetch (cached) + render all
    ./venv/bin/python3 build/terrain.py --render   # skip fetch, render from cache

SOURCE (downloads user-approved, round 3): AWS Open Data 'Terrain Tiles',
terrarium encoding — land elevation from NASA/USGS SRTM (public domain),
ocean bathymetry from NOAA ETOPO1 (public domain); tile service courtesy
Mapzen/AWS (attribution carried in the app's About and README).
  https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png
  elevation_m = R*256 + G + B/256 - 32768

WHAT THIS PRODUCES: per view (meso z8, basin z11, city z12) and per season
(dry Nov-Apr, wet May-Oct), a hillshaded hypsometric basemap JPEG in web/img/,
rendered IN THE APP'S PROJECTION — plate carrée over the view extent with the
app's cos(mid-lat) x-scale, so the basemap and the vector layers are a matched
pair (ARCHITECTURE-PATTERNS §6: change them together or not at all).

The seasonal palettes are a MODELLED rendering choice (greener wet season,
straw dry season), not a land-cover dataset; the About panel says so. The
elevations and the shelf are measured data. The 1519 lakes are NOT in the
terrain (the modern DEM post-dates the drainage); the app draws the named
reconstruction's lake polygons over this base — reconstruction over
measurement, layered honestly.

Self-checks before writing: Popocatépetl > 4,700 m in the basin grid; the
Basin floor 2,150-2,350 m; the Gulf off Veracruz deeper than -500 m; the
Yucatán shelf shallower than -300 m.
"""

from __future__ import annotations

import io
import math
import os
import sys
import time
import urllib.request

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "terrain")
OUT = os.path.join(ROOT, "web", "img")
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

# view -> (lon0, lat0, lon1, lat1, zoom, out_width)
# TERRAIN EXTENTS — a matched pair with DATA.meta.terrain in emit.py (the app
# positions each image by these exact extents). The CITY image is wider than
# the city camera preset on purpose, so panning near the island stays sharp.
# z12 is SRTM's native grain (~30 m) at this latitude; the round-4 curvature
# and slope shading synthesise legible sub-grid texture from the measured
# surface itself (ARCHITECTURE-PATTERNS §7), never from noise.
VIEWS = {
    "meso":  (-105.0, 13.5, -86.5, 22.5, 9, 3072),
    "basin": (-99.55, 19.02, -98.55, 19.95, 12, 2600),
    "city":  (-99.32, 19.27, -98.94, 19.57, 12, 2400),
}

SEASONS = ("dry", "wet")


def merc_xy(lon, lat, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x, y


def fetch_tiles(view):
    lon0, lat0, lon1, lat1, z, _ = VIEWS[view]
    x0, y0 = merc_xy(lon0, lat1, z)          # top-left
    x1, y1 = merc_xy(lon1, lat0, z)          # bottom-right
    xs = range(int(x0), int(x1) + 1)
    ys = range(int(y0), int(y1) + 1)
    got = 0
    for x in xs:
        for y in ys:
            p = os.path.join(CACHE, str(z), str(x), f"{y}.png")
            if os.path.exists(p):
                continue
            os.makedirs(os.path.dirname(p), exist_ok=True)
            url = URL.format(z=z, x=x, y=y)
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(url, timeout=30) as r:
                        data = r.read()
                    with open(p, "wb") as f:
                        f.write(data)
                    got += 1
                    break
                except Exception as e:                     # noqa: BLE001 - report, retry
                    if attempt == 2:
                        raise RuntimeError(f"tile {url} failed: {e}") from e
                    time.sleep(1.5 * (attempt + 1))
    n = len(xs) * len(ys)
    print(f"  {view}: z{z} {len(xs)}x{len(ys)} = {n} tiles ({got} fetched, {n-got} cached)")
    return (int(x0), int(y0), int(x1), int(y1), z)


def mosaic(view):
    """Elevation mosaic (float32 metres) + its mercator pixel origin."""
    x0, y0, x1, y1, z = fetch_tiles(view)
    W, H = (x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256
    E = np.zeros((H, W), np.float32)
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            p = os.path.join(CACHE, str(z), str(tx), f"{ty}.png")
            a = np.asarray(Image.open(p).convert("RGB"), np.float32)
            e = a[:, :, 0] * 256.0 + a[:, :, 1] + a[:, :, 2] / 256.0 - 32768.0
            E[(ty - y0) * 256:(ty - y0 + 1) * 256,
              (tx - x0) * 256:(tx - x0 + 1) * 256] = e
    return E, x0, y0, z


def sample_equirect(view):
    """Resample the mercator mosaic onto the app's plate-carrée grid."""
    lon0, lat0, lon1, lat1, z, W = VIEWS[view]
    kx = math.cos(math.radians((lat0 + lat1) / 2.0))
    H = int(round(W * ((lat1 - lat0) * 110.6) / ((lon1 - lon0) * 111.32 * kx)))
    E, mx0, my0, z = mosaic(view)
    lons = np.linspace(lon0, lon1, W, dtype=np.float64)
    lats = np.linspace(lat1, lat0, H, dtype=np.float64)      # top row = north
    n = 2.0 ** z
    px = (lons + 180.0) / 360.0 * n * 256.0 - mx0 * 256.0
    py = ((1.0 - np.arcsinh(np.tan(np.radians(lats))) / math.pi) / 2.0
          * n * 256.0 - my0 * 256.0)
    px = np.clip(px, 0, E.shape[1] - 1.001)
    py = np.clip(py, 0, E.shape[0] - 1.001)
    x0i = px.astype(np.int32); y0i = py.astype(np.int32)
    fx = (px - x0i)[None, :]; fy = (py - y0i)[:, None]
    a = E[y0i][:, x0i]; b = E[y0i][:, x0i + 1]
    c = E[y0i + 1][:, x0i]; d = E[y0i + 1][:, x0i + 1]
    G = a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
    # metres per output pixel, for the hillshade gradient
    mpp_x = (lon1 - lon0) * 111320.0 * kx / W
    mpp_y = (lat1 - lat0) * 110600.0 / H
    return G.astype(np.float32), (mpp_x + mpp_y) / 2.0


def _lut(stops, e):
    """Piecewise-linear palette: stops = [(elev, (r,g,b)), ...]."""
    es = np.array([s[0] for s in stops], np.float32)
    cols = np.array([s[1] for s in stops], np.float32)
    out = np.empty(e.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(e, es, cols[:, c])
    return out

LAND = {
    "dry": [(0, (154, 158, 108)), (700, (150, 148, 96)), (1600, (146, 138, 88)),
            (2250, (162, 150, 100)), (2700, (104, 112, 74)), (3200, (78, 92, 62)),
            (3900, (120, 122, 112)), (4400, (158, 160, 160)), (4750, (232, 236, 240)),
            (5700, (248, 250, 252))],
    "wet": [(0, (96, 138, 84)), (700, (92, 132, 78)), (1600, (94, 126, 74)),
            (2250, (118, 134, 84)), (2700, (74, 100, 62)), (3200, (58, 82, 52)),
            (3900, (110, 116, 106)), (4400, (152, 156, 158)), (4750, (230, 234, 238)),
            (5700, (246, 248, 252))],
}
OCEAN = [(-6500, (14, 30, 52)), (-3500, (18, 40, 66)), (-1500, (28, 56, 88)),
         (-400, (40, 76, 108)), (-120, (58, 104, 132)), (-25, (92, 142, 156)),
         (0, (118, 160, 164))]


def render(view):
    E, mpp = sample_equirect(view)
    gy, gx = np.gradient(E, mpp)
    # hillshade, sun from the NW at 45 degrees
    az, alt = math.radians(315), math.radians(45)
    slope = np.arctan(np.hypot(gx, gy) * 1.4)          # gentle exaggeration
    aspect = np.arctan2(-gx, gy)
    hs = (math.sin(alt) * np.cos(slope)
          + math.cos(alt) * np.sin(slope) * np.cos(az - aspect))
    hs = np.clip(hs, 0, 1)
    # round 4 — sub-grid legibility from the measured surface itself:
    #   curvature (Laplacian): darken ravine floors, lift ridge crests;
    #   steep ground (> ~28 deg) shifts toward bare rock.
    # The Laplacian must be taken on a lightly smoothed surface, and its gain
    # must FADE OUT once the output grid is finer than SRTM's ~30 m native
    # grain — otherwise bilinear upsampling's second derivative renders as a
    # checkerboard that reads as structure (TRAPS B1, caught visually in the
    # first city render).
    Es = E.copy()
    for _ in range(2):
        Es = (Es + np.roll(Es, 1, 0) + np.roll(Es, -1, 0)
              + np.roll(Es, 1, 1) + np.roll(Es, -1, 1)) / 5.0
    lap = (np.roll(Es, 1, 0) + np.roll(Es, -1, 0) + np.roll(Es, 1, 1)
           + np.roll(Es, -1, 1) - 4 * Es) / max(mpp, 1.0)
    native_gain = min(1.0, max(0.0, (mpp - 18.0) / 25.0))
    curv = np.clip(lap * 6.0 * native_gain, -0.22, 0.22)
    hs2 = np.clip(hs + curv, 0, 1.15)
    rock = np.clip((slope - math.radians(28)) / math.radians(18), 0, 1)[..., None]
    land = E >= 0
    outs = {}
    for season in SEASONS:
        col = _lut(LAND[season], np.clip(E, 0, 5700))
        col = col * (1 - rock * 0.45) + np.array([124, 118, 108], np.float32) * rock * 0.45
        oce = _lut(OCEAN, np.clip(E, -6500, 0))
        shade_l = (0.40 + 0.72 * hs2)[..., None]
        shade_o = (0.82 + 0.25 * hs)[..., None]
        img = np.where(land[..., None], col * shade_l, oce * shade_o)
        # shoreline glint: thin bright line where |E| is tiny
        shore = (np.abs(E) < 6)[..., None]
        img = np.where(shore & ~land[..., None], img * 1.25 + 18, img)
        outs[season] = np.clip(img, 0, 255).astype(np.uint8)
    return E, outs


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    total = 0
    for view in VIEWS:
        E, outs = render(view)
        # ---- self-checks: the terrain must contain the world we know ----
        lon0, lat0, lon1, lat1, _, _ = VIEWS[view]
        def at(lon, lat):
            j = int((lon - lon0) / (lon1 - lon0) * (E.shape[1] - 1))
            i = int((lat1 - lat) / (lat1 - lat0) * (E.shape[0] - 1))
            return float(E[i, j])
        if view == "basin":
            popo = at(-98.628, 19.023)
            floor = at(-99.05, 19.45)
            assert popo > 4700, f"Popocatépetl only {popo:.0f} m — wrong tiles?"
            assert 2150 < floor < 2350, f"Basin floor {floor:.0f} m — projection slip?"
            print(f"  basin checks: Popocatépetl {popo:.0f} m, lakebed {floor:.0f} m")
        if view == "meso":
            gulf = at(-95.5, 19.6)
            shelf = at(-90.0, 20.5)
            assert gulf < -500, f"Gulf off Veracruz {gulf:.0f} m — bathymetry missing?"
            assert shelf > -300, f"Campeche shelf {shelf:.0f} m — too deep?"
            print(f"  meso checks: Gulf {gulf:.0f} m, Campeche shelf {shelf:.0f} m")
        for season, img in outs.items():
            p = os.path.join(OUT, f"terrain-{view}-{season}.jpg")
            Image.fromarray(img).save(p, quality=84, optimize=True)
            kb = os.path.getsize(p) / 1024
            total += kb
            print(f"  wrote {os.path.basename(p):24} {img.shape[1]}x{img.shape[0]}  {kb:6.0f} KB")
    print(f"  total basemaps {total/1024:.2f} MB (budget 25 MB)")


if __name__ == "__main__":
    if "--render" not in sys.argv:
        pass          # fetch happens lazily inside mosaic()
    main()
