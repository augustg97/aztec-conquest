# Research — conquest-of-Mexico knowledge base for Aztec Conquest

**Started 2026-07-27.** A standing research programme and expert system covering the Basin of
Mexico c. 1519 (terrain, lakes, hydraulic works), the Triple Alliance tributary system, the
altepetl network, the 1519–21 campaign and its sources, the epidemic, and the 1521–50
aftermath.

**This folder does not change the model.** Nothing here is imported by `build/`. Its output is
*evidence and models* that inform continuous updates to the app — so that when a number, a
boundary, a label or a card changes, the change has a citation and a mechanism behind it rather
than a guess.

---

## How it is organised

```
Research/
├── SOURCE-SURVEY.md              what data exists, in what frame, under what licence
├── MODEL-GAPS.md                 the register that ties research to app defects
├── research/                     evidence: dossiers per domain, with sources and caution flags
│   ├── 01-basin-and-lakes/       terrain, lake system, hydraulic works, chinampas
│   ├── 02-tributary-system/      provinces, tribute, how and when each altepetl entered
│   ├── 03-the-campaign/          the dated itinerary and the events, per source
│   ├── 04-the-sources/           each chronicle's vantage, motive and reliability
│   ├── 05-epidemic/              introduction, spread, the mortality debate
│   ├── 06-aftermath-1521-50/     encomienda, congregación, drainage, continued campaigns
│   └── 09-source-documents/      fetched primary material, kept verbatim
├── research reports/             illustrated white papers, each ending in actions
│   └── STAGED-CHANGES.md         the handover surface
├── modeling/                     runnable models + read-only audits
└── figures/
    ├── authored/                 generated FROM the models, so they cannot drift
    └── collected/                third-party + MANIFEST.json (licence + review verdict)
```

*(Dossier folders are created as their round produces them; 01 and 09 exist from the scaffold —
rename/extend to the scheme above as content lands.)*

---

## The models

All runnable, all self-testing. Each prints a worked demonstration.

```bash
cd Research/modeling && python3 <module>.py
```

| module | what it is | current state |
|---|---|---|
| `calendar.py` *(planned, A1)* | Julian ↔ Gregorian ↔ xiuhpohualli/tonalpohualli, correlation constant explicit | not yet built |
| `georef.py` *(planned, A2)* | control points + residuals for the 1524 map and the lake reconstruction | not yet built |
| `allegiance.py` *(planned, B2)* | the per-altepetl state machine | not yet built |

## The audits

Read-only; they change nothing.

| script | catches | current result |
|---|---|---|
| `audit_all.py` | runner (scaffolded) | no audits registered yet |
| card audit *(planned, C1)* | a contested claim stated flatly; missing `accounts:`; era gaps | not yet built |
| witness audit *(planned, E1)* | causeways/aqueducts/lake/footprint vs archaeology | not yet built |

## The dossiers

| file | covers |
|---|---|
| *(none yet — round 1 opens 01, 02, 03, 04)* | |

## The white papers

| paper | thesis |
|---|---|
| *(planned, round 1)* "The conquest had more participants than the story does" | the force-composition question, measured, with what each source claims and why each would claim it |

---

## Working method

1. **Verify, don't reconstruct from memory.** Every claim traces to a named source; where a
   fetched source is internally inconsistent, the dossier says so rather than propagating it.
2. **Say what is contested.** A card that states an open question flatly misrepresents how well
   it is known.
3. **Prefer a model to a table.** Every finding that could be a hand-written row is written as a
   function with a selftest, so a new input produces a defensible answer without new authoring.
4. **Figures are generated, not drawn.** They read from the same modules, so a corrected value
   propagates automatically.
5. **Every white paper ends in actions**, and every action lands in `MODEL-GAPS.md`.

---

## Status

**v0 (kickoff), 2026-07-27.**

*Round 0 (kickoff)* — scope adopted from the Studio's worked example; source survey done
(all P1 sources confirmed to exist digitally, licences flagged for verification); scaffold
running and visually verified; gap register seeded with 9 items.

No models or audits exist yet. See [`MODEL-GAPS.md`](MODEL-GAPS.md) for the **9 open items,
6 at P1**.

**Round 1, in priority order:**

1. **A1 `calendar.py`** — the frame decision as code, with selftest; every authored date tagged
   with its source system. *Do this before authoring a single dated event.*
2. **A2 georeference** the chosen lake reconstruction and the 1524 Nuremberg map; record the
   residuals. Everything spatial rests on this — and round 1 must **name** the canonical lake
   reconstruction (SOURCE-SURVEY §1 lists the candidates).
3. **B1 the altepetl gazetteer** — name (Nahuatl/Spanish/modern), coordinates, tribute
   province, date and manner of entry into the tributary system, confidence. The model's spine.
4. **B2 the allegiance state machine** with its selftest — the layer that makes this a model.
5. **C1 the `accounts:` schema** + "What the sources say" card section + the card audit that
   fails on a flatly-stated contested claim.
6. **E1 the archaeological witness audit** — score asserted causeways, aqueducts, lake extent
   and city footprint against Templo Mayor / survey literature *before drawing anything on top*.
7. **The first white paper**: *"The conquest had more participants than the story does"* — the
   force-composition series with published ranges, and what each source claims and why.

Then hand findings across `research reports/STAGED-CHANGES.md` per the working rules — research
informs the model; it does not silently edit it.
