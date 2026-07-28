"""The allegiance state machine — the model's spine. Stdlib only.

One timeline per polity: which side of the war each altepetl stood on, on any
day of 1502-1550, derived from (a) its pre-war standing in the gazetteer and
(b) the dated, cited events whose `effects` move it. THE MAP'S COLOURING IS
THIS MODULE'S OUTPUT — if a viewer's first glance shows two colours, the model
has already lied (SCOPE.md §1).

States:
  alliance-core     Triple Alliance seat (Tenochtitlan, Tlatelolco*, Texcoco, Tlacopan)
  tributary         inside the tribute system
  independent       outside it (Tlaxcallan, Metztitlan, Tototepec, Yopitzinco, Teotitlan...)
  rival             the Purépecha state
  contested         in play: risen, split, fought over
  allied-coalition  fighting with the Cortés-Tlaxcallan coalition
  occupied          under coalition/Spanish military control (wartime and immediate aftermath)
  colonial-ally     post-war: privileged ally under the crown (Tlaxcallan)
  new-spain         post-war: absorbed into colonial New Spain
  spanish           a Spanish foundation (exists only from its founding date)

MODELLED SIMPLIFICATIONS, stated per Working Rule 10 and drawn as modelled:
  * a polity with no explicit post-war event passes occupied/allied/tributary ->
    new-spain at the CONSOLIDATION default (1 June 1522), confidence 'moderate';
  * a polity occupied later than the fall passes -> new-spain one year after its
    occupation date;
  * allegiance below the altepetl is NOT modelled (SCOPE §9) — a 'contested'
    state is the resolution floor;
  * Mexica counter-diplomacy 1520-21 briefly regained towns the machine keeps
    'contested' — reversion transitions are deliberately excluded in round 1
    (register B2-c).

Run me:  python3 allegiance.py
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gazetteer                     # noqa: E402
import events as events_mod          # noqa: E402
from calendar import t_of_julian     # noqa: E402

T0, T1 = 1502.0, 1551.0

STATES = ("alliance-core", "tributary", "independent", "rival", "contested",
          "allied-coalition", "occupied", "colonial-ally", "new-spain", "spanish")

INITIAL = {"triple-alliance-core": "alliance-core",
           "tributary": "tributary",
           "independent": "independent",
           "rival-state": "rival",
           "spanish-foundation": "spanish"}

ALLOWED = {
    "alliance-core":    {"contested", "allied-coalition", "occupied"},
    "tributary":        {"contested", "allied-coalition", "occupied", "new-spain"},
    "independent":      {"contested", "allied-coalition", "occupied", "new-spain"},
    "rival":            {"occupied"},
    "contested":        {"allied-coalition", "occupied", "new-spain"},
    "allied-coalition": {"occupied", "colonial-ally", "new-spain"},
    "occupied":         {"new-spain"},
    "colonial-ally":    set(),
    "new-spain":        set(),
    "spanish":          set(),
}

CONSOLIDATION_T = t_of_julian(1522, 6, 1)
FALL_T = t_of_julian(1521, 8, 13)

# Post-war standing that is NOT the default: Tlaxcallan's crown privileges.
COLONIAL_ALLY = {"tlaxcala"}


def _build():
    """timelines[slug] = [(t, state, cause, confidence), ...] ascending."""
    tl = {}
    for e in gazetteer.ENTRIES:
        s = INITIAL[e["group"]]
        if s == "spanish":
            continue                                    # born at its founding event
        tl[e["slug"]] = [(T0, s, "standing-at-1502", "good")]

    # Spanish foundations are born at their founding event.
    for ev in events_mod.EVENTS:
        if ev["id"] == "villa-rica-founded":
            tl["villa-rica"] = [(ev["t"], "spanish", ev["id"], "good")]

    # Apply the dated effects, in event order (events are chronological).
    for ev in events_mod.EVENTS:
        for slug, new in ev["effects"]:
            cur = tl[slug][-1][1]
            if new == cur:
                continue
            assert new in ALLOWED[cur], \
                f"illegal transition {cur} -> {new} for {slug} at {ev['id']}"
            tl[slug].append((ev["t"], new, ev["id"], ev["confidence"]))

    # Consolidation rules (modelled; confidence 'moderate').
    for slug, tline in tl.items():
        t_last, s_last, _, _ = tline[-1]
        if s_last == "spanish":
            continue
        if slug in COLONIAL_ALLY and s_last == "allied-coalition":
            tline.append((FALL_T, "colonial-ally", "postwar-privileged-ally", "moderate"))
            continue
        if s_last == "occupied":
            t_ns = max(CONSOLIDATION_T, t_last + 1.0)
            tline.append((t_ns, "new-spain", "consolidation-modelled", "moderate"))
        elif s_last in ("tributary", "contested", "allied-coalition", "independent"):
            t_ns = max(CONSOLIDATION_T, t_last + 0.25)
            tline.append((t_ns, "new-spain", "consolidation-modelled", "moderate"))
        # rival with no event would be a bug caught by the selftest below.
    return tl


TIMELINES = _build()


def state_at(slug: str, t: float):
    """(state, since, cause, confidence) at time t; None before the polity exists."""
    tline = TIMELINES[slug]
    if t < tline[0][0]:
        return None
    cur = tline[0]
    for row in tline:
        if row[0] <= t:
            cur = row
        else:
            break
    return {"state": cur[1], "since": cur[0], "cause": cur[2], "confidence": cur[3]}


def counts_at(t: float):
    out = {}
    for slug in TIMELINES:
        st = state_at(slug, t)
        if st:
            out[st["state"]] = out.get(st["state"], 0) + 1
    return out


def series(slug: str):
    """[[t, state], ...] — the app-artifact form."""
    return [[round(t, 4), s] for (t, s, _c, _cf) in TIMELINES[slug]]


def _selftest():
    known_ids = set(events_mod.BY_ID) | {"standing-at-1502", "consolidation-modelled",
                                         "postwar-privileged-ally"}
    for slug, tline in TIMELINES.items():
        # sorted, legal, known causes
        ts = [r[0] for r in tline]
        assert ts == sorted(ts), f"{slug}: unsorted timeline"
        assert len(ts) == len(set(ts)), f"{slug}: duplicate transition instants"
        for (a, b) in zip(tline, tline[1:]):
            assert b[1] in ALLOWED[a[1]], f"{slug}: {a[1]} -> {b[1]}"
        for r in tline:
            assert r[2] in known_ids, f"{slug}: unknown cause {r[2]}"
            assert r[1] in STATES, f"{slug}: bad state {r[1]}"
        # every polity ends the window inside the colonial order
        final = tline[-1][1]
        assert final in ("new-spain", "colonial-ally", "spanish"), \
            f"{slug}: ends 1550 as {final}"

    # The pre-war world contains no coalition.
    c1519 = counts_at(1519.0)
    assert c1519.get("allied-coalition", 0) == 0, c1519
    assert c1519.get("independent", 0) >= 5

    # After Tlaxcala (Sep 1519) the coalition exists.
    c_oct19 = counts_at(t_of_julian(1519, 10, 1))
    assert c_oct19.get("allied-coalition", 0) >= 5, c_oct19

    # Mid-siege (July 1521): the map is a coalition map, not a two-colour war.
    c_siege = counts_at(t_of_julian(1521, 7, 15))
    assert c_siege.get("allied-coalition", 0) + c_siege.get("occupied", 0) >= 25, c_siege
    assert c_siege.get("alliance-core", 0) <= 2      # only the island cities still stand

    # Tenochtitlan is never coalition, and occupied only from the fall.
    assert state_at("tenochtitlan", t_of_julian(1521, 8, 12))["state"] == "contested"
    assert state_at("tenochtitlan", t_of_julian(1521, 8, 13))["state"] == "occupied"
    for (t, s, _c, _cf) in TIMELINES["tenochtitlan"]:
        assert s != "allied-coalition"

    # Villa Rica does not exist before its foundation.
    assert state_at("villa-rica", 1519.3) is None
    assert state_at("villa-rica", 1520.0)["state"] == "spanish"

    # Tlaxcallan: independent -> allied (Sep 1519) -> colonial-ally, never tributary/occupied.
    seq = [s for (_t, s, _c, _cf) in TIMELINES["tlaxcala"]]
    assert seq == ["independent", "allied-coalition", "colonial-ally"], seq

    # The rival state ends occupied -> new-spain via its 1522 event.
    seq_tz = [s for (_t, s, _c, _cf) in TIMELINES["tzintzuntzan"]]
    assert seq_tz == ["rival", "occupied", "new-spain"], seq_tz

    # By 1524 the old categories are gone from the living map.
    c1524 = counts_at(1524.5)
    assert c1524.get("tributary", 0) == 0 and c1524.get("alliance-core", 0) == 0, c1524

    print(f"selftest OK — {len(TIMELINES)} timelines, "
          f"{sum(len(v) for v in TIMELINES.values())} transitions; "
          f"coalition at mid-siege: {c_siege.get('allied-coalition', 0)} allied "
          f"+ {c_siege.get('occupied', 0)} occupied vs "
          f"{c_siege.get('contested', 0)} contested + {c_siege.get('alliance-core', 0)} core")


if __name__ == "__main__":
    _selftest()
    from calendar import julian_of_t
    print("\nthe war, as the machine sees it:")
    for label, (y, m, d) in [("the day before the landing", (1519, 4, 20)),
                             ("after the Tlaxcala alliance", (1519, 10, 1)),
                             ("after the Noche Triste", (1520, 7, 15)),
                             ("siege midpoint", (1521, 7, 1)),
                             ("one year after the fall", (1522, 8, 13)),
                             ("mid-century", (1550, 1, 1))]:
        c = counts_at(t_of_julian(y, m, d))
        row = ", ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1]))
        print(f"  {label:28} {row}")
