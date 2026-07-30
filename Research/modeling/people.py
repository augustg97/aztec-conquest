"""People of the war (register B2-d). Stdlib only.

Thirty of the scope's ~40 people. The first eighteen were chosen because the
events already named them: the tlahtohqueh, the coalition's architects, the
captains, and the figures through whom the aftermath ran. The round-7 tranche
corrects that list's bias — it ran three Mexica lords against six Spaniards,
which quietly argued the opposite of this model's thesis — by adding the
second and third alliance seats (Coanacochtzin, Tetlepanquetzatzin), the
administration that survived the conquest (Tlacotzin), Tlatelolco's governor
and one of its ordinary soldiers, and the WITNESSES whose books every other
card cites (Bernal Díaz, Aguilar, Velázquez de Cuéllar).

ONE CANDIDATE WAS REJECTED, and the reason is a rule: Chimalpahin, the Chalca
annalist this model leans on for Chalco's point of view, was born in 1579 —
outside the 1502-1551 window. A card for him would have required an `active`
span the man did not have. He stays a source and does not become a person. People are CARDS, not map dots — they
move; the app lists whoever is politically active at t and the card's eras
rewrite themselves like every other card's, including past death ("what
became of them" is part of the model, so the eras tile to the model's end).

Windows: `active` = politically active span inside 1502-1550 (the People
panel's filter); eras tile [1502, 1551] like all entities (the card audit's
universal tiling check applies unchanged).

Sensitive-material rules apply with force here (SCOPE §8): Malintzin's agency,
Moctezuma's conduct, Xicohtencatl the Younger's execution and Cacama's death
are contested IN PRINT and carry accounts. Birth years for Nahua figures are
mostly unrecorded — 'c.' and confidence fields, never invented precision.

Run me:  python3 people.py
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calendar import t_of_julian

T0, T1 = 1502.0, 1551.0
CONFIDENCE = ("good", "moderate", "contested")


def P(slug, name, role, active, conf, sources, eras, facts, note="", accounts=()):
    return {"slug": slug, "name": name, "role": role, "active": active,
            "confidence": conf, "sources": sources, "eras": eras, "facts": facts,
            "note": note, "accounts": list(accounts)}


_t = t_of_julian

PEOPLE = [
    P("moctezuma-ii", "Motēuczōma Xōcoyōtzin (Moctezuma II)",
      "huey tlatoani of the Triple Alliance, 1502-1520",
      (T0, _t(1520, 6, 30)), "good",
      ["[FC]", "[C2]", "[BD]", "[DUR]", "[TH]"],
      [{"from": T0, "to": _t(1519, 11, 8),
        "text": "Ninth huey tlatoani: consolidator more than conqueror — the empire's "
                "last expansions, the courtly centralisation, the flower-wars against "
                "Tlaxcallan that never close. The sources written after his fall made "
                "him a fatalist; the record of his reign shows a careful, formidable "
                "administrator."},
       {"from": _t(1519, 11, 8), "to": _t(1520, 6, 30),
        "text": "Host, then hostage: receives the strangers with royal formality on "
                "8 November 1519 and is seized within the week. For months he governs "
                "as a captive — the empire's obedience to its centre turned against "
                "it — until the Tóxcatl massacre makes the arrangement impossible."},
       {"from": _t(1520, 6, 30), "to": T1,
        "text": "Dead in Spanish custody on 30 June 1520 — stoned by his own people in "
                "the Spanish telling, killed by his captors in the unanimous Nahua "
                "accounts. His daughters are married into the conquerors' order; his "
                "name becomes, unfairly, a byword for surrender."}],
      [["Reign", "1502 – June 1520"], ["Died", "30 Jun 1520, in custody (disputed)"],
       ["House", "Tenochtitlan, line of Axayácatl"]],
      note="how he died, and what his welcome speech meant, are both contested — see "
           "the linked events' accounts",
      ),
    P("cuitlahuac", "Cuitláhuac",
      "tenth huey tlatoani — the eighty-day war leader",
      (_t(1515, 1, 1), _t(1520, 12, 4)), "good",
      ["[FC]", "[DUR]", "[TH]"],
      [{"from": T0, "to": _t(1520, 9, 16),
        "text": "Lord of Iztapalapan, brother of Moctezuma, head of the war party: "
                "the counsellor who argued from the first embassies that the "
                "strangers should never enter the city."},
       {"from": _t(1520, 9, 16), "to": _t(1520, 12, 4),
        "text": "Elected huey tlatoani after the Noche Triste he engineered: reopens "
                "the causeways, rebuilds the alliances Moctezuma's captivity had "
                "frozen, offers Tlaxcallan the partnership the empire had always "
                "refused — and is refused. Dies of the smallpox after roughly eighty "
                "days, his reign spent entirely at war."},
       {"from": _t(1520, 12, 4), "to": T1,
        "text": "Dead of the huey zahuatl in early December 1520. The defence he "
                "organised — and the alliance diplomacy he almost pulled off — is the "
                "war the empire might have won."}],
      [["Reign", "Sep – Dec 1520 (~80 days)"], ["Died", "smallpox, Dec 1520"],
       ["Seat", "Iztapalapan"]]),
    P("cuauhtemoc", "Cuāuhtemōc",
      "eleventh and last huey tlatoani",
      (_t(1520, 12, 1), _t(1525, 2, 28)), "good",
      ["[FC]", "[AT]", "[C3]", "[BD]"],
      [{"from": T0, "to": _t(1521, 2, 1),
        "text": "Young lord of Tlatelolco's line, son of Ahuítzotl: raised to the "
                "rulership in a city burying its leaders, with the ring already "
                "closing."},
       {"from": _t(1521, 2, 1), "to": _t(1521, 8, 13),
        "text": "Leads the defence of the siege: the causeway battles, the refusal of "
                "terms, the compression into Tlatelolco. Taken by brigantine on "
                "13 August 1521 while crossing the lake; asks Cortés for the dagger."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Captive figurehead: tortured for the treasure within weeks, kept as "
                "an instrument of indirect rule, dragged on the Honduras march, and "
                "hanged at Itzamkánac in February 1525 on an informer's word. In "
                "modern Mexico, the resister's name — avenues, a metro station, the "
                "young grandfather of the nation."}],
      [["Reign", "Dec 1520 – Aug 1521"], ["Died", "28 Feb 1525, hanged at Itzamkánac"],
       ["House", "Tlatelolco line of Ahuítzotl"]]),
    P("malintzin", "Malintzin (doña Marina; 'La Malinche')",
      "interpreter and political instrument of the conquest",
      (_t(1519, 3, 25), _t(1529, 1, 1)), "contested",
      ["[BD]", "[C2]", "Townsend, Malintzin's Choices (2006)", "[FC] images"],
      [{"from": T0, "to": _t(1519, 3, 25),
        "text": "A Nahua girl of the Coatzacoalcos borderlands, sold or given into "
                "Maya slavery as a child — the trade in persons that the tribute "
                "world ran on, seen from below."},
       {"from": _t(1519, 3, 25), "to": _t(1521, 8, 13),
        "text": "Handed to the strangers at Potonchan among twenty enslaved women; "
                "within months she is the expedition's tongue — Nahuatl to Maya to "
                "Spanish — and its political intelligence. Every negotiation of the "
                "war passes through her; the Nahua accounts draw the pair as one "
                "speaking figure and call Cortés by HER name, 'Malinche'."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Bears Cortés a son, is married to Juan Jaramillo with a dowry of "
                "encomiendas, serves once more as interpreter on the Honduras march, "
                "and disappears from the record by about 1529 — probably dead in her "
                "late twenties. Four centuries of Mexican argument about her begin."}],
      [["Origin", "Coatzacoalcos region, c. 1500"], ["Role", "interpreter, adviser"],
       ["Died", "c. 1527-29 (record falls silent)"]],
      note="her agency is the contested question — see accounts",
      accounts=[
        {"source": "Bernal Díaz",
         "claim": "'without doña Marina we could not have understood the language of "
                  "New Spain and Mexico' — a great lady, indispensable and honoured",
         "note": "the soldiers' memory, affectionate and self-serving at once"},
        {"source": "later nationalist tradition ('malinchismo')",
         "claim": "the archetypal traitress who opened Mexico to the invader",
         "note": "a 19th-20th century construction laid onto a 16th-century enslaved teenager"},
        {"source": "modern scholarship (Townsend 2006)",
         "claim": "an enslaved woman navigating impossible constraints with visible skill; "
                  "'choice' itself is the anachronism",
         "note": "the model presents her acts and lets the framings argue"},
      ]),
    P("cortes", "Hernán Cortés",
      "commander of the expedition; marqués del Valle",
      (_t(1519, 2, 18), T1), "good",
      ["[C2]", "[C3]", "[BD]", "[TH]"],
      [{"from": T0, "to": _t(1519, 2, 18),
        "text": "Minor Extremaduran hidalgo, Cuba encomendero, twice nearly arrested "
                "by his own governor before sailing — the expedition is illegal from "
                "the start, which shapes every letter he writes about it."},
       {"from": _t(1519, 2, 18), "to": _t(1521, 8, 13),
        "text": "The war's improviser: the cabildo trick at Villa Rica, the Tlaxcala "
                "alliance, the hostage regime, the catastrophe of the Noche Triste, "
                "the brigantine siege. His Cartas construct the version — donation, "
                "vassalage, lawful conquest — that the crown will find convenient to "
                "believe."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Governor, then progressively shelved: the Honduras fiasco, the "
                "residencia, a marquisate and 23,000 vassals instead of the "
                "government of New Spain. Dies in Spain in 1547 still petitioning; "
                "his bones, like his reputation, are moved and fought over for "
                "centuries."}],
      [["Born", "1485, Medellín"], ["In Mexico", "1519-28, 1530-40"],
       ["Died", "2 Dec 1547, Castilleja de la Cuesta"]]),
    P("alvarado", "Pedro de Alvarado ('Tonatiuh')",
      "captain; author of the Tóxcatl massacre",
      (_t(1519, 2, 18), _t(1541, 7, 4)), "good",
      ["[BD]", "[FC]", "[TH]"],
      [{"from": T0, "to": _t(1520, 5, 22),
        "text": "The expedition's most flamboyant captain — the Nahua called him "
                "Tonatiuh, the Sun, for his hair. Left in command of the garrison "
                "when Cortés marched against Narváez."},
       {"from": _t(1520, 5, 22), "to": _t(1521, 8, 13),
        "text": "Orders the massacre of the Tóxcatl celebrants — the act that ends "
                "the hostage regime and raises the city. Commands the Tlacopan camp "
                "through the siege, including the causeway disaster of 30 June."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Takes the conquest method south: Guatemala 1524, with Tlaxcalteca "
                "and Mexica armies, then an adelantado's career of expeditions until "
                "a horse crushes him in the Mixtón war, 1541. The Kaqchikel annals "
                "remember him without affection."}],
      [["Epithet", "Tonatiuh — 'the Sun'"], ["Commands", "Tlacopan camp; Guatemala"],
       ["Died", "4 Jul 1541, Guadalajara"]]),
    P("sandoval", "Gonzalo de Sandoval",
      "the siege's steadiest captain",
      (_t(1519, 2, 18), _t(1528, 1, 1)), "good", ["[BD]", "[C3]"],
      [{"from": T0, "to": T1,
        "text": "Youngest of the senior captains and the one the accounts trust: "
                "alguacil of Villa Rica, commander of the Iztapalapan and then "
                "Tepeyacac camps, leader of the flank expeditions. Dies at "
                "thirty-ish in Spain in 1528, accompanying Cortés home."}],
      [["Commands", "Iztapalapan, then Tepeyacac camp"], ["Died", "1528, Palos"]]),
    P("olid", "Cristóbal de Olid",
      "captain of the Coyohuacan camp; the mutineer of Honduras",
      (_t(1519, 2, 18), _t(1524, 11, 1)), "moderate", ["[BD]", "[C5]"],
      [{"from": T0, "to": T1,
        "text": "Commands the Coyohuacan causeway camp through the siege; receives "
                "the Purépecha submission at Tzintzuntzan in 1522; sent to Honduras "
                "in 1524, declares for himself, and is murdered by his own rivals — "
                "the mutiny that draws Cortés into the jungle march that kills "
                "Cuauhtémoc."}],
      [["Commands", "Coyohuacan camp; Michoacán; Honduras"], ["Died", "1524, Naco"]]),
    P("narvaez", "Pánfilo de Narváez",
      "Velázquez's instrument — and the epidemic's ship-master",
      (_t(1520, 4, 20), _t(1520, 12, 1)), "good", ["[BD]", "[TH]"],
      [{"from": T0, "to": T1,
        "text": "Sent with the largest Spanish force yet seen to arrest Cortés; "
                "loses an eye and his army in one night at Cempoala. His fleet's "
                "lasting cargo is the smallpox. Later drowns leading the Florida "
                "expedition whose four survivors include Cabeza de Vaca."}],
      [["Defeated", "28-29 May 1520, Cempoala"], ["Died", "1528, Gulf of Mexico"]]),
    P("xicohtencatl-elder", "Xīcohtēncatl the Elder (Xicohtencatl Huehuetl)",
      "senior lord of Tlaxcallan; architect of the alliance",
      (T0, _t(1522, 6, 1)), "moderate", ["[MC]", "[BD]"],
      [{"from": T0, "to": T1,
        "text": "Aged head of Tizatlan, one of Tlaxcallan's four seats: argues the "
                "council into the Spanish alliance against his own son's war party, "
                "is baptised, and gives the coalition its indigenous foundation. "
                "Dies c. 1522; Tlaxcala's petitions build on his choice for a "
                "century."}],
      [["Seat", "Tizatlan, Tlaxcallan"], ["Chose", "the alliance, Sep 1519"]]),
    P("xicohtencatl-younger", "Xīcohtēncatl the Younger (Axayacatzin)",
      "Tlaxcallan's war captain — and the alliance's dissenter",
      (_t(1519, 8, 31), _t(1521, 5, 12)), "contested",
      ["[BD]", "[MC]", "[C3]", "[HAS]"],
      [{"from": T0, "to": _t(1519, 9, 23),
        "text": "Commands the Tlaxcalteca armies that maul the strangers for two "
                "weeks in September 1519 — the only indigenous commander to fight "
                "them to a standstill in the open field — and argues to finish them."},
       {"from": _t(1519, 9, 23), "to": _t(1521, 5, 12),
        "text": "Overruled by the council, he serves the alliance he opposed, "
                "leading Tlaxcalteca contingents through the war while trusting "
                "none of it."},
       {"from": _t(1521, 5, 12), "to": T1,
        "text": "Leaves the army as the siege opens — desertion in the Spanish "
                "account, a political withdrawal in kinder readings — and is hanged "
                "at Cortés's order with Tlaxcalteca consent the sources dispute. "
                "Four centuries later he is the resister-hero of Tlaxcalan memory."}],
      [["Role", "war captain of Tlaxcallan"], ["Died", "May 1521, hanged"]],
      note="the execution's legality and Tlaxcala's consent are contested — see accounts",
      accounts=[
        {"source": "Bernal Díaz; Cortés's party",
         "claim": "deserted the army at the siege's opening and was lawfully hanged for it",
         "note": "the executioners' record"},
        {"source": "Tlaxcalan tradition; modern readings [HAS]",
         "claim": "a leader who had opposed the alliance from the first, removed at a "
                  "moment when Tlaxcala's council could not afford to defend him",
         "note": "the coalition's internal politics, visible for once"},
      ]),
    P("maxixcatzin", "Māxīxcatzin",
      "lord of Ocotelolco; the alliance's other pillar",
      (T0, _t(1520, 11, 1)), "moderate", ["[BD]", "[MC]"],
      [{"from": T0, "to": T1,
        "text": "Head of Ocotelolco, the alliance's steadiest advocate: argues for "
                "receiving the broken column after the Noche Triste when others "
                "counsel finishing it. Dies of the smallpox in late 1520 — the "
                "epidemic reaching into the coalition's own council."}],
      [["Seat", "Ocotelolco, Tlaxcallan"], ["Died", "smallpox, late 1520"]]),
    P("cacama", "Cacamatzin",
      "tlatoani of Texcoco, 1515-1520",
      (_t(1515, 6, 1), _t(1520, 7, 1)), "contested", ["[C2]", "[BD]", "[IXT]"],
      [{"from": T0, "to": _t(1520, 1, 15),
        "text": "Moctezuma's nephew, installed over his half-brother's rebellion in "
                "1515 — the Acolhua succession that fractures the alliance's second "
                "seat four years before the war."},
       {"from": _t(1520, 1, 15), "to": T1,
        "text": "Plans resistance to the hostage regime, is betrayed and chained; "
                "dies in custody around the Noche Triste — killed by the retreating "
                "Spaniards in most accounts. His brother Ixtlilxóchitl inherits the "
                "claim and delivers it to the coalition."}],
      [["Reign", "Texcoco, 1515-1520"], ["Died", "1520, in Spanish custody"]],
      note="the manner of his death is contested",
      accounts=[
        {"source": "Alva Ixtlilxóchitl; Nahua accounts",
         "claim": "murdered in his chains during the Spanish breakout",
         "note": "the family chronicler, with reason to record it"},
        {"source": "Spanish accounts",
         "claim": "died in the confusion of the retreat",
         "note": "custody deaths are always 'the confusion' in the custodians' telling"},
      ]),
    P("ixtlilxochitl-ii", "Ixtlilxōchitl II of Texcoco",
      "the coalition's Acolhua architect",
      (_t(1515, 6, 1), _t(1531, 1, 1)), "moderate", ["[IXT]", "[C3]", "[BD]"],
      [{"from": T0, "to": _t(1520, 12, 31),
        "text": "The passed-over half-brother who holds the northern Acolhua "
                "highlands in arms from 1516 — the empire's largest internal "
                "fracture before any Spaniard has seen the Basin."},
       {"from": _t(1520, 12, 31), "to": T1,
        "text": "Delivers Texcoco's manpower, food and shipyard to the coalition; "
                "fights through the siege at the head of Acolhua armies; is "
                "baptised Fernando and rules Texcoco under the new order. His "
                "great-great-grandson the chronicler will spend a lifetime "
                "arguing that the conquest was half Texcoco's work."}],
      [["Holds", "northern Acolhuacan from 1516"], ["Baptised", "don Fernando"],
       ["Died", "c. 1530-31"]]),
    P("tecuichpo", "Tecuichpotzin (doña Isabel Moctezuma)",
      "Moctezuma's daughter — the dynasty under the new order",
      (_t(1509, 1, 1), T1), "moderate", ["[GIB]", "Chipman (2005)"],
      [{"from": T0, "to": _t(1521, 8, 13),
        "text": "Moctezuma's favoured daughter, married as a child into the war's "
                "politics — to Cuitláhuac, then to Cuauhtémoc: three times a "
                "tlatoani's consort before she is fifteen."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Married in series to conquerors, granted the encomienda of Tacuba "
                "as her father's heir — the largest held by any woman in New Spain — "
                "and made, deliberately, the exhibit of dynastic continuity under "
                "the crown. Her lawsuits and her heirs' run for generations: the "
                "empire's line persisting as colonial property."}],
      [["Father", "Moctezuma II"], ["Encomienda", "Tacuba"], ["Died", "1550/51"]]),
    P("zumarraga", "Juan de Zumárraga",
      "first bishop of Mexico",
      (_t(1528, 12, 6), _t(1548, 6, 3)), "good", ["[GIB]"],
      [{"from": T0, "to": T1,
        "text": "Franciscan bishop and 'Protector of the Indians': fights the first "
                "audiencia's abuses, brings the printing press, founds the colleges "
                "— and burns don Carlos of Texcoco, the pyre that ends his "
                "inquisition over native converts. Both halves are the colonial "
                "church, in one man."}],
      [["Bishop", "1528-1548"], ["Founded", "press 1539; colleges"],
       ["Died", "3 Jun 1548"]]),
    P("vasco-quiroga", "Vasco de Quiroga ('Tata Vasco')",
      "judge, then bishop of Michoacán — the utopian experiment",
      (_t(1531, 1, 10), T1), "good", ["[GIB]"],
      [{"from": T0, "to": T1,
        "text": "Second-audiencia judge who answers Guzmán's devastation of the "
                "west by founding hospital-towns on More's Utopia — communal land, "
                "craft specialisation by village — and becomes Michoacán's first "
                "bishop. The Purépecha still call him Tata Vasco; the crafts "
                "villages still keep his assignments."}],
      [["Audiencia judge", "1531-35"], ["Bishop of Michoacán", "1536-1565"]]),
    P("sahagun", "Bernardino de Sahagún",
      "friar-ethnographer — Book XII's maker",
      (_t(1529, 6, 1), T1), "good", ["Sahagún, prologues", "[GIB]"],
      [{"from": T0, "to": _t(1547, 6, 1),
        "text": "Arrives in 1529, masters Nahuatl at the missions, teaches at the "
                "Colegio de Tlatelolco — the generation of contact between the "
                "friars' project and the Nahua intellectual class."},
       {"from": _t(1547, 6, 1), "to": T1,
        "text": "Begins the systematic questionnaires that will grow, over forty "
                "years, into the Florentine Codex: Nahua elders' testimony, taken "
                "down in Nahuatl by his Tlatelolca students — including Book XII, "
                "the account of this war that this model cites on nearly every "
                "card. The source is being written inside the model's window."}],
      [["Arrives", "1529"], ["Begins the work", "c. 1547, Tlatelolco"],
       ["Died", "1590, Mexico City"]]),

    # ------------------------------------------------------------------ #
    # Round 7 tranche (register B2-d). Weighted deliberately toward the    #
    # Nahua side: the model's argument is that this was a war fought       #
    # mostly by Nahua polities against a Nahua empire, and a cast that     #
    # ran three Mexica lords against six Spaniards was quietly arguing     #
    # the opposite. Also adds the WITNESSES — the men whose books are the  #
    # sources every other card cites — because who wrote the record is     #
    # itself one of this model's claims (SCOPE §5).                        #
    # ------------------------------------------------------------------ #

    P("coanacochtzin", "Coanacochtzin",
      "tlatoani of Tetzcohco — the half of Texcoco that stayed",
      (_t(1520, 1, 1), _t(1525, 3, 1)), "moderate",
      ["[FC]", "Alva Ixtlilxóchitl", "[TH]"],
      [{"from": T0, "to": _t(1520, 1, 1),
        "text": "A son of Nezahualpilli in a succession the empire had already "
                "interfered with once. Texcoco, the alliance's second seat and its "
                "house of law and letters, enters the war with its royal family "
                "split down the middle."},
       {"from": _t(1520, 1, 1), "to": _t(1521, 8, 13),
        "text": "Takes Texcoco's rulership and holds it for the Mexica while his "
                "brother Ixtlilxóchitl takes the north for the coalition. When the "
                "coalition occupies the city at the end of 1520 he withdraws to "
                "Tenochtitlan and fights the siege from inside it. The single most "
                "important fact about Texcoco in this war is that it was on both "
                "sides at once."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Taken with Cuauhtémoc at the fall. Hanged with him and with "
                "Tetlepanquetzatzin on the Honduras march of 1525, on a charge of "
                "conspiracy that no source outside Cortés's own circle supports."}],
      [["Rules", "c. 1520 – 1521"], ["Seat", "Tetzcohco"],
       ["Died", "1525, on the Honduras march"]],
      note="his brother Ixtlilxóchitl's descendants wrote much of the surviving "
           "Texcocan record, and they wrote him as the loser he was"),

    P("tetlepanquetzatzin", "Tetlepanquetzatzin",
      "tlatoani of Tlacopan — the third seat, to the end",
      (_t(1515, 1, 1), _t(1525, 3, 1)), "moderate",
      ["[FC]", "[C3]", "[TH]"],
      [{"from": T0, "to": _t(1519, 11, 8),
        "text": "Lord of the smallest of the three alliance seats — Tlacopan took a "
                "fifth of the tribute where Tenochtitlan and Texcoco took two fifths "
                "each, and its independence of action was proportionate."},
       {"from": _t(1519, 11, 8), "to": _t(1521, 8, 13),
        "text": "Stays with the Mexica through everything: the hostage year, the "
                "expulsion, the smallpox, the siege. Tlacopan is the western causeway's "
                "landward end and becomes Alvarado's siege camp; its lord fights on "
                "from the island after his own city is lost."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Captured at the fall, tortured with Cuauhtémoc over the missing "
                "treasure, and hanged beside him in 1525. The Triple Alliance ends "
                "with two of its three rulers on the same rope."}],
      [["Seat", "Tlacopan"], ["Tribute share", "one fifth"],
       ["Died", "1525, on the Honduras march"]]),

    P("tlacotzin", "Tlacotzin (don Juan Velázquez Tlacotzin)",
      "cihuacoatl — the empire's chief minister, and its first colonial governor",
      (_t(1519, 1, 1), _t(1526, 6, 1)), "moderate",
      ["[FC]", "Chimalpahin", "[TH]"],
      [{"from": T0, "to": _t(1520, 9, 1),
        "text": "The cihuacoatl was the standing half of Mexica government — internal "
                "administration, justice and the tribute machinery — against the "
                "tlatoani's external and military half. The office ran the state "
                "while the huey tlatoani fought."},
       {"from": _t(1520, 9, 1), "to": _t(1521, 8, 13),
        "text": "Serves Cuauhtémoc through the siege and is captured with him. It is "
                "Tlacotzin, in the Nahua accounts, who answers the Spanish "
                "interrogation about the treasure — the administrator explaining that "
                "the gold the conquerors are looking for went into the lake on the "
                "night they threw it there."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Baptised don Juan Velázquez and installed as governor of the ruined "
                "city — the empire's chief bureaucrat kept on to administer its "
                "conquest. Dies in 1526 returning from the same Honduras march that "
                "killed the lords he had served."}],
      [["Office", "cihuacoatl"], ["Then", "governor of Tenochtitlan, 1521-26"],
       ["Died", "1526"]],
      note="the continuity of Mexica administration through the conquest is one of "
           "the least-told facts of it"),

    P("itzquauhtzin", "Itzquauhtzin",
      "tlacochcalcatl and governor of Tlatelolco",
      (_t(1515, 1, 1), _t(1520, 7, 1)), "moderate",
      ["[FC]", "[TH]"],
      [{"from": T0, "to": _t(1519, 11, 8),
        "text": "Governor of Tlatelolco — the twin city Tenochtitlan had conquered in "
                "1473 and ruled through military governors ever since. Tlatelolco kept "
                "the empire's greatest market and a permanent grievance."},
       {"from": _t(1519, 11, 8), "to": _t(1520, 7, 1),
        "text": "Held with Moctezuma through the hostage months and killed at the same "
                "time, in the same place, in the same disputed circumstances. His body "
                "is thrown out of the palace with Moctezuma's; the Tlatelolca who gave "
                "Sahagún his account remembered that theirs was received with grief "
                "and Moctezuma's with anger."},
       {"from": _t(1520, 7, 1), "to": T1,
        "text": "Remembered in Book XII, which is a Tlatelolca book — the fullest "
                "surviving Nahua account of the war is told from the city he governed, "
                "and it is not a Tenochca story."}],
      [["Office", "governor of Tlatelolco"],
       ["Died", "late June 1520, with Moctezuma"]]),

    P("tzilacatzin", "Tzilacatzin",
      "Otomi warrior of Tlatelolco — the war fought from below",
      (_t(1520, 6, 1), _t(1521, 8, 13)), "contested",
      ["[FC]"],
      [{"from": T0, "to": _t(1520, 6, 1),
        "text": "An otomitl — a member of one of the Mexica warrior societies entered "
                "by capture-count rather than by birth. The model's other cards are "
                "lords; this one is a soldier, because the sources contain a few and "
                "the war was fought by them."},
       {"from": _t(1520, 6, 1), "to": _t(1521, 8, 13),
        "text": "Named repeatedly in Book XII as breaking Spanish and Tlaxcalteca "
                "attacks in Tlatelolco by hurling stones, fighting in three different "
                "disguises so the enemy could not learn to expect him. He is the only "
                "common soldier in this model with a name, and he has one because his "
                "own city's elders insisted on it thirty years later."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "No source records what became of him. The silence is ordinary: the "
                "record keeps lords and loses everyone else, and the exception here "
                "exists only because Sahagún asked Tlatelolca veterans directly."}],
      [["Society", "otomitl"], ["City", "Tlatelolco"], ["Fate", "unrecorded"]],
      note="a named individual attested in one source only — kept because what it "
           "shows about the record is worth as much as the man",
      accounts=[
        {"source": "Florentine Codex Bk XII [FC]",
         "claim": "Tzilacatzin personally broke several assaults and was famous enough to be named",
         "note": "a heroic set-piece in a book collected from the survivors of the losing side, decades on"},
        {"source": "the model's reading",
         "claim": "the details are not independently checkable and may be composite or embellished",
         "note": "shown as testimony, not as established fact — the card says who is speaking"},
      ]),

    P("cuauhpopoca", "Cuauhpopoca",
      "Mexica governor at Nauhtla — the burning that made the hostage regime",
      (_t(1519, 8, 1), _t(1519, 12, 1)), "contested",
      ["[C2]", "[BD]", "[FC]", "[TH]"],
      [{"from": T0, "to": _t(1519, 8, 1),
        "text": "One of the empire's provincial governors on the Gulf coast, in the "
                "zone where Totonac towns had just stopped paying tribute under "
                "Spanish protection — the exact place where imperial authority and the "
                "new arrivals had to collide first."},
       {"from": _t(1519, 8, 1), "to": _t(1519, 12, 1),
        "text": "A clash near Nauhtla kills several Spaniards. Cortés uses it to demand "
                "Moctezuma hand the governor over, then has him burned alive in the "
                "square outside the palace — with Moctezuma put in irons while it "
                "happens. It is the moment the captivity stops being a fiction of "
                "hospitality, and it is staged as theatre."},
       {"from": _t(1519, 12, 1), "to": T1,
        "text": "Whether he acted on Moctezuma's orders is the whole question, and "
                "every source answers it in its own interest."}],
      [["Post", "Nauhtla, Gulf coast"], ["Died", "late 1519, burned in Tenochtitlan"]],
      accounts=[
        {"source": "Cortés, Second Letter [C2]",
         "claim": "the governor confessed that Moctezuma ordered the attack, justifying both the execution and the irons",
         "note": "the confession is reported by the man who needed it to exist; it arrives exactly when his legal position requires it"},
        {"source": "Nahua accounts [FC] and modern readings [TH]",
         "claim": "the execution was a demonstration staged to convert a guest's presence into a hostage's, whatever the governor had done",
         "note": "no Nahua source records the order Cortés says was confessed to"},
      ]),

    P("aguilar", "Jerónimo de Aguilar",
      "interpreter — the first link in the chain",
      (_t(1519, 3, 1), _t(1526, 1, 1)), "good",
      ["[BD]", "[C2]", "[TH]"],
      [{"from": T0, "to": _t(1519, 3, 1),
        "text": "Shipwrecked on the Yucatán coast in 1511 and held among the Maya for "
                "eight years, learning Yucatec Maya as a captive. A priest by training, "
                "and by 1519 barely distinguishable from the people he lived with."},
       {"from": _t(1519, 3, 1), "to": _t(1521, 8, 13),
        "text": "Ransomed by Cortés and made half of the translation chain: Nahuatl to "
                "Maya by Malintzin, Maya to Spanish by Aguilar. Every word exchanged "
                "between Moctezuma and Cortés in 1519 passed through two people and "
                "three languages — which is the single best reason to distrust every "
                "speech the sources record."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Displaced as Malintzin's Spanish improves and the middle link becomes "
                "unnecessary. Given an encomienda; dies in Mexico City around 1531, "
                "far less remembered than the woman he worked beside."}],
      [["Captive", "1511-1519, Yucatán"], ["Chain", "Nahuatl → Maya → Spanish"],
       ["Died", "c. 1531"]]),

    P("gonzalo-guerrero", "Gonzalo Guerrero",
      "the shipwreck's other survivor — the man who refused",
      (T0, _t(1536, 1, 1)), "contested",
      ["[BD]", "Landa", "[TH]"],
      [{"from": T0, "to": _t(1519, 3, 1),
        "text": "Wrecked on the same coast as Aguilar in 1511. Where Aguilar remained a "
                "captive priest, Guerrero rose among the Maya of Chetumal, married a "
                "noblewoman, had children, and became a war captain — the first "
                "Spaniard to take a side and stay on it."},
       {"from": _t(1519, 3, 1), "to": _t(1536, 1, 1),
        "text": "Sent the same ransom offer as Aguilar and refused it. In Bernal Díaz's "
                "telling he points to his tattooed face and pierced ears and says his "
                "children are handsome — the flat, unanswerable refusal that the whole "
                "enterprise had no category for. He is then reported fighting Spanish "
                "expeditions in Yucatán and Honduras for another fifteen years."},
       {"from": _t(1536, 1, 1), "to": T1,
        "text": "Reported killed by gunshot fighting against a Spanish force in "
                "Honduras around 1536. The model keeps him because the conquest is "
                "usually told as if crossing over ran in one direction only."}],
      [["Wrecked", "1511, Yucatán"], ["Refused ransom", "1519"],
       ["Died", "c. 1536, Honduras (reported)"]],
      accounts=[
        {"source": "Bernal Díaz [BD]; Landa",
         "claim": "Guerrero refused ransom, led Maya forces, and died fighting Spaniards",
         "note": "the famous refusal speech is reported second-hand by men who were not there; the outline is corroborated, the words are not"},
        {"source": "modern scholarship [TH]",
         "claim": "much of the surrounding detail is later accretion, and he has been retrospectively made a symbol by parties who need one",
         "note": "the model states the outline and marks the speech as literature"},
      ]),

    P("bernal-diaz", "Bernal Díaz del Castillo",
      "soldier, and the memoirist this model argues with",
      (_t(1519, 2, 1), T1), "good",          # he outlives the window; the card stops with it
      ["[BD]", "[TH]"],
      [{"from": T0, "to": _t(1519, 2, 1),
        "text": "A soldier from Medina del Campo, on the earlier Córdoba and Grijalva "
                "voyages before Cortés's — one of the few men in the enterprise who "
                "had seen the coast three times before the war started."},
       {"from": _t(1519, 2, 1), "to": _t(1521, 8, 13),
        "text": "Present through the whole campaign in the ranks, not the command tent. "
                "His account is the only sustained one from that level, and its "
                "particularity — who stood where, what was eaten, which horse — is why "
                "it survives being wrong about so much else."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Settles in Guatemala and writes the Historia verdadera decades later, "
                "in old age and open irritation at Gómara's court history, which had "
                "given Cortés everything and the men nothing. It is a counter-memoir "
                "with a grievance, which is exactly how this model reads it."}],
      [["Campaigns", "1517, 1518, 1519-21"], ["Writes", "from c. 1550s, Guatemala"],
       ["Died", "1584, Santiago de Guatemala"]],
      note="a witness with an interest: he is arguing for the veterans' rewards, and "
           "against a rival book, on every page"),

    P("velazquez-cuba", "Diego Velázquez de Cuéllar",
      "governor of Cuba — the war Cortés fought behind him",
      (T0, _t(1524, 6, 1)), "good",
      ["[C1]", "[BD]", "[TH]"],
      [{"from": T0, "to": _t(1519, 2, 1),
        "text": "Conqueror and then governor of Cuba, and the man who commissioned the "
                "expedition — as a trading and reconnaissance voyage, under his "
                "authority, with his money in it."},
       {"from": _t(1519, 2, 1), "to": _t(1521, 8, 13),
        "text": "Tries to recall the fleet before it sails, then spends two years "
                "trying to arrest the man who took it. Narváez's expedition of 1520 is "
                "his; it delivers Cortés eight hundred more men and the smallpox. Half "
                "of what Cortés does in Mexico is shaped by needing a legal case "
                "against this one Spaniard."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Loses the jurisdictional fight at court and dies in Cuba in 1524, the "
                "conquest of Mexico having been carried out in defiance of his orders "
                "and then legitimised over his objection."}],
      [["Office", "governor of Cuba"], ["Sends Narváez", "1520"],
       ["Died", "1524, Santiago de Cuba"]],
      note="the Cortés letters are addressed to the crown about this quarrel as much "
           "as about the war"),

    P("antonio-mendoza", "Antonio de Mendoza",
      "first viceroy of New Spain",
      (_t(1535, 11, 14), T1), "good",
      ["[TH]", "Codex Mendoza"],
      [{"from": T0, "to": _t(1535, 11, 14),
        "text": "In Spain, in the crown's service, while the territory he will "
                "eventually govern is first the Triple Alliance's and then, after "
                "1521, run by conquistador government and by two Audiencias — the "
                "first of them violent enough that the crown recalled it."},
       {"from": _t(1535, 11, 14), "to": _t(1550, 1, 1),
        "text": "Arrives as the crown's answer to rule by conquerors: royal government, "
                "the encomienda curbed on paper, the New Laws of 1542 pushed through "
                "far enough to provoke and not far enough to end the system. The Codex "
                "Mendoza — the tribute roll this model's gazetteer is built on — is "
                "compiled for him, to show Spain what had been taken."},
       {"from": _t(1550, 1, 1), "to": T1,
        "text": "Leaves for Peru in 1550. The model's window closes on a functioning "
                "colonial state, which is the point at which the conquest stops being "
                "an event and becomes an arrangement."}],
      [["Viceroy", "1535-1550"], ["Commissions", "the Codex Mendoza, c. 1541"],
       ["Then", "viceroy of Peru, 1551"]]),

    P("nuno-guzman", "Nuño Beltrán de Guzmán",
      "president of the first Audiencia — the violence after the war",
      (_t(1528, 12, 1), _t(1538, 1, 1)), "good",
      ["[TH]", "Las Casas"],
      [{"from": T0, "to": _t(1528, 12, 1),
        "text": "Governor of Pánuco from 1527, where he ran a slave trade shipping "
                "Huastec people to the Caribbean islands — the model's window includes "
                "this because the conquest's economics did not stop at the fall."},
       {"from": _t(1528, 12, 1), "to": _t(1538, 1, 1),
        "text": "Heads the first Audiencia, whose rule is corrupt and brutal enough that "
                "the crown recalls it; then leads the campaigns into the west and "
                "northwest that become Nueva Galicia, with a reputation for cruelty "
                "marked even by the standards of the men around him. Arrested in 1537."},
       {"from": _t(1538, 1, 1), "to": T1,
        "text": "Sent back to Spain and held under a form of house arrest until his "
                "death in 1558, never tried. Included because the aftermath was not a "
                "tidying-up, and the first colonial government was worse than the war."}],
      [["Governor of Pánuco", "1527"], ["First Audiencia", "1528-1530"],
       ["Recalled", "1537"]]),

    # ------------------------------------------------------------------ #
    # Round 8 tranche, completing B2-d at 40. Fills the three remaining    #
    # holes: the years BEFORE 1519 (the model opens in 1502 and had        #
    # almost nobody alive in it), the war's technicians and middle ranks   #
    # rather than only its principals, and the missionary generation who   #
    # made the record the later cards are written from.                    #
    # ------------------------------------------------------------------ #

    P("nezahualpilli", "Nezahualpilli",
      "tlatoani of Tetzcohco — the reign the model opens inside",
      (T0, _t(1515, 1, 1)), "moderate",
      ["Alva Ixtlilxóchitl", "[DUR]", "[TH]"],
      [{"from": T0, "to": _t(1515, 1, 1),
        "text": "Son of Nezahualcóyotl and ruler of the alliance's second seat for more "
                "than forty years: a lawgiver and astronomer in the Texcocan tradition, "
                "and the one lord in the alliance with standing enough to refuse "
                "Tenochtitlan. The model's first thirteen years are his."},
       {"from": _t(1515, 1, 1), "to": _t(1519, 11, 8),
        "text": "His death in 1515 opens the succession Tenochtitlan then interferes "
                "with — Cacama installed with Moctezuma's backing, Ixtlilxóchitl taking "
                "the north in arms, Coanacochtzin waiting. The Triple Alliance's second "
                "seat is already broken four years before the strangers land, and that "
                "fracture is the doorway the whole war walks through."},
       {"from": _t(1519, 11, 8), "to": T1,
        "text": "Remembered by his own descendants as the last ruler of an independent "
                "Texcoco — the chronicler Alva Ixtlilxóchitl is writing about his own "
                "great-great-grandfather, and it shows."}],
      [["Rules", "1472-1515"], ["Seat", "Tetzcohco"],
       ["Died", "1515 — the succession crisis begins"]],
      note="the pre-war fracture in the alliance's second seat is the single most "
           "consequential thing in this model that happened before 1519"),

    P("teuhtlilli", "Teuhtlilli (Tendile)",
      "Moctezuma's governor on the coast — the empire's eyes",
      (_t(1519, 4, 1), _t(1519, 11, 8)), "moderate",
      ["[BD]", "[C2]", "[FC]"],
      [{"from": T0, "to": _t(1519, 4, 1),
        "text": "A provincial governor in the Cuetlaxtlan district, running the tribute "
                "and the road reports on the Gulf coast — one node in a standing "
                "intelligence system that had already logged two Spanish voyages."},
       {"from": _t(1519, 4, 1), "to": _t(1519, 11, 8),
        "text": "Meets Cortés on the dunes within days of the landing, with food, gifts "
                "and PAINTERS — men who drew the ships, the horses, the guns and the "
                "faces, so that a report could be on the road to the capital in a week. "
                "The relay covered roughly 400 km. Whatever else the empire lacked, it "
                "was not information."},
       {"from": _t(1519, 11, 8), "to": T1,
        "text": "Vanishes from the record after the embassies. He matters because the "
                "story is usually told as if the empire were surprised, and its first "
                "act was to commission a drawing."}],
      [["District", "the Gulf coast, Cuetlaxtlan"],
       ["First contact", "April 1519"], ["Sent", "painters, and a running relay"]]),

    P("tzihuacpopocatzin", "Tzihuacpopocatzin",
      "the lord sent to be mistaken for Moctezuma",
      (_t(1519, 9, 1), _t(1519, 11, 8)), "contested",
      ["[FC]", "[TH]"],
      [{"from": T0, "to": _t(1519, 9, 1),
        "text": "A Mexica lord of the ruling house, otherwise unrecorded — one of the "
                "great many people in this war whose lives survive only as a single "
                "action in somebody else's account."},
       {"from": _t(1519, 9, 1), "to": _t(1519, 11, 8),
        "text": "Sent out to the advancing column and presented, in the Nahua telling, "
                "as the huey tlatoani himself — a substitution meant either to test the "
                "strangers' claim to know a god when they saw one, or simply to keep "
                "the real ruler out of reach. It fails: the Tlaxcalteca in the column "
                "know the difference and say so."},
       {"from": _t(1519, 11, 8), "to": T1,
        "text": "The episode is one of the few places the sources let you watch the "
                "empire improvising — and it is recorded only by the losing side."}],
      [["Sent", "autumn 1519, on the road"], ["Outcome", "recognised, and refused"]],
      accounts=[
        {"source": "Florentine Codex Bk XII [FC]",
         "claim": "Moctezuma deliberately sent a double, and the deception was exposed by the Tlaxcalteca",
         "note": "part of a sequence in Book XII that presents Moctezuma as increasingly desperate — a characterisation the same book has reasons to make"},
        {"source": "the Spanish accounts",
         "claim": "no substitution is described at all",
         "note": "silence is not refutation, but the episode rests on one tradition and the model says so"},
      ]),

    P("coyohuehuetzin", "Coyohuehuetzin",
      "tlacatecatl of Tlatelolco — the siege's field command",
      (_t(1520, 7, 1), _t(1521, 8, 13)), "moderate",
      ["[FC]", "[AT]"],
      [{"from": T0, "to": _t(1520, 7, 1),
        "text": "A Tlatelolca commander in the Mexica military hierarchy — the ranks "
                "below the tlatoani that actually moved troops, and that the Spanish "
                "accounts almost never name because they did not know them."},
       {"from": _t(1520, 7, 1), "to": _t(1521, 8, 13),
        "text": "Named repeatedly in Book XII and the Anales de Tlatelolco directing the "
                "defence as the coalition compresses the city northward: the causeway "
                "fighting, the barricades, the last quarter. When Tenochtitlan's "
                "resistance collapses into Tlatelolco, the war is being run by men like "
                "this one."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Among the lords who surrender with Cuauhtémoc. What follows is not "
                "recorded, which is the ordinary fate of a name in these sources."}],
      [["Rank", "tlacatecatl"], ["City", "Tlatelolco"],
       ["Commands", "the northern defence, 1521"]]),

    P("temilotzin", "Temilotzin",
      "tlacatecatl and poet — a captain who left songs",
      (_t(1520, 7, 1), _t(1525, 3, 1)), "moderate",
      ["[FC]", "[AT]", "Cantares Mexicanos"],
      [{"from": T0, "to": _t(1520, 7, 1),
        "text": "A Tlatelolca lord and war captain of the generation that fought the "
                "siege, and one of the very few in this model who is attested twice "
                "over — once as a soldier in the annals, once as a voice in the "
                "surviving Nahuatl song collections."},
       {"from": _t(1520, 7, 1), "to": _t(1521, 8, 13),
        "text": "Fights through the siege in the Tlatelolca command and is named among "
                "the lords taken with Cuauhtémoc at the end."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Taken on the Honduras march with the other captive lords and dies on "
                "it, in 1525 — by one account throwing himself into the water rather "
                "than continue. A song attributed to him survives in the Cantares: 'I "
                "have come to make friends here,' it begins, and it is the only thing in "
                "this model that is a Mexica captain's own voice rather than a report of "
                "one."}],
      [["Rank", "tlacatecatl"], ["Attested in", "the annals and the Cantares"],
       ["Died", "1525, on the Honduras march"]],
      note="the attribution of the Cantares song is traditional rather than documentary"),

    P("martin-lopez", "Martín López",
      "shipwright — the man who built the thirteen brigantines",
      (_t(1519, 2, 1), _t(1530, 1, 1)), "good",
      ["[BD]", "[C3]", "his own probanza (1528-40)", "[TH]"],
      [{"from": T0, "to": _t(1519, 2, 1),
        "text": "A carpenter and shipwright out of Seville, in Cuba with the rest of the "
                "expedition's tradesmen — the sort of person a conquest depends on and a "
                "conquest narrative forgets."},
       {"from": _t(1519, 2, 1), "to": _t(1521, 8, 13),
        "text": "Builds the four brigantines used on the lake during the hostage year, "
                "loses them when the city rises, and then does the thing the siege turns "
                "on: cuts and frames thirteen more at Tlaxcala, 90 km away and 2,000 m "
                "up, to be carried in pieces over the sierra by thousands of Tlaxcalteca "
                "porters and assembled in a canal dug for the purpose. Without the "
                "brigantines the lake belongs to the canoe fleet and the causeways cannot "
                "be held."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Spends the next twenty years petitioning for reward, and the probanzas "
                "he filed are now among the better sources for how the fleet was "
                "actually built. He was paid badly, and complained in writing, which is "
                "why we know anything."}],
      [["Built", "4 brigantines 1520; 13 in 1521"],
       ["Carried", "in pieces from Tlaxcala, ~90 km"],
       ["Source", "his own reward petitions"]],
      note="the single most decisive piece of engineering in the war, done by a "
           "tradesman who had to sue to be noticed"),

    P("andres-tapia", "Andrés de Tapia",
      "captain, and one of the campaign's witnesses",
      (_t(1519, 2, 1), _t(1540, 1, 1)), "moderate",
      ["his Relación (c. 1539)", "[BD]", "[TH]"],
      [{"from": T0, "to": _t(1519, 2, 1),
        "text": "A young hidalgo who joins the expedition in Cuba and stays close to "
                "Cortés throughout — one of the inner group rather than the ranks."},
       {"from": _t(1519, 2, 1), "to": _t(1521, 8, 13),
        "text": "Present at Cholula, in the city through the hostage months, and in the "
                "siege. His short Relación is the source for some of the most-quoted "
                "and least-corroborated scenes of the war, including the count of skulls "
                "on the tzompantli — a number modern scholarship treats with great "
                "caution and which this model does not repeat as fact."},
       {"from": _t(1521, 8, 13), "to": T1,
        "text": "Serves in the later campaigns and writes his account around 1539, "
                "within the argument between Cortés's partisans and his critics. A "
                "witness, and a partisan, and the model reads him as both."}],
      [["Joins", "1519, Cuba"], ["Writes", "c. 1539"],
       ["Known for", "the tzompantli count — treated with caution"]]),

    P("motolinia", "Toribio de Benavente 'Motolinía'",
      "one of the Twelve — the first Franciscan mission",
      (_t(1524, 6, 1), T1), "good",
      ["his Historia de los indios (c. 1541)", "[TH]"],
      [{"from": T0, "to": _t(1524, 6, 1),
        "text": "In Spain. The religious conquest has not begun: the first three years "
                "after the fall are soldiers and encomenderos, not friars."},
       {"from": _t(1524, 6, 1), "to": _t(1541, 1, 1),
        "text": "Arrives with the Twelve in 1524 — a party that walked barefoot from the "
                "coast, which the Nahua noticed and named him for: motolinía, 'he is "
                "poor'. He takes the name and keeps it. Baptises on an industrial scale, "
                "founds houses across the centre and the west, and writes the earliest "
                "sustained account of what the conquest did to the people who survived "
                "it — including the plagues, which he counted."},
       {"from": _t(1541, 1, 1), "to": T1,
        "text": "Ends up publicly opposing Las Casas, arguing that the conquest was "
                "providential and the friars' work justified it. Two men who both "
                "recorded the catastrophe drew opposite conclusions from it, and this "
                "model carries both."}],
      [["Arrives", "1524, with the Twelve"],
       ["Named by", "the Nahua — 'he is poor'"], ["Writes", "c. 1541"]]),

    P("pedro-de-gante", "Pedro de Gante",
      "Franciscan lay brother — the school at San José",
      (_t(1523, 8, 1), T1), "good",
      ["[TH]", "his own letters"],
      [{"from": T0, "to": _t(1523, 8, 1),
        "text": "In Flanders. A lay brother, never ordained, and reportedly a relative "
                "of the emperor Charles V — which did not stop him spending the rest of "
                "his life in a school."},
       {"from": _t(1523, 8, 1), "to": T1,
        "text": "Arrives in 1523, a year ahead of the Twelve, and does the thing almost "
                "none of the others did: learns Nahuatl properly and teaches in it. The "
                "school he runs at San José de los Naturales trains Nahua boys in "
                "reading, writing, singing, painting and the trades, and its graduates "
                "are the scribes and artists who produce the codices, the catechisms and "
                "eventually the Florentine Codex's illustrations. The Nahua record of "
                "this war is written in an alphabet taught in his classroom."}],
      [["Arrives", "1523"], ["Teaches in", "Nahuatl"],
       ["School", "San José de los Naturales"],
       ["Died", "1572, Mexico City"]],
      note="the alphabetic Nahuatl that carries most of this model's indigenous "
           "sources is a product of this mission-school generation"),

    P("las-casas", "Bartolomé de las Casas",
      "bishop and prosecutor of the conquest",
      (_t(1502, 1, 1), T1), "good",
      ["Brevísima relación (1552)", "Historia de las Indias", "[TH]"],
      [{"from": T0, "to": _t(1514, 1, 1),
        "text": "In the Caribbean from 1502 as a settler and encomendero, holding "
                "labourers of his own on Hispaniola and Cuba — he begins on the side he "
                "spends the rest of his life prosecuting."},
       {"from": _t(1514, 1, 1), "to": _t(1542, 1, 1),
        "text": "Renounces his encomienda in 1514 and becomes the system's most "
                "relentless opponent: decades of petitioning, the Dominican habit, "
                "failed experiments in peaceful colonisation, and the case that drives "
                "the New Laws of 1542. His statistics are polemical and were attacked as "
                "such immediately; his central charge — that the encomienda was killing "
                "people at scale — was correct."},
       {"from": _t(1542, 1, 1), "to": T1,
        "text": "Bishop of Chiapas from 1544, where the colonists refuse him the "
                "sacraments' authority and he leaves. The Brevísima relación is printed "
                "in 1552, just past this model's window, and becomes both the conscience "
                "of the empire and the raw material of its rivals' propaganda."}],
      [["In the Indies", "from 1502"], ["Renounces encomienda", "1514"],
       ["Bishop of Chiapas", "1544"], ["Prints the Brevísima", "1552"]],
      note="his numbers are contested and his indictment is not — the model uses him "
           "for the charge, not for the arithmetic"),
]


def _selftest():
    slugs = [p["slug"] for p in PEOPLE]
    assert len(slugs) == len(set(slugs)), "duplicate people slugs"
    for p in PEOPLE:
        assert p["confidence"] in CONFIDENCE, p["slug"]
        assert p["sources"] and p["facts"], p["slug"]
        a0, a1 = p["active"]
        assert T0 <= a0 < a1 <= T1, f"{p['slug']}: bad active window"
        # eras tile [T0, T1] — the universal card contract
        eras = p["eras"]
        assert abs(eras[0]["from"] - T0) < 1e-6 and abs(eras[-1]["to"] - T1) < 1e-6, p["slug"]
        for a, b in zip(eras, eras[1:]):
            assert abs(a["to"] - b["from"]) < 1e-6, f"{p['slug']}: era gap"
        for e in eras:
            assert len(e["text"]) > 60, f"{p['slug']}: thin era"
        if p["confidence"] == "contested":
            assert p["accounts"] and len(p["accounts"]) >= 2, \
                f"{p['slug']}: contested person without accounts"
        for a in p["accounts"]:
            assert a["source"] and a["claim"] and a["note"], p["slug"]
    # the war's two sides and the aftermath are all represented
    roles = " ".join(p["role"] for p in PEOPLE)
    for needed in ("huey tlatoani", "Tlaxcallan", "interpreter", "bishop"):
        assert needed in roles, f"missing: {needed}"
    print(f"selftest OK — {len(PEOPLE)} people; "
          f"{sum(1 for p in PEOPLE if p['accounts'])} with accounts; eras tile {T0}-{T1}")


if __name__ == "__main__":
    _selftest()
    for p in PEOPLE:
        a0, a1 = p["active"]
        print(f"  {p['name']:44} active {a0:7.1f}-{a1:7.1f}  ({p['confidence']})")
