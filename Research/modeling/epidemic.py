"""The 1520-21 smallpox wave, modelled on the altepetl network. Stdlib only.

Register D2 — the mechanism (SCOPE §3): spread on the settlement network,
seeded at the DOCUMENTED introduction, calibrated to the DOCUMENTED arrival in
the capital, mortality carried as an explicitly wide band. This makes the
epidemic a derived layer instead of scenery.

THE MECHANISM, honestly stated: a travelling wave on a k-nearest-neighbour
graph of the gazetteer's polities, at constant effective speed along network
distance. Two facts pin it and everything else is interpolation:

  * seed: the epidemic is on the Gulf coast with the Narváez expedition by
    May 1520 (Cempoala region) [BD; Motolinía];
  * calibration: it burns through Tenochtitlan for sixty days beginning
    c. late Sep / Oct 1520 [FC Bk XII], killing Cuitláhuac in early December.

The model therefore CALIBRATES its one free parameter (wave speed) so the
capital's onset lands on 1 Oct 1520, and reports every other polity's onset as
a MODELLED window (confidence 'moderate' in the Basin, degrading with network
distance). Onset dates are windows, not events; mortality is the band
30-50 percent [CMH range for central Mexico 1520-21], never a number.

What this deliberately does NOT model (register D2, recorded): differential
mortality by altitude/density, second waves, the 1531 and 1545 epidemics
(events only), and any sub-altepetl structure.

Run me:  python3 epidemic.py
"""

from __future__ import annotations

import heapq
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gazetteer
from calendar import t_of_julian
from georef import dist_km

SEED_SLUG = "cempoala"
SEED_T = t_of_julian(1520, 5, 10)          # with the Narváez camp at Cempoala
CALIB_SLUG = "tenochtitlan"
CALIB_T = t_of_julian(1520, 10, 1)         # onset in the capital [FC]
DURATION = 60 / 365.25                     # the sixty days of Bk XII, per polity
MORTALITY_BAND = (0.30, 0.50)              # contested; the band IS the claim
K_NEIGHBOURS = 5


def _graph():
    nodes = {e["slug"]: (e["lat"], e["lon"]) for e in gazetteer.ENTRIES}
    edges = {s: [] for s in nodes}
    for s, (la, lo) in nodes.items():
        near = sorted(((dist_km(la, lo, la2, lo2), s2)
                       for s2, (la2, lo2) in nodes.items() if s2 != s))[:K_NEIGHBOURS]
        for d, s2 in near:
            edges[s].append((d, s2))
            edges[s2].append((d, s))      # symmetric — infection travels both ways
    return nodes, edges


def _network_dist():
    """Dijkstra from the seed over the kNN graph. km per polity."""
    _, edges = _graph()
    dist = {SEED_SLUG: 0.0}
    pq = [(0.0, SEED_SLUG)]
    while pq:
        d, s = heapq.heappop(pq)
        if d > dist.get(s, float("inf")):
            continue
        for w, s2 in edges[s]:
            nd = d + w
            if nd < dist.get(s2, float("inf")):
                dist[s2] = nd
                heapq.heappush(pq, (nd, s2))
    return dist


NETWORK_KM = _network_dist()
_SPEED_KM_PER_YR = NETWORK_KM[CALIB_SLUG] / (CALIB_T - SEED_T)   # the one free parameter


def onset(slug: str):
    """(onset_t, end_t, confidence) — a modelled window, or None if unreached."""
    d = NETWORK_KM.get(slug)
    if d is None:
        return None
    t0 = SEED_T + d / _SPEED_KM_PER_YR
    conf = "moderate" if d <= NETWORK_KM[CALIB_SLUG] * 1.6 else "contested"
    return (round(t0, 4), round(t0 + DURATION, 4), conf)


def windows():
    return {s: onset(s) for s in NETWORK_KM}


def _selftest():
    ws = windows()
    assert len(ws) == len(gazetteer.ENTRIES), "graph does not reach every polity"
    # the two pins (windows are stored at 4-decimal grain ≈ ±0.9 day)
    assert abs(ws[SEED_SLUG][0] - SEED_T) < 3e-3
    assert abs(ws[CALIB_SLUG][0] - CALIB_T) < 3e-3, ws[CALIB_SLUG]
    # nothing precedes the seed; onset grows with network distance
    for s, (t0, t1, conf) in ws.items():
        assert t0 >= SEED_T - 3e-3 and t1 > t0, s
        assert conf in ("moderate", "contested")
    ordered = sorted(ws, key=lambda s: NETWORK_KM[s])
    ts = [ws[s][0] for s in ordered]
    assert ts == sorted(ts), "onset not monotone in network distance"
    # the Basin burns in the documented season (autumn 1520 - winter 1520/21)
    basin = ["tenochtitlan", "tlatelolco", "texcoco", "tlacopan", "xochimilco",
             "chalco", "azcapotzalco", "iztapalapa"]
    for s in basin:
        t0 = ws[s][0]
        assert t_of_julian(1520, 8, 15) <= t0 <= t_of_julian(1521, 1, 15), (s, t0)
    # Tlaxcala is struck before the capital (it lies on the road) — the recorded
    # death of Maxixcatzin in late 1520 is consistent
    assert ws["tlaxcala"][0] < ws[CALIB_SLUG][0] + 0.05
    # the far south arrives later than the Basin, within the attested 1520-21 spread
    assert ws["xoconochco"][0] > ws[CALIB_SLUG][0]
    assert ws["xoconochco"][0] <= t_of_julian(1522, 6, 30), ws["xoconochco"]
    # the band is honestly wide
    lo, hi = MORTALITY_BAND
    assert hi >= 1.5 * lo
    print(f"selftest OK — wave speed {_SPEED_KM_PER_YR/365.25:.1f} km/day over "
          f"{len(ws)} polities; capital onset pinned {CALIB_T:.4f}; "
          f"mortality band {int(lo*100)}-{int(hi*100)}% (contested)")


if __name__ == "__main__":
    _selftest()
    from calendar import fmt_julian, jdn_of_julian, julian_of_t
    print("\nmodelled onsets (windows, not events):")
    for s in ["cempoala", "tlaxcala", "cholula", "tenochtitlan", "texcoco",
              "xochimilco", "tzintzuntzan", "coyolapan", "xoconochco"]:
        t0, t1, conf = windows()[s]
        y, m, d = julian_of_t(t0)
        print(f"  {s:16} ~{fmt_julian(jdn_of_julian(y, m, d)):>12}  ({conf}; "
              f"{NETWORK_KM[s]:5.0f} km by network)")
