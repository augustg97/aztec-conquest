# SCOPE — Aztec Conquest

The contract. Produced by the scoping interview at kickoff; every later "was that in scope?" is
settled by reading this file. Amend it deliberately, with a date, rather than drifting.

*Scoped 2026-07-27, adopting the Studio's worked example
(`Modeling Studio/worked-example/AZTEC-CONQUEST.md`) as the interview's answers, per the user's
instruction. Every factual claim herein is provisional until verified in research rounds — that
is the point of the method.*

---

## 1. The claim

> The Mexica empire was not defeated by 500 Spaniards. It was pulled apart along its own
> fracture lines by a coalition of Nahua city-states — above all Tlaxcala and, later, Texcoco —
> who found in Cortés's company a lever against a tributary hegemony most of them had entered
> under duress within living memory. Old-world disease, a lake city with four cutable arteries,
> and steel and horses at the margin decided how fast; the coalition decided whether.

A viewer should leave able to say **who was fighting whom, and why each side chose as it did** —
and should find that the map itself makes the coalition visible, because the model draws
allegiance rather than a two-colour war.

**The default view is the argument.** If a viewer's first glance shows two colours, the model
has already lied.

## 2. Extent

| | |
|---|---|
| time | **1502 → 1550**, with the campaign 1519–1521 at day resolution |
| stored step | day, over 1519-02 → 1521-08; year elsewhere |
| shown step | day inside the campaign; the scrubber's scale is **non-linear, piecewise, with the breakpoints marked on screen** |
| space | **three nested scales**: Mesoamerica (the tributary and alliance system), the Basin of Mexico, and Tenochtitlan–Tlatelolco at causeway-and-canal resolution |
| finest legible thing | a causeway breach, a bridge, a chinampa district boundary |
| projection / substrate | reconstructed Basin-of-Mexico terrain and lake system at c. 1519; WGS84 lon/lat storage, fixed projected map |

The non-linear time axis is a design decision, not a convenience: two years carry the whole
campaign and 48 carry the context. A linear scrubber would make the campaign four pixels wide.
Show the scale on screen so nobody mistakes it for linear.

## 3. The layer table

| layer | kind | mechanism (if modelled) or source (if authored) | engine |
|---|---|---|---|
| Regional terrain + ocean shelf | **authored** (measured data, rendered) | NASA SRTM elevation + NOAA ETOPO1 bathymetry (AWS terrain tiles), hillshaded per view; seasonal wet/dry palette **modelled**; amended 2026-07-27 (round 3) from the INEGI-CEM plan — same layer, better-licensed source at the model's scales | field (raster basemaps × season) |
| Lake system c. 1519 | **authored** (reconstructed) | published lake-extent reconstruction (named, see SOURCE-SURVEY), drawn OVER the modern terrain — reconstruction over measurement, labelled | feature |
| Lake level, seasonal and annual | **modelled** | rainfall seasonality over the closed basin, calibrated to the 1519 reconstruction; the dike of Nezahualcoyotl as a control structure | field |
| Chinampa districts, causeways, dikes, aqueducts | **authored** | archaeology + the 1524 Nuremberg map + colonial surveys | feature |
| Altepetl (city-states), ~200+ | **authored** | Codex Mendoza tribute provinces, archaeological gazetteers, Gerhard | feature |
| **Allegiance — the model's spine** | **modelled** | a state machine per altepetl: `tributary → contested → allied-to-coalition → occupied`, driven by dated events, distance, tributary burden and neighbour state | feature |
| Tribute flows | **authored + interpolated** | Codex Mendoza / Matrícula de Tributos, drawn as arcs from province to capital | feature |
| Campaign track — the Spanish-led column | **authored** | dated itinerary from the letters and chronicles, with disputed segments flagged | feature |
| Force composition over time | **modelled from authored series** | Spanish, Tlaxcalteca, Texcocan, Huexotzinca and others as a stacked series — the single most argument-carrying readout on screen | readout |
| Epidemic | **modelled** | spread on the altepetl network weighted by exchange intensity, seeded at the documented introduction, with an explicitly stated and wide mortality band | field over the network |
| Siege state | **modelled** | causeway control, aqueduct control, brigantine control of the lake → supply and water state per district | feature + field |
| Events | **authored** | ~90 dated markers, each with a card and its sources | feature |
| Chapters | **authored** | ~10 narrative eras | timeline |

**Every modelled layer names a mechanism.** The allegiance state machine is the one that decides
whether this is a model or an illustrated chronology. Build it first; everything else is scenery
until it exists.

## 4. The evidence boundary

The record is **dense and partisan, not sparse** — a different problem from a sparse-record
subject, and the UI must solve a different one.

| dimension | how well constrained |
|---|---|
| the itinerary and the dated events | good — multiple independent accounts, though they disagree on detail |
| the lake shoreline at 1519 | **reconstruction**, not survey; the lakes were drained after the conquest |
| the interior street plan of Tenochtitlan | partial — the 1524 map is schematic; archaeology gives the ceremonial precinct |
| force numbers | **contested by an order of magnitude** on the indigenous side |
| population of Tenochtitlan | **contested**: published estimates run roughly 50,000–200,000+ |
| epidemic mortality | **contested**, widely |
| motive and speech | **the least constrained thing in the whole subject** |

The sources are witnesses to their own case: Cortés's *Cartas* are a legal argument for
retroactive legitimacy addressed to a monarch who could ruin him; Bernal Díaz wrote decades
later against López de Gómara and for the soldiery's claims; Book XII of the Florentine Codex
was compiled a generation later under Franciscan supervision largely from **Tlatelolca**
informants; Tlaxcalteca sources were produced while Tlaxcala petitioned the crown for
privileges.

**What the UI does at the boundary — the central UI decision of this project:** where the
accounts diverge, the model does not adjudicate silently. A card shows **who says what**, and
the map's disputed elements are drawn as disputed. Set-pieces that modern scholarship treats as
post-conquest constructions (Moctezuma's supposed speech of submission; Cortés received as a
returning god) are neither dramatised nor deleted — the card states the argument on both sides.

| disagreement | shape | how the model handles it |
|---|---|---|
| indigenous force numbers | amount (order of magnitude) | ranges, never single numbers; the readout draws the band |
| population of Tenochtitlan | amount | stated range on the card, confidence `contested` |
| epidemic mortality | amount (wide) | explicit band on the layer and its cards |
| Moctezuma's submission speech; the "returning god" story | existence | `accounts:` array; card states both positions; never asserted flatly |
| segments of the campaign itinerary | position | disputed segments drawn as disputed on the track |
| lake shoreline detail | position | one named reconstruction, labelled as reconstruction |
| Nahua ↔ Julian date correlation | position (in time) | Nahua dates shown as attested; Julian equivalent marked as a correlation |

## 5. The canonical frame

Four systems, not one — the reference-frame trap (TRAPS §A1) is unusually rich here.

| dimension | canonical choice | sources that differ, and the conversion |
|---|---|---|
| calendar | **Julian**, as the sources use, with Gregorian shown alongside | Spanish accounts are Julian (Gregorian reform is 1582). Nahua dates are in the 365-day *xiuhpohualli* and 260-day *tonalpohualli*; **the correlation to the Julian calendar is itself contested**, so a Nahua date is shown as attested and its Julian equivalent is marked as a correlation, never asserted flatly |
| coordinates | WGS84 lon/lat | every historical map georeferenced into it, **with the residual recorded** — a georeference is a measurement with an error, not a fact |
| names | **Nahuatl endonym first, Spanish exonym second**: *Mēxihco-Tenōchtitlan (Tenochtitlán)*, *Tlaxcallan (Tlaxcala)*, *Chōlōllān (Cholula)* | modern Mexican toponyms noted where a viewer needs the anchor |
| peoples / polity | **Mexica** for the people, **Triple Alliance** for the polity | "Aztec" is a modern scholarly coinage and never a self-designation. Say so once, in the About panel, then use the right words. The project title keeps "Aztec" for findability; the model does not |
| administrative units | Codex Mendoza tribute provinces, as of c. 1519 | colonial-era repartitions recorded per source in the gazetteer |
| the lake | one reconstruction, named, with its date and author | competing reconstructions differ; **name the one in use**, never average them |

Conversions live in `Research/modeling/calendar.py` with a selftest, and **every date in the
data carries the system it was authored in**. This is one file and it prevents the most
expensive possible bug in this subject.

## 6. The card contract

Every card carries:

- eyebrow (what kind of thing this is) · title (**endonym, exonym**)
- 2–4 fact rows
- prose **for the current date** — `eras: [{from, to, text}]`
- the span shown to the reader
- confidence (`good` / `moderate` / `contested`) — a field on the data, not a footnote
- citations

Plus, for anything contested, an **`accounts:` array** rendered as a "What the sources say"
section:

```js
accounts: [
  {source: "Cortés, Segunda carta (1520)", claim: "…",
   note: "written to justify an unauthorised expedition to the crown"},
  {source: "Florentine Codex Bk XII (c. 1555–79)", claim: "…",
   note: "Tlatelolca informants, a generation later, under Franciscan supervision"},
]
```

It costs one schema field and it is the difference between a model and a retelling.

Fallback tiers, with the heading naming the tier:

1. curated exception → **"Recorded here"** — attested for this place and date
2. model-derived → **"Typical of this altepetl"** — derived from the tribute province and the settlement model
3. generic → **"General to the Basin in this period"** — *and the heading says so*

Approximate card counts: ~200 altepetl · ~90 events · ~40 people · ~25 features of the lake and
city · ~10 chapters. That is card-generator territory, not hand-authoring: build the generator
and the card audit together, in the same round.

## 7. The standard for done

Named reference artefacts a result is compared against, at a stated scale:

- the published Basin-of-Mexico lake-and-settlement reconstructions (the named one in use, plus
  competitors for comparison);
- the georeferenced **1524 Nuremberg map** (Newberry Library scan, public domain, 5000 px);
- the comparison **scripted so it re-runs**.

The independent witness: **the archaeological record** — Templo Mayor excavation, the causeway
and dike surveys, the Basin-of-Mexico settlement-pattern survey (Sanders, Parsons & Santley
1979; Parsons' survey data on tDAR). It is independent of the chronicles, which is exactly what
makes it able to settle a dispute the chronicles are party to.

**The check worth building in round 1:** the model asserts causeway and aqueduct positions,
lake extent and city footprint. Score them against the archaeology before drawing anything else
on top. A beautiful siege drawn on a wrong lake is worse than no siege.

## 8. Sensitivities

This subject is a conquest whose descendants are living communities and whose framing is
actively contested. **Carry it in the substance, not in a disclaimer** (the Territorial US
template):

- **The coalition is the map's default state** → carried by the allegiance layer being the
  spine. Spain-versus-Mexico two-colour framing is a factual error, not a framing choice.
- **Whose names the map uses is itself a claim** → Nahuatl endonyms first, always.
- **Why the coalition was available** → the tributary system is drawn — which altepetl entered
  it when, and by what force.
- **The epidemic is not scenery** → its own layer, its own cards, an explicit and honestly wide
  mortality band.
- **The conquest does not end on 13 August 1521** → the model runs to 1550 so encomienda,
  congregación, the drainage of the lakes and the continued campaigns are inside the frame.
- **Nahua accounts are primary sources** → cited in the same register as Cortés, not as "the
  native perspective" in a sidebar.

Naming convention and why: see §5. "Aztec" appears in the project title for findability and in
the About panel once, explained; the model itself says Mexica / Triple Alliance / the altepetl's
own name.

## 9. Non-goals

- Not a real-time strategy game; there is no counterfactual mode.
- Not a battle simulator; tactical engagements are cards and outcomes, not unit combat.
- No modelling below the altepetl for allegiance — the sources cannot support it.
- No reconstruction of individual streets outside the ceremonial precinct and the causeways.
- Not a general history of Mesoamerica; the tributary system is drawn because it explains the
  coalition, not for its own sake.

## 10. Budget and delivery

| | |
|---|---|
| delivery | static site, GitHub Pages (`docs/` on `main`), relative paths, `.nojekyll`, data-version stamp |
| total bytes over the wire | **< 45 MB** total — *amended 2026-07-29 (round 7), deliberately.* The original 25 MB was set before the terrain field existed and the basemaps reached 23.9 MB of it, which would have made every future raster decision a fight with a number chosen in ignorance. 45 MB keeps the ceiling real (it still forbids a tile pyramid) while leaving room for 4:4:4 coasts and a further level. **Lazy loading matters more than the total**: time-to-first-frame is the binding constraint below |
| time to first usable frame | **< 1.5 s** to a usable map |
| offline / `file://` required? | no — fetched JSON permitted; lazy loading from first paint |
| pipeline? | yes — `build/`: georeferencing, terrain/lake fields, card generation, validators |

The Basin terrain is one small field set — the whole Basin is roughly 100 km across, so a 10 m
grid is a few megabytes, far more resolution per byte than a global model gets. **Spend it on
the city.**
