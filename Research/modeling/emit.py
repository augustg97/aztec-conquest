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
        facts.append(["Modern", e["modern"]])
        conf = "contested" if e["coord_conf"] == "contested" else e["entry_conf"]
        note = e["note"]
        if e["coord_conf"] == "contested" and "approximate" not in (note or "").lower() \
           and "debated" not in (note or "").lower():
            note = (note + " " if note else "") + "Location approximate."
        ents.append({
            "id": slug, "name": name, "kind": KIND_LABEL[e["group"]],
            "layer": "altepetl", "lon": e["lon"], "lat": e["lat"],
            "from": round(t_from, 4), "to": None,
            "confidence": conf, "note": note or "",
            "facts": facts, "eras": eras,
            "allegiance": allegiance.series(slug),
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
    return ents


def build_events_js():
    evs = []
    for e in events_mod.EVENTS:
        if e["place"]:
            g = gazetteer.BY_SLUG[e["place"]]
            lon, lat = g["lon"], g["lat"]
        else:
            lat, lon = e["latlon"]
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
        })
    return evs


# In-app update log — written for a reader, not a changelog: the effect first,
# the number as evidence. Rendered in the About panel.
UPDATES = [
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
        "Indigenous force numbers are contested by an order of magnitude; population "
        "and epidemic mortality more. Every such quantity is a band, never a number.",
        "Motive and speech are the least constrained things in the record. Contested "
        "episodes carry a 'What the sources say' section instead of a verdict.",
        "Nahua calendar equivalents are correlations anchored at 13 Aug 1521 = 1 Cóatl; "
        "the correlation itself is contested and is labelled as such.",
        "Allegiance below the altepetl is not modelled; 'contested' is the resolution "
        "floor. Post-war absorption dates marked 'modelled' are defaults, not records.",
    ],
    "sources": [
        "Cortés, Cartas de relación (1519-26) — a legal self-defence, used as such",
        "Bernal Díaz, Historia verdadera (c. 1568) — the soldiers' counter-memoir",
        "Florentine Codex Book XII (c. 1555-79) — Nahua testimony, Tlatelolca vantage",
        "Anales de Tlatelolco; Durán; Alva Ixtlilxóchitl; Muñoz Camargo",
        "Codex Mendoza (Berdan & Anawalt 1992); Gerhard (1972); Smith & Berdan (1996)",
        "González Aparicio (1973), Plano reconstructivo — the named lake reconstruction",
        "Thomas (1993); Hassig (2006); Gibson (1964) — modern chronology and aftermath",
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
        "layers": [
            {"id": "water", "label": "Lakes & works (1519 reconstruction)", "on": True},
            {"id": "altepetl", "label": "Altepetl & allegiance", "on": True},
            {"id": "tribute", "label": "Tribute flows", "on": True},
            {"id": "track", "label": "Campaign track", "on": True},
            {"id": "events", "label": "Events", "on": True},
            {"id": "works", "label": "Causeways & aqueduct cards", "on": True},
        ],
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

    files = []
    files.append(write("meta.js", header + "DATA.meta = " + j(meta) + ";\n"))
    files.append(write("eras.js", header + "DATA.eras = " + j(CHAPTERS) + ";\n"
                       + "DATA.events = " + j([{"t": e["t"], "name": e["name"],
                                                "id": e["id"]} for e in evs]) + ";\n"))
    files.append(write("entities.js", header + "DATA.entities = " + j(ents) + ";\n"))
    files.append(write("eventsFull.js", header + "DATA.eventsFull = " + j(evs) + ";\n"))
    files.append(write("geo.js", header + "DATA.geo = " + j({
        "features": [{"id": k, "kind": g["kind"], "closed": g["closed"],
                      "confidence": g["confidence"], "points": g["points"]}
                     for k, g in georef.GEOMETRY.items()],
        "anchors": [{"id": k, "lat": v[0], "lon": v[1]} for k, v in georef.ANCHORS.items()],
    }) + ";\n" + "DATA.forces = " + j(forces.app_series()) + ";\n"))

    total = sum(n for _, n in files)
    for p, n in files:
        print(f"  wrote {os.path.basename(p):16} {n/1024:7.1f} KB")
    print(f"  total {total/1024:.1f} KB (budget: 25 MB — {total/(25*1024*1024)*100:.2f}% used)")
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
