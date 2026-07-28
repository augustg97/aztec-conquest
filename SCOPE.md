# SCOPE — Aztec Conquest

The contract. Produced by the scoping interview at kickoff; every later "was that in scope?" is
settled by reading this file. Amend it deliberately, with a date, rather than drifting.

*Scoped 2026-07-27.*

---

## 1. The claim

One paragraph. Not the topic — what a viewer should walk away understanding.

## 2. Extent

| | |
|---|---|
| time | {{START}} → {{END}} |
| stored step | {{STORAGE_STEP}} |
| shown step | {{DISPLAY_STEP}} |
| space | {{SPATIAL_EXTENT}} |
| finest legible thing | {{FINEST_FEATURE}} |
| projection / substrate | {{SUBSTRATE}} |

## 3. The layer table

Every layer, and which of the four it is. A layer that cannot be put in one of these boxes is not
yet designed.

| layer | kind | mechanism (if modelled) or source (if authored) | engine |
|---|---|---|---|
| | modelled / authored / interpolated / static | | field / feature / procedural |

## 4. The evidence boundary

Where the record stops and inference begins: **{{BOUNDARY}}**.

What the UI does past it: {{UI_BEHAVIOUR}}.

Where the sources disagree, and the shape of the disagreement (position / amount / existence):

| disagreement | shape | how the model handles it |
|---|---|---|

## 5. The canonical frame

| dimension | canonical choice | sources that differ, and the conversion |
|---|---|---|
| coordinates | | |
| dates / calendar | | |
| names | | |
| administrative units | | |

Conversions live in `{{CONVERSION_CODE}}` with tests. **Never combine two sources without
checking they are in the same frame.**

## 6. The card contract

Every card carries:

- eyebrow (what kind of thing this is), title
- {{N}} fact rows
- prose **for the current time** — `eras: [{from, to, text}]`
- the era span, shown to the reader
- citations
- {{CONFIDENCE_IF_NEEDED}}

Fallback tiers, and the heading each is shown under:

1. curated exception → "{{HEADING_1}}"
2. model-derived → "{{HEADING_2}}"
3. generic → "{{HEADING_3}}" — **the heading must say it is generic.**

Approximate card counts: {{COUNTS}}.

## 7. The standard for done

Named reference artefacts a result is compared against, at a stated scale:

- {{REFERENCE_1}}

The independent witness — the second, genuinely independent source the model can be scored
against: {{WITNESS}}.

## 8. Sensitivities

What this subject carries, and how the model carries it — **in the substance, distributed
through the layers, not in a disclaimer**.

- {{SENSITIVITY}} → carried by {{HOW}}

Naming convention and why: {{NAMING}}.

## 9. Non-goals

The only defence against a model that grows a layer a week and never ships.

- {{NON_GOAL}}

## 10. Budget and delivery

| | |
|---|---|
| delivery | {{DELIVERY}} |
| total bytes over the wire | {{BYTES}} |
| time to first usable frame | {{TTFF}} |
| offline / `file://` required? | {{OFFLINE}} |
| pipeline? | {{PIPELINE}} |
