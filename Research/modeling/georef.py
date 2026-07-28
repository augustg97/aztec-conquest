"""Georeference frame: anchors, authored geometry, and residuals. Stdlib only.

THE CANONICAL LAKE RECONSTRUCTION IS NAMED HERE (register A2):

    González Aparicio, Luis (1973). *Plano reconstructivo de la región de
    Tenochtitlan*. SEP / INAH, Mexico City. (1st map ed. 1968; reissued 1980.)

It is the planimetric reconstruction the archaeological literature itself uses
(Templo Mayor alignment studies, settlement and hydraulic-management papers),
which is exactly the property the standard-for-done needs. Competing
reconstructions exist (Niederberger's palaeoenvironmental work; the Sanders/
Parsons/Santley survey base maps); per SCOPE §5 the model names ONE and never
averages them.

WHAT THIS MODULE IS, HONESTLY: the geometry below is AUTHORED at visualization
grade — simplified polylines and polygons drawn against (a) the documented
archaeological anchors table, (b) the modern street lines that follow the
causeways (Calzada México-Tacuba; Calzada de Tlalpan / the Iztapalapan road;
Calzada de los Misterios; Avenida Chapultepec for the aqueduct), and (c) the
published shape of the González Aparicio reconstruction. It is faithful for
visualization, not survey-grade (the Territorial US precedent). The anchors are
measurements; the polygons are a reconstruction OF a reconstruction and carry
confidence fields saying so. audit_witness.py scores what is actually drawn
against the anchors and against independent literature values (city footprint
area, lake area, containment relations) — that audit, not this file, is the
honesty instrument.

Pixel-space georeferencing of the 1524 Nuremberg map scan (control points ->
affine fit -> residual) requires the scan itself and is register item A2-b,
recorded as not done this round.

Run me:  python3 georef.py
"""

from __future__ import annotations

import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CONFIDENCE = ("good", "moderate", "contested", "none")

# ---------------------------------------------------------------------------
# the anchor table — documented locations the drawn world must agree with
# ---------------------------------------------------------------------------
# lat, lon, what pins it, confidence
ANCHORS = {
    "templo-mayor":        (19.43481, -99.13177, "Templo Mayor excavation (INAH), the city's ceremonial centre", "good"),
    "tlatelolco-templo":   (19.45056, -99.13722, "Tlatelolco templo mayor, Plaza de las Tres Culturas", "good"),
    "chapultepec-springs": (19.42056, -99.18194, "Chapultepec hill and springs — the aqueduct's source", "good"),
    "tepeyac":             (19.48472, -99.11722, "Tepeyacac hill — north causeway terminal", "good"),
    "tacuba-plaza":        (19.45900, -99.18800, "Tlacopan centre — west causeway terminal", "good"),
    "iztapalapa-centre":   (19.35700, -99.09200, "Iztapalapan centre — south causeway terminal", "moderate"),
    "coyoacan-plaza":      (19.34670, -99.16170, "Coyohuacan centre — southwest causeway terminal", "good"),
    "culhuacan":           (19.33720, -99.10780, "Cōlhuahcan centre, on the Iztapalapa peninsula strait", "good"),
    "cerro-estrella":      (19.33630, -99.08970, "Huixachtlan (Cerro de la Estrella) — New Fire hill", "good"),
    "texcoco-centre":      (19.50800, -98.88300, "Tetzcohco centre; the brigantine canal ran to the lakeshore west of it", "good"),
}

# ---------------------------------------------------------------------------
# authored geometry (visualization grade; sources + confidence per feature)
# ---------------------------------------------------------------------------
# Every feature: kind, points [(lon, lat)...], closed?, source note, confidence.

GEOMETRY = {
    # -- the four arteries and the works --------------------------------------
    "causeway-tlacopan": {
        "kind": "causeway", "closed": False, "confidence": "good",
        "source": "line of Calzada México-Tacuba; González Aparicio (1973)",
        "note": "the Noche Triste route",
        "points": [(-99.1318, 19.4348), (-99.1470, 19.4390),
                   (-99.1720, 19.4480), (-99.1880, 19.4590)],
    },
    "causeway-tepeyac": {
        "kind": "causeway", "closed": False, "confidence": "good",
        "source": "line of Calzada de los Misterios; González Aparicio (1973)",
        "note": "the north causeway",
        "points": [(-99.1318, 19.4348), (-99.1250, 19.4500),
                   (-99.1200, 19.4680), (-99.1172, 19.4847)],
    },
    "causeway-iztapalapa": {
        "kind": "causeway", "closed": False, "confidence": "good",
        "source": "line of Calzada de Tlalpan / San Antonio Abad to the Xoloc fork, then the Iztapalapan branch; González Aparicio (1973)",
        "note": "the entry route of 8 Nov 1519; Fort Xoloc at the fork",
        "points": [(-99.1318, 19.4348), (-99.1330, 19.4260),
                   (-99.1350, 19.4060),                       # Xoloc / Acachinanco
                   (-99.1250, 19.3750), (-99.1150, 19.3620),  # Mexicaltzingo
                   (-99.0920, 19.3570)],
    },
    "causeway-coyoacan": {
        "kind": "causeway", "closed": False, "confidence": "moderate",
        "source": "branch from the Xoloc fork to Coyohuacan; González Aparicio (1973)",
        "note": "Olid's siege approach",
        "points": [(-99.1350, 19.4060), (-99.1450, 19.3790), (-99.1617, 19.3467)],
    },
    "aqueduct-chapultepec": {
        "kind": "aqueduct", "closed": False, "confidence": "good",
        "source": "line of Avenida Chapultepec; the twin-channel aqueduct of the sources",
        "note": "cut 26 May 1521 — the siege's first act",
        "points": [(-99.1819, 19.4206), (-99.1650, 19.4230),
                   (-99.1500, 19.4270), (-99.1400, 19.4310), (-99.1330, 19.4348)],
    },
    "dike-nezahualcoyotl": {
        "kind": "dike", "closed": False, "confidence": "contested",
        "source": "the albarradón of Nezahualcóyotl, c. 1449; course after González Aparicio (1973)",
        "note": "held the saline lake off the chinampa west; its exact course is debated",
        "points": [(-99.0900, 19.4900), (-99.0750, 19.4500),
                   (-99.0700, 19.4000), (-99.0850, 19.3600)],
    },

    # -- the island city footprint -------------------------------------------
    "city-footprint": {
        "kind": "footprint", "closed": True, "confidence": "moderate",
        "source": "Calnek's ~12-15 km² urban island; González Aparicio (1973)",
        "note": "Tenochtitlan with Tlatelolco north — the island at its 1519 extent",
        "points": [(-99.1480, 19.4200), (-99.1140, 19.4200), (-99.1100, 19.4440),
                   (-99.1200, 19.4580), (-99.1420, 19.4600), (-99.1500, 19.4420)],
    },

    # -- the 1519 lake system, after González Aparicio (1973), simplified ----
    "lake-texcoco": {
        "kind": "lake", "closed": True, "confidence": "moderate",
        "source": "González Aparicio (1973), simplified to visualization grade",
        "note": "the saline main body, with the México lagoon west of the dike",
        "points": [(-99.1750, 19.4700), (-99.1700, 19.5000), (-99.1300, 19.5450),
                   (-99.0600, 19.5750), (-98.9900, 19.5450), (-98.9000, 19.5200),
                   (-98.8800, 19.5000), (-98.8850, 19.4550), (-98.9650, 19.4200),
                   (-99.0000, 19.3700), (-99.0400, 19.3620), (-99.0900, 19.3630),
                   (-99.1180, 19.3630), (-99.1450, 19.3700), (-99.1600, 19.4000),
                   (-99.1700, 19.4350)],
    },
    "lake-xochimilco-chalco": {
        "kind": "lake", "closed": True, "confidence": "moderate",
        "source": "González Aparicio (1973), simplified",
        "note": "the freshwater chinampa lakes",
        "points": [(-99.1400, 19.2900), (-99.1000, 19.3000), (-99.0400, 19.2950),
                   (-98.9800, 19.2850), (-98.9300, 19.2800), (-98.9100, 19.2600),
                   (-98.9300, 19.2350), (-98.9600, 19.2300), (-99.0400, 19.2350),
                   (-99.1050, 19.2600), (-99.1400, 19.2700)],
    },
    "lake-zumpango-xaltocan": {
        "kind": "lake", "closed": True, "confidence": "moderate",
        "source": "González Aparicio (1973), simplified",
        "note": "the shallow northern lakes",
        "points": [(-99.1550, 19.7750), (-99.1000, 19.7900), (-99.0450, 19.7900),
                   (-99.0000, 19.7600), (-99.0200, 19.7200), (-99.0600, 19.6800),
                   (-99.1100, 19.6900), (-99.1400, 19.7300)],
    },
}

# ---------------------------------------------------------------------------
# geodesy helpers (small-region approximations are fine at Basin scale)
# ---------------------------------------------------------------------------

def dist_km(lat1, lon1, lat2, lon2):
    """Haversine distance in km."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def polygon_area_km2(points):
    """Shoelace on a local equirectangular projection about the polygon's centroid."""
    lat0 = sum(p[1] for p in points) / len(points)
    kx = 111.320 * math.cos(math.radians(lat0))     # km per degree lon
    ky = 110.574                                    # km per degree lat
    xy = [(lon * kx, lat * ky) for lon, lat in points]
    s = 0.0
    for (x1, y1), (x2, y2) in zip(xy, xy[1:] + xy[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def point_in_polygon(lat, lon, points):
    """Ray casting in lon/lat space (fine at this scale)."""
    inside = False
    n = len(points)
    for i in range(n):
        (x1, y1), (x2, y2) = points[i], points[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            xin = (x2 - x1) * (lat - y1) / (y2 - y1) + x1
            if lon < xin:
                inside = not inside
    return inside


def dist_to_polygon_km(lat, lon, points):
    """Distance from a point to the polygon boundary (vertex-sampled; audit-grade)."""
    best = float("inf")
    n = len(points)
    for i in range(n):
        (x1, y1), (x2, y2) = points[i], points[(i + 1) % n]
        for f in (0.0, 0.25, 0.5, 0.75, 1.0):
            px, py = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
            best = min(best, dist_km(lat, lon, py, px))
    return best


# ---------------------------------------------------------------------------
# the residual table — endpoints of drawn arteries vs the anchor table
# ---------------------------------------------------------------------------

RESIDUAL_PAIRS = [
    ("causeway-tlacopan", -1, "tacuba-plaza"),
    ("causeway-tlacopan", 0, "templo-mayor"),
    ("causeway-tepeyac", -1, "tepeyac"),
    ("causeway-tepeyac", 0, "templo-mayor"),
    ("causeway-iztapalapa", -1, "iztapalapa-centre"),
    ("causeway-coyoacan", -1, "coyoacan-plaza"),
    ("aqueduct-chapultepec", 0, "chapultepec-springs"),
]


def residuals_km():
    out = []
    for feat, idx, anchor in RESIDUAL_PAIRS:
        lon, lat = GEOMETRY[feat]["points"][idx]
        alat, alon = ANCHORS[anchor][0], ANCHORS[anchor][1]
        out.append((feat, anchor, dist_km(lat, lon, alat, alon)))
    return out


def _selftest():
    for name, (lat, lon, what, conf) in ANCHORS.items():
        assert 19.0 <= lat <= 20.0 and -99.5 <= lon <= -98.6, name
        assert conf in CONFIDENCE and what, name
    for name, g in GEOMETRY.items():
        assert g["kind"] in ("causeway", "aqueduct", "dike", "lake", "footprint"), name
        assert g["confidence"] in CONFIDENCE and g["source"], name
        assert len(g["points"]) >= (3 if g["closed"] else 2), name
        for lon, lat in g["points"]:
            assert 19.0 <= lat <= 20.0 and -99.5 <= lon <= -98.6, f"{name}: {lon},{lat}"
    # geometry helpers behave
    sq = [(-99.10, 19.40), (-99.00, 19.40), (-99.00, 19.50), (-99.10, 19.50)]
    a = polygon_area_km2(sq)
    assert 110 < a < 122, a            # 0.1° x 0.1° at 19.45° ≈ 116 km²
    assert point_in_polygon(19.45, -99.05, sq) and not point_in_polygon(19.55, -99.05, sq)
    # residuals: drawn terminals sit on their anchors (internal consistency, < 300 m)
    for feat, anchor, d in residuals_km():
        assert d < 0.3, f"{feat} vs {anchor}: {d*1000:.0f} m"
    print(f"selftest OK — {len(ANCHORS)} anchors, {len(GEOMETRY)} features; "
          f"max terminal residual {max(d for _, _, d in residuals_km())*1000:.0f} m")


if __name__ == "__main__":
    _selftest()
    print("\ncanonical reconstruction: González Aparicio (1973), Plano reconstructivo "
          "de la región de Tenochtitlan, SEP/INAH")
    print("\nresiduals (drawn terminal vs anchor):")
    for feat, anchor, d in residuals_km():
        print(f"  {feat:22} vs {anchor:20} {d*1000:6.0f} m")
    for name in ("city-footprint", "lake-texcoco", "lake-xochimilco-chalco",
                 "lake-zumpango-xaltocan"):
        print(f"  area {name:22} {polygon_area_km2(GEOMETRY[name]['points']):7.1f} km²")
