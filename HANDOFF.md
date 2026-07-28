# Handoff — Aztec Conquest

Paste this whole file as the first message of a new session.

---

## What you are working on

**Aztec Conquest** — the fall of Tenochtitlan, 1502–1550: an interactive model of the coalition
that pulled the Mexica empire apart.

- Repo: `/Users/augustgweon/Aztec Conquest` · GitHub: `augustg97/aztec-conquest`
- Live: https://augustg97.github.io/aztec-conquest/ (Pages serves `main:/docs` — docs/ is empty
  until the first build round)
- **Read `README.md` first.** It documents the goals, the standing working rules (§2, including
  five project-specific ones), the traps (§7), and the known limits (§9).
- `SCOPE.md` is the contract: the claim, the layer table, the canonical frame, the evidence
  boundary, the card contract, the standard for done, the non-goals. It was adopted at kickoff
  from `Modeling Studio/worked-example/AZTEC-CONQUEST.md` per the user's instruction.

## The current task

Kickoff (`/model-kickoff`) is **complete**: scope, source survey, scaffold, charter, seeded
register. **No model layer exists yet** — the app is the Studio's scaffold shell with
placeholder data (an "Example Place" dot and a 1750 default year from the shell's demo data).

**Next: run `/model-research` round 1**, per `Research/README.md` "Round 1" — in order:
calendar.py (A1) → georeference + name the lake reconstruction (A2) → altepetl gazetteer (B1) →
allegiance state machine (B2) → `accounts:` card contract + card audit (C1) → witness audit
(E1) → white paper 1 on force composition. Then `/model-build` wires the shell to real data
(1502–1550 time axis with the non-linear campaign scale, chapters, first entities).

## Reference material and the measurement harness

- `Modeling Studio/references/` — working rules, architecture patterns, research method, audit
  patterns, traps, sourcing. The five skills (`/model-research`, `/model-build`,
  `/model-verify`, `/model-ship`) apply here.
- `Research/SOURCE-SURVEY.md` — every P1 source confirmed to exist digitally, with access
  routes: INEGI CEM 4.0 (15 m DEM), the 1524 Nuremberg map (Newberry scan, PD, 5000 px, on
  Commons), Codex Mendoza (INAH digital edition), Getty Digital Florentine Codex (Book XII),
  Sanders/Parsons/Santley settlement survey (tDAR project 192 = the independent witness).
  Licences marked "verify" are register item A3.
- No measurement harness exists yet — E1 (witness audit) builds the first one. The standard for
  done is SCOPE §7: scripted comparison against the named lake reconstruction and the
  georeferenced 1524 map.

## State right now

- Last live deploy: **none** (docs/ empty; Pages will serve once the first build lands)
- Committed and not deployed: the full kickoff (scaffold + charter + survey + register)
- Uncommitted: none at handoff-writing time
- Preview: `.claude/launch.json` (project) and `~/.claude/launch.json` (session-global copy)
  serve `web/` on port 8140; the shell was run and **visually verified** at kickoff
- The scaffold's shell data (`web/data/*.js`) is placeholder demo content — replacing it is
  round-1 build work, not a bug

## What this round found

All from the kickoff source survey (verified by web search 2026-07-27, licences pending A3):

1. The 1524 Nuremberg map exists as a **public-domain 5000×3168 Newberry scan** — shippable and
   georeferenceable.
2. INEGI CEM 4.0 gives the Basin at **15 m / RMSE 4.8 m**, free with attribution; download by
   area selection, not the 6.5 GB national file. The DEM is post-drainage — 1519 terrain is a
   *reconstruction* built from it, and is labelled as one.
3. The 1519 lake exists only as **competing published reconstructions** — round 1 must name the
   canonical one (candidates listed in SOURCE-SURVEY §1); the Commons SVG is likely CC-SA →
   measure-against-only.
4. The independent witness is real and digital: **Parsons' Valley of Mexico survey data, tDAR
   project 192**, plus the 1979 monograph and Gorenflo's compilation.
5. The Getty **Digital Florentine Codex** serves Book XII with Nahuatl/Spanish/English in
   parallel — the Nahua account enters as a primary source in the same register as Cortés.

## Traps that have each cost real time

- **Four frames, not one** — Julian / Gregorian / xiuhpohualli / tonalpohualli, and three
  naming systems. `calendar.py` first; every date tagged with its system; Nahua↔Julian
  correlation is *itself contested*, so correlations are marked as correlations.
- **The modern DEM is post-drainage** — never present it as 1519 terrain.
- **The two-colour map is a factual error** — allegiance is the spine and the default view.
- **Correct licence ≠ correct subject** — `verified_subject: false` until a human looks.

Plus the standing ones:

- a process backgrounded with `&` inside a tool call dies when that call ends; `nohup` does not
  save it. The tell is a log that stops after one line.
- `pgrep -f <script>` matches the waiter's own command line. **Wait on a PID** —
  `until ! kill -0 "$PID"`.
- a static host can serve stale JSON after a successful push. Stamp the data version **before**
  copying the app file, and verify the live value.

## The work queue

Ranked by how much of the remaining gap each closes (= `Research/MODEL-GAPS.md` order):

1. A1 `calendar.py` with selftest — the frame as code, before any dated event is authored.
2. A2 georeference the 1524 map + the lake reconstruction; **name** the reconstruction; record
   residuals.
3. B1 altepetl gazetteer (~200+, from Codex Mendoza / Gerhard / Smith & Berdan).
4. B2 allegiance state machine with selftest.
5. C1 `accounts:` schema + card generator + card audit, built together.
6. E1 archaeological witness audit before anything is drawn on the substrate.
7. White paper 1: *"The conquest had more participants than the story does"* (force
   composition, D1 feeds it).

## Commands

```bash
# run the app locally (or: preview_start name="aztec-conquest")
python3 -m http.server 8140 --directory web

# validators (no audits registered yet — E1/C1 build the first)
python3 "Research/modeling/audit_all.py"
```

## How the user wants this done

Read the working rules in `README.md` §2 — each came from a specific failure. The ones that
matter most:

- **Visually verify.** Render it and look. Statistics are not confirmation.
- **Fix the system, not the instance.**
- **Measure before tuning.**
- **Address every item raised**, and say so explicitly when something cannot be done.
- **Be honest in the assessment** — a truthful yes/no against the reference, not an optimistic
  one.
- Subject-specific: **never state a contested claim flatly** (`accounts:` on every contested
  card), **ranges not numbers** for forces/population/mortality, **Nahuatl endonyms first**.
