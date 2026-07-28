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

*Rewritten after research round 1, 2026-07-27. Round 0 seeded 9 items (6 P1); round 1
delivered all six P1s as staged artifacts + audits, and opened 7 successor items.*

---

## APPLIED

| item | what shipped | measured |
|---|---|---|
| *(none yet — round 1 artifacts are STAGED; the build pass applies them)* | | |

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
| D1 | P2 | Force composition as ranges + readout | `forces.py`, `DATA.forces` | **DELIVERED** — 3 contingents × 5 phases, per-source claims with stakes; WP-01; figure |
| D2 | P2 | Epidemic model on the altepetl exchange network, mortality as a band | new `epidemic.py` | **open — NOT built in round 1.** The epidemic exists as dated events with accounts and band language, not as a network mechanism. This is the largest unbuilt SCOPE §3 layer |
| D2-b | P2 | Siege-state mechanism (causeway/aqueduct/brigantine control → per-district supply and water) | new `siege.py` | open — round 1 carries the siege as events + works cards |

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

**Count: 8 open items — 0 at P1.** All six kickoff P1s are DELIVERED as staged artifacts.
The ones that would move the model furthest next, in order:

1. **D2 epidemic network model** — the largest unbuilt SCOPE layer.
2. **D2-b siege-state mechanism** — turns the siege from events into a derived state.
3. **B2-d events to ~90 + people cards** — the narrative texture the scope promises.
4. **A2-b/A2-c/A2-d** — proper tracing, chinampas, terrain field.
5. **B1-b** — the remaining Mendoza roster.
