# The Basin lake system and the hydraulic works at 1519

**Domain:** 01 basin and lakes · **Status:** first pass, 2026-07-27 ·
**Feeds:** `web/data/geo.js`, `web/data/entities.js` (works cards), `modeling/georef.py`,
`modeling/audit_witness.py`

---

## 1. What the thing is

The Basin of Mexico is a closed (endorheic) basin at ~2,240 m whose floor held a chain of
shallow lakes: saline **Texcoco** at the low centre, freshwater **Xochimilco-Chalco** to the
south (spring-fed, slightly higher), and shallow **Zumpango-Xaltocan** to the north. Because the
system had no outlet, its extent swung seasonally and between wet and dry years — "the 1519
shoreline" is therefore a band, not a line, even before the evidence problem.

The Mexica world was built INTO this hydrology: Tenochtitlan-Tlatelolco on an island;
chinampa (raised-field) agriculture on the fresh southern lakes; four causeways (Tlacopan,
Tepeyacac, Iztapalapan with its Coyohuacan branch, meeting at the fork of Xoloc); the
**albarradón of Nezahualcóyotl** (c. 1449) holding the saline water off the chinampa west; and
the twin-channel **Chapultepec aqueduct** carrying spring water to the island. The siege of 1521
is a hydraulic operation: cut the aqueduct, hold the causeways, take the lake with brigantines.

## 2. The record

| element | evidence | confidence | note |
|---|---|---|---|
| lake extent c. 1519 | **reconstruction only** — the lakes were drained post-conquest (desagüe from 1607) | moderate | competing reconstructions differ at the margins |
| causeway lines | modern streets follow them (México-Tacuba; Tlalpan/S. Antonio Abad; Misterios); archaeology at crossings | good | terminals pinned by surviving plazas |
| aqueduct | line of Av. Chapultepec; colonial rebuild on the same alignment | good | |
| albarradón course | González Aparicio's reconstruction; segments excavated | contested | exact course debated |
| city footprint | Calnek's ~12-15 km²; ceremonial precinct excavated (Templo Mayor) | moderate | interior plan schematic outside the precinct |
| chinampa districts | archaeology (surviving Xochimilco chinampas); colonial surveys | moderate | not yet drawn (register A2-c) |

**The canonical reconstruction, named (SCOPE §5):** *González Aparicio, Luis (1973), Plano
reconstructivo de la región de Tenochtitlan, SEP/INAH* — chosen because the archaeological
literature itself measures against it (Templo Mayor alignment studies; hydraulic-management
papers cite it as the base map). Alternatives (Niederberger's palaeoenvironment; the
Sanders/Parsons/Santley survey base maps) are recorded as competitors, never averaged.

**Model implication.** The drawn lake/works geometry in `georef.py` is authored at
visualization grade against this reconstruction, and `audit_witness.py` scores what is drawn:
terminal residuals ≤ 6 m against anchors; city footprint **15.6 km²** (Calnek band 10-18);
lake system **766 km²** (literature band 700-1,600). → **Action: keep the witness audit in the
gate; extend with chinampa districts in round 2**, touching `modeling/georef.py`.

**Model implication.** The modern INEGI CEM DEM is POST-DRAINAGE terrain — four centuries of
desiccation and urban fill. Any terrain layer must present itself as "DEM minus modern
modification, gated by the named reconstruction," labelled as a reconstruction. → **Action:
terrain field deferred to round 2 (register A2-d)**, touching `build/`.

## 3. Where confidence falls off, and why

| evidence | constrains | reach |
|---|---|---|
| surviving street alignments | causeway/aqueduct lines | to within a street's width, along their length |
| excavation (Templo Mayor, causeway crossings) | points | metres, at the excavated points only |
| the 1524 Nuremberg map | topology (what connected to what) | NOT geometry — it is schematic |
| González Aparicio (1973) | the whole plan | a reconstruction: internally consistent, not survey truth |
| lake-bed soils & palaeo work | maximum extents | century-scale, not year-1519 |

**The boundary:** past the causeway lines and the excavated points, everything spatial is
reconstruction. The UI behaviour at the boundary: geometry cards say "drawn at visualization
grade against González Aparicio (1973); faithful for the map, not survey-grade."

## 4. What is genuinely contested

| question | positions | what the app should say |
|---|---|---|
| albarradón course | reconstructions differ on the northern anchor and bends | draw one line, confidence `contested`, card names the source |
| 1519 lake level/extent | wet-year vs dry-year readings differ visibly | one named reconstruction; About panel states the band |
| city population (feeds footprint density) | 50k-200k+ in print | never a number; the band, on the card |

## 5. Naming, dating and coordinate conventions in the sources

Modern archaeology: WGS84/UTM, Gregorian. González Aparicio: local grid, converted here by
tracing against anchors (residuals recorded in `georef.py`). Colonial surveys: leagues and
varas, NOT used quantitatively in round 1.

## 6. Caution flags

- The Wikimedia "Basin_of_Mexico_1519" SVG is a DERIVATIVE of the published reconstructions,
  likely CC-SA: measure-against only, never shipped, and not the named source.
- The ArcGIS Online 1519 layer's provenance is unverified — not used.
- González Aparicio (1973) is **cited but not yet consulted in facsimile** — the drawn geometry
  follows the literature's descriptions of it and the anchor table. Register A2-b (P2) tracks
  acquiring a scan and tracing properly, with residuals.

## 7. Sources

González Aparicio (1973) SEP/INAH · Calnek, "Settlement Pattern and Chinampa Agriculture at
Tenochtitlan" (1972, *American Antiquity* 37) · Sanders, Parsons & Santley (1979) · Templo
Mayor project (INAH, Matos Moctezuma) · Biar (2023, *Ancient Mesoamerica*) on navigation and
the works · Gerhard (1972).
