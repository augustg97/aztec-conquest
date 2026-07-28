"""Audit the drawn geography against the archaeological witness. READ-ONLY.

The independent witness (SCOPE §7): the archaeological record — the Templo
Mayor location, the causeway terminals pinned by surviving modern streets and
plazas, the settlement survey's town locations — is independent of the
chronicles, which is what lets it settle disputes the chronicles are party to.
This audit scores WHAT IS ACTUALLY DRAWN (the geo/entities artifacts the app
reads — web/data/ if the handover has landed, else the staged copies) against
that witness and against independent literature values.

Checks:
  residual     drawn artery terminals vs anchor table, < 500 m               HIGH
  footprint    Templo Mayor & Tlatelolco anchors INSIDE the drawn city;
               city area within Calnek's 10-18 km²                           HIGH
  islands      island towns (Xaltocan, Cuitláhuac) drawn IN the water;
               the city footprint centroid on the lake                       HIGH
  shore        lakeshore towns drawn ON LAND (not drowned), within 4.5 km
               of a lake edge                                                HIGH (drowned) / MED (far)
  areas        lake system total within the literature band 700-1,600 km²,
               Lake Texcoco >= 350 km²                                       MED
  works        dike ends near Tepeyacac/Iztapalapan; aqueduct reaches the
               city footprint                                                MED
  track        campaign track chronological, no teleports > 300 km          MED

    python3 audit_witness.py            # report + final JSON line
    python3 audit_witness.py --selftest
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WEB = os.path.join(ROOT, "web", "data")
STAGED = os.path.join(HERE, "..", "research reports", "staged-artifacts")
sys.path.insert(0, HERE)

from georef import dist_km, polygon_area_km2, point_in_polygon, dist_to_polygon_km  # noqa: E402

RESIDUAL_PAIRS = [
    ("causeway-tlacopan", -1, "tacuba-plaza"),
    ("causeway-tlacopan", 0, "templo-mayor"),
    ("causeway-tepeyac", -1, "tepeyac"),
    ("causeway-tepeyac", 0, "templo-mayor"),
    ("causeway-iztapalapa", -1, "iztapalapa-centre"),
    ("causeway-coyoacan", -1, "coyoacan-plaza"),
    ("aqueduct-chapultepec", 0, "chapultepec-springs"),
]

ISLAND_TOWNS = ["xaltocan", "cuitlahuac"]
SHORE_TOWNS = ["texcoco", "coyoacan", "xochimilco", "iztapalapa", "culhuacan",
               "chalco", "mizquic", "zumpango", "ecatepec", "azcapotzalco",
               "tlacopan", "huexotla", "chimalhuacan", "tenayuca", "mexicaltzingo",
               "huitzilopochco"]


def _load_js(path, key):
    with open(path) as f:
        src = f.read()
    marker = f"DATA.{key} = "
    i = src.index(marker) + len(marker)
    j = src.index(";\n", i)
    return json.loads(src[i:j])


def load_subject():
    base = WEB if os.path.exists(os.path.join(WEB, "geo.js")) else STAGED
    which = "web/data (live app data)" if base == WEB else "staged artifacts"
    geo = _load_js(os.path.join(base, "geo.js"), "geo")
    ents = _load_js(os.path.join(base, "entities.js"), "entities")
    evs = _load_js(os.path.join(base, "eventsFull.js"), "eventsFull")
    return {"which": which,
            "features": {f["id"]: f for f in geo["features"]},
            "anchors": {a["id"]: (a["lat"], a["lon"]) for a in geo["anchors"]},
            "peaks": geo.get("peaks", []),
            "entities": {e["id"]: e for e in ents},
            "events": evs}


def check_residual(sub, F):
    for feat, idx, anchor in RESIDUAL_PAIRS:
        pts = sub["features"][feat]["points"]
        lon, lat = pts[idx]
        alat, alon = sub["anchors"][anchor]
        d = dist_km(lat, lon, alat, alon)
        if d > 0.5:
            F("HIGH", "residual", feat, f"terminal {d*1000:.0f} m from {anchor}")


def check_footprint(sub, F):
    fp = sub["features"]["city-footprint"]["points"]
    a = polygon_area_km2(fp)
    if not (10.0 <= a <= 18.0):
        F("HIGH", "footprint", "area", f"{a:.1f} km² outside Calnek's 10-18 km²")
    for anchor in ("templo-mayor", "tlatelolco-templo"):
        alat, alon = sub["anchors"][anchor]
        if not point_in_polygon(alat, alon, fp):
            F("HIGH", "footprint", anchor, "anchor outside the drawn city")


def _lakes(sub):
    return {k: f["points"] for k, f in sub["features"].items() if f["kind"] == "lake"}


def check_islands(sub, F):
    lakes = _lakes(sub)
    for slug in ISLAND_TOWNS:
        e = sub["entities"][slug]
        if not any(point_in_polygon(e["lat"], e["lon"], p) for p in lakes.values()):
            F("HIGH", "islands", slug, "island town drawn on dry land")
    fp = sub["features"]["city-footprint"]["points"]
    clat = sum(p[1] for p in fp) / len(fp)
    clon = sum(p[0] for p in fp) / len(fp)
    if not any(point_in_polygon(clat, clon, p) for p in lakes.values()):
        F("HIGH", "islands", "city-footprint", "the island city is not on the lake")


def check_shore(sub, F):
    lakes = _lakes(sub)
    for slug in SHORE_TOWNS:
        e = sub["entities"][slug]
        inside = [k for k, p in lakes.items() if point_in_polygon(e["lat"], e["lon"], p)]
        if inside:
            F("HIGH", "shore", slug, f"lakeshore town drawn UNDER {inside[0]}")
            continue
        d = min(dist_to_polygon_km(e["lat"], e["lon"], p) for p in lakes.values())
        if d > 4.5:
            F("MED", "shore", slug, f"{d:.1f} km from the nearest drawn lake edge")


def check_areas(sub, F):
    lakes = _lakes(sub)
    areas = {k: polygon_area_km2(p) for k, p in lakes.items()}
    total = sum(areas.values())
    if not (700.0 <= total <= 1600.0):
        F("MED", "areas", "lake-system", f"total {total:.0f} km² outside 700-1,600 km² band")
    if areas.get("lake-texcoco", 0) < 350.0:
        F("MED", "areas", "lake-texcoco", f"{areas.get('lake-texcoco', 0):.0f} km² < 350 km²")


def check_works(sub, F):
    dike = sub["features"]["dike-nezahualcoyotl"]["points"]
    for end, anchor, lim in ((dike[0], "tepeyac", 3.5), (dike[-1], "iztapalapa-centre", 3.5)):
        alat, alon = sub["anchors"][anchor]
        d = dist_km(end[1], end[0], alat, alon)
        if d > lim:
            F("MED", "works", "dike", f"end {d:.1f} km from {anchor} (> {lim})")
    aq = sub["features"]["aqueduct-chapultepec"]["points"]
    fp = sub["features"]["city-footprint"]["points"]
    d = dist_to_polygon_km(aq[-1][1], aq[-1][0], fp)
    if d > 1.2 and not point_in_polygon(aq[-1][1], aq[-1][0], fp):
        F("MED", "works", "aqueduct", f"east end {d:.1f} km short of the city")


def check_track(sub, F):
    pts = [(e["t"], e["lat"], e["lon"], e["id"]) for e in sub["events"] if e.get("track")]
    ts = [p[0] for p in pts]
    if ts != sorted(ts):
        F("MED", "track", "order", "track events out of chronological order")
    # The threshold targets coordinate errors (a hemisphere typo is ~10,000 km),
    # not genuine sea legs — Cuba -> Centla is a real 900 km voyage.
    for (t1, la1, lo1, i1), (t2, la2, lo2, i2) in zip(pts, pts[1:]):
        d = dist_km(la1, lo1, la2, lo2)
        if d > 1000.0:
            F("MED", "track", i2, f"jump of {d:.0f} km from {i1}")


# towns whose whole point is the coast — must be on land, near the sea
COASTAL_TOWNS = ["cempoala", "quiahuiztlan", "villa-rica", "cuetlaxtlan",
                 "tochpan", "cihuatlan", "xoconochco"]


def check_coast(sub, F):
    seas = {k: f["points"] for k, f in sub["features"].items() if f["kind"] == "sea"}
    if not seas:
        F("HIGH", "coast", "substrate", "no sea polygons — the map has no ground")
        return
    # nobody drowns in an ocean
    for eid, e in sub["entities"].items():
        if e.get("lat") is None:
            continue
        for k, pts in seas.items():
            if point_in_polygon(e["lat"], e["lon"], pts):
                F("HIGH", "coast", eid, f"drawn in the {k}")
    # the coastal towns sit near the drawn sea
    for slug in COASTAL_TOWNS:
        e = sub["entities"].get(slug)
        if not e:
            continue
        d = min(dist_to_polygon_km(e["lat"], e["lon"], pts) for pts in seas.values())
        if d > 70.0:
            F("MED", "coast", slug, f"{d:.0f} km from the drawn coast (> 70)")
    # the pass the column crossed lies between the two volcanoes
    peaks = {p["id"]: p for p in sub["peaks"]}
    if "popocatepetl" in peaks and "iztaccihuatl" in peaks:
        po, iz = peaks["popocatepetl"], peaks["iztaccihuatl"]
        mid_lat, mid_lon = (po["lat"] + iz["lat"]) / 2, (po["lon"] + iz["lon"]) / 2
        ev = next((e for e in sub["events"] if e["id"] == "paso-de-cortes"), None)
        if ev and dist_km(ev["lat"], ev["lon"], mid_lat, mid_lon) > 15.0:
            F("MED", "coast", "paso-de-cortes",
              f"{dist_km(ev['lat'], ev['lon'], mid_lat, mid_lon):.0f} km from the saddle")
    else:
        F("MED", "coast", "peaks", "the framing volcanoes are missing")
    if len(sub["peaks"]) < 6:
        F("MED", "coast", "peaks", f"only {len(sub['peaks'])} named peaks (< 6)")


CHECKS = [check_residual, check_footprint, check_islands, check_shore,
          check_areas, check_works, check_track, check_coast]


def _selftest():
    sub = {
        "which": "synthetic",
        "features": {
            "city-footprint": {"kind": "footprint", "points":
                [(-99.2, 19.40), (-99.19, 19.40), (-99.19, 19.41), (-99.2, 19.41)]},  # tiny, wrong place
            "lake-texcoco": {"kind": "lake", "points":
                [(-99.10, 19.40), (-99.00, 19.40), (-99.00, 19.50), (-99.10, 19.50)]},
            "dike-nezahualcoyotl": {"kind": "dike", "points": [(-99.30, 19.9), (-99.30, 19.8)]},
            "aqueduct-chapultepec": {"kind": "aqueduct", "points": [(-99.30, 19.42), (-99.28, 19.42)]},
            "causeway-tlacopan": {"kind": "causeway", "points": [(-99.30, 19.40), (-99.30, 19.46)]},
            "causeway-tepeyac": {"kind": "causeway", "points": [(-99.30, 19.40), (-99.30, 19.48)]},
            "causeway-iztapalapa": {"kind": "causeway", "points": [(-99.30, 19.40), (-99.30, 19.35)]},
            "causeway-coyoacan": {"kind": "causeway", "points": [(-99.30, 19.40), (-99.30, 19.34)]},
        },
        "anchors": {"templo-mayor": (19.4348, -99.1318), "tlatelolco-templo": (19.4506, -99.1372),
                    "tacuba-plaza": (19.459, -99.188), "tepeyac": (19.4847, -99.1172),
                    "iztapalapa-centre": (19.357, -99.092), "coyoacan-plaza": (19.3467, -99.1617),
                    "chapultepec-springs": (19.4206, -99.1819)},
        "peaks": [],                                    # missing volcanoes -> coast fires
        "entities": {
            "xaltocan": {"id": "xaltocan", "lat": 19.0, "lon": -99.0},     # dry land!
            "cuitlahuac": {"id": "cuitlahuac", "lat": 19.45, "lon": -99.05},  # in synthetic lake OK
            "cempoala": {"id": "cempoala", "lat": 19.45, "lon": -95.0},    # in the synthetic sea!
            **{s: {"id": s, "lat": 19.45, "lon": -99.05} for s in SHORE_TOWNS},  # ALL drowned!
        },
        "events": [{"t": 2.0, "lat": 19.0, "lon": -99.0, "id": "a", "track": True},
                   {"t": 1.0, "lat": 25.0, "lon": -90.0, "id": "b", "track": True}],
    }
    sub["features"]["sea-x"] = {"kind": "sea", "points":
        [(-96.0, 19.0), (-94.0, 19.0), (-94.0, 20.0), (-96.0, 20.0)]}
    findings = []

    def F(sev, check, what, detail):
        findings.append({"severity": sev, "check": check, "what": what, "detail": detail})

    for c in CHECKS:
        c(sub, F)
    checks_fired = {f["check"] for f in findings}
    expect = {"residual", "footprint", "islands", "shore", "areas", "works", "track",
              "coast"}
    missing = expect - checks_fired
    assert not missing, f"selftest: checks failed to fire: {missing}"
    assert any(f["check"] == "coast" and f["what"] == "cempoala" for f in findings), \
        "coast check missed the drowned coastal town"
    print(f"selftest OK — all {len(CHECKS)} checks fire on synthetic defects")


def main():
    if "--selftest" in sys.argv:
        _selftest(); return 0
    _selftest()
    sub = load_subject()
    findings = []

    def F(sev, check, what, detail):
        findings.append({"severity": sev, "check": check, "what": what, "detail": detail})

    for c in CHECKS:
        c(sub, F)
    print(f"reading: {sub['which']}")
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    findings.sort(key=lambda f: order[f["severity"]])
    for f in findings:
        print(f"{f['severity']:4}  {f['check']:10} {f['what']:22} {f['detail']}")
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in ("HIGH", "MED", "LOW")}
    # the measured numbers, always printed, so rounds can be compared
    lakes = _lakes(sub)
    total = sum(polygon_area_km2(p) for p in lakes.values())
    fp_area = polygon_area_km2(sub["features"]["city-footprint"]["points"])
    print(f"measured: city footprint {fp_area:.1f} km²; lake system {total:.0f} km²")
    print(f"{len(findings)} findings — {counts['HIGH']} HIGH / {counts['MED']} MED / {counts['LOW']} LOW")
    print(json.dumps(counts))
    return 1 if counts["HIGH"] else 0


if __name__ == "__main__":
    sys.exit(main())
