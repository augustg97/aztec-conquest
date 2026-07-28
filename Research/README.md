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
| `calendar.py` | Julian/Gregorian/JDN + tonalpohualli/xiuhpohualli, correlation anchored 13 Aug 1521 = 1 Cóatl, explicit and swappable | **selftest green** — 3 Caso pairs mutually consistent; reproduces Caso's veintena days |
| `gazetteer.py` | 75 polities: endonym/exonym/modern, coords, province, tributary entry, confidence | **selftest green** — 30 of ~38 Mendoza provinces; omissions recorded (B1-b) |
| `events.py` | 64 dated cited events 1502-1550; 19 with `accounts`; 79 allegiance effects; 14 track points | **selftest green** — contested ⇒ ≥2 accounts enforced |
| `allegiance.py` | the per-altepetl state machine — the spine | **selftest green** — 75 timelines, 228 transitions, all legal |
| `georef.py` | anchors + authored geometry after **González Aparicio (1973)**, the named reconstruction; geodesy helpers | **selftest green** — terminal residuals ≤ 6 m |
| `forces.py` | force composition as per-source ranges, 3 contingents × 5 phases | **selftest green** — asserts allies ≥ 10× Spanish at siege from the sources' own numbers |
| `emit.py` | the card generator + artifact emitter → staged-artifacts/ | **selftest green** — 82 entities, 64 events, 167.5 KB |
| `make_figures.py` | authored SVG figures from the models | both figures generated + visually verified |

## The audits

Read-only; they change nothing.

| script | catches | current result |
|---|---|---|
| `audit_all.py` | the gate: refuses on regression vs baseline | **all at baseline** |
| `audit_cards.py` | era gaps; contested stated flatly; missing sources/allegiance; unlabelled correlations; anachronisms; banned naming | **0 HIGH / 0 MED** — 7 checks, each selftest-proven to fire |
| `audit_witness.py` | drawn geography vs the archaeological witness + literature bands | **0 HIGH / 0 MED** — caught 5 drowned towns in draft geometry before anything shipped; footprint 15.6 km², lakes 766 km² |

## The dossiers

| file | covers |
|---|---|
| `01-basin-and-lakes/01-lake-system-and-works.md` | the lake system, the works, the reconstruction problem, the named canonical source |
| `04-the-sources/01-witnesses-to-their-own-case.md` | the five source families, each one's stake, and the `accounts:` doctrine |
| *(02 tributary system, 03 campaign — record lives in gazetteer.py/events.py; prose dossiers pending, register B2-b)* | |

## The white papers

| paper | thesis |
|---|---|
| `WP-01-more-participants-than-the-story.md` | the "500 Spaniards" defect has 3 independent causes; the cheapest is the map itself, fixed structurally by the allegiance layer; measured ratios from the sources' own numbers |

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

**v1 (research round 1 complete), 2026-07-27.**

*Round 1* — all six kickoff P1s DELIVERED as staged artifacts: the calendar frame as code, the
named lake reconstruction (González Aparicio 1973) with authored geometry and residuals, the
75-polity gazetteer, the 64-event skeleton, the allegiance machine, the `accounts:` card
system, both audits (0 HIGH / 0 MED, all checks selftest-proven), the force bands, WP-01, and
two authored, visually verified figures.

All selftests pass; `audit_all.py` at baseline. See [`MODEL-GAPS.md`](MODEL-GAPS.md) for the
**8 open items, 0 at P1** — and for what the audits did NOT find, and the honest corrections
(the witness audit caught 5 drowned towns in the draft geometry; two events were demoted from
`contested` to `moderate` by the accounts-requirement).

**The handover is staged:** `research reports/STAGED-CHANGES.md` lists 7 changes in 3 tiers,
each with artifact, specific edit and gate. `/model-build` executes it.

**Round 2, in priority order:**

1. **D2 the epidemic network model** — the largest unbuilt SCOPE §3 layer (currently events +
   bands, not a mechanism).
2. **D2-b the siege-state mechanism** — causeway/aqueduct/brigantine control → derived supply
   and water per district.
3. **B2-d events to ~90 and the ~40 people cards.**
4. **A2-b/c/d** — trace the reconstruction and the 1524 map properly (scans + control points);
   chinampa districts; the terrain field from INEGI CEM (minus post-conquest modification).
5. **B1-b the remaining Mendoza roster**; **A3 licence verification** before any collected
   figure ships.
