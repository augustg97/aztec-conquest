# The sources are witnesses to their own case

**Domain:** 04 the sources · **Status:** first pass, 2026-07-27 ·
**Feeds:** the `accounts:` schema (`Research/DATA-SCHEMA.md`), `modeling/events.py`,
`modeling/audit_cards.py`, every contested card

---

## 1. What the thing is

The record of this war is dense — multiple long eyewitness and near-eyewitness accounts from
both sides — and almost every one of them was produced BY a party to the events, FOR a purpose
the events decided. That is a different evidence problem from scarcity, and the model's central
UI decision (`accounts:` / "What the sources say") is its answer: where accounts diverge, show
who says what and why each would say it; never adjudicate silently.

## 2. The record

| source | when | vantage | the case it argues | confidence as testimony |
|---|---|---|---|---|
| Cortés, *Cartas de relación* | 1519-26 | commander | legal self-defence: he sailed in defiance of his governor, so every letter argues retroactive legitimacy to a monarch who could ruin him; the "donation" speech is exactly what his legal position required | good for dates/logistics; **contested for motive, speech, numbers** |
| Bernal Díaz, *Historia verdadera* | c. 1568 (pub. 1632) | foot soldier | against Gómara's Cortés-hero narrative and for the soldiers' claims to reward; five decades of memory | good for texture and sequence; numbers inflate; chronology occasionally slips |
| **Florentine Codex Book XII** | c. 1555-79 | Nahua elders, **Tlatelolca** informants, under Sahagún's supervision | Nahua memory of the war — from the sister-city whose own quarrel with Tenochtitlan predates the Spaniards; compiled under Franciscan auspices a generation later | the indispensable inside account; its framing passages (omens, the "returning god") are **post-hoc constructions by its own generation** |
| *Anales de Tlatelolco* | c. 1540s | Tlatelolca annalists | earliest Nahua account; grief-literature register | early, fragmentary, invaluable |
| Alva Ixtlilxóchitl | c. 1610-40 | Texcocan mestizo noble | his great-great-grandfather Ixtlilxóchitl as co-conqueror; Texcoco's service to the crown | carries Acolhua detail nothing else has; systematically inflates his house |
| Muñoz Camargo; Lienzo de Tlaxcala | c. 1552-85 | Tlaxcalteca | Tlaxcala as free co-conqueror, deserving perpetual privilege | the coalition's own memory; produced while petitioning |
| Durán; Codex Ramírez | c. 1581 | friar with Nahua sources | a lost Nahua chronicle refracted through Dominican purposes | major for the Mexica court's view |
| Gómara | 1552 | Cortés's chaplain-secretary, never in Mexico | the authorised hero-biography | useful only where others confirm |

**Model implication.** Every contested event carries `accounts` with per-source `note` fields
naming the witness's stake (19 events do in round 1). → **Action: card audit fails a contested
claim without ≥2 accounts** — done, `audit_cards.py check_contested`, baseline 0.

**Model implication.** Nahua accounts are primary sources in the same register as Cortés
(SCOPE §8): Book XII and the Anales appear in `sources` arrays alongside the Cartas, not in a
"native perspective" sidebar. → **Action: hold this in review for every future card.**

## 3. Where confidence falls off, and why

Dates and movements: multiply attested, disagreements of days — **good**. Numbers: partisan in
every direction (see WP-01) — **bands only**. Motive and speech: the least constrained thing in
the subject; the famous set-pieces (Moctezuma's "surrender", the returning-god identification,
the Cholula "plot") are each SOME party's case — **accounts, never verdicts**.

## 4. What is genuinely contested

| question | positions | what the app says |
|---|---|---|
| Moctezuma's welcome speech | donation (Cortés) · courtesy rhetoric (FC XII) · post-hoc construction (Restall 2018, Townsend 2019) | the three positions, on the card |
| the "returning god" story | FC XII narrates it; modern scholarship reads it as post-conquest sense-making | stated as such wherever it appears |
| Cholula: plot or example? | plot pre-empted (Cortés, Díaz, Malintzin's warning) · unprovoked massacre (FC XII) · unverifiable (moderns) | four accounts on the event card |
| who killed Moctezuma | his own people's stones (Spanish) · the Spaniards (Nahua, unanimous) | both, with the custody fact plain |
| Alvarado at Tóxcatl | pre-emption (his defence) · massacre of unarmed dancers (every Nahua account) | both, with the name the massacre carries |

## 5. Naming, dating and coordinate conventions in the sources

Spanish sources: Julian, regnal formulae, Spanish exonyms. Nahua sources: xiuhpohualli year
bearers and day signs (correlation contested — `calendar.py`), Nahuatl endonyms. Gómara/later
compilations: silently "corrected" dates — never used for chronology.

## 6. Caution flags

- Round-1 citations are to source FAMILIES and standard editions; **folio/chapter-level pinning
  is not done** — register B2-b (P3). Dates follow the modern chronologies [TH][HAS].
- Berdan & Anawalt province count: 37, 38 or 39 in different editions/reviews depending on how
  Tlatelolco and the frontier entries are counted; the model says "some 38" and does not
  hang anything on the integer.

## 7. Sources

Editions: Cortés ed. Delgado Gómez (1993); Díaz ed. Serés (2011); Florentine Codex — Getty
Digital Florentine Codex (florentinecodex.getty.edu) and Anderson & Dibble; Lockhart, *We
People Here* (1993); Restall, *When Montezuma Met Cortés* (2018); Townsend, *Fifth Sun* (2019);
Thomas (1993); Hassig (2006).
