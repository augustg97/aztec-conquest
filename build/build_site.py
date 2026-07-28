#!/usr/bin/env python3
"""Build the static site: validator gate -> stamp -> copy web/ -> docs/.

    python3 build/build_site.py            # full build
    SKIP_AUDIT=1 python3 build/build_site.py   # override, deliberately awkward

Order matters (TRAPS D2 — the deploy that looks like it never landed):

  1. run the validators and REFUSE TO PUBLISH on a regression;
  2. stamp the data version INTO meta.js BEFORE anything is copied, and give
     every data <script> a ?dv= cache-buster in the copied index.html — GitHub
     Pages serves with max-age and an ETag, and a returning viewer can sit on
     stale JSON long after a successful push;
  3. copy web/ -> docs/ (docs is what Pages serves from main:/docs);
  4. print the stamp so the live value can be checked after the push.

Relative paths only, so the project directory can move. It will.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, "web")
DOCS = os.path.join(ROOT, "docs")
AUDIT = os.path.join(ROOT, "Research", "modeling", "audit_all.py")


def main() -> int:
    # 1 — the gate
    print("validators:")
    r = subprocess.run([sys.executable, AUDIT], cwd=os.path.dirname(AUDIT))
    if r.returncode != 0:
        print("\nBUILD REFUSED: a validator is below baseline. Fix it or tighten "
              "the baseline in the same commit — never publish over a regression.")
        return 1

    # 2 — the stamp
    stamp = time.strftime("%Y%m%d-%H%M%S")
    with open(os.path.join(WEB, "data", "meta.js")) as f:
        meta = f.read()
    if '"dataVersion":null' not in meta and '"dataVersion": null' not in meta:
        print("BUILD REFUSED: meta.js has no null dataVersion slot to stamp — "
              "was a stamped copy committed back into web/?")
        return 1
    meta_stamped = meta.replace('"dataVersion":null', f'"dataVersion":"{stamp}"') \
                       .replace('"dataVersion": null', f'"dataVersion":"{stamp}"')

    # 3 — copy web -> docs, stamped file first, cache-busted script tags
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    shutil.copytree(WEB, DOCS)
    with open(os.path.join(DOCS, "data", "meta.js"), "w") as f:
        f.write(meta_stamped)
    idx_path = os.path.join(DOCS, "index.html")
    with open(idx_path) as f:
        idx = f.read()
    for name in ("meta", "eras", "entities", "eventsFull", "geo"):
        idx = idx.replace(f'src="data/{name}.js"', f'src="data/{name}.js?dv={stamp}"')
    idx = idx.replace('src="js/app.js"', f'src="js/app.js?dv={stamp}"') \
             .replace('href="css/styles.css"', f'href="css/styles.css?dv={stamp}"')
    with open(idx_path, "w") as f:
        f.write(idx)
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    n = sum(len(fs) for _, _, fs in os.walk(DOCS))
    size = sum(os.path.getsize(os.path.join(dp, fn))
               for dp, _, fns in os.walk(DOCS) for fn in fns)
    print(f"\nbuilt docs/ — {n} files, {size/1024:.0f} KB")
    print(f"data version: {stamp}")
    print("after pushing, VERIFY THE LIVE STAMP:")
    print(f"  curl -s https://augustg97.github.io/aztec-conquest/data/meta.js"
          f" | grep -o 'dataVersion[^,]*'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
