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
# the substrate: seas, sierra, peaks (round 2 — closes the black-map defect)
# ---------------------------------------------------------------------------
# The user's round-1 report: "unable to view the map itself — just a black
# background." Correct: the map had no land/sea substrate. These polygons give
# it one. AUTHORED at visualization grade: a simplified modern coastline
# (the 1519 coastline differs only below this drawing's resolution), stylised
# ridgelines for the great sierras, and real named peaks. Every coastal-town
# relationship is scored by audit_witness.py check_coast.

SEAS = {
    "sea-gulf-caribbean": {
        "kind": "sea", "closed": True, "confidence": "moderate",
        "source": "simplified modern coastline, authored; visualization grade",
        "points": [(-97.75, 22.60), (-97.72, 22.20), (-97.55, 21.60), (-97.33, 21.00),
                   (-97.20, 20.60), (-96.75, 20.20), (-96.30, 19.55), (-96.10, 19.15),
                   (-95.75, 18.75), (-95.00, 18.40), (-94.40, 18.15), (-93.50, 18.40),
                   (-92.60, 18.65), (-91.55, 18.75), (-90.70, 19.35), (-90.48, 20.00),
                   (-90.35, 21.00), (-89.80, 21.30), (-88.90, 21.50), (-88.10, 21.55),
                   (-87.05, 21.55), (-86.80, 21.10), (-86.85, 20.40), (-87.45, 19.60),
                   (-87.65, 18.70), (-88.25, 18.40), (-88.30, 17.60), (-88.25, 16.55),
                   (-88.85, 15.95), (-86.20, 15.75), (-86.20, 22.60)],
    },
    "sea-pacific": {
        "kind": "sea", "closed": True, "confidence": "moderate",
        "source": "simplified modern coastline, authored; visualization grade",
        "points": [(-105.40, 20.60), (-105.00, 20.30), (-104.80, 19.80), (-104.30, 19.10),
                   (-103.50, 18.60), (-102.20, 17.95), (-101.55, 17.62), (-100.85, 17.20),
                   (-99.90, 16.83), (-98.75, 16.53), (-97.80, 15.97), (-96.50, 15.66),
                   (-95.20, 16.15), (-94.80, 16.28), (-94.10, 16.15), (-93.55, 15.85),
                   (-92.90, 15.35), (-92.25, 14.55), (-91.30, 13.95), (-90.30, 13.75),
                   (-89.60, 13.45), (-89.30, 13.20), (-105.40, 13.20)],
    },
}

RIDGES = {
    "ridge-volcanic-belt": {
        "kind": "ridge", "confidence": "moderate", "label": "Trans-Mexican Volcanic Belt",
        "points": [(-103.60, 19.45), (-102.30, 19.55), (-101.00, 19.45), (-99.85, 19.20),
                   (-99.20, 19.12), (-98.64, 19.05), (-98.10, 19.15), (-97.45, 19.05),
                   (-97.15, 19.45)],
    },
    "ridge-sm-oriental": {
        "kind": "ridge", "confidence": "moderate", "label": "Sierra Madre Oriental",
        "points": [(-98.30, 22.40), (-98.55, 21.20), (-98.35, 20.30), (-97.70, 19.75)],
    },
    "ridge-sm-del-sur": {
        "kind": "ridge", "confidence": "moderate", "label": "Sierra Madre del Sur",
        "points": [(-100.90, 17.25), (-99.60, 17.35), (-98.30, 17.05), (-97.20, 16.60),
                   (-96.30, 16.10)],
    },
    "ridge-sm-chiapas": {
        "kind": "ridge", "confidence": "moderate", "label": "Sierra Madre de Chiapas",
        "points": [(-93.90, 15.65), (-92.90, 15.15), (-91.90, 14.85), (-91.00, 14.55)],
    },
    "ridge-basin-west-rim": {
        "kind": "ridge", "confidence": "moderate", "label": "Sierra de las Cruces / Ajusco",
        "points": [(-99.24, 19.12), (-99.30, 19.26), (-99.36, 19.40), (-99.33, 19.55),
                   (-99.29, 19.68)],
    },
    "ridge-basin-east-rim": {
        "kind": "ridge", "confidence": "moderate", "label": "Sierra Nevada",
        "points": [(-98.63, 19.00), (-98.64, 19.18), (-98.68, 19.30), (-98.71, 19.41),
                   (-98.76, 19.55)],
    },
}

# real, well-located summits — the visual anchors of the pass and the rims
PEAKS = {
    "citlaltepetl":   (19.030, -97.268, "Citlaltépetl (Pico de Orizaba)", "meso"),
    "popocatepetl":   (19.023, -98.628, "Popocatépetl", "both"),
    "iztaccihuatl":   (19.179, -98.641, "Iztaccíhuatl", "both"),
    "nevado-toluca":  (19.108, -99.758, "Nevado de Toluca", "meso"),
    "malinche":       (19.231, -98.032, "Matlalcueye (La Malinche)", "meso"),
    "cofre-perote":   (19.492, -97.150, "Cofre de Perote", "meso"),
    "ajusco":         (19.209, -99.258, "Ajusco", "basin"),
    "cerro-estrella": (19.336, -99.090, "Huixachtlan (Cerro de la Estrella)", "basin"),
}

SEA_LABELS = [(-94.3, 20.9, "Gulf of Mexico"), (-99.8, 15.1, "Pacific Ocean")]

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
    # substrate: seas closed and big, ridges open, peaks in frame
    for name, g in SEAS.items():
        assert g["closed"] and len(g["points"]) >= 10, name
    for name, g in RIDGES.items():
        assert len(g["points"]) >= 3 and g["label"], name
    for pid, (lat, lon, label, views) in PEAKS.items():
        assert 13.0 <= lat <= 23.0 and -106.0 <= lon <= -86.0 and label, pid
        assert views in ("meso", "basin", "both"), pid
    # the Paso de Cortés lies between the two volcanoes
    po, iz = PEAKS["popocatepetl"], PEAKS["iztaccihuatl"]
    assert abs((po[0] + iz[0]) / 2 - 19.101) < 0.02
    # no altepetl may drown in an ocean (gazetteer cross-check runs in the audit,
    # but the canonical land anchors must be on land here too)
    for (lat, lon) in ((19.4348, -99.1318), (19.318, -98.238)):   # Tenochtitlan, Tlaxcala
        for name, g in SEAS.items():
            assert not point_in_polygon(lat, lon, g["points"]), f"{name} swallows {lat},{lon}"
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
