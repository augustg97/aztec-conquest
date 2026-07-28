#!/usr/bin/env python3
"""Fetch licence-safe card images from Wikimedia Commons (round 3, downloads
user-approved). Run with the venv python:

    ./venv/bin/python3 build/fetch_images.py

Discipline (SOURCING-AND-LICENSING §2-3, MANIFEST policy):
  * accept ONLY: public domain / PD-* / CC0 / plain CC BY (any version);
    REFUSE share-alike, NC, ND, fair use, unmarked — checked against the
    LicenseShortName Commons reports, and the verdict recorded per image;
  * every image gets a row in Research/figures/collected/MANIFEST.json with
    source URL, author, licence, and `verified_subject: false` UNTIL a human
    (or a session that actually opened it) has looked — correct licence never
    implies correct subject; a contact sheet is emitted for exactly that;
  * originals cache to data/images-src/ (gitignored); the app ships downscaled
    JPEGs (<= 900 px, q80) in web/img/cards/ with credit lines carried into
    every card that uses one.
"""

from __future__ import annotations

import io
import json
import os
import time
import urllib.parse
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "images-src")
OUT = os.path.join(ROOT, "web", "img", "cards")
MANIFEST = os.path.join(ROOT, "Research", "figures", "collected", "MANIFEST.json")
SHEET = os.path.join(ROOT, "Research", "figures", "collected", "contact-sheet.jpg")

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "AztecConquestModel/1.0 (research/education; augustgweon@gmail.com)"}

ACCEPT = ("public domain", "pd", "cc0", "cc by 4.0", "cc by 3.0", "cc by 2.5",
          "cc by 2.0", "cc-by 4.0", "cc-by 3.0", "attribution")
REFUSE = ("sa", "share", "nc", "nd", "fair")

# slug -> (search query, what the subject MUST be — the review criterion)
WISHLIST = {
    "map-1524":        ("Map of Tenochtitlan and Gulf of Mexico 1524",
                        "the Nuremberg/Peypus 1524 woodcut map of Tenochtitlan"),
    "mendoza-founding": ("Codex Mendoza folio 2r",
                         "Codex Mendoza frontispiece: the eagle on the cactus"),
    "mendoza-tribute": ("Codex Mendoza folio 46r tribute",
                        "a Codex Mendoza tribute-list folio"),
    "fc-smallpox":     ("Florentine Codex smallpox",
                        "Book XII drawing of smallpox victims"),
    "fc-siege":        ("Florentine Codex conquista guerra Tenochtitlan",
                        "Book XII conquest-war plate"),
    "lienzo-meeting":  ("Lienzo de Tlaxcala Cortes Tlaxcala meeting",
                        "Lienzo de Tlaxcala plate: Tlaxcalteca lords meet Cortés"),
    "lienzo-cholula":  ("Lienzo de Tlaxcala Cholula massacre",
                        "Lienzo de Tlaxcala plate: the Cholula massacre"),
    "toxcatl":         ("matanza Templo Mayor codex Duran",
                        "16th-c codex image of the Tóxcatl massacre"),
    "noche-triste":    ("Noche Triste",
                        "a pre-1900 depiction of the Noche Triste"),
    "siege-painting":  ("Conquista de Mexico Kislak Tenochtitlan",
                        "the 17th-c 'Conquista de México' siege painting"),
    "uppsala-map":     ("Uppsala map Mexico City 1550",
                        "the c. 1550 Mapa Uppsala of Mexico City"),
    "moctezuma":       ("Moctezuma II portrait Antonio Rodriguez",
                        "a pre-1900 portrait of Moctezuma II"),
    "cortes":          ("Hernan Cortes portrait 16th century",
                        "a pre-1900 portrait of Hernán Cortés"),
    "malintzin":       ("La Malinche Florentine Codex",
                        "a codex image showing Malintzin interpreting"),
    "cuauhtemoc":      ("Cuauhtemoc Tovar codex",
                        "a codex-derived depiction of Cuauhtémoc"),
}


def api(params):
    q = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(f"{API}?{q}", headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def licence_ok(short):
    s = (short or "").lower()
    if any(r in s for r in REFUSE):
        return False
    return any(a in s for a in ACCEPT)


def pick(query):
    """First search hit whose licence passes the policy."""
    res = api({"action": "query", "generator": "search",
               "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
               "gsrlimit": 8, "prop": "imageinfo",
               "iiprop": "url|extmetadata|size", "iiurlwidth": 1400})
    pages = (res.get("query") or {}).get("pages") or {}
    ranked = sorted(pages.values(), key=lambda p: p.get("index", 99))
    for p in ranked:
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata") or {}
        short = (meta.get("LicenseShortName") or {}).get("value", "")
        if not licence_ok(short):
            continue
        if (ii.get("width", 0) or 0) < 500:
            continue
        artist = (meta.get("Artist") or {}).get("value", "")
        # strip html from artist crudely
        while "<" in artist and ">" in artist:
            artist = artist[:artist.index("<")] + artist[artist.index(">") + 1:]
        return {"title": p.get("title"), "url": ii.get("thumburl") or ii.get("url"),
                "page": ii.get("descriptionshorturl") or ii.get("descriptionurl"),
                "licence": short, "artist": artist.strip() or "unknown"}
    return None


def main():
    os.makedirs(SRC, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    with open(MANIFEST) as f:
        manifest = json.load(f)
    have = {i["slug"] for i in manifest.get("items", [])}
    thumbs = []
    for slug, (query, expect) in WISHLIST.items():
        cached = os.path.join(SRC, slug + ".img")
        if slug in have and os.path.exists(os.path.join(OUT, slug + ".jpg")):
            print(f"  {slug:18} cached")
            thumbs.append((slug, os.path.join(OUT, slug + ".jpg")))
            continue
        info = pick(query)
        if not info:
            print(f"  {slug:18} NO LICENCE-SAFE RESULT — recorded as negative")
            manifest["items"].append({"slug": slug, "query": query,
                                      "result": "negative — nothing acceptably licensed in top 8",
                                      "licence_ok": False, "verified_subject": False})
            continue
        req = urllib.request.Request(info["url"], headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(cached, "wb") as f:
            f.write(data)
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img.thumbnail((900, 900))
        outp = os.path.join(OUT, slug + ".jpg")
        img.save(outp, quality=80, optimize=True)
        manifest["items"].append({
            "slug": slug, "query": query, "file": info["title"],
            "source_url": info["page"], "author": info["artist"],
            "licence": info["licence"], "licence_ok": True,
            "expected_subject": expect,
            "verified_subject": False,
            "review": "PENDING — verify on the contact sheet before shipping",
        })
        kb = os.path.getsize(outp) / 1024
        print(f"  {slug:18} {info['licence']:24} {kb:5.0f} KB  {info['title'][:60]}")
        thumbs.append((slug, outp))
        time.sleep(0.4)

    # contact sheet for the visual review (A4: licence ok != subject ok)
    if thumbs:
        cols = 4
        cell = 320
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * (cell + 24)), (16, 18, 22))
        from PIL import ImageDraw
        d = ImageDraw.Draw(sheet)
        for i, (slug, p) in enumerate(thumbs):
            im = Image.open(p); im.thumbnail((cell - 8, cell - 8))
            x = (i % cols) * cell; y = (i // cols) * (cell + 24)
            sheet.paste(im, (x + 4, y + 4))
            d.text((x + 6, y + cell + 4), slug, fill=(230, 230, 230))
        sheet.save(SHEET, quality=85)
        print(f"  contact sheet -> {os.path.relpath(SHEET, ROOT)}")

    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1024
    print(f"  card images total {total:.0f} KB")


if __name__ == "__main__":
    main()
