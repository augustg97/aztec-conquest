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
| A2-c | P2 | Chinampa districts drawn (archaeology + colonial surveys) | `georef.py` | open |
| A2-d | P2 | Basin terrain field: INEGI CEM minus post-conquest modification, gated by the reconstruction; labelled as reconstruction | `build/` | open — the DEM is post-drainage; never present it raw |
| A3 | P3 | Verify flagged licences before shipping any collected figure: INEGI terms; Getty DFC per-image; Bodleian/INAH; tDAR redistribution | `figures/collected/MANIFEST.json` | open — no third-party figure is shipped in round 1 (both figures authored), so nothing currently rests on it |

## B. The spine — gazetteer and allegiance

| # | P | item | touches | status |
|---|---|---|---|---|
| B1 | P1 | Altepetl gazetteer, first tranche | `gazetteer.py` | **DELIVERED** — 75 polities, 30 of ~38 Mendoza provinces, endonym/exonym/modern, coords + entry + confidence per row |
| B1-b | P2 | The remaining Mendoza roster: ~9 poorly-located frontier provinces (named in gazetteer.py docstring) + the ~400 tribute towns below province level | `gazetteer.py` | open — omissions RECORDED, not silent |
| B2 | P1 | Allegiance state machine | `allegiance.py` | **DELIVERED** — 75 timelines, 228 transitions, all legal; selftest asserts the coalition shape (mid-siege: 27 allied + 12 occupied vs 3 contested + 0 core) |
| B2-b | P3 | Page/folio-level citation pinning for event dates and force claims (currently source families + modern chronologies [TH][HAS]) | `events.py`, `forces.py` | open |
| B2-c | P4 | Mexica counter-diplomacy reversions (towns briefly regained 1520-21) — deliberately excluded from round 1 | `allegiance.py` | open, recorded in module docstring |
| B2-d | P2 | Events catalogue: 64 events vs SCOPE's ~90 target; people cards (~40) not yet authored | `events.py`, new `people.py` | open |

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

**Count: 6 open items — 0 at P1, none user-visible.** Remaining, in value order — note the
first two need EXTERNAL DATA the session cannot fetch without the user (file downloads):

1. **A2-b** trace González Aparicio + the 1524 Nuremberg map from scans (needs the scans
   downloaded; the 24 MB Newberry file is public domain).
2. **A2-d** Basin terrain field from INEGI CEM (needs the DEM download; area-selection route).
3. **A2-c** chinampa districts (authorable from literature descriptions; medium).
4. **B1-b** remaining Mendoza roster (the omitted provinces are omitted BECAUSE poorly
   located — adding them means researching locations, not typing names).
5. **B2-d-rest** people 18 → ~40; **B2-b** page/folio-level source pinning.
6. **B2-c** Mexica counter-diplomacy reversions (thin evidence; may close negative).
