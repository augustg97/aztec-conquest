"""Audit the card system against the card contract (SCOPE §6). READ-ONLY.

Reads THE ARTIFACT THE APP READS — web/data/*.js if the handover has been
executed, else the staged copies in Research/research reports/staged-artifacts/
— never a private rebuild (TRAPS D5). Says which it read.

Checks (severity: HIGH = factually wrong or misleading · MED = incomplete or
over-confident · LOW = polish):

  tiling        era arrays tile each entity's life to T1, no gaps or overlaps  HIGH
  chapters      DATA.eras tiles [t0, t1] exactly                              HIGH
  contested     a contested card with no accounts/note — stated flatly        HIGH
  sources       a card with no sources — an assertion                         HIGH
  allegiance    an altepetl entity without a legal allegiance series          HIGH
  dates         a day-precision event without its correlation-labelled
                Nahua date, or an unlabelled correlation                      MED
  anachronism   a term used inside an era window that predates the term      MED
  naming        "Aztec"/"Montezuma" anywhere in model text (About excepted)  MED

    python3 audit_cards.py            # report + final JSON line
    python3 audit_cards.py --selftest # synthetic input with known answers
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WEB = os.path.join(ROOT, "web", "data")
STAGED = os.path.join(HERE, "..", "research reports", "staged-artifacts")

STATES = {"alliance-core", "tributary", "independent", "rival", "contested",
          "allied-coalition", "occupied", "colonial-ally", "new-spain", "spanish"}

# term -> first t at which it may appear inside an era/event window.
# These dates are calibrated to THIS MODEL'S TERRITORY, not to the word's first
# use anywhere: "encomienda" is barred before 1521.6 because that is when the
# institution reaches Mexico, though the word is Caribbean from 1503.
ANACHRONISMS = {"New Spain": 1520.8, "Mexico City": 1521.6, "viceroy": 1535.8,
                "Viceroy": 1535.8, "encomienda": 1521.6}

# The narrow, documented exceptions: (term, owner) pairs where the card is
# legitimately outside the model's territory and the territorial date does not
# apply. Each needs a reason, and the list stays SHORT — an exemption that grows
# is an audit that has stopped working. Fires as a LOW if the exemption is
# stale (the term is no longer in that card), so dead entries get cleaned up.
ANACHRONISM_EXEMPT = {
    ("encomienda", "person-las-casas"):
        "his 1502-1514 years are in the Caribbean, where the encomienda dates "
        "from Ovando's grants of 1503 — he held one on Hispaniola and Cuba "
        "before New Spain existed, and renouncing it in 1514 is the hinge of "
        "his life. The model's territorial date of 1521.6 is about Mexico.",
}
BANNED = ("Aztec", "Montezuma")     # house orthography and naming rules


def _load_js(path, key):
    """Parse `DATA.key = <json>;` out of a generated JS literal file."""
    with open(path) as f:
        src = f.read()
    marker = f"DATA.{key} = "
    i = src.index(marker) + len(marker)
    j = src.index(";\n", i)
    return json.loads(src[i:j])


def load_subject():
    base = WEB if os.path.exists(os.path.join(WEB, "eventsFull.js")) else STAGED
    which = "web/data (live app data)" if base == WEB else "staged artifacts (handover not yet executed)"
    return {
        "which": which,
        "meta": _load_js(os.path.join(base, "meta.js"), "meta"),
        "chapters": _load_js(os.path.join(base, "eras.js"), "eras"),
        "entities": _load_js(os.path.join(base, "entities.js"), "entities"),
        "events": _load_js(os.path.join(base, "eventsFull.js"), "eventsFull"),
    }


def check_tiling(sub, F):
    t1 = sub["meta"]["t1"]
    for e in sub["entities"]:
        eras = e.get("eras") or []
        if not eras:
            F("HIGH", "tiling", e["id"], "no eras array"); continue
        if abs(eras[-1]["to"] - t1) > 1e-6:
            F("HIGH", "tiling", e["id"], f"eras end at {eras[-1]['to']}, not {t1}")
        for a, b in zip(eras, eras[1:]):
            if abs(a["to"] - b["from"]) > 1e-6:
                F("HIGH", "tiling", e["id"], f"gap/overlap {a['to']} -> {b['from']}")
        for era in eras:
            if len(era.get("text", "")) < 30:
                F("MED", "tiling", e["id"], f"thin era text at {era['from']}")


def check_chapters(sub, F):
    m, ch = sub["meta"], sub["chapters"]
    if abs(ch[0]["from"] - m["t0"]) > 1e-6 or abs(ch[-1]["to"] - m["t1"]) > 1e-6:
        F("HIGH", "chapters", "span", f"chapters cover {ch[0]['from']}..{ch[-1]['to']}, "
                                      f"model is {m['t0']}..{m['t1']}")
    for a, b in zip(ch, ch[1:]):
        if abs(a["to"] - b["from"]) > 1e-6:
            F("HIGH", "chapters", a["name"], f"gap/overlap at {a['to']}")


def check_contested(sub, F):
    for e in sub["entities"]:
        if e.get("confidence") == "contested" and not (e.get("note") or e.get("accounts")):
            F("HIGH", "contested", e["id"], "contested entity with no note/accounts")
    for ev in sub["events"]:
        if ev.get("confidence") == "contested" and len(ev.get("accounts") or []) < 2:
            F("HIGH", "contested", ev["id"], "contested event stated flatly (<2 accounts)")


def check_sources(sub, F):
    for coll, key in (("entities", "id"), ("events", "id")):
        for x in sub[coll]:
            if not x.get("sources"):
                F("HIGH", "sources", x[key], "no sources — a card without a source is an assertion")


def check_allegiance(sub, F):
    for e in sub["entities"]:
        if e.get("layer") != "altepetl":
            continue
        s = e.get("allegiance")
        if not s:
            F("HIGH", "allegiance", e["id"], "altepetl without allegiance series"); continue
        ts = [row[0] for row in s]
        if ts != sorted(ts):
            F("HIGH", "allegiance", e["id"], "unsorted allegiance series")
        for _, st in s:
            if st not in STATES:
                F("HIGH", "allegiance", e["id"], f"unknown state {st!r}")


def check_dates(sub, F):
    for ev in sub["events"]:
        facts = dict((k, v) for k, v in (ev.get("facts") or []))
        if "Date (Julian)" not in facts:
            F("MED", "dates", ev["id"], "no Julian date fact")
        nahua = facts.get("Nahua day (correlation)")
        if ev.get("precision") == "day":
            if not nahua:
                F("MED", "dates", ev["id"], "day-precision event without Nahua correlation fact")
            elif "correlation" not in nahua:
                F("MED", "dates", ev["id"], "Nahua date not labelled as a correlation")


def _texts_with_windows(sub):
    for e in sub["entities"]:
        for era in e.get("eras") or []:
            yield e["id"], era["from"], era["text"]
    for ev in sub["events"]:
        yield ev["id"], ev["t"], ev.get("text", "")
    for ch in sub["chapters"]:
        yield f"chapter:{ch['name']}", ch["from"], ch.get("text", "") + " " + ch.get("title", "")


def check_anachronism(sub, F):
    used_exemptions = set()
    for owner, t_from, text in _texts_with_windows(sub):
        for term, not_before in ANACHRONISMS.items():
            if term in text and t_from < not_before - 1e-6:
                if (term, owner) in ANACHRONISM_EXEMPT:
                    used_exemptions.add((term, owner))
                    continue
                F("MED", "anachronism", owner,
                  f"'{term}' inside a window opening {t_from:.2f} (term exists from {not_before})")
        for term in BANNED:
            if term in text:
                F("MED", "naming", owner, f"'{term}' in model text (allowed only in About)")

    # An exemption that no longer suppresses anything is dead weight, and dead
    # weight in an audit is how audits stop working. Report it so it gets removed.
    for (term, owner), _why in ANACHRONISM_EXEMPT.items():
        if (term, owner) not in used_exemptions:
            F("LOW", "audit-hygiene", owner,
              f"stale anachronism exemption for '{term}' — nothing suppressed; delete it")


def check_images(sub, F):
    """Licence discipline on the cards: an image must carry caption AND credit."""
    def probe(owner, img):
        if not img:
            return
        if not img.get("src") or not img.get("credit") or not img.get("caption"):
            F("HIGH", "images", owner, "image without src/caption/credit — licence "
                                       "discipline broken")
    for e in sub["entities"]:
        probe(e["id"], e.get("image"))
    for ev in sub["events"]:
        probe(ev["id"], ev.get("image"))
    n_ch = sum(1 for c in sub["chapters"] if c.get("image"))
    for c in sub["chapters"]:
        probe(f"chapter:{c['name']}", c.get("image"))
    if n_ch < 8:
        F("MED", "images", "chapters", f"only {n_ch} of {len(sub['chapters'])} chapters "
                                       f"illustrated (< 8)")



def check_image_targets(sub, F):
    """Every image the emitter assigns must land on something that exists.

    Added round 8 after two ENTITY_IMAGE keys ('toxcatl-massacre', 'siege-begins')
    named events that were really 'toxcatl' and 'siege-camps'. Nothing failed: the
    dict lookup simply missed and the card shipped without its picture. A silent
    drop is the worst kind of defect because the artifact looks finished, so the
    orphan is now HIGH — the emitter is asserting a link that is not there.
    """
    known = {e["id"] for e in sub["entities"]} | {ev["id"] for ev in sub["events"]}
    seen_with_image = {e["id"] for e in sub["entities"] if e.get("image")}
    seen_with_image |= {ev["id"] for ev in sub["events"] if ev.get("image")}
    if "_image_map" in sub:                     # selftest injects; never mutates the emitter
        assigned = set(sub["_image_map"])
    else:
        try:
            sys.path.insert(0, HERE)
            import emit as _emit
            assigned = set(_emit.ENTITY_IMAGE)
        except Exception as e:                  # unimportable: say so, do not pass silently
            F("LOW", "image-targets", "emit.py", f"could not read ENTITY_IMAGE ({e})")
            return
    for owner in sorted(assigned - known):
        F("HIGH", "image-targets", owner,
          "an image is assigned to this id, but no entity or event has it")
    for owner in sorted(assigned & known - seen_with_image):
        F("MED", "image-targets", owner,
          "assigned an image that did not reach the card")


CHECKS = [check_image_targets, check_tiling, check_chapters, check_contested, check_sources,
          check_allegiance, check_dates, check_anachronism, check_images]


def run():
    sub = load_subject()
    findings = []

    def F(sev, check, what, detail):
        findings.append({"severity": sev, "check": check, "what": what, "detail": detail})

    for c in CHECKS:
        c(sub, F)          # not wrapped — a guard that cannot run must raise (TRAPS D3)
    return sub, findings


def _selftest():
    """Every check against synthetic input with a known answer."""
    sub = {
        "which": "synthetic",
        "meta": {"t0": 0.0, "t1": 10.0},
        "chapters": [{"from": 0.0, "to": 4.0, "name": "a", "text": "x" * 40,
                      "image": {"src": "x.jpg"}},                     # image, no credit!
                     {"from": 5.0, "to": 10.0, "name": "b", "text": "y" * 40}],  # gap!
        "entities": [
            {"id": "ok", "layer": "altepetl", "confidence": "good", "sources": ["s"],
             "eras": [{"from": 0.0, "to": 10.0, "text": "long enough era text ........."}],
             "allegiance": [[0.0, "tributary"]]},
            {"id": "bad", "layer": "altepetl", "confidence": "contested", "sources": [],
             "eras": [{"from": 0.0, "to": 3.0, "text": "x" * 40}],       # ends early!
             "allegiance": [[0.0, "nonsense"]]},                          # bad state!
        ],
        "events": [
            {"id": "e1", "t": 1.0, "precision": "day", "confidence": "contested",
             "accounts": [], "sources": ["s"], "text": "New Spain rises",   # anachronism at t=1!
             "facts": [["Date (Julian)", "x"]]},                            # no Nahua fact!
            {"id": "e2", "t": 1.0, "precision": "month", "confidence": "good",
             "accounts": [], "sources": ["s"], "text": "New Spain rises",   # SAME anachronism...
             "facts": [["Date (Julian)", "x"]]},                            # ...but exempted below
        ],
    }
    # prove the exemption path: e2 carries the same anachronism as e1 and must
    # NOT be reported, while the unused real exemption must be flagged stale
    ANACHRONISM_EXEMPT[("New Spain", "e2")] = "synthetic, to prove the path"
    findings = []

    def F(sev, check, what, detail):
        findings.append({"severity": sev, "check": check, "what": what, "detail": detail})

    sub["_image_map"] = {"no-such-entity": "whatever"}   # prove the orphan branch
    for c in CHECKS:
        c(sub, F)
    got = {(f["check"], f["what"]) for f in findings}
    expect = {("chapters", "a"), ("tiling", "bad"), ("contested", "bad"),
              ("contested", "e1"), ("sources", "bad"), ("allegiance", "bad"),
              ("dates", "e1"), ("anachronism", "e1"), ("images", "chapter:a"),
              ("image-targets", "no-such-entity")}
    missing = expect - got
    assert not missing, f"selftest: checks failed to fire: {missing}"
    assert ("anachronism", "e2") not in got, \
        "selftest: the anachronism exemption did not suppress"
    assert any(c == "audit-hygiene" for c, _ in got), \
        "selftest: a stale anachronism exemption was not reported"
    del ANACHRONISM_EXEMPT[("New Spain", "e2")]
    print(f"selftest OK — all {len(CHECKS)} checks fire on synthetic defects "
          f"({len(findings)} findings on the synthetic input)")


def main():
    if "--selftest" in sys.argv:
        _selftest(); return 0
    _selftest()
    sub, findings = run()
    print(f"reading: {sub['which']}")
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    findings.sort(key=lambda f: order[f["severity"]])
    for f in findings:
        print(f"{f['severity']:4}  {f['check']:12} {f['what']:24} {f['detail']}")
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in ("HIGH", "MED", "LOW")}
    print(f"{len(findings)} findings — {counts['HIGH']} HIGH / {counts['MED']} MED / {counts['LOW']} LOW")
    print(json.dumps(counts))
    return 1 if counts["HIGH"] else 0


if __name__ == "__main__":
    sys.exit(main())
