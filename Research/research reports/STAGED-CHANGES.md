# Staged changes — everything ready to apply to the model

The research folder does not change the app. This file is the handover: every
item that would touch the app, **with the artifact that makes it a drop-in**,
ordered by measured value rather than register number.

*Staged 2026-07-27, end of research round 1. The build pass (/model-build) executes this list
in order, then rewrites MODEL-GAPS.md statuses DELIVERED → APPLIED with the measurements.*

## Tier 1 — measured, high value, ready now

### 1. Replace the shell's placeholder data with the generated artifacts · A1 A2 B1 B2 C1 D1

**Evidence:** all module selftests green; audit_all at baseline (cards 0/0, witness 0/0);
82 entities, 64 events, 10 chapters, 167.5 KB total (0.65% of the 25 MB budget).
**Artifact:** `Research/research reports/staged-artifacts/{meta,eras,entities,eventsFull,geo}.js`
— complete, strict-JSON-bodied, schema-documented replacements.
**Change:** copy the five files into `web/data/` (replacing the three placeholder files);
add `<script src="data/eventsFull.js">` and `<script src="data/geo.js">` to `index.html`.
**Gate:** `audit_all.py` re-run pointing at `web/data/` (the audits auto-switch to it) — must
stay 0 HIGH / 0 MED.
**Cost:** none.

### 2. The time model: Julian fractional years + the non-linear scrubber · SCOPE §2

**Evidence:** calendar.py t-scalar roundtrips at day resolution 1502-1550; meta.timescale
gives the campaign 56% of the track (linear would give it 5.3% — a 10.6× legibility gain).
**Artifact:** `DATA.meta.timescale` + `DATA.meta.campaign` in staged meta.js.
**Change:** in `web/js/app.js` — replace linear `xOf` with the piecewise map and add its exact
inverse `tOf` (track pointer + hash use it); draw the two breakpoints on the track with a
"day-scale inside the campaign" label; `fmtT(t)` renders `d MMM yyyy (Julian)` inside the
campaign window, the year outside; step buttons move by one day inside the campaign, one month
outside.
**Gate:** `xOf(tOf(x)) ≡ x` to float precision across the track (console-checkable);
scrubbing 1519-1521 changes the readout by days.
**Cost:** none.

### 3. Allegiance colouring — the default view IS the argument · B2, WP-01

**Evidence:** allegiance-states.svg; selftest counts (mid-siege 27 allied + 12 occupied vs 30
tributary + 3 contested + 4 independent + 1 rival) — four-plus colours at every wartime date.
**Artifact:** per-entity `allegiance` series + `meta.stateColor` / `meta.stateLabel`.
**Change:** `drawLayer('altepetl')` colours each marker by `lastLE(e.allegiance, t)`; marker
size by group (alliance-core largest); a legend chip row in the right rail showing the states
present AT the current t with counts (reads the same series — one source of truth).
**Gate:** at t=1519.0 the map shows NO green (coalition) markers; at t=1521.5 it must show
≥ 25 green/blue; Tenochtitlan is never green (selftest-mirrored spot checks in the console).
**Cost:** none.

### 4. Geography: lakes, causeways, dike, aqueduct, city, campaign track · A2, E1

**Evidence:** witness audit 0/0 with measured footprint 15.6 km², lakes 766 km².
**Artifact:** `DATA.geo` + works entities + track flags on eventsFull.
**Change:** `drawBase()` draws the lake polygons (layer `water`), then works polylines (layer
`works`, clickable → cards); campaign track drawn as a dated polyline up to current t (layer
`track`); three view buttons (Mesoamerica / Basin / Tenochtitlan) from `meta.views` switching
the projection extent.
**Gate:** witness audit unchanged (it reads the same geo.js); visual check at Basin view: no
town in open water, causeways meet the city.
**Cost:** none.

## Tier 2 — text and cards

### 5. "What the sources say" + calendar facts on cards · C1, A1

**Evidence:** 19 events with ≥2 accounts; card audit contested-check at 0.
**Artifact:** `accounts` arrays + date facts (Julian/Gregorian/Nahua-correlation) on
eventsFull entities.
**Change:** `openCard()` renders `accounts` as an "What the sources say" section (source —
claim — stake note); event markers near current t (layer `events`) and timeline dots open the
same cards; confidence chip (good/moderate/contested) on the eyebrow row.
**Gate:** card audit stays 0; the Cholula card must show four accounts.
**Cost:** none.

### 6. Chapters, About, and the forces readout · D1, SCOPE §8

**Evidence:** chapters tile exactly; WP-01 measured ratios (allies ≥ 25:1 at the siege on the
sources' own numbers).
**Artifact:** staged eras.js chapters; `meta.about`; `DATA.forces`.
**Change:** About panel populated from `meta.about` (what it is, naming note, what the model
does not know, sources); a "Who is fighting" context panel reading `DATA.forces` — bands drawn
as ranges with the word "contested" where it applies, never a bare number.
**Gate:** anachronism/naming audit stays 0 (About is exempt from the "Aztec" ban by design —
it is where the word is explained).
**Cost:** none.

## Tier 3 — adopt the validators

### 7. The gate in the build script · AUDIT-PATTERNS

**Evidence:** audit_all.py runs both audits against web/data once files land (auto-switch).
**Artifact:** `Research/modeling/audit_all.py`.
**Change:** `build/build_site.py` (new): run audit_all (refuse on regression) → stamp
`dataVersion` into `web/data/meta.js` BEFORE copying → copy `web/` → `docs/` → print the
stamp for post-push verification.
**Gate:** the script refuses to build when either audit regresses; SKIP_AUDIT=1 stays awkward.
**Cost:** none.
