"""Emit the app's data artifacts from the research models. Stdlib only.

THE HANDOVER ARTIFACT GENERATOR (working rule 11): this writes complete,
drop-in replacements for `web/data/*.js` into

    Research/research reports/staged-artifacts/

and NOTHING into the app itself. /model-build copies them across deliberately,
in one pass, and records what landed. The audits (audit_cards.py,
audit_witness.py) read web/data/ if the handover has been executed, else the
staged copies — always the artifact the app will actually read, never a private
rebuild (TRAPS D5).

Everything here is DERIVED from the models — gazetteer, events, allegiance,
georef, forces, calendar — so a corrected date or coordinate propagates by
re-running:  python3 emit.py

The card generator: every polity card's era prose is generated from its
allegiance timeline through state templates, with curated openers for the
majors. Every era text is plain sentences with dates; every card carries
sources and confidence; contested cards carry accounts or an explanatory note
(audit-enforced, working rule 2.11).
"""

from __future__ import annotations

import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gazetteer
import events as events_mod
import allegiance
import georef
import forces
import epidemic
import siege
import people as people_mod
from calendar import (t_of_julian, julian_of_t, jdn_of_julian, fmt_julian,
                      gregorian_of_jdn, tonalpohualli, MONTHS)

T0, T1 = 1502.0, 1551.0
STAGED = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "research reports", "staged-artifacts")

# ---------------------------------------------------------------------------
# chapters — the timeline's table of contents (authored editorial layer)
# ---------------------------------------------------------------------------

def _t(y, m, d):
    return round(t_of_julian(y, m, d), 4)

CHAPTERS = [
    {"from": T0, "to": _t(1519, 4, 21), "name": "The Fifth Sun",
     "title": "The empire at its height — and its fracture lines",
     "text": "From 1502 Moctezuma II rules a Triple Alliance taking tribute from some 38 "
             "provinces — a network of obligations over local dynasts, not a bordered state. "
             "Inside it: recently conquered peoples with living memories of independence. "
             "Outside it: unconquered Tlaxcallan, blockaded and waiting. The map's colours "
             "are the fracture lines the war will follow."},
    {"from": _t(1519, 4, 21), "to": _t(1519, 11, 8), "name": "Landfall",
     "title": "The corridor: Cempoala, Tlaxcallan, Cholula",
     "text": "A private expedition of a few hundred, illegal from its first day, lands inside "
             "the tribute province of Cuetlaxtlan. What turns it into a war is not steel but "
             "politics: the Totonac tribute grievance, then — after two weeks of hard fighting — "
             "the Tlaxcala alliance. The column that climbs to the Basin in November is already "
             "mostly Nahua."},
    {"from": _t(1519, 11, 8), "to": _t(1520, 5, 22), "name": "The hostage regime",
     "title": "An empire ruled through a captive centre",
     "text": "Received as guests on 8 November, the Spaniards seize Moctezuma within the week "
             "and rule through him for six months. Tribute keeps flowing; the provinces watch; "
             "Texcoco's succession crisis deepens. The system's obedience to its centre is the "
             "weapon turned against it."},
    {"from": _t(1520, 5, 22), "to": _t(1520, 7, 1), "name": "Rupture",
     "title": "Tóxcatl, the rising, the Noche Triste",
     "text": "Alvarado's massacre of the Tóxcatl celebrants ends the hostage regime in blood. "
             "The city rises, Moctezuma dies in Spanish custody — by whose hand is disputed to "
             "this day — and on the night of 30 June the company is destroyed on the Tlacopan "
             "causeway. The coalition survives because Tlaxcallan chooses to keep it alive."},
    {"from": _t(1520, 7, 1), "to": _t(1520, 12, 31), "name": "The plague year",
     "title": "Smallpox, Tepeaca, and the war for the corridor",
     "text": "Smallpox, landed with the Narváez fleet, burns through a hemisphere with no "
             "immunity — killing, among uncounted others, the new huey tlatoani Cuitláhuac, "
             "on the defending side only. The coalition retakes the eastern road by terror. "
             "The epidemic is not scenery: it is a combatant, and the model draws its "
             "mortality as the wide band it honestly is."},
    {"from": _t(1520, 12, 31), "to": _t(1521, 5, 22), "name": "The ring closes",
     "title": "Texcoco changes sides; the lake is prepared",
     "text": "On the last day of 1520 the alliance's second capital passes to the coalition — "
             "Acolhua manpower, food, and a shipyard. Chalco follows, then the circuits: north "
             "around the lakes, south through Cuauhnáhuac and Xochimilco. Thirteen brigantines "
             "are carried overland in pieces and launched. The siege exists before it begins."},
    {"from": _t(1521, 5, 22), "to": _t(1521, 8, 13), "name": "The siege",
     "title": "Four arteries: causeways, aqueduct, lake, food",
     "text": "Three camps seal the causeways; the Chapultepec aqueduct is cut on day four; the "
             "brigantines break the canoe fleet and the island starves. Perhaps 900 Spaniards "
             "and — by every account including Cortés's own — tens of thousands of Nahua "
             "allies unmake the city street by street. It ends on 13 August, the day 1 Cóatl, "
             "with Cuauhtémoc taken on the water."},
    {"from": _t(1521, 8, 13), "to": _t(1524, 6, 1), "name": "The world remade",
     "title": "The conquest does not end at the fall",
     "text": "Mexico City rises on the razed grid; the provinces pass to the new regime — "
             "some by column, some by letter. Michoacán, never conquered by the Mexica, "
             "submits without a siege. The allies who won the war begin learning what they "
             "have won: encomienda, tribute reassessed, and lords hanged on suspicion."},
    {"from": _t(1524, 6, 1), "to": _t(1535, 11, 14), "name": "Conquistador New Spain",
     "title": "Friars, encomenderos, and wars that do not stop",
     "text": "The Twelve arrive barefoot to replace a sacred order; Cuauhtémoc is hanged on "
             "the Honduras march; Guzmán burns the Purépecha cazonci and devastates the west. "
             "Native New Spain fights on both sides of every colonial war — the conquest "
             "continues under legal forms."},
    {"from": _t(1535, 11, 14), "to": T1, "name": "Viceroyalty",
     "title": "Bureaucratic empire and the vanishing lake",
     "text": "Royal government arrives with Mendoza; the Mixtón war is put down with tens of "
             "thousands of Nahua troops; the cocoliztli of 1545-48 kills on a scale that "
             "dwarfs the siege. By 1550 the survivors are being gathered into planned towns "
             "and the lakes are shrinking — the world this model opened with is gone."},
]

# ---------------------------------------------------------------------------
# the card generator
# ---------------------------------------------------------------------------

KIND_LABEL = {"triple-alliance-core": "Triple Alliance seat",
              "tributary": "Tributary altepetl",
              "independent": "Independent polity",
              "rival-state": "Rival empire",
              "spanish-foundation": "Spanish foundation"}

STATE_COLOR = {"alliance-core": "#a83232", "tributary": "#c96f4a",
               "independent": "#7d5fb2", "rival": "#8a6d3b",
               "contested": "#d9a441", "allied-coalition": "#3f8f6b",
               "occupied": "#5a7d9a", "colonial-ally": "#4a9a8f",
               "new-spain": "#8a8f98", "spanish": "#6b7fa8"}

# Curated openers the generator must never speak over (working rule: curated tier).
CURATED_OPENER = {
    "tenochtitlan": "Island capital of the Mexica and seat of the huey tlatoani: canals, "
        "causeways, the twin temple over the sacred precinct, and a market system feeding "
        "perhaps 50,000-200,000 people — the population itself is contested. Tribute from "
        "38 provinces converges here.",
    "tlatelolco": "Tenochtitlan's twin on the same island, self-governing until 1473, home "
        "of the great market the Spaniards thought larger than Seville's. Its people's "
        "testimony, taken a generation later, becomes Book XII — this war's Nahua voice.",
    "texcoco": "Second seat of the Triple Alliance and the Acolhua capital, famed for law "
        "and works of engineering. Its succession splits in 1515 — and that split, not any "
        "Spanish sword, is what will deliver its manpower to the siege.",
    "tlacopan": "The alliance's third, junior seat, heir of the Tepanec world the Mexica "
        "broke in 1428. The war's worst night happens on its causeway.",
    "tlaxcala": "A confederation of four altepetl that the empire never conquered — ringed, "
        "blockaded and salt-starved instead. Its choice in September 1519 to use the "
        "strangers rather than destroy them is the hinge of the entire war.",
    "cholula": "The holy city of Quetzalcóatl, pilgrimage centre of the highlands, "
        "independent but aligned toward Tenochtitlan by 1519 — and about to become the "
        "war's most disputed atrocity.",
    "huexotzinco": "Independent altepetl between the volcanoes, Tlaxcallan's sometime ally "
        "and rival, ground down by flower-war against the Mexica; it joins the coalition "
        "in its first season.",
    "cempoala": "The Totonac city where the coalition begins: its lord's tribute grievance, "
        "aired to strangers in 1519, is the first thread pulled from the imperial web.",
    "chalco": "Conquered by the Mexica in 1465 after a generation of war and worked hard "
        "under tribute since, the Chalca confederation is the Basin's granary — and its "
        "memory of independence is one year older than its conquerors think.",
    "xochimilco": "The chinampa heartland: raised-field agriculture on the freshwater lake, "
        "feeding the island capital it serves under tribute.",
    "tzintzuntzan": "Capital of the Purépecha state — the other empire, which broke "
        "Axayácatl's invasion in the 1470s and holds the west with bronze and bowmen. It "
        "watches the Mexica die of siege and plague, and draws its own conclusion.",
    "quauhnahuac": "Head of the cotton-rich warm lands over the sierra, tributary since "
        "Itzcóatl's day; its cloth clothes the capital.",
    "metztitlan": "An independent valley kingdom the empire ringed but never took — a "
        "standing proof, one valley wide, that the tributary web had holes.",
    "villa-rica": "The first Spanish municipality in Mexico — founded chiefly so that its "
        "own cabildo could commission Cortés and cut the legal cord to Cuba. A device of "
        "law, built of palm and sand.",
}

_EVENT_NAME = {e["id"]: e["name"] for e in events_mod.EVENTS}
_EVENT_T = {e["id"]: e["t"] for e in events_mod.EVENTS}


def _fmt_t(t):
    y, m, d = julian_of_t(t)
    return f"{d} {MONTHS[m-1]} {y}"


def _entered_phrase(entered):
    y, ruler, manner = entered
    return f"c. {y} under {ruler} ({manner})"


def _state_text(e, state, since, cause, conf):
    """One era's prose, from the state templates."""
    n = e["nahuatl"] if e["nahuatl"] != "—" else e["exonym"]
    role = e["role"]
    if state == "tributary":
        s = (f"{n} stands inside the Triple Alliance's tribute web — {role}. It renders "
             f"goods and service through the province of {e['province']}, having entered the "
             f"system {_entered_phrase(e['entered'])}.")
        if e["note"]:
            s += f" {e['note'].capitalize()}."
        return s
    if state == "alliance-core":
        return CURATED_OPENER.get(e["slug"], f"{n} is a seat of the Triple Alliance.")
    if state == "independent":
        s = f"{n} stands outside the tribute system — {role}."
        if e["note"]:
            s += f" {e['note'].capitalize()}."
        return s
    if state == "rival":
        return CURATED_OPENER.get(e["slug"], f"{n} heads a rival state outside the empire.")
    if state == "contested":
        return (f"{n} is in play: {_EVENT_NAME.get(cause, 'events')} "
                f"({_fmt_t(since)}) has put its allegiance in question. The sources for "
                f"exactly who held it, week by week, thin out here — the map says "
                f"'contested' rather than invent a holder.")
    if state == "allied-coalition":
        return (f"{n} fights with the coalition against Tenochtitlan, from "
                f"{_fmt_t(since)} ({_EVENT_NAME.get(cause, cause)}). Its warriors, porters "
                f"and food are part of the host the Spanish accounts undercount.")
    if state == "occupied":
        return (f"{n} is under coalition military control from {_fmt_t(since)} "
                f"({_EVENT_NAME.get(cause, cause)}).")
    if state == "colonial-ally":
        return ("Tlaxcallan enters the colonial order as a privileged ally of the crown — "
                "exempt from encomienda, governing itself under its own cabildo, its "
                "service in the war the basis of petitions for generations. The privilege "
                "is real, and so is the asymmetry it decorates.")
    if state == "new-spain":
        s = (f"{n} is absorbed into colonial New Spain: encomienda or crown tribute, "
             f"the missions, and epidemic loss remake it.")
        if cause == "consolidation-modelled":
            s += (" (The transition date is a modelled consolidation default, not an "
                  "attested act — the record for this polity's absorption is thin.)")
        return s
    if state == "spanish":
        return CURATED_OPENER.get(e["slug"], f"{n} is a Spanish foundation.")
    raise ValueError(state)


def build_entities():
    ents = []
    for e in gazetteer.ENTRIES:
        slug = e["slug"]
        tline = allegiance.TIMELINES[slug]
        t_from = tline[0][0]
        name = e["nahuatl"] if e["nahuatl"] != "—" else e["exonym"]
        if e["nahuatl"] != "—" and e["exonym"] and e["exonym"] != e["nahuatl"]:
            name = f"{e['nahuatl']} ({e['exonym']})"
        eras = []
        for i, (t, s, cause, cf) in enumerate(tline):
            t_end = tline[i + 1][0] if i + 1 < len(tline) else T1
            opener = (CURATED_OPENER.get(slug) if i == 0 and slug in CURATED_OPENER
                      else None)
            text = opener or _state_text(e, s, t, cause, cf)
            if opener and s not in ("alliance-core", "rival", "spanish", "independent"):
                # curated opener still needs the standing sentence
                text += " " + _state_text(e, s, t, cause, cf)
            eras.append({"from": round(t, 4), "to": round(t_end, 4), "text": text})
        facts = [["Standing in 1519", KIND_LABEL[e["group"]]]]
        if e["province"]:
            facts.append(["Tribute province", e["province"]])
        if e["entered"]:
            facts.append(["Entered tribute system", _entered_phrase(e["entered"])])
        if e.get("goods"):
            facts.append(["Principal tribute [CM]", e["goods"]])
        facts.append(["Modern", e["modern"]])
        conf = "contested" if e["coord_conf"] == "contested" else e["entry_conf"]
        note = e["note"]
        if e["coord_conf"] == "contested" and "approximate" not in (note or "").lower() \
           and "debated" not in (note or "").lower():
            note = (note + " " if note else "") + "Location approximate."
        epi = epidemic.windows().get(slug)
        ents.append({
            "id": slug, "name": name, "kind": KIND_LABEL[e["group"]],
            "layer": "altepetl", "lon": e["lon"], "lat": e["lat"],
            "from": round(t_from, 4), "to": None,
            "confidence": conf, "note": note or "",
            "facts": facts, "eras": eras,
            "allegiance": allegiance.series(slug),
            "epidemic": [epi[0], epi[1]] if epi else None,
            "sources": e["sources"],
        })

    # features: the works, as clickable entities
    FEATURE_CARDS = {
        "causeway-tlacopan": ("Causeway", "The Tlacopan causeway",
            "The western artery: the shortest causeway, the Noche Triste's escape route, "
            "and Alvarado's siege station. Modern Calzada México-Tacuba follows it."),
        "causeway-iztapalapa": ("Causeway", "The Iztapalapan causeway",
            "The great southern entrance with the fort of Xoloc at its fork — the road "
            "Cortés entered by on 8 November 1519 and assaulted along in 1521."),
        "causeway-tepeyac": ("Causeway", "The Tepeyacac causeway",
            "The northern artery, left open longest during the siege as a tempting exit; "
            "Sandoval closed it. Modern Calzada de los Misterios follows it."),
        "causeway-coyoacan": ("Causeway", "The Coyohuacan branch",
            "The southwestern branch joining the Iztapalapan causeway at Xoloc; Olid's "
            "siege approach."),
        "aqueduct-chapultepec": ("Aqueduct", "The Chapultepec aqueduct",
            "Twin terracotta channels from the Chapultepec springs — the island's fresh "
            "water. Cut on 26 May 1521, the siege's first and most decisive act."),
        "dike-nezahualcoyotl": ("Dike", "The albarradón of Nezahualcóyotl",
            "The 16-km dike of c. 1449 that held the saline lake off the chinampa west. "
            "Its exact course is debated; the drawn line follows González Aparicio (1973)."),
        "city-footprint": ("City", "The island city",
            "Tenochtitlan-Tlatelolco at its 1519 extent — roughly 13 km² of urban island, "
            "drawn after González Aparicio (1973) and Calnek."),
    }
    for gid, (kind, name, text) in FEATURE_CARDS.items():
        g = georef.GEOMETRY[gid]
        lons = [p[0] for p in g["points"]]; lats = [p[1] for p in g["points"]]
        ents.append({
            "id": gid, "name": name, "kind": kind, "layer": "works",
            "lon": sum(lons) / len(lons), "lat": sum(lats) / len(lats),
            "from": T0, "to": None,
            "confidence": g["confidence"], "note": g["note"],
            "facts": [["Kind", kind], ["Source", g["source"]]],
            "eras": [{"from": T0, "to": T1, "text": text + " Drawn at visualization "
                      "grade against the named reconstruction — faithful for the map, "
                      "not survey-grade."}],
            "sources": [g["source"]],
        })

    # the city model's cards (round 4) — phase-aware: the same place, read in
    # 1519 and in 1540, tells the before and the after
    _fall = t_of_julian(1521, 8, 13)
    _col = t_of_julian(1522, 1, 15)
    CITY_CARDS = [
        ("city-sacred-precinct", "The sacred precinct", "Precinct", 19.4346, -99.1313,
         "moderate", "Templo Mayor excavations; Calnek; the 1524 map",
         [{"from": T0, "to": _fall,
           "text": "The walled ceremonial heart: the twin-shrined great temple, the "
                   "calmecac schools, the skull rack, the ballcourt — some seventy-eight "
                   "structures by the fullest count, serving as the empire's ritual "
                   "centre. Tóxcatl's massacre happens in this courtyard."},
          {"from": _fall, "to": T1,
           "text": "Razed after the fall; its stones go into the colonial city and the "
                   "first cathedral rises at its southern edge. The Templo Mayor's "
                   "platforms sleep under the plaza until 1978."}]),
        ("city-palace-axayacatl", "The palace of Axayácatl", "Palace", 19.4347, -99.1340,
         "moderate", "Calnek; [C2][BD] — the company's quarters",
         [{"from": T0, "to": _fall,
           "text": "The old ruler's palace west of the precinct: the Spaniards' "
                   "quarters from November 1519, Moctezuma's prison, the treasure "
                   "chamber's site, and the fortress of the palace siege of June 1520."},
          {"from": _fall, "to": T1,
           "text": "Ruined in the war; the block passes into the colonial city's fabric."}]),
        ("city-palace-moctezuma", "The new palaces of Moctezuma", "Palace", 19.4327, -99.1286,
         "moderate", "Calnek; the sources' 'casas nuevas'",
         [{"from": T0, "to": _fall,
           "text": "Moctezuma's own compound southeast of the precinct — audience "
                   "halls, aviaries, gardens the soldiers struggled to describe."},
          {"from": _fall, "to": T1,
           "text": "Its site becomes the seat of New Spain's government — the "
                   "viceregal palace stands on the tlatoani's ground."}]),
        ("city-tlatelolco-market", "The great market of Tlatelōlco", "Market", 19.4505, -99.1353,
         "moderate", "[C2][BD] descriptions; Calnek",
         [{"from": T0, "to": _fall,
           "text": "The tianquiztli that stunned the Spaniards: tens of thousands "
                   "trading daily under the market court's supervision — the economic "
                   "engine of the lake world, and the war's final pocket."},
          {"from": _fall, "to": T1,
           "text": "The market quarter is the last ground to fall; trade returns "
                   "under the colony but the great court does not."}]),
        ("city-campan", "The four campan", "City quarters", 19.4300, -99.1310,
         "moderate", "Calnek; the axes fossilised in the colonial grid",
         [{"from": T0, "to": T1,
           "text": "The causeway axes quartered the island: Cuepopan (NW), Atzacoalco "
                   "(NE), Moyotlan (SW), Teopan (SE), with Tlatelōlco to the north — "
                   "each with its own temples, schools and barrio structure. The "
                   "colonial parcialidades reused the same divisions, which is how the "
                   "modern streets still remember them."}]),
        ("city-chinampas", "The island's chinampa skirts", "Chinampas", 19.4220, -99.1300,
         "moderate", "Calnek (1972)",
         [{"from": T0, "to": _fall,
           "text": "Raised-field ribbons fringing the island's south and west: the "
                   "city's kitchen gardens, threaded by canals, worked from canoes."},
          {"from": _fall, "to": T1,
           "text": "War-torn and then slowly rebuilt; the chinampa economy persists "
                   "at Xochimilco far longer than at the capital's own edge."}]),
        ("city-traza", "The traza", "Colonial city", 19.4340, -99.1310,
         "good", "the 1522+ grid; [GIB]",
         [{"from": T0, "to": _col,
           "text": "Not yet: until the fall this ground is the Mexica centre itself."},
          {"from": _col, "to": T1,
           "text": "The Spanish city's chequerboard, laid on the Mexica axes with "
                   "native labour and temple stone: thirteen blocks a side for the "
                   "conquerors, the surviving Mexica moved to the parcialidades at "
                   "the edges. The plaza mayor sits beside the razed precinct."}]),
        ("city-san-francisco", "San Francisco", "Church", 19.4339, -99.1391,
         "moderate", "founded 1524; [GIB]",
         [{"from": T0, "to": t_of_julian(1524, 6, 1),
           "text": "Not yet: the site holds Moctezuma's aviary until the war."},
          {"from": t_of_julian(1524, 6, 1), "to": T1,
           "text": "The Franciscans' mother church, founded 1524 on the aviary's "
                   "site — the spiritual conquest's headquarters, school and stage."}]),
    ]
    for cid, name, kind, lat, lon, conf, src, eras in CITY_CARDS:
        ents.append({
            "id": cid, "name": name, "kind": kind, "layer": "city",
            "lon": lon, "lat": lat, "from": T0, "to": None,
            "confidence": conf, "note": "drawn at visualization grade from the city "
                                        "model — see the About panel",
            "facts": [["Kind", kind], ["Source", src]],
            "eras": eras, "sources": [src, "Calnek (1972, 1976); González Aparicio (1973)"],
        })

    # people — cards, not map dots (they move); the People panel lists whoever
    # is active at t, and the eras tile to T1 so a card read in 1540 says what
    # became of them
    for p in people_mod.PEOPLE:
        ents.append({
            "id": "person-" + p["slug"], "name": p["name"], "kind": "Person",
            "layer": "people", "lon": None, "lat": None,
            "from": T0, "to": None,
            "confidence": p["confidence"], "note": p["note"],
            "facts": [["Role", p["role"]]] + p["facts"],
            "eras": p["eras"], "accounts": p["accounts"],
            "active": [round(p["active"][0], 4), round(p["active"][1], 4)],
            "sources": p["sources"],
        })
    return ents


def build_events_js():
    evs = []
    for e in events_mod.EVENTS:
        # a placement override (round 4) wins over the place slug's centroid —
        # the slug keeps the semantic link, the placement carries the position
        if e["latlon"]:
            lat, lon = e["latlon"]
        else:
            g = gazetteer.BY_SLUG[e["place"]]
            lon, lat = g["lon"], g["lat"]
        y, m, d = e["julian"]
        jdn = e["jdn"]
        gy, gm, gd = gregorian_of_jdn(jdn)
        prec_mark = {"day": "", "month": " (month approximate)",
                     "year": " (year-level date)"}[e["precision"]]
        date_facts = [["Date (Julian)", f"{d} {MONTHS[m-1]} {y}{prec_mark}"],
                      ["Gregorian", f"{gd} {MONTHS[gm-1]} {gy}"]]
        if e["precision"] == "day":
            num, sign = tonalpohualli(jdn)
            date_facts.append(["Nahua day (correlation)",
                               f"{num} {sign} — a correlation, not an attestation"])
        evs.append({
            "id": e["id"], "t": round(e["t"], 4), "name": e["name"],
            "kind": e["kind"], "precision": e["precision"],
            "lon": lon, "lat": lat,
            "confidence": e["confidence"],
            "facts": date_facts,
            "text": e["text"], "accounts": e["accounts"],
            "sources": e["sources"], "track": e["track"],
            # B2-b: where the claim actually lives in the work, when it is
            # locatable to a chapter/book/folio. Absent means the date comes
            # from the modern chronologies synthesising several accounts, and
            # there is no single passage to point at — not that it was missed.
            "pins": e.get("pins") or None,
        })
    return evs


# Card images (round 3): every entry verified visually against its subject
# (figures/collected/MANIFEST.json carries the review); all public domain,
# served downscaled from web/img/cards/. Credits render on every card that
# uses one — an image without its credit is an audit failure.
_C = "public domain, via Wikimedia Commons"
IMAGES = {
    "toxcatl": {"src": "img/cards/toxcatl.jpg",
                "caption": "The Tóxcatl massacre in the walled precinct: the drum, the "
                           "dancers, and Alvarado's men in the gateways",
                "credit": f"16th-c. codex image, {_C}"},
    "siege-painting": {"src": "img/cards/siege-painting.jpg",
                       "caption": "The assault on the causeway and the temple — painted "
                                  "c. 1696, 175 years after the event and from the "
                                  "victors' side",
                       "credit": f"'Conquista de México' series, {_C}"},
    "malintzin": {"src": "img/cards/malintzin.jpg",
                  "caption": "Durán Codex, 1576: Malintzin stands between the ship and "
                             "the Spanish party, labelled 'marina' beside 'marques' — "
                             "the interpreter drawn as the centre of the exchange",
                  "credit": f"Durán, Historia de las Indias, {_C}"},
    "cuauhtemoc": {"src": "img/cards/cuauhtemoc.jpg",
                   "caption": "The capture of Cuauhtémoc on the lake, 13 August 1521 — "
                              "the event that ends the siege, not a portrait of the man; "
                              "no likeness from life survives",
                   "credit": f"'Conquista de México' series, c. 1696, {_C}"},
    "ring-closes": {"src": "img/cards/ring-closes.jpg",
                    "caption": "The ring closing on the island: the causeway camps and "
                               "the brigantines, in a late-17th-c. retelling",
                    "credit": f"'Conquista de México' series, {_C}"},
    "fc-siege": {"src": "img/cards/fc-siege.jpg",
                 "caption": "Book XII, fol. 67v: captured Spaniards and their allies "
                            "sacrificed at Colhuacatonco during the siege — the war "
                            "drawn by the Nahua artists who survived it",
                 "credit": f"Florentine Codex, {_C}"},
    "map-1524": {"src": "img/cards/map-1524.jpg",
                 "caption": "The 1524 Nuremberg woodcut: Tenochtitlan as Europe first saw it "
                            "— schematic (best-fit residual 2.2 km), west at top",
                 "credit": f"Newberry Library scan, {_C}"},
    "mendoza-founding": {"src": "img/cards/mendoza-founding.jpg",
                         "caption": "Codex Mendoza fol. 2r: the eagle on the nopal — the founding "
                                    "of Tenochtitlan, painted by Nahua scribes c. 1541",
                         "credit": f"Bodleian Library MS. Arch. Selden. A. 1, {_C}"},
    "mendoza-tribute": {"src": "img/cards/mendoza-tribute.jpg",
                        "caption": "A Codex Mendoza tribute folio: town glyphs and their "
                                   "semi-annual dues in cloth, feathers and stone",
                        "credit": f"Bodleian Library, {_C}"},
    "fc-smallpox": {"src": "img/cards/fc-smallpox.jpg",
                    "caption": "Book XII: a healer tends smallpox victims, drawn by Nahua "
                               "artists who lived the epidemic's aftermath",
                    "credit": f"Florentine Codex, Biblioteca Medicea Laurenziana, {_C}"},
    "lienzo-meeting": {"src": "img/cards/lienzo-meeting.jpg",
                       "caption": "The Lienzo de Tlaxcala: Cortés and the lords of Tlaxcallan "
                                  "— Malintzin interpreting at the centre",
                       "credit": f"Lienzo de Tlaxcala (c. 1552), {_C}"},
    "lienzo-cholula": {"src": "img/cards/lienzo-cholula.jpg",
                       "caption": "The Lienzo de Tlaxcala's Cholula plate — the massacre as the "
                                  "coalition's own artists recorded it",
                       "credit": f"Lienzo de Tlaxcala (c. 1552), {_C}"},
    "noche-triste": {"src": "img/cards/noche-triste.jpg",
                     "caption": "The Sad Night, from the 17th-century Conquest of Mexico "
                                "series: the causeway fight under a crescent moon",
                     "credit": f"17th-c. oil, Library of Congress (Kislak), {_C}"},
    "uppsala-map": {"src": "img/cards/uppsala-map.jpg",
                    "caption": "The Uppsala map, c. 1550: Mexico City drawn by Nahua hands a "
                               "generation after the fall — the world this model ends in",
                    "credit": f"Mapa Uppsala (c. 1550), {_C}"},
    "moctezuma": {"src": "img/cards/moctezuma.jpg",
                  "caption": "Moctezuma II as the 17th century imagined him — a portrait of "
                             "memory, not of life",
                  "credit": f"attr. school of Antonio Rodríguez, {_C}"},
    "cortes": {"src": "img/cards/cortes.jpg",
               "caption": "Cortés in a copy portrait inscribed 1525 — the commander as his "
                          "own century painted him",
               "credit": f"anonymous copy portrait, {_C}"},
}

# where each image goes: chapters by name, events/people/works by id
CHAPTER_IMAGE = {"The Fifth Sun": "mendoza-founding", "Landfall": "lienzo-meeting",
                 "The hostage regime": "moctezuma", "Rupture": "noche-triste",
                 "The plague year": "fc-smallpox", "The siege": "map-1524",
                 "The world remade": "mendoza-tribute",
                 "Conquistador New Spain": "cortes", "Viceroyalty": "uppsala-map",
                 "The ring closes": "ring-closes"}
ENTITY_IMAGE = {"cholula-massacre": "lienzo-cholula", "tlaxcala-alliance": "lienzo-meeting",
                "entry-tenochtitlan": "moctezuma", "moctezuma-dies": "moctezuma",
                "noche-triste": "noche-triste", "smallpox-basin": "fc-smallpox",
                "fall-tenochtitlan": "map-1524", "codex-mendoza-made": "mendoza-tribute",
                "congregacion-1550": "uppsala-map",
                "person-moctezuma-ii": "moctezuma", "person-cortes": "cortes",
                "person-malintzin": "malintzin", "city-footprint": "map-1524",
                "toxcatl": "toxcatl", "person-cuauhtemoc": "cuauhtemoc",
                "siege-camps": "siege-painting", "tlatelolco-ambush": "fc-siege"}

# In-app update log — written for a reader, not a changelog: the effect first,
# the number as evidence. Rendered in the About panel.
UPDATES = [
    {"version": "2.6", "date": "30 July 2026",
     "title": "Where each claim actually comes from",
     "summary": "The events of the dated spine now show you the passage, not "
                "just the book — Bernal Díaz by chapter, the Florentine Codex "
                "by book and chapter, Cortés by letter. And zooming between "
                "map levels no longer softens the landscape on the way.",
     "items": [
         "Fifty-three citations pinned across the twenty-five events the war's "
         "chronology rests on. Open the Noche Triste and the sources line now "
         "reads: Cortés, Second Letter, the retreat from the city · Bernal Díaz "
         "cap. 128 · Florentine Codex Bk XII, ch. 24 · Anales de Tlatelolco f. 36.",
         "Deliberately not page numbers. A page belongs to one printing, and "
         "this model does not have those printings in hand — a page number here "
         "would look checkable while being unverifiable, which is worse than "
         "naming the book. Chapters and folios are carried by the works "
         "themselves and survive every edition.",
         "A source shown without a passage is not an omission. It means the "
         "date comes from modern chronologies reconciling several accounts, and "
         "there is no single place to point at.",
         "Zooming between map levels used to soften the terrain briefly: two "
         "renderings of the same mountains were being averaged half-and-half "
         "on the way through. The fade now crosses that point about four times "
         "faster, so the landscape holds its detail while the camera moves.",
     ]},
    {"version": "2.5", "date": "30 July 2026",
     "title": "Forty people, and the pictures that were missing",
     "summary": "The cast now runs from 1502 rather than starting at the "
                "landing, and reaches past the principals to the people who "
                "actually did the work. Six illustrations that earlier rounds "
                "had failed to find are in — including the one chapter that "
                "had never had a picture.",
     "items": [
         "Ten more people, to forty. The model opened in 1502 with almost "
         "nobody alive in it; Nezahualpilli now holds the first thirteen years, "
         "and the Texcoco succession crisis his death opens is the fracture the "
         "whole war later walks through.",
         "Martín López, the shipwright, has a card. He cut thirteen brigantines "
         "at Tlaxcala, ninety kilometres away and two thousand metres up, to be "
         "carried over the sierra in pieces — the single most decisive piece of "
         "engineering in the war, done by a tradesman who then had to petition "
         "for twenty years to be paid.",
         "Teuhtlilli, who met the landing party with food, gifts and painters, "
         "so a drawing of the ships was on the road to the capital within a "
         "week. The empire's first act was to commission a picture.",
         "Six images that previous rounds recorded as failures are in: the "
         "Tóxcatl massacre, the siege, Malintzin interpreting in the Durán "
         "Codex, Cuauhtémoc's capture on the water, a Book XII war plate, and "
         "the ring-closes chapter, which had never had one. All sixteen "
         "pictures in the model are now licence-checked and eye-checked, and "
         "each is pinned to an exact source file rather than to a search.",
         "Cuauhtémoc's card shows his capture, not his face. No likeness of him "
         "from life survives, and the caption says so.",
     ]},
    {"version": "2.4", "date": "30 July 2026",
     "title": "The chinampas, and a war that could go backwards",
     "summary": "The southern lakes get the thing they existed for: four "
                "districts of raised fields, drawn where the lake was shallow "
                "enough to build in. And the allegiance model stops pretending "
                "the war ran one way — Chalco changes sides, gets taken back, "
                "and is taken again.",
     "items": [
         "The chinampa districts of Xochimilco, Cuitláhuac, Mízquic and Chalco. "
         "Their extents are not drawn by hand — each is the lake's own shoreline "
         "over a named stretch, pushed inward by a stated width and stopped at "
         "the far shore where the lake is too narrow. Zoom in and the individual "
         "plots resolve, standing out of their ditch water with the willow rows "
         "that held their edges together.",
         "They come to about 46 km² against roughly 120 km² for the real system. "
         "The difference is this model's simplified lake, not a claim that the "
         "chinampería was smaller — and widening the districts alone to match the "
         "literature would have put fields in open water to make a total look right.",
         "Allegiance can now run backwards. Excluding the Mexica counter-offensive "
         "had quietly made every defection permanent and made holding ground free; "
         "Chalco now goes tributary, coalition, contested, coalition. The event for "
         "the Mexica counter-attack had been on the map since round 2 with nothing "
         "attached to it.",
         "Twelve more people, chosen to correct the cast: the other two Triple "
         "Alliance seats, the chief minister who administered the empire and then "
         "its conquest, Tlatelolco's governor, one ordinary soldier who is named "
         "only because his own city's elders insisted, and the witnesses whose "
         "books every other card here cites.",
         "Seven frontier provinces of the tribute roll that had been left out are "
         "now in, each marked as a province we can name and a town we cannot place.",
         "The lake's surface no longer carries the pale streaks reported last "
         "round; the light on the water is softer and reads as depth.",
     ]},
    {"version": "2.3", "date": "28 July 2026",
     "title": "The city, built",
     "summary": "Tenochtitlan is no longer an outline with dots on it. Zoom in and the "
                "island has its fabric: blocks of courtyard compounds under lime and "
                "thatch, canals and streets with width, chinampa strips, jetties where "
                "the city meets its lake, the walled precinct with its stepped pyramid — "
                "and every other altepetl has a town of its own, on its own plan.",
     "items": [
         "The dense world moved to a canvas layer under the map, which is what makes "
         "thousands of buildings per frame affordable; everything you can click stays "
         "in the layer above it.",
         "Blocks have grain: each shares an orientation off the canal line and a "
         "roofing material, with lordly four-wing compounds near the precinct, garden "
         "blocks, and tight commoner wards toward the water — Calnek's finding that "
         "lot sizes varied by an order of magnitude, made visible.",
         "The sacred precincts are architecture: a walled, paved court with gates on "
         "the causeway axes, the great temple as five terraces with twin stairways and "
         "the shrines of Tlaloc and Huitzilopochtli, the round temple of Ehecatl, the "
         "ballcourt, the tzompantli, and the calmecac ranges along the walls.",
         "Towns differ from each other: dispersed wards for Tlaxcallan's four "
         "cabeceras, compact plaza towns on the roads, linear towns along the "
         "lakeshore — and Cholula carries the Tlachihualtepetl, the greatest pyramid "
         "by volume in the Americas, grassed over already in 1519.",
         "The siege is legible on the ground: the causeway breaches the defenders cut "
         "and the attackers spent the siege filling, the arteries reddening as each is "
         "severed, the island charring south to north under its smoke, and the market "
         "crowd thinning to nothing.",
         "After 1522 the same ground rebuilds as the traza — red-tiled courtyard "
         "blocks around their patios, the plaza and cathedral on the razed precinct — "
         "while the Mexica parcialidades keep their old fabric at the edges.",
         "Landscape detail is GROWN from the measured terrain rather than invented: "
         "the elevation data is 30 m and the screen asks for one, so woodland clusters "
         "where the ground is darker than its neighbourhood, with field terraces on "
         "worked land and grain over everything.",
     ]},
    {"version": "2.2", "date": "27 July 2026",
     "title": "Uniform ground, and the world peopled",
     "summary": "The whole war theatre now carries the same sharp terrain — a new "
                "corridor render from Veracruz to the Basin ends the blur beyond the "
                "valley — and the model gains its figure scale: files of soldiers on "
                "the march, skirmishes you can watch, canoes on the lake, porters on "
                "the tribute roads, the exodus after the fall, and the island's own "
                "house fabric at street zoom. All of it impression, and labelled so.",
     "items": [
         "A z11 terrain level covers the corridor Veracruz-Tlaxcallan-Basin-Morelos, "
         "and the base map doubles to its data's native grain — the seam a reader "
         "rightly photographed east of the Basin is gone.",
         "At street zoom Tenochtitlan fills with its houses — densest toward the "
         "precinct, charring south-to-north during the razing, rebuilt as orthogonal "
         "traza blocks after 1522 — with trees on the chinampa gardens.",
         "The column marches as a file: a steel-grey Spanish file and the far longer "
         "tan allied file behind it, lengths scaled to the model's own force bands.",
         "Battles play as scenes: defenders ring the ground, attackers close on it "
         "through the event's window; massacres close a ring instead. Deterministic "
         "in t — scrub back and the same scene replays.",
         "The lake lives: canoe traffic runs between the shore towns and the island "
         "until the day the brigantines break the fleet, waterfowl drift indifferent, "
         "porters walk the tribute arcs while their towns still owe, and for six "
         "weeks after the fall the causeways carry the grey file of the exodus.",
         "Every figure-scale element is a seeded procedural impression rooted in the "
         "accounts — counts from the force bands, nothing at figure scale an "
         "attestation — stated in About and on the layer's own name.",
     ]},
    {"version": "2.1", "date": "27 July 2026",
     "title": "The city itself, and the war in motion",
     "summary": "Tenochtitlan stops being an outline: precincts, palaces, the canal "
                "fabric, the chinampa skirts and the four campan, phased across the "
                "timeline — intact, besieged and burning, ruined, then colonial. The "
                "terrain sharpens to its data's native grain, and events stop being "
                "identical diamonds: the column marches, battles pulse, the epidemic "
                "front expands, the arteries redden as they are cut.",
     "items": [
         "The city model (drawn from Calnek, the excavations and the street fossils "
         "of the modern Centro): sacred precincts, the palaces of Axayácatl and "
         "Moctezuma, the great market, schematic canals — dashed because schematic — "
         "chinampa fringes, then the colonial traza and its churches after 1522. Every "
         "element is a card; the same place reads differently in 1519 and 1540.",
         "City events sit where they happened: the meeting at Xoloc on the causeway, "
         "the seizure in Axayácatl's palace, Tóxcatl in the precinct courtyard, the "
         "last stand in Tlatelolco's market — and labels stack instead of "
         "overprinting, so the plague year's crowded weeks read cleanly.",
         "The war moves: the column is drawn in transit between its dated waypoints; "
         "battles and massacres pulse rings for days after their date; the arteries "
         "turn crimson as each is cut; brigantines hold the lake; smoke stands over "
         "the razing; the epidemic's modelled front expands from the coast.",
         "Terrain at native grain (z9/z12) with curvature-shaded ravines and rock on "
         "steep ground — and a rendering lesson kept honest: the first city render "
         "amplified upsampling noise into a checkerboard, was caught visually, and "
         "the curvature now fades below the data's 30 m grain.",
     ]},
    {"version": "2.0", "date": "27 July 2026",
     "title": "A living landscape, a continuous camera, and the record illustrated",
     "summary": "The map becomes terrain: real elevation and ocean depth (NASA SRTM and "
                "NOAA ETOPO), hillshaded and breathing with the wet and dry seasons. The "
                "camera zooms freely between the scales. Chapters open as illustrated "
                "cards, and the record's own images — codices, the Lienzo, the 1524 "
                "woodcut — appear on the cards they belong to, each with its credit.",
     "items": [
         "Terrain everywhere: the Basin's ravined sierra, the drained lakebed under the "
         "reconstructed 1519 lakes, the Gulf's turquoise shelf and the Pacific trench — "
         "measured data, rendered wet and dry; the seasons crossfade as the year turns.",
         "Popocatépetl smokes for its attested 1519-1528 active years (see 'Ordaz climbs "
         "the smoking mountain'), and cloud shadows thicken with the rains.",
         "Zoom with the wheel, pan by dragging, or fly between the three named scales; "
         "the terrain streams in sharper as you approach.",
         "Chapters are cards now: click one for the period's story, its image and its "
         "events. Ten illustrated with the record's own pictures — Mendoza folios, Book "
         "XII's smallpox plate, the Lienzo de Tlaxcala, the Kislak Sad Night, the "
         "Uppsala map.",
         "The 1524 Nuremberg map is georeferenced and measured: best-fit residual 2.2 km "
         "(5.5 km at the city) — beautiful topology, unusable geometry, and the About "
         "panel now says exactly that with the number.",
         "Every image is public domain, subject-verified, and credited on its card; the "
         "five searches that found nothing licence-safe are recorded as negatives in the "
         "manifest rather than papered over.",
     ]},
    {"version": "1.1", "date": "27 July 2026",
     "title": "The land under the war — and the war's slower weapons",
     "summary": "The map now has its ground: coasts, seas, the sierras and the named "
                "volcanoes (a first-release report said, correctly, that the map was a "
                "black background). And two layers stop being scenery: the smallpox is a "
                "modelled wave, and the siege is a derived state.",
     "items": [
         "Land and sea: a simplified authored coastline, the Gulf and Pacific, the "
         "great sierras and eight named peaks — including the two volcanoes whose pass "
         "the column crossed in November 1519.",
         "The epidemic is a mechanism now: a wave on the settlement network, seeded at "
         "the coast in May 1520 and calibrated to the documented sixty days in the "
         "capital from October — every polity shows its modelled onset window, and "
         "mortality stays a band (30-50%, contested).",
         "The siege is derived, not narrated: six arteries — four causeways, the "
         "aqueduct, the open lake — each cut by a dated, cited event; a panel counts "
         "the tourniquets 0 to 6 between 22 May and 13 August 1521.",
         "Eighteen people join the model as time-aware cards — the three last "
         "tlahtohqueh, Malintzin (with the four-century argument about her carried as "
         "accounts), the Tlaxcalteca leadership, and the aftermath's builders.",
         "Twenty-five new events carry the record to ~90, including the contested "
         "Guadalupe tradition (dated as tradition, with the documentary silence "
         "stated), don Carlos of Texcoco's burning, the Colegio de Tlatelolco, and "
         "Sahagún beginning the interviews that became this model's own chief source.",
         "Province cards now list their principal Mendoza tribute — cacao, quetzal "
         "feathers, gold dust, cochineal — so the web the coalition broke is legible "
         "good by good.",
     ]},
    {"version": "1.0", "date": "27 July 2026",
     "title": "The coalition is on the map",
     "summary": "First release. The map draws allegiance per altepetl per day — 75 polities "
                "through the war and its aftermath — instead of a two-colour conquest.",
     "items": [
         "Every polity's standing (tributary, contested, coalition, occupied, New Spain) is "
         "computed from 64 dated, cited events; the mid-siege map shows 24 allied and 12 "
         "occupied against 30 still-tributary — the coalition, visibly.",
         "Contested episodes — Cholula, Tóxcatl, Moctezuma's death and his famous 'surrender' "
         "— carry a 'What the sources say' section naming who claims what and why each would.",
         "The lakes, causeways, dike and aqueduct follow González Aparicio's 1973 "
         "reconstruction, scored against the Templo Mayor anchor table (residuals under 6 m; "
         "no town drawn in the water).",
         "The timeline gives the two war years 56% of the track at day resolution, with the "
         "scale breaks drawn; dates are Julian, with Nahua equivalents labelled as the "
         "correlations they are.",
         "Force numbers appear only as ranges: at the siege, 700-950 Spaniards beside "
         "24,000-200,000 Nahua allies — the sources are parties to every count.",
     ]},
]

ABOUT = {
    "what": "An interactive model of the fall of Tenochtitlan and its aftermath, "
            "1502-1550: the tributary system, the coalition that pulled it apart, the "
            "siege, and the colonial consolidation — every polity's allegiance computed "
            "per day from dated, cited events.",
    "naming": "\"Aztec\" appears in this project's title for findability only. It is a "
              "modern coinage and never a self-designation: this model says Mexica for "
              "the people, Triple Alliance for the polity, and each altepetl's own name "
              "— Nahuatl endonym first, Spanish exonym second.",
    "notKnow": [
        "The 1519 lake shoreline is a reconstruction (González Aparicio 1973), drawn "
        "here at visualization grade — the lakes were drained after the conquest.",
        "The coastline and sierra are simplified authored cartography (the modern "
        "coast, at this drawing's resolution, stands in for 1519's); the epidemic "
        "layer is a modelled wave pinned only at its documented start and its "
        "documented arrival in the capital — every other onset is a window, not a "
        "record.",
        "Indigenous force numbers are contested by an order of magnitude; population "
        "and epidemic mortality more. Every such quantity is a band, never a number.",
        "Motive and speech are the least constrained things in the record. Contested "
        "episodes carry a 'What the sources say' section instead of a verdict.",
        "Nahua calendar equivalents are correlations anchored at 13 Aug 1521 = 1 Cóatl; "
        "the correlation itself is contested and is labelled as such.",
        "Allegiance below the altepetl is not modelled; 'contested' is the resolution "
        "floor. Post-war absorption dates marked 'modelled' are defaults, not records.",
        "The 1524 Nuremberg woodcut is georeferenced and measured at a mean best-fit "
        "residual of 2.2 km (5.5 km at the city itself): topology, not geometry. It "
        "appears here as a document, and nothing in the model traces it.",
        "Figure-scale scenes — the marching files, skirmishes, canoe traffic, porters, "
        "refugees, the city's house fabric and its trees — are procedural ARTISTIC "
        "IMPRESSIONS rooted in the accounts (Calnek's urban fabric; the chroniclers' "
        "canoe-borne city; the causeway exodus after the fall). Contingent sizes follow "
        "the model's own force bands; positions are deterministic seeds, not records. "
        "Nothing at figure scale is an attestation.",
    ],
    "sources": [
        "Cortés, Cartas de relación (1519-26) — a legal self-defence, used as such",
        "Bernal Díaz, Historia verdadera (c. 1568) — the soldiers' counter-memoir",
        "Florentine Codex Book XII (c. 1555-79) — Nahua testimony, Tlatelolca vantage",
        "Anales de Tlatelolco; Durán; Alva Ixtlilxóchitl; Muñoz Camargo",
        "Codex Mendoza (Berdan & Anawalt 1992); Gerhard (1972); Smith & Berdan (1996)",
        "González Aparicio (1973), Plano reconstructivo — the named lake reconstruction",
        "Thomas (1993); Hassig (2006); Gibson (1964) — modern chronology and aftermath",
        "Terrain: NASA/USGS SRTM elevation and NOAA ETOPO1 bathymetry via the AWS Open "
        "Data Terrain Tiles (Mapzen terrarium) — public domain sources, rendered by this "
        "project's own pipeline; the seasonal palette is a modelled rendering choice",
        "Card images: public-domain scans via Wikimedia Commons (Newberry Library; "
        "Bodleian; Biblioteca Medicea Laurenziana; Library of Congress/Kislak; Uppsala "
        "University Library), each subject-verified and credited on its card",
    ],
}


def emit():
    os.makedirs(STAGED, exist_ok=True)

    def j(x):
        return json.dumps(x, ensure_ascii=False, separators=(",", ":"))

    def write(name, text):
        p = os.path.join(STAGED, name)
        with open(p, "w") as f:
            f.write(text)
        return p, len(text)

    header = "/* GENERATED by Research/modeling/emit.py — do not hand-edit. */\n" \
             "window.DATA = window.DATA || {};\n"

    ents = build_entities()
    evs = build_events_js()

    meta = {
        "t0": T0, "t1": T1, "step": 0.02, "unit": "yr",
        "speeds": [0.05, 0.2, 1, 3, 8, 20],
        "dataVersion": None,   # stamped by the build
        "timescale": [
            {"from": T0, "to": _t(1519, 2, 18), "w": 0.22},
            {"from": _t(1519, 2, 18), "to": _t(1521, 8, 20), "w": 0.56},
            {"from": _t(1521, 8, 20), "to": T1, "w": 0.22},
        ],
        "campaign": [_t(1519, 2, 18), _t(1521, 8, 20)],
        "views": {
            "meso":  {"lon0": -105.0, "lat0": 13.5, "lon1": -86.5, "lat1": 22.5,
                      "label": "Mesoamerica"},
            "basin": {"lon0": -99.55, "lat0": 19.02, "lon1": -98.55, "lat1": 19.95,
                      "label": "Basin of Mexico"},
            "city":  {"lon0": -99.235, "lat0": 19.325, "lon1": -99.030, "lat1": 19.515,
                      "label": "Tenochtitlan"},
        },
        # basemap extents — A MATCHED PAIR with build/terrain.py VIEWS (the city
        # image is wider than the city camera preset on purpose)
        "terrain": {
            "meso":     {"lon0": -105.0, "lat0": 13.5, "lon1": -86.5, "lat1": 22.5},
            "corridor": {"lon0": -100.2, "lat0": 17.9, "lon1": -95.8, "lat1": 20.4},
            "basin":    {"lon0": -99.55, "lat0": 19.02, "lon1": -98.55, "lat1": 19.95},
            "city":     {"lon0": -99.32, "lat0": 19.27, "lon1": -98.94, "lat1": 19.57},
        },
        "layers": [
            {"id": "water", "label": "Lakes & works (1519 reconstruction)", "on": True},
            {"id": "altepetl", "label": "Altepetl & allegiance", "on": True},
            {"id": "epidemic", "label": "Epidemic wave (modelled)", "on": True},
            {"id": "tribute", "label": "Tribute flows", "on": True},
            {"id": "track", "label": "Campaign track", "on": True},
            {"id": "events", "label": "Events", "on": True},
            {"id": "works", "label": "Causeways & aqueduct cards", "on": True},
            {"id": "city", "label": "City model (phased)", "on": True},
            {"id": "figures", "label": "Figures & life (impression)", "on": True},
        ],
        "siege": {"start": siege.SIEGE_START, "end": siege.SIEGE_END,
                  "arteries": [{"id": a["id"], "label": a["label"],
                                "cut": round(a["cut"], 4),
                                "confidence": a["confidence"]} for a in siege.ARTERIES]},
        "epidemicBand": [int(epidemic.MORTALITY_BAND[0] * 100),
                         int(epidemic.MORTALITY_BAND[1] * 100)],
        "epidemicFront": {"lat": gazetteer.BY_SLUG["cempoala"]["lat"],
                          "lon": gazetteer.BY_SLUG["cempoala"]["lon"],
                          "t0": round(epidemic.SEED_T, 4),
                          "kmPerYear": round(epidemic._SPEED_KM_PER_YR, 1)},
        "cityPhases": {"siege": siege.SIEGE_START, "fall": siege.SIEGE_END,
                       "colonial": _t(1522, 1, 15)},
        "stateColor": STATE_COLOR,
        "stateLabel": {
            "alliance-core": "Triple Alliance seat", "tributary": "Tributary",
            "independent": "Independent", "rival": "Rival empire",
            "contested": "Contested", "allied-coalition": "Coalition",
            "occupied": "Occupied", "colonial-ally": "Colonial ally (privileged)",
            "new-spain": "New Spain", "spanish": "Spanish foundation"},
        "about": ABOUT,
        "updates": UPDATES,
    }

    # attach images (with credit — audited) and per-chapter event listings
    for e in ents + evs:
        img = ENTITY_IMAGE.get(e["id"])
        if img:
            e["image"] = IMAGES[img]
    chapters = [dict(c) for c in CHAPTERS]
    for c in chapters:
        img = CHAPTER_IMAGE.get(c["name"])
        if img:
            c["image"] = IMAGES[img]
        inside = [ev for ev in evs if c["from"] <= ev["t"] < c["to"]]
        c["chapterEvents"] = [{"t": ev["t"], "name": ev["name"], "id": ev["id"]}
                              for ev in inside[:10]]
        c["nEvents"] = len(inside)

    files = []
    files.append(write("meta.js", header + "DATA.meta = " + j(meta) + ";\n"))
    files.append(write("eras.js", header + "DATA.eras = " + j(chapters) + ";\n"
                       + "DATA.events = " + j([{"t": e["t"], "name": e["name"],
                                                "id": e["id"]} for e in evs]) + ";\n"))
    files.append(write("entities.js", header + "DATA.entities = " + j(ents) + ";\n"))
    files.append(write("eventsFull.js", header + "DATA.eventsFull = " + j(evs) + ";\n"))
    files.append(write("geo.js", header + "DATA.geo = " + j({
        "city": [{"id": k, "kind": g["kind"], "closed": g["closed"],
                  "confidence": g["confidence"], "phases": list(g["phases"]),
                  "points": g["points"]} for k, g in georef.CITY.items()],
        "campanLabels": [{"name": n, "lat": la, "lon": lo}
                         for n, la, lo in georef.CAMPAN_LABELS],
        "rivers": [{"id": k, "label": g["label"], "confidence": g["confidence"],
                    "note": g["note"], "points": g["points"]}
                   for k, g in georef.RIVERS.items()],
        "chinampaZones": [{"id": k, "label": g["label"],
                           "confidence": g["confidence"], "note": g["note"],
                           "points": g["points"]}
                          for k, g in georef.CHINAMPA_ZONES.items()],
        "features": [{"id": k, "kind": g["kind"], "closed": g["closed"],
                      "confidence": g["confidence"], "points": g["points"]}
                     for k, g in georef.GEOMETRY.items()]
                    + [{"id": k, "kind": g["kind"], "closed": True,
                        "confidence": g["confidence"], "points": g["points"]}
                       for k, g in georef.SEAS.items()]
                    + [{"id": k, "kind": g["kind"], "closed": False,
                        "confidence": g["confidence"], "points": g["points"],
                        "label": g["label"]}
                       for k, g in georef.RIDGES.items()],
        "anchors": [{"id": k, "lat": v[0], "lon": v[1]} for k, v in georef.ANCHORS.items()],
        "peaks": [{"id": k, "lat": v[0], "lon": v[1], "label": v[2], "views": v[3]}
                  for k, v in georef.PEAKS.items()],
        "seaLabels": [{"lon": lo, "lat": la, "label": lb}
                      for lo, la, lb in georef.SEA_LABELS],
    }) + ";\n" + "DATA.forces = " + j(forces.app_series()) + ";\n"))

    total = sum(n for _, n in files)
    for p, n in files:
        print(f"  wrote {os.path.basename(p):16} {n/1024:7.1f} KB")
    # SCOPE §10, amended round 7: 45 MB over the wire for the whole site. The
    # data files are a rounding error in that — the basemaps are the budget.
    print(f"  total {total/1024:.1f} KB (site budget: 45 MB — data is "
          f"{total/(45*1024*1024)*100:.2f}% of it; the basemaps are the rest)")
    return files


def _selftest():
    ents = build_entities()
    ids = [e["id"] for e in ents]
    assert len(ids) == len(set(ids))
    for e in ents:
        # era tiling: contiguous from first era to T1
        eras = e["eras"]
        assert eras, e["id"]
        assert abs(eras[-1]["to"] - T1) < 1e-6, e["id"]
        for a, b in zip(eras, eras[1:]):
            assert abs(a["to"] - b["from"]) < 1e-6, f"{e['id']}: era gap {a['to']} -> {b['from']}"
        for era in eras:
            assert era["to"] > era["from"], e["id"]
            assert len(era["text"]) > 30, f"{e['id']}: thin era text"
        assert e["sources"], e["id"]
        if e["confidence"] == "contested":
            assert e.get("note") or e.get("accounts"), f"{e['id']}: contested, no note/accounts"
    evs = build_events_js()
    assert len(evs) == len(events_mod.EVENTS)
    for ev in evs:
        assert ev["sources"] and ev["text"], ev["id"]
        if ev["confidence"] == "contested":
            assert len(ev["accounts"]) >= 2, ev["id"]
    print(f"selftest OK — {len(ents)} entities ({sum(1 for e in ents if e['layer']=='altepetl')} "
          f"altepetl, {sum(1 for e in ents if e['layer']=='works')} works), {len(evs)} events")


if __name__ == "__main__":
    _selftest()
    emit()
