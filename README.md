# Aztec Conquest

The fall of Tenochtitlan, 1502–1550 — an interactive model of the coalition that pulled the
Mexica empire apart.

**Live:** https://augustg97.github.io/aztec-conquest/ (GitHub Pages serves `main:/docs`)
**Contact:** augustgweon@gmail.com

*("Aztec" appears in the title for findability. It is a modern coinage and never a
self-designation; the model itself says **Mexica** for the people, **Triple Alliance** for the
polity, and each altepetl's own name. The About panel explains this once.)*

---

## 1. What this is trying to be

A **model**, not a slideshow. The app ships an altepetl gazetteer, dated cited events, an
allegiance state machine, tribute and campaign geometry, and a reconstructed Basin substrate —
state and rules — and assembles the world at render time for whatever date the timeline holds.
Nothing is a pre-rendered picture of a moment.

That choice is the whole architecture, and everything below follows from it:

- Allegiance is **computed per altepetl per day** from dated events and the state machine, so
  the map's colouring *is* the model's argument — a coalition assembling, not two sides trading
  territory.
- The siege state (supply, water, lake control) is **derived from causeway/aqueduct/brigantine
  control events**, so the city's strangulation is a consequence, not an animation.
- Every layer is derived from the same underlying data, so the layers cannot disagree with each
  other.

**The claim** (SCOPE.md §1): the Mexica empire was not defeated by 500 Spaniards. It was pulled
apart along its own fracture lines by a coalition of Nahua city-states — above all Tlaxcala
and, later, Texcoco — who found in Cortés's company a lever against a tributary hegemony most
had entered under duress within living memory. Disease, a lake city with four cutable arteries,
and steel at the margin decided how fast; the coalition decided whether. **The default view is
the argument: if a viewer's first glance shows two colours, the model has already lied.**

### Goals

1. **Veracity first.** Where the record says something, follow it — the dated skeleton of the
   campaign is authored from the sources, cited card by card. Where it does not, model the
   mechanism and say plainly that it is modelled: allegiance, epidemic spread, lake level and
   siege state are mechanisms, and the About panel says so.
2. **Coherence.** One world, internally consistent: one gazetteer, one event list, one calendar
   module, one georeferenced frame — every layer reads from them.
3. **Detail that survives inspection.** At full zoom the finest legible things — a causeway
   breach, a bridge, a chinampa district — sit on a Basin substrate built from a 15 m DEM and a
   named lake reconstruction, scored against archaeology. The interesting scale is the city,
   and the byte budget is spent there.
4. **Honesty about uncertainty.** Force numbers are contested by an order of magnitude,
   population and mortality more; contested cards carry a "What the sources say" section
   (`accounts:`) naming who claims what and why they would. The UI labels reconstruction as
   reconstruction, correlation as correlation, and degrades toward "we do not know" rather than
   toward confident invention.

---

## 2. Working rules

Standing constraints on how work is done here, not suggestions. Each came from a specific
failure. *(Copied from `Modeling Studio/references/WORKING-RULES.md` — keep in sync; add rules
as new failures produce them.)*

**2.1 Always visually verify.** An update is not done when the data contains the value. It is
done when it has been rendered and looked at.

**2.2 Fix the system, not the instance.** Make the change at the level that fixes the whole class
across the whole timeline.

**2.3 Prefer structural, model-based changes over cosmetic ones.** Model the object or process;
let the appearance fall out of it.

**2.4 Measure before tuning.** If you cannot say what the number is now, you cannot say your
change improved it.

**2.5 Track every request; never silently drop one.** If something cannot be done, say so and say
why.

**2.6 Always deploy, and verify the live artefact.** Local-only changes read as "not done".

**2.7 Never ship on an average.** Score every item individually and classify every regression.

**2.8 When an audit disagrees with the app, check the audit first.**

**2.9 Say what is contested.** Confidence is a field on the data, not a footnote.

**2.10 "Unknown" is a legitimate return** — and where a fallback is unavoidable, the UI labels it.

### Project-specific rules

**2.11 Never state a contested claim flatly.** Anything the sources dispute carries an
`accounts:` array and renders "What the sources say". The card audit enforces it. This subject's
sources are witnesses to their own case; silent adjudication in either direction is the failure
mode.

**2.12 Every date carries its source system.** Julian, Gregorian, xiuhpohualli or tonalpohualli
— conversions only through `Research/modeling/calendar.py`, never by eye. The Nahua↔Julian
correlation is contested: attested Nahua dates are facts, their Julian equivalents are
correlations and are marked as such.

**2.13 Nahuatl endonym first, everywhere.** *Mēxihco-Tenōchtitlan (Tenochtitlán)*. Whose names
the map uses is itself a claim, and this is the map's answer.

**2.14 Ranges, not numbers, for contested quantities.** Forces, population, mortality. The
readouts draw bands. A single confident number anywhere in that territory is a bug.

**2.15 A georeference is a measurement with an error.** Control points and residuals recorded
per historical map in `Research/modeling/georef.py`; the residual is honest metadata, not noise
to hide.

---

## 3. Repository layout

```
web/            the app: index.html, css/, js/, data/ (content as JS literals), fields/
docs/           the built static site — GitHub Pages serves main:/docs
build/          offline pipeline: georeferencing, terrain/lake fields, card generation → web/
Research/       the research programme; NEVER imported by build/ or web/
  SOURCE-SURVEY.md      what exists, per layer, with licence and frame (Phase 2 output)
  MODEL-GAPS.md         the register: every open item, prioritised — the handover surface
  DATA-SCHEMA.md        the card/entity schema contract
  modeling/             runnable stdlib-only models + audits (calendar.py, georef.py, …)
  research/             domain dossiers
  research reports/     white papers, STAGED-CHANGES.md, NO-REGRESSION-PROTOCOL.md
  figures/              authored/ (ours) + collected/ (licence-gated, MANIFEST.json)
SCOPE.md        the contract — claim, extent, layers, frame, boundary, non-goals
HANDOFF.md      live state + work queue for the next session
CLAUDE.md       standing instructions for Claude sessions
```

---

## 4. The layers

| layer | kind | source or mechanism |
|---|---|---|
| Basin terrain + lake c. 1519 | authored (reconstructed) | INEGI CEM 15 m DEM minus post-conquest drainage, gated by a named lake reconstruction |
| Lake level (seasonal/annual) | modelled | closed-basin rainfall seasonality, calibrated to the 1519 reconstruction; Nezahualcoyotl's dike as control structure |
| Chinampas, causeways, dikes, aqueducts | authored | archaeology + 1524 Nuremberg map + colonial surveys |
| Altepetl (~200+) | authored | Codex Mendoza provinces, gazetteers, Gerhard |
| **Allegiance (the spine)** | **modelled** | per-altepetl state machine: `tributary → contested → allied-to-coalition → occupied`, driven by dated events, distance, tributary burden, neighbour state |
| Tribute flows | authored + interpolated | Codex Mendoza / Matrícula de Tributos, arcs province → capital |
| Campaign track | authored | dated itinerary from the chronicles, disputed segments flagged |
| Force composition | modelled from authored series | stacked series: Spanish, Tlaxcalteca, Texcocan, Huexotzinca, … — the argument-carrying readout |
| Epidemic | modelled | spread on the altepetl exchange network from the documented introduction; mortality as an explicit wide band |
| Siege state | modelled | causeway/aqueduct/brigantine control → supply and water per district |
| Events (~90) | authored | dated markers, each a card with sources |
| Chapters (~10) | authored | narrative eras |

Full table with engine assignments: SCOPE.md §3.

---

## 5. Subsystems

To be written as they are built. Planned spine, in build order:

1. `calendar.py` — the four calendar systems and their conversions, with selftest (the frame,
   as code).
2. `georef.py` — control points + residuals for the 1524 map and the lake reconstruction.
3. The altepetl gazetteer (name, endonym, coordinates, province, entry into tributary system,
   confidence).
4. The allegiance state machine with its selftest.
5. The card generator + card audit (schema in `Research/DATA-SCHEMA.md`, `accounts:` enforced).
6. The archaeological-witness audit (causeways, aqueducts, lake extent, city footprint).

---

## 6. Build and deploy

```bash
# run the app locally (no build needed for the shell)
python3 -m http.server 8140 --directory web

# validators — the build refuses to publish on a regression
python3 "Research/modeling/audit_all.py"
python3 "Research/modeling/audit_all.py" --quick

# build + deploy (to be written in build/): stamps data version BEFORE copying the app file,
# copies web/ -> docs/, then commit + push; verify the live stamp after every push
```

| check | baseline | what it catches |
|---|---|---|
| *(to be built in round 1 — card audit, existence windows, witness audit)* | — | — |

The baselines are not all zero and should not be — a genuine open disagreement belongs in the
baseline with a note. **None of them may move backwards**; when one legitimately improves,
tighten the baseline in the same commit. `SKIP_AUDIT=1` overrides, deliberately awkwardly.

**Verify the live data-version stamp after every push.**

---

## 7. Traps

Failures that cost real time on prior projects and apply with force here. *(General catalogue:
`Modeling Studio/references/TRAPS.md`; add new ones to both.)*

- **A1, two sources in different frames** — four calendar/naming/coordinate systems in this
  subject. Everything goes through `calendar.py` / `georef.py`. Julian vs Gregorian alone is
  ten days and a moving year boundary.
- **A2, the record's boundary** — here it runs through *kinds of claims* (motive and speech
  worst of all), not through a date. The `accounts:` mechanism is the boundary behaviour.
- **The DEM is not the substrate** — the modern DEM shows the basin after four centuries of
  drainage and fill. 1519 terrain = DEM minus post-conquest modification, gated by the named
  lake reconstruction, and labelled as a reconstruction.
- **A4, correct licence ≠ correct subject** — every collected figure stays
  `verified_subject: false` until a human looked at it.
- **D2, the deploy that looks like it never landed** — data-version stamp bumped before the app
  file is copied; live value checked after every push.

---

## 8. Sources

| role | source |
|---|---|
| terrain | INEGI CEM 4.0 (15 m); Copernicus GLO-30 fallback |
| lake at 1519 | one named published reconstruction (round 1 names it; candidates in SOURCE-SURVEY) |
| city plan | 1524 Nuremberg map, Newberry scan (public domain), georeferenced with residual |
| tributary system | Codex Mendoza (INAH digital edition), Matrícula de Tributos, Gerhard, Smith & Berdan |
| Nahua account | Florentine Codex Book XII (Getty Digital Florentine Codex) — primary, same register as Cortés |
| Spanish accounts | Cortés *Cartas de relación*; Bernal Díaz *Historia verdadera* |
| other chronicles | Durán; Ixtlilxochitl (Texcocan); Muñoz Camargo (Tlaxcalteca); *Anales de Tlatelolco* |
| independent witness | Templo Mayor excavations; causeway/dike surveys; Basin settlement survey (Sanders, Parsons & Santley 1979; tDAR project 192) |

**Canonical frame:** WGS84 lon/lat · Julian dates (Gregorian alongside; Nahua dates attested,
correlations marked) · Nahuatl endonyms first · Mexica / Triple Alliance — every source is
converted into it; the conversions are in `Research/modeling/calendar.py` and
`Research/modeling/georef.py`.

---

## 9. Known limits

The section that makes the rest credible.

- **The lake shoreline is a reconstruction.** The lakes were drained after the conquest; every
  shoreline drawn is a published reconstruction, and the model names the one in use rather than
  averaging competitors.
- **Indigenous force numbers are contested by an order of magnitude**, Tenochtitlan's
  population (50,000–200,000+) and epidemic mortality more so. The model draws bands and the
  cards say `contested`.
- **Motive and speech are the least constrained thing in the subject.** Famous set-pieces
  (Moctezuma's submission, the "returning god") are shown as what the sources say, with the
  scholarship's argument, never asserted.
- **The Nahua↔Julian calendar correlation is itself contested** — Nahua dates are shown as
  attested; Julian equivalents are correlations.
- **Allegiance below the altepetl is not modelled** — the sources cannot support it.
- **The 1524 map is schematic**; street-level Tenochtitlan outside the ceremonial precinct and
  causeways is not reconstructed.

---

## 10. Reference material

- `Modeling Studio/worked-example/AZTEC-CONQUEST.md` — the kickoff scoping this project adopted.
- `Modeling Studio/references/` — working rules, architecture patterns, research method, audit
  patterns, traps, sourcing policy.
- Reference imagery and scholarly maps live in `reference/` (gitignored) — measured against,
  never reproduced.

`HANDOFF.md` carries the live state, the measured facts, and the work queue for a fresh session.
