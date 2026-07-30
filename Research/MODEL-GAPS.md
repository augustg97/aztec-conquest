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

*Rewritten after round 2, 2026-07-27. Round 0 seeded 9 items (6 P1); round 1 delivered all six
P1s; round 2 answered the user's black-map report (substrate), built the epidemic and siege
mechanisms, and added people/events/goods depth.*

---

## APPLIED

*Build pass 2026-07-27 executed all 7 staged changes; statuses below moved DELIVERED → APPLIED.*

| item | what shipped | measured |
|---|---|---|
| A1 calendar frame | Julian day readout in-campaign; Gregorian + labelled Nahua correlation on day-precision event cards | 3 Caso anchors consistent; t-scalar roundtrips at day resolution |
| A2 named geography | González Aparicio (1973) lakes/works/footprint drawn + clickable, labelled visualization-grade | residuals ≤ 6 m; footprint 15.6 km² (band 10-18); lakes 766 km² (band 700-1,600) |
| B1+B2 spine | 75 altepetl coloured by allegiance from one canonical reader; legend + tally read the same series | 1519: 0 coalition on screen; mid-siege: 24 allied + 12 occupied vs 30 tributary; 1550: 73 new-spain + 1 colonial-ally |
| C1 card contract | accounts ("What the sources say"), confidence chip, era-span line, sources on every card | card audit 0 HIGH / 0 MED over 82 entities + 64 events; Cholula card renders 4 accounts |
| D1 forces | "Who is fighting" panel, ranges only | siege 700-950 Spanish vs 24,000-200,000 allies, on screen |
| E1+F1 gates | audit_all wired into build_site.py; refuses to publish on regression | both audits 0/0 reading web/data (the artifact the app executes) |
| SCOPE §2 time axis | piecewise scrubber, campaign = 56% of track, breakpoints drawn + labelled | xOf/tOf exact inverses; day-stepping in-campaign |
| **Round 2** — substrate (user-reported defect) | authored coastline + Gulf/Pacific + 6 sierra ridgelines + 8 named peaks; land/sea fills at every view | coast check green: 0 polities in ocean, 7 coastal towns ≤ 70 km of drawn coast; pass-between-volcanoes ≤ 15 km |
| D2 epidemic mechanism | wave on kNN settlement network, seeded Cempoala May 1520, calibrated to capital onset 1 Oct 1520 [FC]; halos + onset windows | speed 2.3 km/day; Basin onsets all Aug 1520-Jan 1521; Tlaxcala before capital (consistent w/ Maxixcatzin); band 30-50% stays a band |
| D2-b siege state | 6 arteries, each cut by a dated cited event; in-app panel counts 0→6 | pressure monotone; 3 cut 22 May, 6 by 10 Jun 1521; selftest asserts event-date lockstep |
| B2-d (partial) people + events | 18 people cards (3 with accounts: Malintzin, Xicohtencatl the Younger, Cacama); events 64 → 89 (23 with accounts) | people eras tile 1502-1551; contested people carry accounts; card audit still 0/0 |
| B1 depth: tribute goods | principal Mendoza tribute on 24 province cards | [CM]-sourced fact rows, confidence moderate |

---

## A. The canonical frame

| # | P | item | touches | status |
|---|---|---|---|---|
| A1 | P1 | `calendar.py` — Julian/Gregorian/JDN + tonalpohualli/xiuhpohualli, correlation explicit | `Research/modeling/calendar.py` | **DELIVERED** — selftest green; 3 Caso anchor pairs mutually consistent; veintena arithmetic reproduces Caso's 19 Tecuilhuitontli for the Noche Triste |
| A2 | P1 | Name the canonical lake reconstruction; author the geometry; residuals | `georef.py`, `geo.js` | **DELIVERED** — **González Aparicio (1973) SEP/INAH** named; terminal residuals ≤ 6 m; footprint 15.6 km² (band 10-18); lake system 766 km² (band 700-1,600) |
| A2-b | P2 | Acquire a scan of González Aparicio (1973) and the 1524 Nuremberg map; trace properly with pixel control points; record affine residuals | `georef.py`, `data/` | open — round-1 geometry follows the anchors + literature descriptions; **cited but not consulted in facsimile** (dossier 01 §6) |
| A2-c | P2 | Chinampa districts drawn (archaeology + colonial surveys) | `georef.py` | **CLOSED round 7** — derived from the shoreline, not drawn; selftest asserts they lie in the lake |
| A2-d | P2 | Basin terrain field: INEGI CEM minus post-conquest modification, gated by the reconstruction; labelled as reconstruction | `build/` | open — the DEM is post-drainage; never present it raw |
| A3 | P3 | Verify flagged licences before shipping any collected figure: INEGI terms; Getty DFC per-image; Bodleian/INAH; tDAR redistribution | `figures/collected/MANIFEST.json` | open — no third-party figure is shipped in round 1 (both figures authored), so nothing currently rests on it |

## B. The spine — gazetteer and allegiance

| # | P | item | touches | status |
|---|---|---|---|---|
| B1 | P1 | Altepetl gazetteer, first tranche | `gazetteer.py` | **DELIVERED** — 75 polities, 30 of ~38 Mendoza provinces, endonym/exonym/modern, coords + entry + confidence per row |
| B1-b | P2 | The remaining Mendoza roster: ~9 poorly-located frontier provinces (named in gazetteer.py docstring) + the ~400 tribute towns below province level | `gazetteer.py` | **CLOSED round 7** for the provinces (82 polities, 37 of ~38); the ~400 sub-province towns stay out of scope by SCOPE §9 |
| B2 | P1 | Allegiance state machine | `allegiance.py` | **DELIVERED** — 75 timelines, 228 transitions, all legal; selftest asserts the coalition shape (mid-siege: 27 allied + 12 occupied vs 3 contested + 0 core) |
| B2-b | P3 | Page/folio-level citation pinning for event dates and force claims (currently source families + modern chronologies [TH][HAS]) | `events.py`, `forces.py` | **CLOSED round 9** — 53 citations pinned to stable work divisions; pages deliberately refused |
| B2-c | P4 | Mexica counter-diplomacy reversions (towns briefly regained 1520-21) — deliberately excluded from round 1 | `allegiance.py` | **IMPLEMENTED round 7** — reversion transitions added; Chalco runs the full cycle |
| B2-d | P2 | Events catalogue: 64 events vs SCOPE's ~90 target; people cards (~40) not yet authored | `events.py`, `people.py` | **CLOSED round 8** — events 90, people **40** |

## C. The card system

| # | P | item | touches | status |
|---|---|---|---|---|
| C1 | P1 | `accounts:` schema + card generator + card audit built together | `emit.py`, `audit_cards.py`, `DATA-SCHEMA.md` | **DELIVERED** — 82 entities + 64 events generated; 19 events carry "What the sources say"; audit at 0 HIGH / 0 MED with all 7 checks selftest-proven to fire |

## D. Contested quantities

| # | P | item | touches | status |
|---|---|---|---|---|
| D1 | P2 | Force composition as ranges + readout | `forces.py`, `DATA.forces` | **APPLIED** (round 1) |
| D2 | P2 | Epidemic model on the altepetl network, mortality as a band | `epidemic.py` | **APPLIED** (round 2) — see APPLIED table; sub-altepetl structure, second waves and differential mortality deliberately excluded (module docstring) |
| D2-b | P2 | Siege-state mechanism | `siege.py` | **APPLIED** (round 2) — supply is modelled as cut/not-cut only; no source supports finer (that limit is stated on the panel) |

## E. The independent witness

| # | P | item | touches | status |
|---|---|---|---|---|
| E1 | P1 | Archaeological witness audit | `audit_witness.py` | **DELIVERED** — 7 checks, selftest-proven; caught 5 drowned lakeshore towns + 1 shore-distance defect in the authored polygons before anything shipped; now 0 HIGH / 0 MED |

## F. Housekeeping

| # | P | item | touches | status |
|---|---|---|---|---|
| F1 | P3 | Anachronism + banned-naming screen | `audit_cards.py` | **DELIVERED** — terms with not-before dates ("New Spain" 1520.8, "Mexico City" 1521.6, "viceroy" 1535.8, "encomienda" 1521.6); "Aztec"/"Montezuma" banned from model text |

---

**What the audits did NOT find** (the checks that passed, with numbers — settled, do not
re-litigate):

- 0 era-tiling gaps across 82 entities; chapters tile 1502.0-1551.0 exactly.
- 0 contested cards stated flatly (19 events with ≥2 accounts; contested entities carry notes).
- 0 missing sources; 0 unknown allegiance states; 0 illegal transitions in 228.
- 0 anachronisms and 0 banned terms in ~200 era texts, 64 event texts, 10 chapters.
- Terminal residuals all ≤ 6 m; no town drawn underwater (after the audit caught 5 and the
  polygons were corrected — an honest catch, recorded here as the audit doing its job).
- Track continuity: no jump > 1,000 km (threshold recalibrated from 300 km after firing on
  genuine sea voyages — a check must earn its keep).

**Honest corrections recorded as findings:**

- The witness audit's first run failed 5 HIGH on my own authored polygons (drowned towns) —
  the geometry was corrected against the audit, exactly the intended loop.
- Two events were initially over-labelled `contested` when they were merely thin (moderate) —
  the selftest's accounts-requirement forced the distinction. "Contested" = sources disagree in
  print; "moderate" = thinly attested. The distinction is now load-bearing.
- forces.py's honesty assertion (a contested band must be ≥1.5× wide) rejected my first
  Noche Triste survivor band as too narrow; the fix (400-1,100) is more honest than the draft.

---

**Round 3 (downloads approved) closed the externals:**

| # | outcome |
|---|---|
| A2-d | **APPLIED** — terrain field from SRTM+ETOPO (AWS terrain tiles; INEGI plan amended in SCOPE — better-licensed source at these scales): 6 basemaps, 1.21 MB, self-checked (Popocatépetl 5,386 m vs 5,393 real; lakebed 2,232 m; Gulf -1,930 m); seasonal wet/dry compositing + clouds + attested 1519-28 plume ('Ordaz' event); continuous camera with preset flights |
| A2-b | **RESOLVED, measured** — 1524 Nuremberg map georeferenced on 5 control points: mean residual **2.2 km**, max 5.5 km at the city → topology, not geometry; stated in About; González Aparicio scan still unconsulted (remains below) |
| Images | **DELIVERED** — 10 public-domain card images fetched, subject-verified (1 blank-flyleaf rejected — TRAPS A4 fired again), credited on every card, audit-enforced; **5 recorded negatives** (toxcatl, siege-painting, malintzin*, cuauhtemoc, fc-siege) — *Malintzin card uses the Lienzo meeting scene where she is the central figure |
| Chapters | **DELIVERED** — chapter cards with image, span, story and clickable event list; 9 of 10 illustrated (ring-closes open) |

**Round 4 (user design feedback):**

| # | outcome |
|---|---|
| Terrain detail | **APPLIED** — z9/z12 native-grain renders (Popo 5,399 m vs 5,393 real), curvature + rock shading; the first city render's upsampling-checkerboard was caught VISUALLY and fixed structurally (gain fades below the 30 m native grain) — TRAPS B1's lesson, honoured |
| City model (new: A2-e) | **APPLIED** — phased Tenochtitlan (precincts, palaces, market, schematic canals dashed-as-schematic, chinampas, campan; traza + churches from 1522); 8 phase-aware cards; georef selftest pins the precinct ≤ 350 m from the Templo Mayor anchor |
| Event placement + readability | **APPLIED** — 34 researched intra-city placements (Xoloc, the palace, the precinct, the market...); global label-collision stacker with leader lines; the plague-year cluster now reads |
| Event simulacra | **APPLIED** — interpolated marching column; kind glyphs; deterministic battle/massacre pulse rings; siege arteries redden as cut + brigantines + razing char & smoke; epidemic wavefront ring; t-keyed flowing tribute/track dashes — all pure functions of t, scrub-reproducible |

**Round 5 (user feedback: uniform detail; figure-scale simulation):**

| # | outcome |
|---|---|
| Terrain uniformity | **APPLIED** — corridor z11 level (Veracruz↔Basin↔Morelos, 5120 px) + meso at native z9 (6144 px); the photographed seam east of the Basin eliminated; basemaps 16.6 MB of the 25 MB budget |
| City fabric | **APPLIED** — seeded procedural house fabric at street zoom (density keyed to precinct distance), charring follows the razing S→N, colonial traza blocks after 1522, chinampa trees; labelled impression |
| Figure scale | **APPLIED** — marching files scaled to forces bands; skirmish/massacre scenes; canoe traffic ending at the brigantine victory; tribute porters gated by live allegiance; post-fall causeway exodus; waterfowl; all pure functions of t (seeded, no runtime randomness); About carries the impression disclaimer |

**Round 6 — the rendering loop (8 iterations, user-directed at Google Earth quality):**

| # | outcome |
|---|---|
| Canvas world layer | **APPLIED** — terrain, lakes and urban fabric moved to a canvas under the SVG (SVG keeps everything interactive); thousands of marks/frame affordable |
| A2-e city fabric | **APPLIED** — canal/street network with width and wander, causeways through the city, blocks of courtyard compounds with block-level grain (orientation + material), L-shaped houses, chinampa strips, jetties + moored canoes at the water's edge, Xoloc fort, colonial courtyard-block traza after 1522 |
| Precinct architecture | **APPLIED** — walled paved court with causeway gates, 5-terrace great temple with twin stairways and the Tlaloc/Huitzilopochtli shrines, round temple of Ehecatl, ballcourt, tzompantli, calmecac ranges; Tlatelolco precinct + its market crowd |
| Settlement fabric (all polities) | **APPLIED** — every altepetl draws a town on its own plan (dispersed wards / compact plaza / linear), with temple platform → church at New Spain, burnt roofs while occupied; Cholula's Tlachihualtepetl authored |
| Siege legibility | **APPLIED** — causeway breaches that close as the razing advances, arteries reddening as cut, S→N charring, rubble spoil, smoke |
| A2-d-b ground detail | **APPLIED, with a MEASURED limit** — city basemap is 16.6 m/px vs SRTM's ~30 m native, screen asks 1.1 m/px, so no tile pyramid can help; detail grown from local contrast of the measured surface + world-anchored grain |

**Honest corrections recorded this round:** vegetation blanketed the map twice (first keyed to "green" — the wet palette is green everywhere; then to the global mean — dark valleys read as forest); fixed only by local contrast. A first grain implementation cost **64 ms/frame** (per-frame canvas readback + overlay blend) and was fixed structurally (sample each image once at load; alpha-channel grain) → 8.9 ms. A scope slip (loop-local `lotPx` used in the market block) threw inside `render()` after the canvas drew, leaving a map with a blank date — caught by the console handle, not the screenshot.

**The ceiling, stated:** photographic equivalence is unreachable — Google Earth is sub-metre aerial photography of an extant city; 1519 Tenochtitlan exists only as Calnek's lot reconstructions, the 1524 woodcut (measured 2.2 km error) and excavation. Detail past this point is invented, not derived, and the working rules forbid it.

**Round 7 — the water loop, then the register itself:**

| # | outcome |
|---|---|
| Lake realism (user) | **APPLIED** — hypsometric depth ramp with a shelf break, lake-bed fabric, crinkled shorelines, rivers with deltas. The white "brush strokes" the user then reported were long elongated ellipses (`r*3.4 × r*0.55`) at 0.26 alpha; replaced with soft radial-gradient patches (`r*1.5 × r*0.95`), alpha capped at 0.05, pale tones only above noise 0.80 and at half strength |
| Text selection (user) | **APPLIED** — `body{user-select:none}` with the card prose re-enabled, so dragging the map no longer highlights the UI |
| Budget ceiling (user) | **AMENDED, deliberately** — SCOPE §10 raised 25 MB → **45 MB**. The original was set before the terrain field existed and the basemaps alone are 23.9 MB. 45 MB still forbids a tile pyramid, which is the constraint that was actually doing work. `terrain.py` and `emit.py` print lines corrected to match — `emit.py` was missed on the first pass and printed the old figure for one build |
| **B1-b** | **CLOSED** — the 7 omitted Mendoza frontier provinces added (atlan, oxitipan, quiauhteopan, tlalcozauhtitlan, malinaltepec, cuahuacan, itzcuincuitlapilco), each `coord_conf: "contested"` with a note that the province is attested and its head town's location is the open question. **82 polities, 37 of ~38 provinces.** The ~400 sub-province tribute towns remain out of scope by SCOPE §9 |
| **A2-c** | **CLOSED** — the four chinampa districts, **derived, not drawn**: each is the southern lake's own shoreline over a named longitude span, offset inward by a stated width, clamped to the far shore where the lake is narrower than the district would be. Selftest asserts every vertex lies inside the lake (a chinampa on dry ground is a category error) and that the four together stay under 55% of it |
| **B2-c** | **IMPLEMENTED, not closed negative** — the reversion transitions were the gap, and they were a real distortion: excluding them made the state machine monotone, so every defection was permanent and holding ground cost nothing. `allied-coalition → contested → allied-coalition` now exists and Chalco runs the full cycle (tributary → coalition Jan 1521 → **contested** Mar → coalition Apr → new-spain). `chalco-counterattacks` already existed **with an empty `effects` list** — the event was on the map, doing nothing |
| **B2-d** | **ADVANCED 18 → 30** — the round-7 tranche corrects a bias the first list had: three Mexica lords against six Spaniards, which quietly argued against this model's own thesis. Adds the other two alliance seats (Coanacochtzin, Tetlepanquetzatzin), the administration that survived the conquest (Tlacotzin), Tlatelolco's governor, one ordinary soldier (Tzilacatzin), and the witnesses whose books every other card cites |

**Honest corrections recorded this round:**

- The first chinampa attempt painted **translucent green over water** — a tint, not a place. A
  chinampa is *built ground standing out of the lake*, so the base had to be land far out and
  **ditch water** close in, with the plots drawn on top. Painting land under land is what made
  it read as one flat green field.
- The districts were first authored as four hand-drawn blobs, then rewritten as offsets of the
  measured shoreline. The rewrite immediately caught two authoring errors the blobs had hidden:
  a span running **past the east end of the lake** (now a loud `ValueError`, not a `TypeError`
  ten frames later) and four **contiguous** spans that tiled into one unbroken band.
- Scale stated rather than fudged: the four come to ~46 km² against Parsons' ~120 km² for the
  real system. The gap is the **simplified lake** (124 km² vs a real ~200 km²), not a claim that
  the system was smaller. Widening the districts alone to hit the literature number would put
  chinampas in open water to make a total look right.
- **Chimalpahin was rejected as a person card** — born 1579, outside the 1502-1551 window. A
  card would have needed an `active` span the man did not have. He stays a source.
- The card audit caught `New Spain` in a Mendoza era spanning from 1502 — a term that does not
  exist until 1520.8. The gate refused the publish; the era was reworded.
- A per-plot `fillStyle` + `fillRect` cost **9.6 ms/frame** at close zoom (measured by A/B, not
  guessed). Batching into three fills by crop colour → **0.16 ms**. The world-anchored mottle
  step was the same round-6 mistake again (cost explodes as the camera pulls back) and was put
  back on constant *screen* density.
- The true-scale canal lattice read as **graph paper** at mid zoom; it now fades out below ~16 px
  spacing and lets the district's texture carry it.
- Two screenshots came back **pixel-identical** after real edits. `js/app.js` carries no
  cache-buster in dev, so the browser served a stale file. Caught by reading the function source
  back through the console (`/cpx - 7/.test(String(drawChinampas))`), not by looking harder at
  the picture. This is the third appearance of this trap.

**Round 8 — the rest of the register:**

| # | outcome |
|---|---|
| **B2-d** | **CLOSED at 40 people.** The round-8 tranche fills the three holes the list still had: the years BEFORE 1519 (the model opens in 1502 and had almost nobody alive in it — Nezahualpilli's reign and the Texcoco succession crisis that is the doorway the whole war walks through), the war's technicians and middle ranks rather than only its principals (Martín López, who cut thirteen brigantines at Tlaxcala and had to sue to be noticed; Coyohuehuetzin and Temilotzin, the Tlatelolca field command), and the missionary generation whose classroom produced the alphabetic Nahuatl most of this model's indigenous sources are written in |
| **Images** | **ALL 5 NEGATIVES CLEARED, plus the missing chapter image.** Every one of the round-3 negatives was partly a *ranking* accident: `pick()` took the first licence-safe hit in the top 8 of a free-text query, and the right file was simply ranked lower. All six are now **pinned by exact Commons title** — a build whose illustrations depend on today's search order is not reproducible. 16/16 images licence-safe and subject-verified; **all 10 chapters illustrated** (ring-closes was the last gap) |
| Image audit (new) | **`check_image_targets`** — every image the emitter assigns must land on something that exists. Added after two `ENTITY_IMAGE` keys named events that did not exist; nothing failed, the lookup just missed and the cards shipped without pictures. Orphans are **HIGH**, assigned-but-not-delivered is MED |
| Anachronism exemptions (new) | The term table is calibrated to *this model's territory*: "encomienda" is barred before 1521.6 because that is when the institution reaches Mexico. Las Casas's 1502-1514 Caribbean years are the one card legitimately outside that, so a **narrow, reasoned, per-card exemption list** now exists — and a **stale exemption is itself reported**, so the list cannot quietly rot |

**Honest corrections recorded this round:**

- `fc-siege`'s first pinned title was one I had **read off a truncated probe line**, so it 404'd.
  The corrected file is the Book XII sacrifice plate at Colhuacatonco — kept deliberately: the
  model already carries the Cholula and Tóxcatl massacre images, and showing only Spanish
  violence would be a lopsided editorial choice about whose is depicted.
- `cuauhtemoc`'s image is his **capture on the lake, not a portrait** — no likeness from life
  survives. The caption says so rather than letting a crowded battle scene imply a likeness.
- A scripted edit applied a selftest injection **twice**, once inside `run()`, so the synthetic
  orphan leaked into the real audit and the gate refused to publish. Correct behaviour from the
  gate; the fix was to stop mutating the live emitter at all and **inject the mapping** instead.
- Chimalpahin was rejected again on the same rule as round 7 (born 1579, outside the window).

**Round 9 — the last two items I can reach:**

| # | outcome |
|---|---|
| **B2-b** | **CLOSED, but NOT as asked — and the difference is the point.** The register said "page/folio-level". Page numbers belong to a *printing*, and this model does not have those printings in hand; inventing them would be fabricated precision that **looks** checkable, which is worse than the source-family citation it replaced. So the pin is to the division the WORK carries and every edition preserves: Bernal Díaz by chapter, the Florentine Codex by book+chapter, Cortés by letter and section, codices by folio. **53 citations across the 25 events of the dated spine.** Two guards: a pin naming an event or a source that does not exist raises at import (it caught 5 of my own errors immediately), and the selftest **rejects any page reference** outright, so one cannot be smuggled in later. An event with no pin is not an oversight — its date comes from the modern chronologies synthesising several accounts, and the code says so |
| Zoom seam | **APPLIED, and smaller than reported.** The levels stack, so mid-fade the screen shows `0.5*coarse + 0.5*fine`; their hillshades correlate r=0.89 and r=0.95, so averaging dilutes rather than blends. Easing the ramp hard through the middle (alpha in 0.3-0.7 for **11% of the band instead of 40%**) lifts mean detail across the band from **92.9% → 97.4%** (meso→corridor) and **92.5% → 95.3%** (corridor→basin). The worst case is unchanged at ~90%: the 50/50 point is crossed either way |

**Honest corrections recorded this round:**

- **I measured the wrong layer first.** The initial reading put the crossfade's detail loss at
  **47.8%**, by comparing the basin raster against **meso**. But by the time basin fades in,
  *corridor* is already fully opaque — and corridor carries 93.7% of basin's detail, so the real
  dip is about 10%. The fix was still worth making; the claim was 5× too large. Measure against
  what is actually on screen underneath, not against the layer that shares the name of the seam.
- **The Browser pane was not compositing this round** (canvas width 0, screenshots time out), so
  the seam and the citation line were verified through measured raster simulation and through
  the DOM + computed style respectively — **not** by looking at a picture. That is a weaker
  instrument than this project's standing rule wants, and it is recorded as such rather than
  quietly skipped.

**Count: 1 open item — 0 at P1.**

1. **A2-b-rest** consult González Aparicio (1973) in facsimile and trace properly. No
   licence-safe digital scan has surfaced across four rounds of looking; this needs a library
   visit and **cannot be done from a terminal**. Everything else in the register is closed.
