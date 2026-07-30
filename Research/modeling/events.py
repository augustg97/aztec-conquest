"""The dated event catalogue, 1502-1550 — the war's skeleton and the allegiance
machine's driver. Stdlib only.

Every event: a Julian date with a PRECISION field (day / month / year), a place
(gazetteer slug, or an explicit lat/lon for battle sites that are not polities),
confidence, sources — and, where the accounts genuinely diverge, an `accounts:`
array that the card renders as "What the sources say". Working rule 2.11: never
state a contested claim flatly.

`effects` drive allegiance.py: [(slug, new_state)] applied at this event's date.
States: see allegiance.py STATES.

Dates are Julian (the canonical frame). The event-date chronology follows the
standard modern reconstructions [TH][HAS]; where the primary accounts disagree
on the date itself, the precision is dropped and the note says so.

CITATION PINNING (register B2-b, round 8): 25 events — the dated spine of the
war — carry a `pins` map locating each claim in the division the WORK itself
carries (Bernal Díaz by chapter, the Florentine Codex by book and chapter,
Cortés by letter and section, folios where the source is a codex). Deliberately
NOT page numbers: pages belong to a printing this model does not have in hand,
and inventing them would be fabricated precision that LOOKS checkable. See
PINS below; the selftest enforces the shape and rejects any page reference.

Source keys:
  [C2]/[C3] Cortés, Segunda/Tercera carta de relación (1520/1522)
  [BD]  Bernal Díaz, Historia verdadera (c. 1568, pub. 1632)
  [FC]  Florentine Codex Book XII (Nahua/Tlatelolca testimony, c. 1555-79)
  [AT]  Anales de Tlatelolco (c. 1540s)
  [DUR] Durán, Historia de las Indias (c. 1581)
  [IXT] Alva Ixtlilxóchitl, Historia de la nación chichimeca (c. 1610-40)
  [GOM] López de Gómara (1552)
  [MC]  Muñoz Camargo, Historia de Tlaxcala (c. 1585)
  [TH]  Thomas (1993), Conquest — chronology appendix
  [HAS] Hassig (2006), Mexico and the Spanish Conquest, 2e
  [GIB] Gibson (1964), The Aztecs Under Spanish Rule — aftermath
  [GER] Gerhard (1972) — colonial consolidation dates
  [CMH] Cook & Borah / McCaa — demographic literature (contested, used as ranges)

Run me:  python3 events.py
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calendar import jdn_of_julian, t_of_julian  # noqa: E402

CONFIDENCE = ("good", "moderate", "contested", "none")
PRECISION = ("day", "month", "year")
KINDS = ("political", "campaign", "battle", "massacre", "epidemic", "siege",
         "aftermath", "religious")


def E(eid, y, m, d, precision, kind, name, place, text, conf, sources,
      effects=(), accounts=(), latlon=None, track=False):
    return {"id": eid, "julian": (y, m, d), "precision": precision,
            "kind": kind, "name": name, "place": place, "text": text,
            "confidence": conf, "sources": sources,
            "effects": list(effects), "accounts": list(accounts),
            "latlon": latlon, "track": track,
            "t": t_of_julian(y, m, d), "jdn": jdn_of_julian(y, m, d)}


# ---------------------------------------------------------------------------
# B2-b: citation pinning — at the resolution that is actually verifiable
# ---------------------------------------------------------------------------
# The register asked for "page/folio-level" pinning. PAGE numbers are a trap:
# they belong to a particular printing, and this model does not have those
# printings in hand. Inventing them would be exactly the fabricated precision
# the working rules forbid, and would be worse than the source-family citation
# it replaced, because it would LOOK checkable while being unverifiable.
#
# So the pin is to the division the work itself carries, which is stable across
# every edition and translation:
#
#   [C2]/[C3]  the letter, and its narrative section       "Second Letter"
#   [BD]       Historia verdadera CHAPTER (cap.)           "cap. 88"
#   [FC]       Florentine Codex BOOK and CHAPTER           "Bk XII, ch. 20"
#   [DUR]      Historia de las Indias chapter              "cap. 75"
#   [AT]       Anales de Tlatelolco folio                  "f. 33"
#   [CM]       Codex Mendoza folio                         "fol. 2r"
#
# PINS carries only the events whose dating actually rests on a locatable
# passage. An event with no entry is not "unpinned by oversight" — it is one
# whose date comes from the modern chronologies [TH]/[HAS] synthesising several
# accounts, and there is no single passage to point at. _selftest enforces the
# shape of every pin, so a page number cannot be smuggled in later.
PINS = {
    "ulua-landing":         {"[BD]": "cap. 36-40"},
    "villa-rica-founded":   {"[C2]": "Second Letter, the founding of Villa Rica de la Vera Cruz",
                             "[BD]": "cap. 41-42"},
    "tlaxcala-battles":     {"[C2]": "Second Letter, the fighting in Tlaxcala",
                             "[BD]": "cap. 62-69"},
    "tlaxcala-alliance":    {"[C2]": "Second Letter, the peace with Tlaxcala",
                             "[BD]": "cap. 70-77", "[MC]": "Historia de Tlaxcala, lib. I"},
    "cholula-massacre":     {"[C2]": "Second Letter, the affair at Cholula",
                             "[BD]": "cap. 83", "[FC]": "Bk XII, ch. 11"},
    "entry-tenochtitlan":   {"[C2]": "Second Letter, the entry of 8 November",
                             "[BD]": "cap. 87-88", "[FC]": "Bk XII, ch. 15-16"},
    "moctezuma-seized":     {"[C2]": "Second Letter, the seizure of Moctezuma",
                             "[BD]": "cap. 95", "[FC]": "Bk XII, ch. 17"},
    "cempoala-narvaez":     {"[C2]": "Second Letter, the defeat of Narváez",
                             "[BD]": "cap. 122-123"},
    "toxcatl":              {"[FC]": "Bk XII, ch. 20 — the fullest account, from Tlatelolca witnesses",
                             "[BD]": "cap. 125", "[DUR]": "cap. 75"},
    "moctezuma-dies":       {"[C2]": "Second Letter, the death of Moctezuma",
                             "[BD]": "cap. 126", "[FC]": "Bk XII, ch. 23"},
    "noche-triste":         {"[C2]": "Second Letter, the retreat from the city",
                             "[BD]": "cap. 128", "[FC]": "Bk XII, ch. 24",
                             "[AT]": "f. 36"},
    "otumba":               {"[C2]": "Second Letter, the battle on the plain",
                             "[BD]": "cap. 128"},
    "tepeaca-campaign":     {"[C2]": "Second Letter, the Tepeaca campaign",
                             "[BD]": "cap. 130-135"},
    "smallpox-basin":       {"[FC]": "Bk XII, ch. 29 — the huey zahuatl"},
    "texcoco-taken":        {"[C3]": "Third Letter, the occupation of Texcoco",
                             "[IXT]": "Historia de la nación chichimeca, cap. 88-90"},
    "chalco-defects":       {"[C3]": "Third Letter, the Chalca embassies"},
    "chalco-counterattacks":{"[C3]": "Third Letter, the relief of Chalco"},
    "chalco-relieved":      {"[C3]": "Third Letter, Sandoval's second march to Chalco"},
    "brigantines-launched": {"[C3]": "Third Letter, the launching of the brigantines",
                             "[BD]": "cap. 150"},
    "siege-camps":          {"[C3]": "Third Letter, the disposition of the three camps",
                             "[BD]": "cap. 150-151"},
    "aqueduct-cut":         {"[C3]": "Third Letter, the cutting of the Chapultepec water"},
    "tlatelolco-ambush":    {"[C3]": "Third Letter, the reverse on the causeway",
                             "[BD]": "cap. 152", "[FC]": "Bk XII, ch. 34"},
    "fall-tenochtitlan":    {"[C3]": "Third Letter, the taking of Cuauhtémoc",
                             "[BD]": "cap. 156", "[FC]": "Bk XII, ch. 40-41",
                             "[AT]": "f. 39"},
    "cuauhtemoc-executed":  {"[BD]": "cap. 177"},
    "codex-mendoza-made":   {"[CM] Berdan & Anawalt (1992)": "fol. 1r-71v — the tribute roll itself"},
}


EVENTS = [
    # ---- before the war: the system the war would break ---------------------
    E("moctezuma-accession", 1502, 9, 15, "year", "political",
      "Moctezuma II becomes huey tlatoani", "tenochtitlan",
      "Moctezuma Xocoyotzin succeeds Ahuítzotl as huey tlatoani of the Triple Alliance. "
      "The empire he inherits takes tribute from some 38 provinces but rules through "
      "local dynasts, not garrisons — a network of obligations, not a surface.",
      "moderate", ["[CM] Codex Mendoza", "[DUR]", "[TH]"],
      ),
    E("new-fire-1507", 1507, 11, 15, "year", "religious",
      "The last New Fire ceremony", None,
      "On Huixachtlan (Cerro de la Estrella) the priests bind the 52-year cycle for "
      "what will prove the last time. The ceremony asserts the world's continuation "
      "under Mexica stewardship.",
      "good", ["[FC] Bk VII", "[DUR]"],
      latlon=(19.3363, -99.0897)),
    E("omens-reported", 1509, 6, 1, "year", "religious",
      "The omens later remembered", "tenochtitlan",
      "A comet by day, the temple that burned unquenchably, the lake that boiled "
      "without wind, the weeping woman in the night — Book XII opens with eight "
      "omens said to have troubled the empire's last decade. Whether anyone saw "
      "them before 1519 is exactly the question.",
      "contested", ["[FC] Bk XII ch.1", "[DUR]", "Restall (2018)"],
      accounts=[
        {"source": "Florentine Codex Bk XII (c. 1555-79)",
         "claim": "eight portents foretold the empire's fall, and Moctezuma read them with dread",
         "note": "compiled a generation AFTER the fall — prophecy is easiest in retrospect"},
        {"source": "modern scholarship (Restall 2018; Townsend 2019)",
         "claim": "the omen list is a post-conquest frame, shaped by both Nahua fatalism-in-defeat and European portent conventions",
         "note": "the model shows the omens as MEMORY, not as events of 1509"},
      ]),
    E("tlachquiauhco-1511", 1511, 6, 1, "year", "campaign",
      "The empire's last expansion: Tlachquiauhco", "tlachquiauhco",
      "Moctezuma II's armies take Tlachquiauhco in the Mixteca Alta — the tribute "
      "system's final addition, eight years before Cortés lands.",
      "moderate", ["[CM] conquest folios", "[HAS]"]),
    E("nezahualpilli-dies", 1515, 6, 1, "year", "political",
      "Nezahualpilli of Texcoco dies; the succession splits", "texcoco",
      "Moctezuma backs Cacama for the Acolhua throne; his half-brother Ixtlilxóchitl "
      "refuses the result and holds the northern Acolhua highlands in arms. The "
      "alliance's second seat is fractured four years before any Spaniard arrives.",
      "moderate", ["[IXT]", "[TH]"],
      effects=[("otompan", "contested")],
      accounts=[
        {"source": "Alva Ixtlilxóchitl (c. 1610-40)",
         "claim": "Ixtlilxóchitl held the northern provinces and later delivered half the empire to the coalition",
         "note": "the chronicler is the rebel's great-great-grandson, writing to secure his family's standing"},
        {"source": "Cortés, Cartas; Bernal Díaz",
         "claim": "the Spanish accounts barely register the Acolhua split until 1520",
         "note": "they had no view into alliance politics before Texcoco changed sides"},
      ]),
    E("cordoba-1517", 1517, 3, 1, "month", "campaign",
      "Córdoba's expedition touches Yucatán", None,
      "The first Spanish expedition from Cuba is mauled at Champotón; word of "
      "bearded strangers on the coast begins to travel the trade roads.",
      "moderate", ["[BD]", "[TH]"], latlon=(19.35, -90.72)),
    E("grijalva-1518", 1518, 6, 1, "month", "campaign",
      "Grijalva coasts the Gulf; first embassies", None,
      "Grijalva trades along the Gulf coast. Moctezuma's stewards meet the ships "
      "and carry reports and gifts to Tenochtitlan.",
      "moderate", ["[BD]", "[FC]", "[TH]"], latlon=(18.78, -95.76)),

    # ---- 1519: the corridor and the coalition ------------------------------
    E("depart-cuba", 1519, 2, 18, "day", "campaign",
      "The company leaves Cuba", None,
      "Cortés sails from Cuba with ~500-630 men, ~16 horses and ~11 ships, in "
      "defiance of governor Velázquez's revocation — the expedition is illegal "
      "from its first day, which shapes every letter Cortés will write about it.",
      "moderate", ["[BD]", "[C2]", "[TH]"], latlon=(21.9, -84.9), track=True),
    E("centla", 1519, 3, 25, "day", "battle",
      "Battle of Centla", None,
      "The company defeats the Chontal Maya of Potonchan; among the tribute of "
      "peace is a group of enslaved women including Malintzin, who will become "
      "the expedition's Nahuatl-Maya interpreter and political instrument.",
      "moderate", ["[BD]", "[GOM]", "[TH]"], latlon=(18.28, -92.65), track=True),
    E("ulua-landing", 1519, 4, 21, "day", "campaign",
      "Landing at San Juan de Ulúa", None,
      "The fleet anchors off the dunes opposite San Juan de Ulúa, inside the "
      "tribute province of Cuetlaxtlan. Moctezuma's governors arrive within days "
      "with gifts and painters to record the strangers.",
      "good", ["[BD]", "[C2]", "[FC]", "[TH]"], latlon=(19.21, -96.13), track=True),
    E("villa-rica-founded", 1519, 6, 28, "month", "political",
      "Villa Rica de la Vera Cruz founded; the legal coup", "villa-rica",
      "The company constitutes itself a town, elects a cabildo, and has the new "
      "town commission Cortés directly under the crown — the legal device that "
      "unhooks the expedition from Cuba. The first Totonac alliance is made the "
      "same season.",
      "moderate", ["[C2]", "[BD]", "[TH]"],
      effects=[("cempoala", "allied-coalition"), ("quiahuiztlan", "allied-coalition")],
      accounts=[
        {"source": "Cortés, Primera/Segunda carta (1519-20)",
         "claim": "the town's commission made the enterprise lawful and royal",
         "note": "the letters exist to argue exactly this to a crown that could hang him"},
        {"source": "Velázquez's party; later lawsuits",
         "claim": "a mutiny dressed as a municipality",
         "note": "the rival faction's framing, pursued in court for years"},
      ]),
    E("cempoala-tribute-refusal", 1519, 7, 15, "month", "political",
      "Cempoala seizes Moctezuma's tribute collectors", "cempoala",
      "At Cortés's urging the Totonac towns arrest the imperial collectors — the "
      "first open breach in the tribute system, engineered so the Totonacs cannot "
      "step back. The grievance that made it possible was the tribute itself.",
      "moderate", ["[BD]", "[C2]"],
      ),
    E("ships-scuttled", 1519, 8, 10, "month", "campaign",
      "The ships are run ashore", "villa-rica",
      "Cortés strips and beaches the fleet: no way back to Cuba, every man "
      "committed to the march inland.",
      "moderate", ["[C2]", "[BD]", "[GOM]"],
      accounts=[
        {"source": "Cortés, Segunda carta (1520)",
         "claim": "ships grounded as unseaworthy",
         "note": "understates the coercion of his own Velázquez faction"},
        {"source": "Bernal Díaz; Gómara",
         "claim": "deliberately destroyed to foreclose retreat",
         "note": "the soldiers' memory of the stakes"},
      ]),
    E("march-inland", 1519, 8, 16, "day", "campaign",
      "The march inland begins", "cempoala",
      "~300-400 Spaniards with Totonac porters and warriors leave Cempoala for the "
      "highlands, by way of Xicochimalco toward Tlaxcallan.",
      "moderate", ["[C2]", "[BD]", "[TH]"], track=True),
    E("tlaxcala-battles", 1519, 9, 2, "day", "battle",
      "Tlaxcallan fights the company", "tlaxcala",
      "The Tlaxcalteca under Xicohtencatl the Younger attack the column repeatedly "
      "over two weeks — the hardest indigenous fighting the Spaniards will face "
      "in open field, ended by Tlaxcallan's own council, not by defeat in rout.",
      "good", ["[C2]", "[BD]", "[MC]"], track=True),
    E("tlaxcala-alliance", 1519, 9, 23, "day", "political",
      "The Tlaxcala alliance", "tlaxcala",
      "The company enters Tlaxcallan as guests. The confederation — blockaded and "
      "salt-starved by the Triple Alliance for a generation — chooses the lever: "
      "its warriors, porters and roads become the war's indigenous backbone. "
      "Without this choice there is no siege and no conquest.",
      "good", ["[C2]", "[BD]", "[MC]"],
      effects=[("tlaxcala", "allied-coalition"), ("huexotzinco", "allied-coalition"),
               ("calpan", "allied-coalition")],
      accounts=[
        {"source": "Muñoz Camargo; the Lienzo de Tlaxcala (c. 1552)",
         "claim": "Tlaxcallan as co-conqueror from the first day, by free decision",
         "note": "produced while Tlaxcala petitioned the crown for the privileges that service earned"},
        {"source": "Cortés, Segunda carta",
         "claim": "vassals gained for the crown by his diplomacy",
         "note": "every ally is written as his instrument"},
      ]),
    E("cholula-massacre", 1519, 10, 18, "day", "massacre",
      "The Cholula massacre", "cholula",
      "In the courtyard of the temple of Quetzalcóatl the company and its "
      "Tlaxcalteca allies kill several thousand assembled Chololteca. Whether a "
      "Mexica-backed ambush was pre-empted or an unarmed crowd was made an "
      "example of is the war's most disputed question; the toll itself is "
      "reported from ~3,000 (Cortés) upward.",
      "contested", ["[C2]", "[BD]", "[FC]", "[MC]", "[TH]"],
      effects=[("cholula", "contested")],
      accounts=[
        {"source": "Cortés, Segunda carta (1520)",
         "claim": "an ambush was set; the strike pre-empted it; ~3,000 died",
         "note": "a legal brief for an unauthorised war; the plot justifies the killing"},
        {"source": "Bernal Díaz (c. 1568)",
         "claim": "confirms the plot, credits Malintzin's warning",
         "note": "written decades later, against Gómara, by a participant with his own case"},
        {"source": "Florentine Codex Bk XII (c. 1555-79)",
         "claim": "the Chololteca were assembled unarmed in the sacred courtyard and slaughtered without cause",
         "note": "Tlaxcalteca guides had their own feud with Cholula; Tlatelolca informants a generation later"},
        {"source": "modern scholarship [TH][HAS]",
         "claim": "evidence for the plot is unverifiable; the effect — terror through the region — is not in doubt",
         "note": "the model draws the event and lets the accounts disagree"},
      ]),
    E("ordaz-popocatepetl", 1519, 10, 25, "month", "campaign",
      "Ordaz climbs the smoking mountain", None,
      "Diego de Ordaz and two companions climb Popocatépetl — in eruption "
      "through these years — to the crater's rim, for sulphur, for "
      "reconnaissance and for the astonishment of both armies. The volcano's "
      "plume stood over the whole war; the model draws it for the attested "
      "1519-1528 active period.",
      "moderate", ["[C2]", "[BD]"], latlon=(19.023, -98.628)),
    E("cholula-realigned", 1519, 11, 1, "month", "political",
      "Cholula realigned under coalition lords", "cholula",
      "New lords acceptable to Tlaxcallan and the company are installed; the holy "
      "city passes into the coalition's rear area.",
      "moderate", ["[C2]", "[MC]"],
      effects=[("cholula", "allied-coalition")]),
    E("paso-de-cortes", 1519, 11, 3, "day", "campaign",
      "Over the pass between the volcanoes", None,
      "The column crosses the saddle between Popocatépetl and Iztaccíhuatl and "
      "descends by Amaquemecan toward the lake plain — the first Spanish sight "
      "of the Basin and its cities on the water.",
      "moderate", ["[C2]", "[BD]"], latlon=(19.087, -98.647), track=True),
    E("ayotzinco-halt", 1519, 11, 6, "day", "campaign",
      "Down the lake edge: Ayotzinco and Iztapalapan", "ayotzinco",
      "The column rounds the freshwater lakes by Ayotzinco and Cuitláhuac and is "
      "lodged in Iztapalapan by lords of Moctezuma's own family.",
      "moderate", ["[C2]", "[BD]"], track=True),
    E("entry-tenochtitlan", 1519, 11, 8, "day", "political",
      "The company enters Tenochtitlan; Moctezuma receives Cortés", "tenochtitlan",
      "Over the Iztapalapan causeway, watched by canoe-borne crowds, the company "
      "is received on the causeway's meeting of roads by Moctezuma and lodged in "
      "the palace of Axayácatl. What Moctezuma's speech of welcome MEANT is the "
      "most contested sentence of the entire war.",
      "good", ["[C2]", "[BD]", "[FC]", "[TH]"],
      accounts=[
        {"source": "Cortés, Segunda carta (1520)",
         "claim": "Moctezuma acknowledged the emperor as the lord his ancestors awaited and 'donated' his realm",
         "note": "a donation speech is precisely what legitimises an unauthorised conquest at law; addressed to the monarch who could ruin him"},
        {"source": "Florentine Codex Bk XII (c. 1555-79)",
         "claim": "a courteous royal welcome in high Nahuatl rhetoric: 'you have arrived at your house'",
         "note": "formal host-language, compiled a generation later under Franciscan supervision from Tlatelolca informants"},
        {"source": "modern scholarship (Restall 2018; Townsend 2019)",
         "claim": "the 'surrender' and the 'returning god' reading are post-conquest constructions; the polite formulas were misread or repurposed",
         "note": "the model states the dispute and does not adjudicate"},
      ], track=True),
    E("moctezuma-seized", 1519, 11, 14, "day", "political",
      "Moctezuma seized in his own city", "tenochtitlan",
      "Days after the entry, Cortés takes Moctezuma into custody in the Spanish "
      "quarters. For months the huey tlatoani rules as a hostage; the empire's "
      "centre is captured before its edge knows there is a war.",
      "contested", ["[C2]", "[BD]", "[FC]"],
      accounts=[
        {"source": "Cortés; Bernal Díaz",
         "claim": "a bold pre-emptive seizure days after arrival (the pretext: the Nautla skirmish)",
         "note": "the six-day timeline is Díaz's; Cortés is vague on dates"},
        {"source": "modern scholarship [TH][HAS]",
         "claim": "the seizure may have come weeks later and more gradually than the heroic account implies",
         "note": "the date is drawn at Díaz's timeline with precision marked contested"},
      ]),
    E("quauhpopoca-burned", 1519, 12, 1, "month", "political",
      "Quauhpopoca burned before the palace", "tenochtitlan",
      "The lord of Nautla, whose men had killed Spaniards on the coast, is "
      "surrendered by Moctezuma, tried by Cortés, and burned alive in front of "
      "the palace — on a pyre of the arsenal's own weapons, while the hostage "
      "emperor stands in irons to watch.",
      "contested", ["[C2]", "[BD]", "[TH]"],
      accounts=[
        {"source": "Cortés, Segunda carta",
         "claim": "Quauhpopoca confessed to acting on Moctezuma's orders — proving the emperor's treachery and justifying his seizure",
         "note": "the confession, extracted before burning, is the seizure's legal foundation"},
        {"source": "modern scholarship [TH][HAS]",
         "claim": "more plausibly a coastal tribute conflict; the 'orders' confession is exactly what the occasion required",
         "note": "the model states both readings"},
      ]),
    E("cacama-arrested", 1520, 1, 15, "month", "political",
      "Cacama of Texcoco arrested; Acolhua politics captured", "texcoco",
      "Cacama, planning resistance to the hostage regime, is betrayed, seized and "
      "chained; Cortés installs a pliable brother. The alliance's second seat now "
      "has three claimants and no working government.",
      "moderate", ["[C2]", "[BD]", "[IXT]"],
      effects=[("texcoco", "contested")]),

    E("gold-melted", 1520, 3, 15, "month", "political",
      "The treasure of generations goes into the crucible", "tenochtitlan",
      "Axayácatl's treasure chamber — featherwork, worked gold, the accumulated "
      "art of the tributary system — is inventoried and the gold melted into "
      "portable bars with the royal fifth set aside. What the Mexica had made, "
      "the ledger unmade first.",
      "moderate", ["[C2]", "[BD]", "[FC]"]),

    # ---- 1520: rupture ------------------------------------------------------
    E("narvaez-lands", 1520, 4, 20, "day", "campaign",
      "Narváez lands to arrest Cortés", None,
      "Velázquez's punitive expedition — ~900 men, the largest Spanish force yet "
      "seen on the mainland — lands at San Juan de Ulúa. With it, unrecorded by "
      "anyone at the time, travels smallpox.",
      "moderate", ["[BD]", "[C2]", "[TH]"], latlon=(19.21, -96.13)),
    E("toxcatl", 1520, 5, 22, "day", "massacre",
      "The Tóxcatl massacre", "tenochtitlan",
      "With Cortés away on the coast, Alvarado's garrison falls on the unarmed "
      "celebrants of the feast of Tóxcatl in the sacred precinct and kills the "
      "flower of the Mexica warrior nobility. The city rises; the hostage regime "
      "is finished.",
      "contested", ["[FC]", "[DUR]", "[C2]", "[BD]"],
      effects=[("tenochtitlan", "contested"), ("tlatelolco", "contested")],
      accounts=[
        {"source": "Alvarado's defence, via Cortés and the lawsuits",
         "claim": "an uprising was being prepared under cover of the feast; the strike pre-empted it",
         "note": "the perpetrator's own justification, at law"},
        {"source": "Florentine Codex Bk XII; Durán",
         "claim": "unarmed dancers and drummers butchered in the courtyard, without warning or cause",
         "note": "the Nahua accounts are unanimous and give the massacre its enduring name"},
      ]),
    E("cempoala-narvaez", 1520, 5, 28, "day", "battle",
      "Cortés surprises Narváez at Cempoala", "cempoala",
      "A night assault takes Narváez's camp; the prisoner's army changes sides "
      "almost entire, tripling Cortés's Spanish force at exactly the moment his "
      "position in Tenochtitlan collapses.",
      "moderate", ["[C2]", "[BD]", "[GOM]"]),
    E("cortes-returns", 1520, 6, 24, "day", "campaign",
      "Cortés re-enters a risen city", "tenochtitlan",
      "The reinforced company re-enters Tenochtitlan unopposed — into a trap. The "
      "causeway bridges go up behind them; the palace of Axayácatl becomes a "
      "besieged island inside the island.",
      "good", ["[C2]", "[BD]", "[TH]"], track=True),
    E("moctezuma-dies", 1520, 6, 30, "day", "political",
      "Death of Moctezuma II", "tenochtitlan",
      "Brought to a rooftop to calm the assault, Moctezuma is struck — by whose "
      "hand is disputed to this day — and dies in Spanish custody. With him dies "
      "the fiction that the empire's centre still functions.",
      "contested", ["[C2]", "[BD]", "[FC]", "[DUR]"],
      accounts=[
        {"source": "Cortés; Bernal Díaz; Gómara",
         "claim": "stoned by his own people while appealing for calm; died of the wounds days later, mourned by the Spaniards",
         "note": "the version that absolves the captors, in documents written for the crown"},
        {"source": "Florentine Codex Bk XII; Durán; other Nahua accounts",
         "claim": "the Spaniards killed him once his usefulness ended — some accounts specify garrotting or sword",
         "note": "unanimous that the body the Mexica received showed the Spaniards' work; a generation later, from the other side of the siege"},
      ]),
    E("noche-triste", 1520, 7, 1, "day", "battle",
      "The Noche Triste: the flight from Tenochtitlan", "tenochtitlan",
      "The company breaks out along the Tlacopan causeway in the rain at night "
      "with a portable bridge and the treasure. Caught mid-causeway by canoe "
      "assault, it loses most of its rearguard, most of the treasure, and — by "
      "Cortés's count 150, by Díaz's over 550 — its dead, plus thousands of "
      "Tlaxcalteca allies whose losses no Spanish source counts carefully.",
      "good", ["[C2]", "[BD]", "[FC]", "[AT]"],
      accounts=[
        {"source": "Cortés, Segunda carta",
         "claim": "~150 Spaniards and ~2,000 allies lost",
         "note": "minimising a catastrophe in a letter asking the crown to fund its repair"},
        {"source": "Bernal Díaz",
         "claim": "over 550 Spaniards lost (and 'over 860' counting the Narváez men at Tustepec)",
         "note": "the soldiers' count, against Gómara's hero-narrative"},
        {"source": "Florentine Codex Bk XII; Anales de Tlatelolco",
         "claim": "the canal of the Toltecs choked with horses, men and carried gold",
         "note": "the Mexica memory of a victory the city did not get to keep"},
      ], track=True),
    E("otumba", 1520, 7, 7, "day", "battle",
      "Battle of Otompan (Otumba)", "otompan",
      "The retreating column, harried around the lakes' north end, is intercepted "
      "on the plain of Otompan by a Mexica-led host and cuts its way through — "
      "the cavalry charge that reaches the commander's standard is the day's "
      "hinge. The road to Tlaxcallan is open.",
      "moderate", ["[C2]", "[BD]", "[GOM]"], track=True),
    E("tlaxcala-refuge", 1520, 7, 11, "day", "political",
      "Tlaxcallan holds: the pact renewed", "tlaxcala",
      "The broken company is received, sheltered and re-armed. Tlaxcallan's "
      "council debates Mexica peace overtures and refuses them — the war's "
      "quietest decisive moment: the coalition survives its defeat.",
      "moderate", ["[BD]", "[MC]", "[C2]"],
      accounts=[
        {"source": "Muñoz Camargo; Tlaxcalan tradition",
         "claim": "loyalty freely kept at the hour it mattered, at the price of stated privileges",
         "note": "the petition-era framing of the choice"},
        {"source": "Mexica overtures per [BD][DUR]",
         "claim": "Cuitláhuac offered Tlaxcallan the partnership the Mexica had always refused",
         "note": "reported through hostile intermediaries; terms unrecoverable"},
      ]),
    E("cuitlahuac-tlatoani", 1520, 9, 16, "month", "political",
      "Cuitláhuac becomes huey tlatoani", "tenochtitlan",
      "Iztapalapan's lord, the war party's head, is elected and crowned. He "
      "reopens the causeways, rebuilds alliances where he can, and dies of "
      "smallpox after roughly eighty days of a reign spent entirely at war.",
      "moderate", ["[FC]", "[DUR]", "[TH]"]),
    E("tepeaca-campaign", 1520, 9, 4, "day", "campaign",
      "The Tepeaca campaign; Segura de la Frontera", "tepeaca",
      "The coalition retakes the eastern road by systematic terror — massacre and "
      "enslavement, branding captives with the letter G for guerra. The Spanish "
      "town of Segura de la Frontera is founded in Tepeyacac; the corridor to the "
      "coast will not close again.",
      "moderate", ["[C2]", "[BD]", "[TH]"],
      effects=[("tepeaca", "allied-coalition"), ("itzocan", "allied-coalition")]),
    E("tepeaca-enslavement", 1520, 9, 15, "month", "aftermath",
      "The branding iron at Tepeyacac", "tepeaca",
      "In the retaken towns the coalition brands captives — women and children "
      "among them — with the letter G, for guerra, and distributes them as "
      "slaves. The reprisal economy of the war, recorded without embarrassment "
      "in the Spanish accounts themselves.",
      "moderate", ["[C2]", "[BD]", "[TH]"]),
    E("cuauhquechollan-defects", 1520, 10, 15, "month", "political",
      "Cuauhquechollan turns on its garrison", "cuauhquechollan",
      "The altepetl invites the coalition in against the Mexica garrison quartered "
      "on it — the pattern, repeated down the road: the empire's own structure "
      "supplies the war's manpower. Its lienzo later paints the campaign as its "
      "own conquest, shared with the strangers.",
      "moderate", ["[C2]", "Lienzo de Cuauhquechollan"],
      effects=[("cuauhquechollan", "allied-coalition")]),
    E("smallpox-basin", 1520, 10, 1, "month", "epidemic",
      "Smallpox reaches the Basin", "tenochtitlan",
      "The epidemic that entered at the coast with the Narváez fleet burns "
      "through the lake cities for sixty days by the Nahua account — killing, "
      "among uncounted others, the huey tlatoani Cuitláhuac and lords in every "
      "altepetl, on the defending side of the war only.",
      "contested", ["[FC]", "[Motolinía]", "[CMH]"],
      accounts=[
        {"source": "Florentine Codex Bk XII",
         "claim": "sixty days of huey zahuatl in the city; the dead unburied; the living unable to tend the sick",
         "note": "the only inside account of the epidemic in the capital"},
        {"source": "Motolinía (1541)",
         "claim": "'in most provinces more than half the people died'",
         "note": "a friar's estimate two decades on; the basis of the highest mortality readings"},
        {"source": "modern demography [CMH]",
         "claim": "Basin mortality in 1520-21 plausibly 30-50%; all precise figures are constructions",
         "note": "the model states a band, never a number"},
      ]),
    E("cuitlahuac-dies", 1520, 12, 4, "day", "epidemic",
      "Cuitláhuac dies of smallpox; Cuauhtémoc chosen", "tenochtitlan",
      "The war leader's death after ~80 days leaves the defence to Cuauhtémoc of "
      "Tlatelolco — young, implacable, and crowned in a city already burying its "
      "leadership class.",
      "contested", ["[FC]", "[DUR]", "[TH]"],
      accounts=[
        {"source": "chronology per [TH]",
         "claim": "died 4 December 1520 (some readings: 25 November)",
         "note": "the sources give reign-lengths, not dates; the day is a reconstruction"},
        {"source": "Florentine Codex Bk XII; Durán",
         "claim": "a reign of eighty days, ended by the huey zahuatl",
         "note": "the Nahua accounts count the reign, not the calendar"},
      ]),
    E("texcoco-taken", 1520, 12, 31, "day", "political",
      "The coalition enters Texcoco", "texcoco",
      "Cortés occupies the alliance's second capital unopposed; its Mexica-party "
      "lords flee across the lake. Under Ixtlilxóchitl's faction, Acolhua "
      "manpower, food and the lakeside shipyard pass to the coalition — the "
      "siege becomes materially possible on this day.",
      "good", ["[C3]", "[BD]", "[IXT]"],
      effects=[("texcoco", "allied-coalition"), ("huexotla", "allied-coalition"),
               ("coatlinchan", "allied-coalition"), ("chimalhuacan", "allied-coalition")],
      accounts=[
        {"source": "Alva Ixtlilxóchitl",
         "claim": "Ixtlilxóchitl delivered Texcoco and half the empire's manpower to the siege",
         "note": "family chronicle claiming the credit the Spanish accounts withhold"},
        {"source": "Cortés, Tercera carta",
         "claim": "Texcoco taken by his advance and held by his garrison",
         "note": "allies appear as auxiliaries, never as the reason it worked"},
      ], track=True),

    # ---- 1521: the ring closes ---------------------------------------------
    E("iztapalapa-burned", 1521, 1, 9, "day", "battle",
      "Iztapalapan burned", "iztapalapa",
      "The coalition's first lake-shore strike from Texcoco: Cuitláhuac's own "
      "city, half on the water, is stormed and burned; the defenders open the "
      "dike and nearly drown the raiders on the causeway back.",
      "moderate", ["[C3]", "[BD]"],
      effects=[("iztapalapa", "contested")]),
    E("chalco-defects", 1521, 1, 20, "month", "political",
      "The Chalca towns come over", "chalco",
      "Chalco — conquered by the Mexica within living memory after a "
      "generation-long war — asks the coalition for protection against imperial "
      "reprisal. The southeast lakeshore, the Basin's granary, changes sides.",
      "moderate", ["[C3]", "[BD]", "Chimalpahin"],
      effects=[("chalco", "allied-coalition"), ("tlalmanalco", "allied-coalition"),
               ("amaquemecan", "allied-coalition"), ("ayotzinco", "allied-coalition")]),
    E("xaltocan-circuit", 1521, 2, 15, "month", "campaign",
      "The northern circuit: Xaltocan to Tlacopan", "xaltocan",
      "A sweep around the northern lakes takes island Xaltocan and burns through "
      "Cuauhtitlan, Tenayuca and Azcapotzalco to fight in Tlacopan itself — "
      "mapping the ring the siege will close.",
      "moderate", ["[C3]", "[BD]"],
      effects=[("xaltocan", "allied-coalition"), ("cuauhtitlan", "contested"),
               ("tenayuca", "contested"), ("azcapotzalco", "contested")],
      track=True),
    E("brigantines-carried", 1521, 2, 20, "month", "campaign",
      "A fleet carried over the mountains", "tlaxcala",
      "The thirteen brigantines, prefabricated in Tlaxcallan from the scuttled "
      "ships' iron, are carried in pieces over the sierra to Texcoco by a "
      "porter column the sources describe in the tens of thousands — the "
      "war's plainest demonstration of what allied manpower meant.",
      "moderate", ["[C3]", "[BD]", "[IXT]", "[MC]"]),
    E("chalco-counterattacks", 1521, 3, 15, "month", "battle",
      "The Mexica strike back at Chalco", "chalco",
      "Cuauhtémoc's armies come down on the defected Chalca towns again and "
      "again through the spring. Chalco sends to Cortés twice saying it cannot "
      "hold alone. For some weeks the granary is genuinely back in play — the "
      "one stretch of the war where the empire takes ground back.",
      "moderate", ["[C3]", "[BD]", "Chimalpahin"],
      effects=[("chalco", "contested"), ("tlalmanalco", "contested"),
               ("amaquemecan", "contested"), ("ayotzinco", "contested")],
      accounts=[
        {"source": "Cortés, Third Letter (1522) [C3]",
         "claim": "the Chalca appealed to him as their protector and he despatched relief that settled the matter",
         "note": "the letter is a legal brief for a man who needed to look like a sovereign meeting his obligations"},
        {"source": "Chimalpahin (Chalca annals, early 17th c.)",
         "claim": "the fighting was Chalco's own war, fought by Chalca lords, the coalition arriving late",
         "note": "written from inside Chalco, to record that the town was an agent and not a prize"},
      ]),
    E("chalco-relieved", 1521, 4, 5, "month", "campaign",
      "Sandoval's relief: Chalco held", "chalco",
      "Gonzalo de Sandoval is sent back to the southeast with a heavy column "
      "and the Chalca towns are secured for good. The counter-offensive was "
      "the empire's last chance to break the ring before it closed; from here "
      "the coalition's line around the lakes is continuous.",
      "moderate", ["[C3]", "[BD]", "Chimalpahin"],
      effects=[("chalco", "allied-coalition"), ("tlalmanalco", "allied-coalition"),
               ("amaquemecan", "allied-coalition"), ("ayotzinco", "allied-coalition")]),
    E("southern-circuit", 1521, 4, 13, "day", "campaign",
      "The southern circuit: Cuauhnáhuac and Xochimilco", "quauhnahuac",
      "Crossing the sierra, the coalition storms Cuauhnáhuac, then fights two "
      "days in Xochimilco's canals — the chinampa city nearly kills Cortés — "
      "before circling the lakes home. Every approach to the capital has now "
      "been tested.",
      "moderate", ["[C3]", "[BD]"],
      effects=[("quauhnahuac", "allied-coalition"), ("huaxtepec", "allied-coalition"),
               ("yauhtepec", "allied-coalition"), ("yacapichtla", "allied-coalition"),
               ("xochimilco", "contested")],
      track=True),
    E("xochimilco-battle", 1521, 4, 16, "day", "battle",
      "Two days in the canals of Xōchimīlco", "xochimilco",
      "The chinampa city fights the circuit column canal by canal; Cortés is "
      "dragged from his horse and nearly taken alive before Tlaxcalteca "
      "warriors cut him free. The war's texture at close quarters: causeways, "
      "bridges removed, canoes in the gaps.",
      "moderate", ["[C3]", "[BD]"]),
    E("brigantines-launched", 1521, 4, 28, "day", "siege",
      "Thirteen brigantines launched at Texcoco", "texcoco",
      "Built of the scuttled fleet's ironwork and Tlaxcalteca-carried timber, "
      "assembled by thousands of Acolhua labourers on a dug canal, the lake "
      "flotilla launches. Command of the water — the city's food and its "
      "escape — is about to change hands.",
      "good", ["[C3]", "[BD]", "[IXT]"]),
    E("siege-camps", 1521, 5, 22, "day", "siege",
      "The siege opens: three causeway camps", "tenochtitlan",
      "Alvarado takes station at Tlacopan, Olid at Coyoacán, Sandoval at "
      "Iztapalapan; the brigantines base at Texcoco. Some 700-900 Spaniards — "
      "and, by every account including Cortés's own, tens of thousands of "
      "Tlaxcalteca, Acolhua, Chalca and Huexotzinca — invest a city of perhaps "
      "50,000-200,000.",
      "good", ["[C3]", "[BD]", "[IXT]"],
      effects=[("tlacopan", "occupied"), ("coyoacan", "occupied"),
               ("azcapotzalco", "occupied"), ("iztapalapa", "occupied"),
               ("culhuacan", "occupied"), ("mexicaltzingo", "occupied"),
               ("huitzilopochco", "occupied"), ("cuauhtitlan", "occupied"),
               ("tenayuca", "occupied"), ("tultitlan", "occupied"),
               ("ecatepec", "occupied"), ("xochimilco", "occupied"),
               ("cuitlahuac", "allied-coalition"), ("mizquic", "allied-coalition")]),
    E("aqueduct-cut", 1521, 5, 26, "day", "siege",
      "The Chapultepec aqueduct is cut", "tenochtitlan",
      "The city's fresh water — the twin terracotta channels from the Chapultepec "
      "springs — is broken at the source and the ceramic repaired-channel raids "
      "beaten off. From this day the defenders drink brackish well water.",
      "moderate", ["[C3]", "[BD]", "[FC]"]),
    E("brigantine-victory", 1521, 6, 1, "day", "siege",
      "The lake is lost: the canoe fleet broken", "tenochtitlan",
      "In the first fleet action the brigantines catch the wind and run down the "
      "massed war canoes off Iztapalapan. Supply by water — the island city's "
      "logic — is finished; the causeway assaults begin the same week.",
      "moderate", ["[C3]", "[FC]"]),
    E("sandoval-tepeyac", 1521, 6, 10, "month", "siege",
      "The last road closed: Tepeyacac", "tenochtitlan",
      "Sandoval is reposted to seal the northern causeway, left open until now "
      "as a tempting exit. The ring is complete: six arteries, six tourniquets.",
      "moderate", ["[C3]"]),
    E("tlatelolco-ambush", 1521, 6, 30, "day", "battle",
      "The great ambush: the siege's worst Spanish defeat", "tlatelolco",
      "A premature push into the city is cut off at a broken causeway gap; "
      "53-68 Spaniards are taken alive (Cortés admits 35-40; Díaz counted 66 "
      "plus five more days later) and sacrificed on the pyramid of Tlatelolco "
      "in sight of their camps. The coalition's allies waver for days.",
      "moderate", ["[C3]", "[BD]", "[FC]", "[AT]"],
      accounts=[
        {"source": "Cortés, Tercera carta",
         "claim": "35-40 taken, through a subordinate's disobedience",
         "note": "minimises a defeat that nearly broke the siege"},
        {"source": "Bernal Díaz",
         "claim": "66 comrades taken and sacrificed, named and mourned; 72 with the later captures",
         "note": "the eyewitness count from Alvarado's camp"},
      ]),
    E("water-famine", 1521, 7, 1, "month", "siege",
      "Brackish water and the hunger", "tenochtitlan",
      "With the aqueduct cut and the lake lost, the city drinks from hastily "
      "dug brackish wells and eats, in Book XII's remembering, lizards, "
      "swallows, deerhide and adobe scrapings. The siege's principal weapon "
      "is doing its work; no assault kills as many.",
      "moderate", ["[FC]", "[AT]", "[C3]"]),
    E("malinalco-expedition", 1521, 7, 10, "month", "campaign",
      "The flanks secured: Malinalco and the Matlatzinca", "malinalco",
      "Mexica attempts to raise the southwest against the besiegers' rear are "
      "broken by detached columns at Malinalco and in the Toluca valley.",
      "moderate", ["[C3]", "[BD]"],
      effects=[("malinalco", "allied-coalition"), ("ocuilan", "allied-coalition"),
               ("tolocan", "allied-coalition")]),
    E("razing-advance", 1521, 7, 20, "month", "siege",
      "The city unmade street by street", "tenochtitlan",
      "After the ambush the siege changes method: every canal filled, every "
      "building pulled down as the lines advance, the rubble making the causeway "
      "the attackers need. The Mexica defence compresses into Tlatelolco with "
      "the famine and the wells.",
      "good", ["[C3]", "[FC]", "[AT]"]),
    E("surrender-refused", 1521, 7, 25, "month", "political",
      "The offers refused", "tlatelolco",
      "Between assaults, terms pass across the rubble — and are refused. What "
      "was actually offered, and by whom, each side reports to its own "
      "advantage; what is certain is that the defence chose to continue.",
      "contested", ["[C3]", "[FC]", "[AT]"],
      accounts=[
        {"source": "Cortés, Tercera carta",
         "claim": "repeated generous offers of peace, each spurned by Cuauhtémoc's obstinacy",
         "note": "mercy offered and refused is the conqueror's absolution for what follows"},
        {"source": "Florentine Codex; Anales de Tlatelolco",
         "claim": "the demands amounted to surrender of persons, gods and rule — no terms a tlatoani could take",
         "note": "the defence's arithmetic: annihilation fighting, or annihilation yielding"},
      ]),
    E("tlatelolco-market-fall", 1521, 8, 1, "month", "siege",
      "The last stand compresses into the market", "tlatelolco",
      "The defence, starving, holds a shrinking quarter around the great "
      "market of Tlatelolco. The great pyramid burns; the war songs later "
      "collected from the survivors date themselves to these days: 'broken "
      "spears lie in the roads.'",
      "good", ["[FC]", "[AT]", "[C3]"]),
    E("fall-tenochtitlan", 1521, 8, 13, "day", "siege",
      "The fall: Cuauhtémoc taken on the water", "tlatelolco",
      "On the day 1 Cóatl, with the defence starved into a corner of Tlatelolco, "
      "Cuauhtémoc is captured by brigantine while crossing the lake. The Mexica "
      "state ends; the sack that follows is remembered in Nahua song as the "
      "broken spears and the walls red. Roughly 40,000-100,000 defenders and "
      "civilians died in the siege by varying accounts; no source counted the "
      "allies' dead.",
      "good", ["[C3]", "[BD]", "[FC]", "[AT]"],
      effects=[("tenochtitlan", "occupied"), ("tlatelolco", "occupied"),
               ("chimalhuacan", "occupied"), ("huexotla", "occupied"),
               ("coatlinchan", "occupied"), ("tepetlaoxtoc", "occupied"),
               ("teotihuacan", "occupied"), ("acolman", "occupied"),
               ("otompan", "occupied"), ("xaltocan", "occupied"),
               ("zumpango", "occupied"), ("citlaltepec", "occupied"),
               ("hueypoxtla", "occupied"), ("tepotzotlan", "occupied")]),

    # ---- aftermath to 1550: the conquest continues --------------------------
    E("cuauhtemoc-tortured", 1521, 8, 17, "month", "aftermath",
      "Cuauhtémoc tortured for the treasure", "coyoacan",
      "At the Coyoacán headquarters the royal treasurer has Cuauhtémoc's feet "
      "burned to make him yield the gold lost on the Noche Triste. Cortés "
      "permits it; the gold is mostly not found.",
      "moderate", ["[BD]", "[GOM]"],
      accounts=[
        {"source": "Bernal Díaz; Gómara",
         "claim": "the torture happened and shamed those who allowed it",
         "note": "even the conquerors' own accounts record it"},
        {"source": "Cortés, Cartas",
         "claim": "passes over the episode",
         "note": "silence in a legal self-portrait is itself information"},
      ]),
    E("slaves-branded", 1521, 9, 15, "month", "aftermath",
      "The distribution of persons", "coyoacan",
      "Captives of the siege are branded and allotted; the crown's fifth is "
      "taken in people as well as gold. The coalition's indigenous soldiers "
      "watch their share of the victory assessed at less than they were "
      "promised — the first lesson in what the new order weighs.",
      "moderate", ["[C3]", "[BD]", "[GIB]"]),
    E("coyoacan-banquet", 1521, 10, 15, "month", "aftermath",
      "The victory banquet at Coyohuacan", "coyoacan",
      "Wine from a ship at the coast; a banquet for the conquerors that ends "
      "in drunken scandal Bernal Díaz thought shameful enough to record. "
      "Beside it, in the same weeks: the treasure counted, and found a "
      "fraction of what the Noche Triste swallowed.",
      "moderate", ["[BD]"]),
    E("oaxaca-taken", 1521, 12, 15, "month", "aftermath",
      "The Oaxaca valley occupied", "coyolapan",
      "Orozco's column takes the Valley of Oaxaca garrisons; the southern "
      "tribute provinces pass to the new regime with little fighting.",
      "moderate", ["[GER]", "[HAS]"],
      effects=[("coyolapan", "occupied"), ("coayxtlahuacan", "occupied"),
               ("tlachquiauhco", "occupied"), ("tochtepec", "occupied"),
               ("teotitlan", "occupied")]),
    E("rebuilding-begins", 1522, 1, 15, "month", "aftermath",
      "Mexico City rises on the razed grid", "tenochtitlan",
      "The city is rebuilt as the Spanish capital on Tenochtitlan's own plan — "
      "the traza for the conquerors at the centre, the surviving Mexica moved "
      "to the parcialidades at the edges, native labour and the temple stones "
      "doing the building. San Francisco rises where the aviary stood.",
      "good", ["[GIB]", "[TH]"]),
    E("tototepec-taken", 1522, 3, 1, "month", "aftermath",
      "Alvarado takes Tototepec", "tototepec",
      "The coastal Mixtec kingdom that the Triple Alliance never subdued falls "
      "to a Spanish-led column in weeks — then rises in 1523 against the "
      "occupation's exactions, and is broken again.",
      "moderate", ["[GER]", "[HAS]"],
      effects=[("tototepec", "occupied")]),
    E("michoacan-submits", 1522, 7, 15, "month", "aftermath",
      "The Purépecha state submits without a siege", "tzintzuntzan",
      "The cazonci Tangáxuan, whose armies broke Axayácatl's invasion in the "
      "1470s, watches the greater empire die of siege and plague, and receives "
      "Olid's column at Tzintzuntzan without battle — the other empire ends by "
      "calculation, not conquest.",
      "moderate", ["[GER]", "Relación de Michoacán (1541)"],
      effects=[("tzintzuntzan", "occupied")]),
    E("cortes-governor", 1522, 10, 15, "day", "political",
      "The crown legalises the fact: Cortés governor", "tenochtitlan",
      "Charles V names Cortés governor and captain-general of 'New Spain' — the "
      "retroactive blessing the Cartas were written to obtain. Mexico City is "
      "already rising on Tenochtitlan's razed grid.",
      "good", ["royal cédula 15 Oct 1522", "[TH]"]),
    E("panuco-campaign", 1523, 1, 15, "month", "aftermath",
      "The Pánuco campaign", "tochpan",
      "Cortés subdues the Huasteca in a winter campaign of massacre and "
      "burning; the northeastern provinces are folded into New Spain.",
      "moderate", ["[C4]", "[GER]"],
      effects=[("tochpan", "occupied"), ("tzicoac", "occupied"),
               ("metztitlan", "occupied")]),
    E("guerrero-coast", 1523, 6, 1, "year", "aftermath",
      "The southern coast reduced", "cihuatlan",
      "Columns through Guerrero bring the Pacific tribute coast and the "
      "Tlapanec highlands under the new regime.",
      "moderate", ["[GER]"],
      effects=[("cihuatlan", "occupied"), ("tlappan", "occupied"),
               ("tepequacuilco", "occupied"), ("tlachco", "occupied")]),
    E("soconusco-consolidated", 1524, 1, 1, "year", "aftermath",
      "Soconusco and the far provinces absorbed", "xoconochco",
      "The cacao coast passes under Spanish control as Alvarado's Guatemala "
      "expedition marches through and beyond it.",
      "moderate", ["[GER]"],
      effects=[("xoconochco", "occupied")]),
    E("franciscan-twelve", 1524, 6, 1, "month", "religious",
      "The Twelve arrive: the spiritual conquest begins", "tenochtitlan",
      "Twelve Franciscans walk barefoot from the coast; Cortés kneels to them "
      "before the assembled lords. The systematic replacement of the Mexica "
      "sacred order — temple demolition, the schools, the burnings of the "
      "books — begins.",
      "good", ["[Motolinía]", "Sahagún, Coloquios", "[GIB]"]),
    E("honduras-march", 1524, 10, 12, "day", "campaign",
      "The Honduras march leaves the valley", "tenochtitlan",
      "Cortés marches for Honduras against a mutinous lieutenant, taking the "
      "captive lords — Cuauhtémoc among them — because leaving them behind is "
      "judged more dangerous. Two years of jungle catastrophe follow; the "
      "expedition accomplishes nothing and kills the last huey tlatoani.",
      "good", ["[C5]", "[BD]", "[TH]"], track=False),
    E("cuauhtemoc-executed", 1525, 2, 28, "day", "aftermath",
      "Cuauhtémoc hanged at Itzamkánac", None,
      "On the Honduras march, on an informer's word of conspiracy, Cortés hangs "
      "the last huey tlatoani and the lords of Tlacopan and Texcoco from a "
      "ceiba far from home. Even Spaniards on the march called it murder.",
      "good", ["[BD]", "[C5]", "[TH]"],
      latlon=(17.85, -90.85),
      accounts=[
        {"source": "Cortés, Quinta carta",
         "claim": "a confessed conspiracy justified summary justice",
         "note": "the executioner's account of the necessity"},
        {"source": "Bernal Díaz",
         "claim": "'it was a most unjust thing and appeared wrong to all of us'",
         "note": "a participant's verdict written into the soldiers' history"},
      ]),
    E("first-audiencia", 1528, 12, 9, "month", "political",
      "The first audiencia: government as plunder", "tenochtitlan",
      "The crown's first governing board arrives under Nuño de Guzmán and "
      "makes rapacity systematic — encomiendas reshuffled to friends, native "
      "lords shaken down, the conquerors' own chronicles appalled. Royal "
      "government has arrived; good government has not.",
      "good", ["[GIB]", "[TH]"]),
    E("zumarraga-bishop", 1528, 12, 15, "month", "religious",
      "Zumárraga, first bishop and 'Protector of the Indians'", "tenochtitlan",
      "The Franciscan Juan de Zumárraga arrives as bishop-elect with a "
      "protector's title and a reformer's mandate he cannot yet enforce "
      "against the audiencia. The church becomes, unevenly, both shelter "
      "and instrument.",
      "good", ["[GIB]"]),
    E("guzman-west", 1529, 12, 20, "month", "aftermath",
      "Nuño de Guzmán's western march; the cazonci burned", "tzintzuntzan",
      "The first audiencia's president marches west with an army of Mexica and "
      "Tlaxcalteca auxiliaries, tortures and burns the Purépecha cazonci "
      "Tangáxuan, and devastates the west — colonial violence exceeding the "
      "conquest's, under legal forms.",
      "good", ["trial records", "[GER]", "Relación de Michoacán"],
      accounts=[
        {"source": "Guzmán's own proceso (1530)",
         "claim": "the cazonci tried and executed for treason, idolatry and withholding tribute",
         "note": "a legal record produced by the man who profited"},
        {"source": "Relación de Michoacán (1541); later royal inquiry",
         "claim": "judicial murder for gold; Guzmán was eventually recalled in chains",
         "note": "the crown's own reckoning, a decade late"},
      ]),
    E("second-audiencia", 1531, 1, 10, "month", "political",
      "The second audiencia begins the repair", "tenochtitlan",
      "Under Ramírez de Fuenleal and Vasco de Quiroga the replacement board "
      "reverses Guzmán's grants, hears native suits, and begins building the "
      "legal order that royal government will inherit.",
      "good", ["[GIB]"]),
    E("yope-war", 1531, 6, 1, "year", "aftermath",
      "The Yope rising crushed", "yopitzinco",
      "The Yope enclave — never conquered by the Triple Alliance — rises "
      "against tribute and encomienda and is destroyed as a polity; the last "
      "unconquered pocket of the old map is gone.",
      "moderate", ["[GER]"],
      effects=[("yopitzinco", "occupied")]),
    E("guadalupe-tradition", 1531, 12, 9, "day", "religious",
      "Tepeyacac: the apparition tradition", "tenochtitlan",
      "Later tradition places the Virgin's apparitions to Juan Diego at "
      "Tepeyacac — where the causeway met the shrine of the mother-goddess "
      "Tonantzin — in December 1531. The event's date belongs to the "
      "tradition; the earliest surviving narrative is more than a century "
      "younger, and the devotion's growth is itself part of this model's "
      "aftermath.",
      "contested", ["Nican Mopohua (pub. 1649)", "Sahagún (on Tonantzin/Tepeyacac)", "[GIB]"],
      accounts=[
        {"source": "the Guadalupan tradition (Nican Mopohua, pub. 1649)",
         "claim": "the Virgin appeared to Juan Diego at Tepeyacac, 9-12 December 1531, leaving her image on his tilma",
         "note": "the founding narrative of Mexico's central devotion, first printed 118 years after the date it records"},
        {"source": "the documentary record of the 1530s-40s",
         "claim": "contemporary sources, including Zumárraga's papers, are silent; Sahagún later worried the Tepeyacac cult continued Tonantzin's under a new name",
         "note": "silence is not disproof; the model dates the TRADITION and says which is which"},
      ]),
    E("mendoza-viceroy", 1535, 11, 14, "day", "political",
      "Antonio de Mendoza, first viceroy", "tenochtitlan",
      "Royal government arrives in the person of a viceroy; the conquerors' "
      "improvised regime gives way to bureaucratic empire. It is for Mendoza "
      "that the codex bearing his name is painted.",
      "good", ["[GIB]", "[TH]"]),
    E("colegio-tlatelolco", 1536, 1, 6, "day", "religious",
      "The Colegio de Santa Cruz opens at Tlatelolco", "tlatelolco",
      "A college for the sons of the Nahua nobility: Latin, rhetoric, "
      "medicine, and the scriptorium where, a generation on, Sahagún's "
      "students will write down the elders' memory of this whole war — the "
      "institution that makes Book XII possible.",
      "good", ["[GIB]", "SilverMoon (2007)"]),
    E("printing-press", 1539, 6, 1, "year", "political",
      "The first printing press in the Americas", "tenochtitlan",
      "Juan Pablos sets up Cromberger's press in Mexico City; its first "
      "productions are doctrinas in Nahuatl — the conquerors' faith, set in "
      "the conquered language, on the hemisphere's first press.",
      "good", ["[GIB]"]),
    E("don-carlos-executed", 1539, 11, 30, "day", "religious",
      "Don Carlos of Texcoco burned for heresy", "texcoco",
      "Zumárraga's inquisition tries don Carlos Ometochtzin, lord of Texcoco "
      "and grandson of Nezahualcóyotl, for concealed rites and defiant words, "
      "and burns him at the stake. The scandal reaches Spain; native converts "
      "are afterwards removed from the Inquisition's full reach — one pyre "
      "too visible even for the machinery that lit it.",
      "good", ["trial record (proceso, 1539)", "[GIB]"]),
    E("codex-mendoza-made", 1541, 6, 1, "year", "political",
      "The Codex Mendoza is painted", "tenochtitlan",
      "At the viceroy's commission, Nahua tlacuiloque paint the empire for the "
      "emperor across the sea: the conquests of each ruler, the tribute of "
      "each province, a life from cradle to old age — the very document this "
      "model's gazetteer leans on, made twenty years after the fall by the "
      "system's own scribes.",
      "moderate", ["[CM] Berdan & Anawalt (1992)"]),
    E("mixton-war", 1541, 9, 1, "month", "aftermath",
      "The Mixtón war", None,
      "The peoples of the northwest rise against encomienda and slaving raids "
      "and besiege Guadalajara; Mendoza takes the field with tens of thousands "
      "of Mexica and Tlaxcalteca troops. Native New Spain fights on both sides "
      "of every colonial war.",
      "good", ["[GIB]", "[GER]"], latlon=(21.05, -103.0)),
    E("new-laws", 1542, 11, 20, "day", "political",
      "The New Laws: encomienda checked on paper", "tenochtitlan",
      "Charles V's New Laws bar new encomiendas, free enslaved natives, and "
      "order existing grants to lapse — Las Casas's argument become statute. "
      "In Peru the conquerors revolt; in New Spain the viceroy suspends the "
      "sharpest articles. The law and the fact begin their long negotiation.",
      "good", ["the ordinances (20 Nov 1542)", "[GIB]"]),
    E("cocoliztli-1545", 1545, 6, 1, "year", "epidemic",
      "The great cocoliztli", "tenochtitlan",
      "An epidemic the sources call cocoliztli — its identity still debated — "
      "kills on a scale that dwarfs 1520: estimates run from 800,000 into the "
      "millions across New Spain. The demographic catastrophe of the century "
      "is not the siege but the diseases.",
      "contested", ["[Motolinía]", "[CMH]"],
      accounts=[
        {"source": "colonial counts and chronicles",
         "claim": "deaths in the hundreds of thousands to millions, 1545-48",
         "note": "no reliable base population; every figure is a construction"},
        {"source": "modern demography [CMH]",
         "claim": "central Mexico's population fell by perhaps 80-90% across the 16th century, epidemics the largest cause",
         "note": "the band is wide and the model draws it wide"},
      ]),
    E("sahagun-begins", 1547, 6, 1, "year", "religious",
      "Sahagún begins collecting the elders' testimony", "tlatelolco",
      "Bernardino de Sahagún, with his Nahua students of the Colegio, begins "
      "the systematic interviews that will grow into the Florentine Codex — "
      "including Book XII, this war as the Tlatelolca elders remembered it. "
      "The source this model quotes is being created inside the model's own "
      "window.",
      "good", ["Sahagún, prologues", "[GIB]"]),
    E("congregacion-1550", 1550, 1, 1, "year", "aftermath",
      "Congregación: the map itself is remade", "tenochtitlan",
      "By mid-century the crown is gathering the survivors of dispersed altepetl "
      "into planned towns; the lakes are shrinking under drainage and the "
      "chinampa economy contracting. The world the model opened with — lake "
      "cities in a tributary web — no longer exists to map.",
      "good", ["[GIB]", "[GER]"]),
]

# ---------------------------------------------------------------------------
# Round 4 — intra-city placements. A `place` slug keeps carrying the SEMANTIC
# link (allegiance, cards); the placement puts the marker where the event
# happened within the island, from the sources and the city model:
# the meeting at Xoloc on the causeway [C2][BD]; the company quartered in the
# palace of Axayácatl (west of the precinct) [C2][BD]; Tóxcatl in the sacred
# precinct's courtyard [FC]; the ambush at a causeway gap toward Tlatelolco
# [C3][BD]; the last stand in Tlatelolco's market quarter [FC][AT]; the
# colonial events on their documented sites (San Francisco 1524; the Colegio
# 1536; Tepeyac for the Guadalupe tradition). Confidence follows the source's
# own precision — a placement is never finer than its evidence.
PLACEMENTS = {
    "entry-tenochtitlan": (19.4060, -99.1350),    # Xoloc, the causeway fork
    "moctezuma-seized": (19.4346, -99.1341),      # palace of Axayácatl
    "quauhpopoca-burned": (19.4338, -99.1322),    # before the palace, precinct edge
    "gold-melted": (19.4352, -99.1338),           # the palace treasury
    "toxcatl": (19.4344, -99.1310),               # the precinct courtyard
    "cempoala-narvaez": (19.4460, -96.4040),      # Cempoala (unchanged, explicit)
    "cortes-returns": (19.4360, -99.1336),        # the palace, reoccupied
    "moctezuma-dies": (19.4350, -99.1345),        # the palace roof, west side
    "noche-triste": (19.4390, -99.1470),          # the Tlacopan causeway gaps
    "smallpox-basin": (19.4290, -99.1265),        # Teopan quarter
    "cuitlahuac-tlatoani": (19.4336, -99.1316),   # the precinct
    "cuitlahuac-dies": (19.4326, -99.1332),       # the royal compounds
    "siege-camps": (19.4180, -99.1340),           # the southern approaches
    "brigantine-victory": (19.4300, -99.1050),    # open water east of the island
    "sandoval-tepeyac": (19.4680, -99.1200),      # the northern causeway
    "tlatelolco-ambush": (19.4489, -99.1392),     # the causeway gap at Tlatelolco
    "water-famine": (19.4520, -99.1355),          # the Tlatelolco quarter
    "razing-advance": (19.4310, -99.1330),        # the advancing rubble line
    "surrender-refused": (19.4532, -99.1390),     # the shrinking northern pocket
    "tlatelolco-market-fall": (19.4505, -99.1352),  # the great market
    "fall-tenochtitlan": (19.4470, -99.1240),     # taken on the water, east
    "cuauhtemoc-tortured": (19.3467, -99.1617),   # Coyoacán HQ (unchanged, explicit)
    "rebuilding-begins": (19.4335, -99.1325),     # the traza
    "cortes-governor": (19.4330, -99.1290),       # the new palace block
    "franciscan-twelve": (19.4339, -99.1391),     # San Francisco's site
    "guadalupe-tradition": (19.4847, -99.1172),   # Tepeyacac itself
    "printing-press": (19.4332, -99.1345),        # the Cromberger house, traza
    "codex-mendoza-made": (19.4346, -99.1330),    # the scriptoria by the plaza
    "colegio-tlatelolco": (19.4510, -99.1378),    # Santa Cruz de Tlatelolco
    "sahagun-begins": (19.4506, -99.1364),        # the Colegio's scriptorium
    "cocoliztli-1545": (19.4300, -99.1360),       # the parcialidades
    "congregacion-1550": (19.4380, -99.1260),     # the shrinking eastern shore
    "mendoza-viceroy": (19.4336, -99.1286),       # the viceregal palace block
}

for _e in EVENTS:
    if _e["id"] in PLACEMENTS:
        _e["latlon"] = PLACEMENTS[_e["id"]]

BY_ID = {e["id"]: e for e in EVENTS}


# Attach the pins, and refuse to carry one that does not correspond to a real
# event citing that real source — a citation pointing at nothing is worse than
# no citation, because it looks checked.
_by_id = {e["id"]: e for e in EVENTS}
for _eid, _pins in PINS.items():
    if _eid not in _by_id:
        raise ValueError(f"PINS names an event that does not exist: {_eid}")
    _ev = _by_id[_eid]
    for _key in _pins:
        if _key not in _ev["sources"]:
            raise ValueError(f"PINS[{_eid}] pins {_key}, but that event does not cite it "
                             f"(it cites {_ev['sources']})")
    _ev["pins"] = dict(_pins)


def _selftest():
    # B2-b: every pin must name a division the WORK carries (chapter, book+
    # chapter, folio, or a named letter section) — never a page, which belongs
    # to a printing this model does not have in hand. A bare number, or the
    # words "p."/"pp."/"page", is fabricated precision and fails here.
    import re as _re
    _ok = _re.compile(r"^(cap\.\s*\d|Bk\s+[IVXL]+,\s*ch\.\s*\d|f(ol)?\.\s*\d|"
                      r"(First|Second|Third|Fourth|Fifth)\s+Letter|Historia\s)", _re.I)
    _bad_page = _re.compile(r"\bp{1,2}\.\s*\d|\bpage\b", _re.I)
    npins = 0
    for e in EVENTS:
        for key, ref in (e.get("pins") or {}).items():
            npins += 1
            assert not _bad_page.search(ref), \
                f"{e['id']}/{key}: '{ref}' pins a PAGE — pages belong to a printing, not a work"
            assert _ok.match(ref.strip()), \
                f"{e['id']}/{key}: '{ref}' is not a stable work division"
    assert npins >= 40, f"only {npins} pins — B2-b claims more than it delivers"

    import gazetteer

    ids = [e["id"] for e in EVENTS]
    assert len(ids) == len(set(ids)), "duplicate event ids"

    prev_jdn = None
    for e in EVENTS:
        y, m, d = e["julian"]
        assert 1502 <= y <= 1550, e["id"]
        assert e["precision"] in PRECISION and e["kind"] in KINDS, e["id"]
        assert e["confidence"] in CONFIDENCE, e["id"]
        assert e["sources"], e["id"]
        assert e["text"] and len(e["text"]) > 40, f"{e['id']}: text too thin"
        # place resolves in the gazetteer, or an explicit latlon is given
        if e["place"] is not None:
            assert e["place"] in gazetteer.BY_SLUG, f"{e['id']}: unknown place {e['place']}"
        else:
            assert e["latlon"] is not None, f"{e['id']}: no place and no latlon"
        # a contested event must carry accounts — never state it flatly
        if e["confidence"] == "contested":
            assert len(e["accounts"]) >= 2, f"{e['id']}: contested without accounts"
        # accounts entries are well-formed
        for a in e["accounts"]:
            assert a.get("source") and a.get("claim") and a.get("note"), \
                f"{e['id']}: malformed account"
        # effects reference known polities and known states
        for slug, st in e["effects"]:
            assert slug in gazetteer.BY_SLUG, f"{e['id']}: effect on unknown {slug}"
            assert st in ("contested", "allied-coalition", "occupied"), \
                f"{e['id']}: illegal effect state {st}"
        # ordering (events are authored in chronological order)
        if prev_jdn is not None:
            assert e["jdn"] >= prev_jdn - 45, \
                f"{e['id']}: badly out of order"     # small slack for same-season authoring
        prev_jdn = e["jdn"]

    # The skeleton's load-bearing dates, pinned exactly.
    assert BY_ID["entry-tenochtitlan"]["julian"] == (1519, 11, 8)
    assert BY_ID["noche-triste"]["julian"] == (1520, 7, 1)
    assert BY_ID["fall-tenochtitlan"]["julian"] == (1521, 8, 13)
    assert BY_ID["brigantines-launched"]["julian"] == (1521, 4, 28)

    # Flagship contested episodes all carry multi-party accounts.
    for eid in ("cholula-massacre", "entry-tenochtitlan", "toxcatl",
                "moctezuma-dies", "noche-triste", "smallpox-basin"):
        assert len(BY_ID[eid]["accounts"]) >= 2, eid

    n_track = sum(1 for e in EVENTS if e["track"])
    n_acc = sum(1 for e in EVENTS if e["accounts"])
    print(f"selftest OK — {len(EVENTS)} events, {n_track} campaign-track points, "
          f"{n_acc} with 'What the sources say', "
          f"{sum(len(e['effects']) for e in EVENTS)} allegiance effects")


if __name__ == "__main__":
    _selftest()
    from calendar import fmt_julian
    print("\nthe dated skeleton:")
    for e in EVENTS:
        mark = {"day": " ", "month": "~", "year": "≈"}[e["precision"]]
        print(f"  {mark}{fmt_julian(e['jdn']):>12}  {e['name']}")
