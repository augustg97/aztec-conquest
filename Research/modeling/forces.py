"""Force composition over the war — as RANGES, never single numbers. Stdlib only.

The single most argument-carrying readout in the model (SCOPE §3): who was
actually doing the fighting, phase by phase, with what each source claims and
why each would claim it. Working rule 2.14: a single confident number anywhere
in this territory is a bug.

Numbers are per-source claims or modern reconstructions; every band carries its
sources. Indigenous-ally and defender counts are contested BY AN ORDER OF
MAGNITUDE and the bands are drawn that wide on purpose. No source counted the
allies' dead carefully; that absence is itself displayed.

Source keys as in events.py; page-level pinning is register B2-b.

Run me:  python3 forces.py
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calendar import t_of_julian  # noqa: E402

CONFIDENCE = ("good", "moderate", "contested", "none")

# phase: (id, julian date, label)
PHASES = [
    ("landing",  (1519, 4, 22), "The landing (Apr 1519)"),
    ("march",    (1519, 11, 8), "The march to Tenochtitlan (Nov 1519)"),
    ("merged",   (1520, 6, 24), "After Narváez absorbed (Jun 1520)"),
    ("survivors", (1520, 7, 12), "After the Noche Triste (Jul 1520)"),
    ("siege",    (1521, 6, 15), "The siege of Tenochtitlan (May-Aug 1521)"),
]

# contingent -> phase -> {lo, hi, confidence, claims:[(source, claim, note)]}
SERIES = {
    "Spanish": {
        "landing":  {"lo": 450, "hi": 630, "confidence": "moderate", "claims": [
            ("Bernal Díaz", "508 soldiers besides ~100 mariners",
             "the soldier counting his comrades, decades later"),
            ("modern [TH]", "~530 fighting men, 16 horses", "reconstruction from the muster lists")]},
        "march":    {"lo": 350, "hi": 450, "confidence": "moderate", "claims": [
            ("Cortés [C2]", "leaves ~150 at Villa Rica; marches with the rest",
             "understates losses to keep the enterprise impressive")]},
        "merged":   {"lo": 1100, "hi": 1300, "confidence": "moderate", "claims": [
            ("[BD][TH]", "Narváez's ~900-1,400 join Cortés's ~350-420",
             "the largest Spanish force of the war — weeks before its worst defeat")]},
        "survivors": {"lo": 400, "hi": 1100, "confidence": "contested", "claims": [
            ("Cortés [C2]", "~150 Spaniards lost on the causeway — which would leave ~1,100 standing",
             "minimising catastrophe in a funding request; his own arithmetic is the band's top"),
            ("Bernal Díaz", "over 550 lost ('over 860' with the Tustepec garrison) — leaving ~400-500",
             "the veterans' count, against Gómara's heroics; the band's bottom"),
            ("Gómara", "~450 lost", "the secretary's compromise figure")]},
        "siege":    {"lo": 700, "hi": 950, "confidence": "good", "claims": [
            ("Cortés [C3]", "86 horse, 118 crossbow/arquebus, ~700 foot, 13 brigantines",
             "his own muster at Texcoco, the war's best-documented count")]},
    },
    "Tlaxcalteca and Nahua allies": {
        "landing":  {"lo": 0, "hi": 0, "confidence": "good", "claims": [
            ("—", "no indigenous allies yet — the coalition does not exist",
             "the war's later shape is invisible at the landing")]},
        "march":    {"lo": 2000, "hi": 8000, "confidence": "contested", "claims": [
            ("Cortés [C2]", "a limited Tlaxcalteca escort (he says he declined more)",
             "downplays dependence on allies throughout"),
            ("[MC]; Lienzo de Tlaxcala", "thousands of warriors and porters from the first march",
             "Tlaxcala's petition-era memory of its indispensability"),
            ("Totonac contingent [C2][BD]", "~400-1,300 porters and warriors from Cempoala",
             "the first allied manpower, rarely counted as an army")]},
        "merged":   {"lo": 2000, "hi": 6000, "confidence": "contested", "claims": [
            ("[BD]", "Tlaxcalteca in the palace siege with the garrison",
             "their dead in the breakout went largely uncounted"),
            ("modern [TH][HAS]", "several thousand allied troops trapped in the city with the Spaniards",
             "reconstructions from the breakout's order of march")]},
        "survivors": {"lo": 1000, "hi": 3000, "confidence": "contested", "claims": [
            ("Cortés [C2]", "~2,000 allied dead on the Noche Triste",
             "the only Spanish attempt at an allied casualty figure"),
            ("[FC][AT]", "the canals full of the dead — no count taken",
             "the Mexica remembered the scale, not the number")]},
        "siege":    {"lo": 24000, "hi": 200000, "confidence": "contested", "claims": [
            ("Cortés [C3]", "'more than 150,000' allies at the height of the siege",
             "inflating the host inflates the victory — and the dependence he elsewhere hides"),
            ("Alva Ixtlilxóchitl", "Texcoco alone contributed hundreds of thousands, army and labour",
             "the Acolhua chronicler claiming his ancestor's share of the conquest"),
            ("modern [HAS][TH]", "tens of thousands under arms at any one time; totals across the siege far higher",
             "all reconstructions; the true number is unrecoverable — hence the band's width")]},
    },
    "Mexica defenders": {
        "landing":  {"lo": 0, "hi": 0, "confidence": "none", "claims": [
            ("—", "not yet at war", "")]},
        "march":    {"lo": 0, "hi": 0, "confidence": "none", "claims": [
            ("—", "the empire receives the column as embassy, not invasion", "")]},
        "merged":   {"lo": 20000, "hi": 60000, "confidence": "contested", "claims": [
            ("[BD][C2]", "the risen city's warriors 'without number' in the palace siege",
             "besieged men estimating a sea of enemies"),
            ("modern [HAS]", "the city could plausibly field some tens of thousands",
             "inference from contested population figures, nothing better exists")]},
        "survivors": {"lo": 20000, "hi": 60000, "confidence": "contested", "claims": [
            ("[C2][GOM]", "a vast host intercepts at Otumba",
             "figures of 40,000-200,000 appear in the sources and are not credited by anyone modern"),
            ("modern [HAS]", "a large levy of the lake cities, size unrecoverable",
             "the band repeats the merged-phase estimate for want of anything firmer")]},
        "siege":    {"lo": 30000, "hi": 80000, "confidence": "contested", "claims": [
            ("[C3][BD]", "the city's full remaining strength plus refugees",
             "no defender muster survives; population itself is contested 50,000-200,000+"),
            ("modern [CMH]", "siege deaths 40,000-100,000+ including civilians, famine and disease",
             "every figure a construction on a contested base")]},
    },
}


def band(contingent: str, phase: str):
    return SERIES[contingent][phase]


def phase_t(phase_id: str) -> float:
    for pid, (y, m, d), _ in PHASES:
        if pid == phase_id:
            return t_of_julian(y, m, d)
    raise KeyError(phase_id)


def app_series():
    """[[t, {contingent: [lo, hi]}], ...] — the app-artifact form."""
    out = []
    for pid, (y, m, d), label in PHASES:
        row = {c: [SERIES[c][pid]["lo"], SERIES[c][pid]["hi"]] for c in SERIES}
        out.append([round(t_of_julian(y, m, d), 4), label, row])
    return out


def _selftest():
    pids = [p[0] for p in PHASES]
    assert pids == sorted(pids, key=lambda p: phase_t(p)), "phases out of order"
    for c, phases in SERIES.items():
        assert set(phases) == set(pids), f"{c}: phase mismatch"
        for pid, b in phases.items():
            assert b["lo"] <= b["hi"], (c, pid)
            assert b["confidence"] in CONFIDENCE, (c, pid)
            assert b["claims"], (c, pid)
            for s, cl, note in [(a[0], a[1], a[2]) for a in b["claims"]]:
                assert s and cl, (c, pid)
            # a contested band must actually be wide, and must carry >1 claim
            if b["confidence"] == "contested":
                assert len(b["claims"]) >= 2 or b["hi"] == 0, (c, pid)
                assert b["hi"] >= 1.5 * max(b["lo"], 1), (c, pid, "band too narrow to be honest")
    # The argument in one assertion: at the siege, indigenous allies outnumber
    # Spaniards by at least an order of magnitude on EVERY reading.
    s = SERIES["Spanish"]["siege"]; a = SERIES["Tlaxcalteca and Nahua allies"]["siege"]
    assert a["lo"] >= 10 * s["hi"] * 0.8, "the coalition claim fails its own numbers"
    print(f"selftest OK — {len(SERIES)} contingents × {len(PHASES)} phases; "
          f"siege: Spanish {s['lo']}-{s['hi']} vs allies {a['lo']:,}-{a['hi']:,}")


if __name__ == "__main__":
    _selftest()
    print("\nwho fought, phase by phase (lo-hi):")
    for pid, _, label in PHASES:
        print(f"\n  {label}")
        for c in SERIES:
            b = SERIES[c][pid]
            if b["hi"] == 0:
                continue
            print(f"    {c:32} {b['lo']:>7,} - {b['hi']:>7,}  ({b['confidence']})")
