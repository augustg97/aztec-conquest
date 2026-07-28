# Model gaps register — Aztec Conquest

Every open item this research programme has produced, tied to the specific subsystem it would
change. **This is the handover surface between research and the build.**

Priority: **P1** = closes a known visible defect · **P2** = adds real fidelity ·
**P3** = correctness housekeeping · **P4** = worth knowing, no action yet.

Status: **RESOLVED** = answered, with the answer recorded · **MEASURED** = quantified and ready
to apply · **DELIVERED** = the artifact exists · **APPLIED** = in the app, with the measurement ·
**RETIRED** = no longer needed · **CLOSED, negative result** = tried, did not work, recorded so
nobody retries it · items with no status are open.

IDs are referenced from white papers, code comments and commit messages. **Never recycle one.**

*Seeded at kickoff 2026-07-27 from the scoping (worked example §11) and the source survey.
The app is currently the scaffold shell with placeholder data — every layer in SCOPE §3 is
unbuilt, so the register is the build order.*

---

## APPLIED

<!-- Rewritten in place as items land, so this file describes the app rather than a wish list. -->

| item | what shipped | measured |
|---|---|---|
| | | |

---

## A. The canonical frame

| # | P | item | touches | from |
|---|---|---|---|---|
| A1 | **P1** | `calendar.py` — Julian/Gregorian/xiuhpohualli/tonalpohualli conversions, correlation constant explicit and swappable, with a selftest; **every authored date tagged with its source system**. The frame decision, as code. Build before authoring a single dated event. | `Research/modeling/calendar.py`, data schema | scoping §5; TRAPS A1 |
| A2 | **P1** | Georeference the lake reconstruction and the 1524 Nuremberg map (Newberry scan, PD, 5000 px); record control points and residuals. Everything spatial rests on this. **Includes naming the canonical lake reconstruction** — candidates in SOURCE-SURVEY §1; never average competitors. | `Research/modeling/georef.py`, `build/` | scoping §5, §7; survey §1 |
| A3 | P3 | Verify flagged licences before anything ships: INEGI CEM exact terms; Getty DFC per-image; Bodleian/INAH facsimile hosts; tDAR redistribution terms. Correct licence ≠ correct subject — subject review too. | `figures/collected/MANIFEST.json` | survey §1; TRAPS A4 |

## B. The spine — gazetteer and allegiance

| # | P | item | touches | from |
|---|---|---|---|---|
| B1 | **P1** | The **altepetl gazetteer**: name (Nahuatl/Spanish/modern), coordinates, tribute province, date and manner of entry into the tributary system, confidence. ~200+ entries from Codex Mendoza + Gerhard + Smith & Berdan. The model's spine. | `web/data/`, generator in `build/` | scoping §3 |
| B2 | **P1** | The **allegiance state machine** — `tributary → contested → allied-to-coalition → occupied` per altepetl, driven by dated events, distance, tributary burden, neighbour state — with its selftest. **The layer that makes this a model**; everything else is scenery until it exists. | `Research/modeling/allegiance.py` → app | scoping §3 |

## C. The card system

| # | P | item | touches | from |
|---|---|---|---|---|
| C1 | **P1** | The **`accounts:` schema** and the "What the sources say" card section, plus the card audit that fails when a contested claim is stated flatly, when `accounts:` is missing on a `contested` card, or when eras leave gaps. Build the generator and the audit together. | `Research/DATA-SCHEMA.md`, card generator, card audit | scoping §6 |

## D. Contested quantities

| # | P | item | touches | from |
|---|---|---|---|---|
| D1 | P2 | Force-composition series with **published ranges rather than single numbers** (Spanish, Tlaxcalteca, Texcocan, Huexotzinca, Mexica), and the stacked readout that draws the band. Feeds white paper 1. | data series + readout | scoping §3 |
| D2 | P2 | The epidemic model on the altepetl exchange network — seeded at the documented introduction, mortality stated as an explicitly wide band, never a number. | `Research/modeling/epidemic.py` → layer | scoping §3 |

## E. The independent witness

| # | P | item | touches | from |
|---|---|---|---|---|
| E1 | **P1** | The archaeological witness audit: score asserted causeway and aqueduct positions, lake extent and city footprint against Templo Mayor excavations, causeway/dike surveys and the Basin settlement survey (tDAR 192) — **before drawing anything else on top**. A beautiful siege drawn on a wrong lake is worse than no siege. | `Research/modeling/audit_witness.py` | scoping §7 |

## F. Housekeeping

| # | P | item | touches | from |
|---|---|---|---|---|
| F1 | P3 | Anachronism table for the card audit — vocabulary, technology and political terms with their not-before dates ("Mexico" as polity name, "New Spain", horses as familiar, etc.). | card audit | scoping §11 |

---

**What the audits did NOT find:**

<!-- The section that makes the register trustworthy, and stops the next round re-litigating
     settled questions. List the checks that passed, with their numbers. -->

*(No audits exist yet — nothing has been checked. This section fills in from round 1.)*

---

**Count: 9 items — 6 at P1.** The ones that would move the model furthest, in order:

1. **A1 `calendar.py`** — the frame as code; prevents the most expensive possible bug in this
   subject, and every authored date depends on it.
2. **A2 georeferencing + naming the lake reconstruction** — everything spatial rests on it.
3. **B1 the gazetteer** then **B2 the allegiance state machine** — the spine; the difference
   between a model and an illustrated chronology.
4. **C1 the `accounts:` card contract** — the central UI decision, and retrofitting it at card
   600 costs a week.
5. **E1 the witness audit** — the instrument every later spatial dispute is settled with.
