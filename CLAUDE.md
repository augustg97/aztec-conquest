# Aztec Conquest — instructions for Claude sessions

The fall of Tenochtitlan, 1502-1550 - an interactive model of the coalition that pulled the Mexica empire apart

**Read `README.md` first** — §1 (what this is trying to be), §2 (the working rules), §7 (traps),
§9 (known limits). Then `SCOPE.md` for the contract and `HANDOFF.md` for the live state.

The general protocol lives in `/Users/augustgweon/Modeling Studio`. Its skills apply here:
`/model-research`, `/model-build`, `/model-verify`, `/model-ship`.

---

## Standing rules — these override default behaviour

1. **Always visually verify.** An update is not done when the data contains the value. It is done
   when it has been **rendered and looked at**. Render the frame, `Read` the image, confirm the
   change is on screen and is correct. "The field has the value" is not confirmation.

2. **Fix the system, not the instance.** When correcting an error, make the change at the level
   that fixes the whole **class** across the whole timeline. A patched instance leaves the same
   bug at every other time and place.

3. **Prefer structural, model-based changes over cosmetic ones.** Ask what the real-world object
   or process is, and model that. Let the appearance fall out of it. Parameter tuning produces
   "modest improvements" and never closes a gap.

4. **Measure before tuning.** Histogram it, spectrum it, or A/B each term behind a debug flag
   before changing a constant.

5. **Track every request each round and address all of them.** If something genuinely cannot be
   done, say so explicitly and say why — do not omit it.

6. **Always deploy, and verify the live artefact.** Every round ends with a build, a commit, a
   push, and a check of the live data-version stamp.

7. **Never ship on an average.** Score every item individually, before and after, and classify
   every regression.

8. **When an audit disagrees with the app, check the audit first.**

9. **Say what is contested**, in the data, as a field.

10. **"Unknown" is a legitimate return**, and where a fallback is unavoidable the UI labels it as
    a fallback.

11. **Never state a contested claim flatly.** Anything the sources dispute carries an
    `accounts:` array and renders "What the sources say". The card audit enforces it.

12. **Every date carries its source system** (Julian / Gregorian / xiuhpohualli /
    tonalpohualli); conversions only through `Research/modeling/calendar.py`. Attested Nahua
    dates are facts; their Julian equivalents are *correlations* and are marked as such.

13. **Nahuatl endonym first, everywhere.** Whose names the map uses is itself a claim.

14. **Ranges, not numbers, for contested quantities** (forces, population, mortality). A single
    confident number in that territory is a bug.

15. **A georeference is a measurement with an error** — control points and residuals per
    historical map in `Research/modeling/georef.py`.

---

## The canonical frame

**WGS84 lon/lat** · **Julian** dates with Gregorian alongside (the Gregorian reform is 1582 —
Julian is what every Spanish source uses) · **Nahuatl endonym first**, Spanish exonym second ·
**Mexica** for the people, **Triple Alliance** for the polity ("Aztec" only in the project title
and the About panel, explained once) · the lake is **one named reconstruction**, never an
average of competitors.

Every source is converted into it. The conversions are in `Research/modeling/calendar.py` and
`Research/modeling/georef.py`. **Never combine two sources without checking they are in the
same frame** — this is the most expensive class of bug in this kind of project.

## The evidence boundary

Dense but partisan — the boundary runs through *kinds of claims*, not through a date: the dated
campaign skeleton is well constrained; the 1519 lake shoreline is a reconstruction; force
numbers, population and epidemic mortality are contested by up to an order of magnitude; motive
and speech are the least constrained thing in the whole subject. The sources are witnesses to
their own case (Cortés's legal brief, Bernal Díaz's counter-memoir, the Florentine Codex's
Tlatelolca informants, Tlaxcala's petitions).

Past it, the model is inference and the UI says so: `accounts:` ("What the sources say") on
contested cards, bands instead of numbers, disputed map elements drawn as disputed,
reconstructions labelled as reconstructions.

---

## Commands

```bash
# run the app locally (serves web/; preview config in .claude/launch.json, port 8140)
python3 -m http.server 8140 --directory web

# validators — run before any publish; the build must refuse to publish on a regression
python3 "Research/modeling/audit_all.py"
```

## Traps that have each cost real time here

- **Four frames, not one** (Julian / Gregorian / xiuhpohualli / tonalpohualli; Nahuatl /
  Spanish / modern names). Everything through `calendar.py`; every authored date tagged with
  its system.
- **The modern DEM is post-drainage.** 1519 terrain = DEM minus post-conquest modification,
  gated by the *named* lake reconstruction, labelled as a reconstruction.
- **Correct licence ≠ correct subject** — collected figures stay `verified_subject: false`
  until a human has looked at them (`Research/figures/collected/MANIFEST.json`).
- **The two-colour map.** Spain-versus-Mexico colouring is a factual error, not a style choice.
  The allegiance layer is the spine and the default view.

Plus the standing ones: a process backgrounded with `&` inside a tool call dies when that call
ends; a waiter on a `pgrep` pattern can match itself — wait on a **PID**; a static host can serve
stale JSON after a successful push, so stamp the data version before copying the app file and
verify the live value.
