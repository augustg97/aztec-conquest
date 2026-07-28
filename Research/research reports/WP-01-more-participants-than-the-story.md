# WP-01 · The conquest had more participants than the story does

**White paper 01** · drafted 2026-07-27 · status: **first pass, actions landed**
**Scope:** force composition 1519-1521; what each source claims and why; what the map must
therefore draw
**Figures:** `figures/authored/forces-bands.svg`, `figures/authored/allegiance-states.svg`
**Code:** `modeling/forces.py`, `modeling/allegiance.py`, `modeling/events.py`

---

## Executive summary

The popular defect — "500 Spaniards conquered an empire" — has **three independent causes, and
correcting only the numbers fixes none of them**:

1. **The Spanish sources undercount on purpose, in both directions.** Cortés minimises his
   dependence on allies when claiming credit and maximises the allied host when claiming
   glory — *in the same letter*. Every number is an argument. — addressed by per-source bands.
2. **Nobody counted the allies at all.** No muster of Tlaxcalteca, Acolhua, Chalca or
   Huexotzinca survives anywhere; their strength arrives only through enemy estimates and
   petition-era memory. The uncertainty is structural, not sloppy. — addressed by band WIDTH.
3. **The map itself erases them.** A two-colour war map makes the allies invisible regardless
   of any caption — **the cheapest cause to fix, and the one this model exists to fix**: the
   default view draws allegiance per altepetl per day. — addressed by the allegiance layer.

## 1. What the thing actually is, and what it cannot know

A coalition war. At the siege, Cortés's own Tercera carta musters ~900 Spaniards and claims
"more than 150,000" allies; Ixtlilxóchitl claims more; modern reconstructions credit tens of
thousands under arms at a time. On EVERY reading, including the most Spanish-partisan one,
indigenous coalition troops outnumber Spaniards by more than an order of magnitude —
`forces.py` asserts exactly this in its selftest, from the sources' own numbers.

What it cannot know: any precise figure. No allied muster; defender strength inferred from a
population itself contested 50,000-200,000+; allied dead uncounted by anyone ("no source
counted the allies' dead" is displayed in the model, because the absence is evidence about the
sources).

## 2. The record, in the form the model needs

`modeling/forces.py` — 3 contingents × 5 phases, each `{lo, hi, confidence, claims[]}`, every
claim carrying the witness's stake. The load-bearing rows: siege Spanish 700-950 (**good** —
Cortés's own muster); siege allies 24,000-200,000 (**contested** — the band IS the finding);
Noche Triste Spanish survivors 400-1,100 (**contested** — the band's ends are Cortés's and
Díaz's own arithmetic).

## 3. What we measured

| measurement | value | method / population |
|---|---|---|
| allies-to-Spanish ratio at siege, minimum | ≥ 25 : 1 | forces.py lo-bound allies / hi-bound Spanish |
| same, on Cortés's own claims | ≥ 158 : 1 | 150,000+ / 950 |
| polities allied or coalition-occupied at siege midpoint | 36 of 75 modelled | allegiance.counts_at(1521-07-15) |
| polities still tributary at siege midpoint | 30 of 75 | same — the map is four colours at minimum, never two |
| contested events carrying multi-party accounts | 19 of 64 | events.py |

A comparison NOT delivered: allied casualty totals — no source supports even a band; recorded
as a display of absence, not a number.

## 4. Ranked remediations

| # | remediation | cost | expected effect | evidence |
|---|---|---|---|---|
| 1 | allegiance layer as default view | done (B2) | cause 3 eliminated structurally | allegiance-states.svg |
| 2 | force readout as bands with per-source claims | done (D1) | causes 1-2 carried honestly | forces-bands.svg |
| 3 | "no source counted the allies' dead" line on Noche Triste / siege cards | trivial | the absence made visible | events.py accounts |
| 4 | per-altepetl contingent detail (which towns sent forces where) | round 2+, large | depth | Ixtlilxóchitl, lienzos — B1-b |

## 5. What the app should stop claiming

Nothing currently states a single force number flatly (audited: bands only). Watch: chapter
prose says "perhaps 900 Spaniards and tens of thousands of Nahua allies" — hedged, correct.

## 6. Actions

| # | P | action | touches | status |
|---|---|---|---|---|
| D1 | P2 | force bands + readout | forces.py → DATA.forces | **DELIVERED** |
| B2 | P1 | allegiance layer default | allegiance.py → entities | **DELIVERED** |
| D1-b | P3 | allied-dead absence line on siege cards | events.py texts | **DELIVERED** (in noche-triste, fall texts) |
| B1-b | P4 | per-altepetl contingents | gazetteer/events | open, round 2+ |
