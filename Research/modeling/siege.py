"""The siege as a DERIVED state (register D2-b). Stdlib only.

The city had four cutable arteries (SCOPE §1): the causeways (food and
movement), the Chapultepec aqueduct (fresh water), the open lake (canoe-borne
supply), and — once the ring closed — the market system itself. This module
derives the city's siege state on any day from the dated, cited events of
events.py, instead of narrating it: each artery carries the event that cut it,
and the composite pressure is a COUNT of severed arteries, not a tuned number.

Artery cut dates (Julian 1521), with their evidence:
  causeway-tlacopan     22 May — Alvarado's camp at Tlacopan          [C3][BD]
  causeway-coyoacan     22 May — Olid's camp at Coyohuacan            [C3]
  causeway-iztapalapa   22 May — Sandoval's camp at Iztapalapan       [C3]
  aqueduct              26 May — the Chapultepec channels broken      [C3][BD][FC]
  lake                   1 Jun — the brigantines break the canoe fleet [C3][FC]
  causeway-tepeyac      10 Jun — Sandoval reposted to seal the north  [C3] (month-grade)

Confidence: the sequence is 'good'; the Tepeyac date is 'moderate' (the
sources give the reposting without a day). Water/food consequences appear on
cards as the sources describe them, not as computed calories — no source
supports a supply model finer than "cut / not cut" (that limit is the point).

Run me:  python3 siege.py
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calendar import t_of_julian
import events as events_mod

SIEGE_START = t_of_julian(1521, 5, 22)
SIEGE_END = t_of_julian(1521, 8, 13)

ARTERIES = [
    {"id": "causeway-tlacopan", "label": "Tlacopan causeway",
     "cut": t_of_julian(1521, 5, 22), "event": "siege-camps", "confidence": "good"},
    {"id": "causeway-coyoacan", "label": "Coyohuacan causeway",
     "cut": t_of_julian(1521, 5, 22), "event": "siege-camps", "confidence": "good"},
    {"id": "causeway-iztapalapa", "label": "Iztapalapan causeway",
     "cut": t_of_julian(1521, 5, 22), "event": "siege-camps", "confidence": "good"},
    {"id": "aqueduct-chapultepec", "label": "Chapultepec aqueduct (fresh water)",
     "cut": t_of_julian(1521, 5, 26), "event": "aqueduct-cut", "confidence": "good"},
    {"id": "lake", "label": "The open lake (canoe supply)",
     "cut": t_of_julian(1521, 6, 1), "event": "brigantine-victory", "confidence": "good"},
    {"id": "causeway-tepeyac", "label": "Tepeyacac causeway",
     "cut": t_of_julian(1521, 6, 10), "event": "sandoval-tepeyac", "confidence": "moderate"},
]


def status_at(t: float):
    """[{label, cut(bool), since, confidence}] — the panel's data."""
    return [{"label": a["label"], "cut": t >= a["cut"], "since": a["cut"],
             "confidence": a["confidence"]} for a in ARTERIES]


def pressure(t: float) -> int:
    """How many of the six arteries are severed at t."""
    return sum(1 for a in ARTERIES if t >= a["cut"])


def _selftest():
    known = set(events_mod.BY_ID)
    for a in ARTERIES:
        # every artery's cause is a real, dated, cited event
        assert a["event"] in known, f"{a['id']}: unknown event {a['event']}"
        ev_t = events_mod.BY_ID[a["event"]]["t"]
        assert abs(ev_t - a["cut"]) < 0.02, \
            f"{a['id']}: cut date drifts from its event ({a['cut']:.4f} vs {ev_t:.4f})"
        assert SIEGE_START - 1e-6 <= a["cut"] <= SIEGE_END, a["id"]
    # pressure is monotone through the siege and complete before the fall
    assert pressure(SIEGE_START - 0.01) == 0
    ts = [SIEGE_START + i * 0.005 for i in range(int((SIEGE_END - SIEGE_START) / 0.005) + 1)]
    ps = [pressure(t) for t in ts]
    assert all(b >= a for a, b in zip(ps, ps[1:])), "pressure not monotone"
    assert pressure(t_of_julian(1521, 6, 15)) == 6
    assert pressure(t_of_julian(1521, 5, 24)) == 3
    print(f"selftest OK — 6 arteries, all event-derived; pressure 0 -> 6 across "
          f"{SIEGE_START:.4f}..{SIEGE_END:.4f}")


if __name__ == "__main__":
    _selftest()
    from calendar import julian_of_t
    for (y, m, d) in ((1521, 5, 21), (1521, 5, 24), (1521, 5, 28), (1521, 6, 5),
                      (1521, 6, 15), (1521, 8, 12)):
        t = t_of_julian(y, m, d)
        cut = [s["label"] for s in status_at(t) if s["cut"]]
        print(f"  {d:2} {['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'][m]} 1521: "
              f"pressure {pressure(t)}/6 — {', '.join(cut) if cut else 'the city breathes'}")
