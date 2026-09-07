#!/usr/bin/env python3
"""ERRATA.md が三篇からずれていないかを、機械で当たる。

    pip install pypdf
    python3 verification/check_errata.py

三篇の PDF は Zenodo で公開済みで、もう直せない。**直せるのは正誤表のほうである。**
だから正誤表は、時間とともに一次資料からずれていく。引用が一字変わる。箇所を
数え落とす（実際に、六箇所あるものを三箇所と書いていた）。未解決の項目が
「解決しました」に書き換わる。最終更新の日付が古いまま残る。

条件は verification/audit.toml に宣言してあり、当たるのは errata_check.py が
やる。**判定に推論を使わない。**あるか、無いか、一致するか、しないか。

道具は単一ファイルで、ここに写して使っている。同じものが
https://github.com/cpsbvbng26-dotcom/errata-check にある（MIT、v0.1.0、DOI: 10.5281/zenodo.22649054）。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from errata_check import Audit, load  # noqa: E402

SPEC = os.path.join(HERE, "audit.toml")

spec = load(SPEC)
audit = Audit(spec, root=ROOT)
results = audit.run()

group = None
for r in results:
    if r.group != group:
        group = r.group
        print("\n" + group)
    print(r.line())

# ------------------------------------------------- このリポジトリに固有のこと
print("\n配布物")

extra = []


def check(label, cond, detail=""):
    extra.append((label, bool(cond), detail))
    print("  %s  %s%s" % ("PASS" if cond else "FAIL", label,
                          ("  " + detail) if detail else ""))


declared = sorted(os.path.basename(s["path"]) for s in spec["source"])
actual = sorted(os.listdir(os.path.join(ROOT, "pdf")))
check("配布物は宣言した PDF 三本だけ", declared == actual, ", ".join(actual))
check("正誤表が「もう直せない」側と「直せる」側を分けている",
      "この項目は解決しません" in audit.document_text())

passed = sum(r.ok for r in results) + sum(1 for _, ok, _ in extra if ok)
failed = [r.label for r in results if not r.ok] + \
         [lab for lab, ok, _ in extra if not ok]

print("\n" + "-" * 58)
if failed:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failed)))
    for f in failed:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
