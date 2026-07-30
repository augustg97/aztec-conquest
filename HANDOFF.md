# Handoff — Aztec Conquest

Paste this whole file as the first message of a new session.

---

## What you are working on

**Aztec Conquest** — the fall of Tenochtitlan, 1502–1550: an interactive model of the coalition
that pulled the Mexica empire apart.

- Repo: `/Users/augustgweon/Aztec Conquest` · GitHub: `augustg97/aztec-conquest`
- Live: https://augustg97.github.io/aztec-conquest/ (Pages serves `main:/docs`)
- **Read `README.md` first** (goals; working rules §2 incl. five subject-specific; traps §7;
  limits §9), then `SCOPE.md` (the contract), then `Research/MODEL-GAPS.md` (the register).

## State right now

Kickoff → v1.0 → v1.1 → v2.0 → v2.1 → v2.2 → round 6 (the rendering loop) → v2.3 →
**round 7 (the water loop, then the register) → v2.4** are complete.

**Round 7** finished the user's lake work and then went through the register itself. Closed
**A2-c** (the four chinampa districts, *derived* from the shoreline rather than drawn — the
selftest asserts every vertex lies in the lake) and **B1-b** (82 polities, 37 of ~38 Mendoza
provinces). **Implemented B2-c** rather than closing it negative: excluding reversions had made
the allegiance machine monotone — every defection permanent, holding ground free — and Chalco
now runs tributary → coalition → *contested* → coalition → new-spain. **B2-d** advanced 18 → 30
people, correcting a bias in the first cast (three Mexica lords against six Spaniards, which
quietly argued against this model's own thesis). SCOPE §10's byte budget was amended 25 → 45 MB
with the reasoning recorded. See MODEL-GAPS "Round 7" for the APPLIED table and the eight
honest corrections — including a per-plot draw that cost 9.6 ms/frame until it was batched by
crop colour (0.16 ms), and the **third** appearance of the stale-dev-JS trap, where two
screenshots came back pixel-identical after real edits.

**Four items remain open, none at P1**, and one of them (A2-b-rest, the González Aparicio
facsimile) cannot be done from a terminal — it needs a library visit. Round 6 rebuilt the visual layer: a **canvas world layer** under the SVG carries
terrain, lakes and a full procedural urban fabric (blocks, courtyard compounds, canals,
jetties, precinct architecture, colonial traza), every altepetl draws its own town on its own
plan, the siege is legible on the ground, and landscape detail is grown from the measured
surface within a stated data ceiling. See MODEL-GAPS "Round 6" for the APPLIED table, the
three honest corrections, and the ceiling statement.

Earlier rounds: Round 3 (downloads approved by
the user) added: the real terrain field (SRTM+ETOPO, seasonal wet/dry, clouds, the attested
Popocatépetl plume), the continuous camera (wheel/drag/flights), the 1524 map measured (2.2 km
mean residual — topology not geometry), 10 subject-verified PD card images with credits
(audit-enforced; 5 honest negatives in the manifest), and chapters as illustrated cards.
`build/terrain.py` and `build/fetch_images.py` are the new pipelines (venv/ holds numpy+Pillow;
data/ caches tiles/scans, both gitignored). The app is a working
model: 75 altepetl coloured by a per-day allegiance machine, **89 events** (23 with "What the
sources say"), **18 people cards**, the González Aparicio lake system with clickable works,
**a full land/sea/sierra substrate** (round 2 — a user report of "just a black background"
was correct and is closed), **the epidemic as a calibrated network wave** with per-polity
onset halos, **the siege as a derived six-artery state** with its own panel, tribute goods on
province cards, the campaign track, the piecewise day-scale timeline, three views, force
bands, and an About + update log that say what the model does not know.

- All 7 research-module selftests green; `audit_all.py` at baseline **cards 0/0, witness 0/0**.
- The register (`Research/MODEL-GAPS.md`): **8 open items, 0 at P1** — all kickoff P1s APPLIED
  with measurements recorded in the APPLIED table.
- `web/data/*` is GENERATED — never hand-edit; fix the model in `Research/modeling/`, run
  `python3 emit.py`, copy staged → web/data (or wire that copy into the build).
- Deploy: `python3 build/build_site.py` (gate → stamp → docs/) then commit + push, then
  **verify the live stamp** (the build prints the curl line).

## Honest assessment against SCOPE (what is and is not there)

Delivered vs the layer table: allegiance (the spine) ✓ · events/chapters ✓ · lake system +
works ✓ (visualization grade, named source) · campaign track ✓ · force readout ✓ · tribute
flows ✓ (simple arcs). **Not yet built, and recorded as open:** the epidemic as a network
MECHANISM (D2 — currently dated events + bands), the siege state as a DERIVED quantity (D2-b),
the Basin terrain field (A2-d — the map's substrate is dark glass, not terrain), events 64 of
~90 and no people cards yet (B2-d), 30 of ~38 Mendoza provinces (B1-b), page-level source pins
(B2-b). The scope's card counts (~200 altepetl) exceed the first tranche's 75.

## The work queue (= register order; 6 open, 0 P1)

The top two need EXTERNAL DOWNLOADS the autonomous session must ask the user about first:

1. **A2-b** trace the González Aparicio reconstruction + the 1524 Nuremberg map from scans
   (Newberry scan is public domain, ~24 MB) — pixel control points, affine fit, residuals.
2. **A2-d** Basin terrain field from INEGI CEM (download by area selection; post-drainage —
   always "DEM minus modern modification, gated by the reconstruction, labelled").
3. **A2-c** chinampa districts (authorable); **B1-b** remaining Mendoza roster (needs location
   research, not typing); **B2-d-rest** people to ~40; **B2-b** page-level pins; **B2-c**
   reversions (thin; may close negative); **A3** licence checks before any collected figure.

## Traps that have each cost real time here

- **Four frames, not one** — everything through `calendar.py`; Nahua dates are correlations
  and the UI labels them.
- **The modern DEM is post-drainage** — never present it as 1519 terrain.
- **The two-colour map is a factual error** — allegiance is the spine and default view.
- **The audits read `web/data/`** once it exists (else staged) — keep it that way (TRAPS D5).
- **Local browser caching** hid a data replacement during the build (the preview showed the
  old shell after web/data changed) — hard-reload with a query-string buster when verifying;
  the production build cache-busts via `?dv=` stamps.
- Plus the standing ones: `&`-backgrounded processes die with the tool call; wait on a PID;
  stamp before copying; verify the live value after every push.

## Commands

```bash
# run locally (or: preview_start name="aztec-conquest")
python3 -m http.server 8140 --directory web

# the research loop
cd Research/modeling && python3 <module>.py     # selftests
python3 emit.py                                  # regenerate staged artifacts
python3 audit_all.py                             # the gate

# deploy
python3 build/build_site.py && git add -A && git commit && git push
# then verify the live stamp (the build prints the exact curl)
```

## How the user wants this done

Working rules in `README.md` §2 — the ones that matter most: **visually verify** (render and
look; statistics are not confirmation) · **fix the system, not the instance** · **measure
before tuning** · **address every item raised** and say so when one cannot be done · **never
state a contested claim flatly** (`accounts:`) · **ranges, not numbers** · **Nahuatl endonyms
first** · be honest in the assessment against the reference.
