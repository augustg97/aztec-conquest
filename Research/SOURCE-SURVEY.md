# Source survey — Aztec Conquest

*Surveyed 2026-07-27, before any app code was written. This is Phase 2 of `/model-kickoff`.
Access routes were verified by web search at kickoff; licences marked "verify" must be
confirmed on the source's own page before anything ships. Correct licence never implies
correct subject (TRAPS §A4) — every collected figure stays `verified_subject: false` until a
human has looked at it.*

## 1. What data exists, per layer

| layer | source | format | resolution | licence | access |
|---|---|---|---|---|---|
| Basin terrain | **INEGI Continuo de Elevaciones Mexicano (CEM) 4.0** | GeoTIFF/BIL | 15 m, RMSE ≈ 4.8 m | INEGI Términos de Libre Uso (attribution) — **verify exact terms** | inegi.org.mx/app/geo2/elevacionesmex/ — national file ~6.5 GB in 7 parts; **download by area selection instead** (the Basin is ~100 km across) |
| Basin terrain (fallback) | Copernicus GLO-30 DEM | GeoTIFF | 30 m | free with attribution | AWS/Copernicus open data |
| Lake system c. 1519 | published reconstructions; the Wikimedia derivative **"Basin_of_Mexico_1519_map-en.svg"** traces one | SVG / print maps | schematic | Commons file likely CC BY-SA (**share-alike → measure-against-only, do not ship**); the underlying published reconstruction must be identified and named | commons.wikimedia.org; round 1 names the canonical reconstruction (candidates: González Aparicio 1973; Niederberger; Sanders/Parsons/Santley base maps) |
| Lake system c. 1519 (alt) | ArcGIS Online item "Lake Texcoco and Tenochtitlan 1519" (2021) | feature layer | vector | unverified | arcgis.com item b148fcc404f64ec5bf02fbb434b718bb — provenance must be traced before any use |
| City plan, causeways | **1524 Nuremberg (Peypus) map** — Newberry Library scan | JPEG 5000×3168 | schematic plan | **public domain** (Newberry via Wikimedia Commons) | commons.wikimedia.org "Map of Tenochtitlan and Gulf of Mexico, 1524" — shippable, georeferenceable |
| Causeways, precinct | Templo Mayor excavation reports; causeway/dike surveys | publications | site-level | publications (measure-against) | INAH literature; round 1 compiles coordinates |
| Altepetl gazetteer | **Codex Mendoza** (Bodleian MS. Arch. Selden. A. 1) — INAH digital edition; Berdan & Anawalt edition; Gerhard *Historical Geography of New Spain*; Smith & Berdan province lists | facsimile + scholarly tables | ~38 tribute provinces, ~400 towns | facsimile images PD-old (**verify per host**); scholarly tables measure-against; **the place-name data itself is authored from them with citation** | codicemendoza.inah.gob.mx; publicdomainreview.org/collection/codex-mendoza-1542 |
| Tribute flows | Codex Mendoza part 2; **Matrícula de Tributos** | facsimile | per-province goods | as above | INAH |
| Nahua account of the war | **Florentine Codex Book XII** — Getty Digital Florentine Codex | digital edition, images + Nahuatl/Spanish/English text | full manuscript | Getty DFC is open access; **verify per-image licence** before shipping any figure | florentinecodex.getty.edu |
| Spanish accounts | Cortés *Cartas de relación* (1519–26); Bernal Díaz *Historia verdadera* (pub. 1632) | texts | — | **public domain** (16th–17th c. texts; modern translations are NOT — cite, don't reproduce) | multiple editions online |
| Other chronicles | Durán, Ixtlilxochitl (Texcocan), Muñoz Camargo (Tlaxcalteca), *Anales de Tlatelolco* | texts | — | originals PD; modern critical editions measure-against | libraries, archive.org |
| Settlement pattern | **Sanders, Parsons & Santley 1979** *The Basin of Mexico*; **Parsons' Valley of Mexico survey data on tDAR** (project 192); Gorenflo 2015 compilation | monograph + digital archive | site-level survey | tDAR data for research use (**verify terms**); monograph measure-against | core.tdar.org/project/192 |
| Epidemic | documented introduction + modern epidemiological literature (contested) | papers | — | measure-against | round 2 |
| Force composition | the chronicles' own (partisan) numbers + modern scholarship (Hassig, Restall, Thomas, Townsend) | texts | ranges | measure-against | round 1 white paper |

**Shippable:** INEGI CEM derivatives (with attribution), Copernicus DEM derivatives, the 1524
Newberry scan, PD facsimile images (verified per host), data tables authored by us from the
sources with citation.
**Measure-against-only:** every modern scholarly map, table and translation; anything CC-SA/NC;
the Wikimedia lake SVG; tDAR survey data unless its terms allow redistribution (our derived
*audit results* are ours).

## 2. Frames

The most expensive class of bug in this kind of project is two sources silently in different
coordinate, naming or dating systems. Four systems here, not one.

| source | coordinates | calendar / dating | naming | administrative vintage |
|---|---|---|---|---|
| Cortés, Bernal Díaz, Spanish chronicles | none (itinerary prose; leagues vary by chronicler) | **Julian** | Spanish exonyms | pre-1522 tributary system, seen from outside |
| Florentine Codex Bk XII, Nahua annals | none | **xiuhpohualli / tonalpohualli** (year-count + day-count; correlation to Julian is itself contested) | Nahuatl endonyms | Triple Alliance, seen from Tlatelolco |
| Codex Mendoza / Matrícula | none (schematic) | Nahua year glyphs + Spanish glosses | Nahuatl with Spanish gloss | tribute provinces c. 1519, compiled c. 1541 |
| 1524 Nuremberg map | none (schematic plan; orientation west-up) | — | Latinised | city at 1519–21 |
| INEGI CEM 4.0 | **ITRF / WGS84-compatible**, geographic | — | modern | modern (post-drainage terrain!) |
| tDAR settlement survey | survey grids → georeferenced (verify datum per dataset) | archaeological phases | modern site codes + Nahuatl | pre-Hispanic phases |
| modern scholarship | WGS84 maps | Gregorian (usually proleptic-silent!) | mixed | varies |

**Canonical frame chosen:**
- **Coordinates: WGS84 lon/lat.** Every historical map is georeferenced into it and the
  **residual is recorded** — a georeference is a measurement with an error, not a fact.
- **Calendar: Julian** (what the sources use; Gregorian reform is 1582), Gregorian shown
  alongside; Nahua dates shown as attested, their Julian equivalents marked as *correlations*.
- **Names: Nahuatl endonym first**, Spanish exonym second, modern anchor where needed.
- **Polity terms: Mexica** (people), **Triple Alliance** (polity); "Aztec" only in the project
  title and the About panel, explained once.

**Conversions:** written as tested code in `Research/modeling/calendar.py` (Julian ↔ Gregorian
↔ xiuhpohualli/tonalpohualli with the correlation constant explicit and swappable), and
`Research/modeling/georef.py` (control points + residuals per historical map). Every date in
the data carries the system it was authored in. **Never combine two sources without checking
they are in the same frame.**

**Trap specific to this subject:** the modern DEM shows the basin *after* four centuries of
drainage and urban fill. The 1519 terrain is DEM **minus** post-conquest modification, gated by
the lake reconstruction — the DEM alone is not the substrate, it is an input to a reconstruction
that must be labelled as one.

## 3. Where the record stops

The record here is **dense but partisan** — the boundary is not a date, it runs through *kinds
of claims*:

- **well constrained:** the campaign's dated skeleton (multiple independent accounts), the
  ceremonial precinct (excavated), causeway existence and approximate lines (archaeology).
- **reconstruction:** the 1519 lake shoreline (the lakes were drained; every shoreline is a
  published reconstruction, and the model names the one in use).
- **contested by an order of magnitude:** indigenous force numbers; Tenochtitlan's population
  (~50,000–200,000+); epidemic mortality.
- **least constrained of all: motive and speech.** Moctezuma's submission speech and the
  "returning god" story are treated by modern scholarship as post-conquest constructions.

**What the UI does past the boundary:** the card shows **who says what** (`accounts:` array
rendered as "What the sources say"), quantities appear as ranges or bands, disputed map
elements are drawn as disputed, and reconstruction layers are labelled as reconstructions.
The model never adjudicates silently, in either direction.

## 4. Where the sources disagree

| disagreement | shape (position / amount / existence) | how the model will handle it |
|---|---|---|
| indigenous force numbers | amount (10×) | ranges, never single numbers; the force-composition readout draws bands |
| population of Tenochtitlan | amount | range on the card, confidence `contested` |
| epidemic mortality | amount (wide) | explicit band, stated as a band, on layer and cards |
| Moctezuma's speech; the "returning god" story | existence | `accounts:` array, both positions, never asserted flatly |
| campaign itinerary segments | position | disputed segments drawn as disputed |
| lake shoreline detail | position | one named reconstruction, labelled |
| Nahua ↔ Julian date correlation | position in time | attested Nahua date + Julian shown as correlation |
| who "won" particular engagements | narrative | event cards carry per-source accounts |

## 5. The independent witness

**The archaeological record** — Templo Mayor excavations, causeway and dike surveys, and the
Basin-of-Mexico settlement-pattern survey (Sanders, Parsons & Santley 1979; Parsons' Valley of
Mexico survey data, tDAR project 192; Gorenflo's 2015 digital compilation).

It is independent of the chronicles, which is exactly what makes it able to settle disputes the
chronicles are party to. The round-1 audit scores the model's asserted causeway and aqueduct
positions, lake extent and city footprint against it **before anything else is drawn on top**.

## 6. Layers with no usable source

Marked **authored** or **modelled** in the layer table, deliberately:

- **Allegiance state machine** — modelled; driven by *authored, dated, cited* events. The
  mechanism (tributary burden, distance, neighbour state) is ours and the About panel says so.
- **Lake level seasonality** — modelled from basin hydrology, calibrated to the named 1519
  reconstruction; no per-year record exists.
- **Epidemic spread path** — modelled on the exchange network; only the introduction and gross
  outcomes are documented. Mortality is a band, not a number.
- **Siege supply/water state per district** — modelled from causeway/aqueduct/brigantine
  control; no direct record below city level.
- **Street-level Tenochtitlan outside precinct and causeways** — *not modelled at all*
  (non-goal); the 1524 map is schematic and the sources cannot support it.
