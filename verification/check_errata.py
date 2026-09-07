#!/usr/bin/env python3
"""ERRATA.md が「印字されている」と述べていることを、PDF から取り出して突き合わせる。

    pip install pypdf
    python3 verification/check_errata.py

正誤表は、紙面に何が印字されているかを引用して成り立っています。**引用が正しく
なければ、正誤表そのものが誤りになります。** 紙面には手を入れない方針なので、
紙面のほうが動くことはありません。動くのは正誤表の側です。だからこちらを縛ります。

確かめるのは次の四つです。

    E1  改訂版を指すつもりで初版の DOI を引いている箇所が、実際にその通り印字されているか
    E2  Series III の参考文献 [2] に、本当に DOI が無いか
    E3  同梱を謳う記述が、実際にその通り印字されているか。**そして何箇所あるか**
        （謳っているのは三箇所ではありません。六箇所です）
        あわせて、謳われているファイルがこのリポジトリに無いこと

    最終更新の日付が、本文に書かれたどの日付よりも古くなっていないか

PDF は暗号化されていないので、pypdf の暗号処理は要りません。この環境では
cryptography の読み込みが壊れることがあるため、先に塞いでから読み込みます。
"""

import os
import re
import sys

sys.modules.setdefault("cryptography", None)   # 暗号化されていない PDF なので要らない

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf が要ります: pip install pypdf")
    raise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
passed, failures = 0, []


def check(label, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print("  PASS  " + label + (("  " + detail) if detail else ""))
    else:
        failures.append(label)
        print("  FAIL  " + label + (("  " + detail) if detail else ""))


def section(s):
    print("\n" + s)


def flat(s):
    """空白の入り方は取り出し方で変わる。比較の前に潰す。"""
    return re.sub(r"\s+", " ", s).strip()


PDFS = {
    "Series I": "trinity-infinity-series-i-revised.pdf",
    "Series II": "trinity-infinity-series-ii-revised.pdf",
    "Series III": "trinity-infinity-series-iii.pdf",
}
text = {}
for name, fn in PDFS.items():
    path = os.path.join(ROOT, "pdf", fn)
    text[name] = flat("\n".join(
        (page.extract_text() or "") for page in PdfReader(path).pages))

errata = open(os.path.join(ROOT, "ERRATA.md"), encoding="utf-8").read()
errata_flat = flat(errata)

# ------------------------------------------------------------------ E3
section("E3 — 同梱を謳う記述")

# 紙面に印字されている全ての箇所。謝辞だけではない。
PROMISES = [
    ("Series I", "第2節",
     "We verified both cases computationally (script series1_verification.py, "
     "included with this submission)"),
    ("Series I", "謝辞",
     "the verification script (series1_verification.py) is distributed together "
     "with this PDF so the two results can be reproduced independently"),
    ("Series II", "要旨",
     "All numerical claims are computed and included as a companion script"),
    ("Series II", "第7節",
     "the companion script series2_verification.py, distributed with this PDF, "
     "reproduces every number reported"),
    ("Series II", "謝辞",
     "the verification script (series2_verification.py) is distributed together "
     "with this PDF"),
    ("Series III", "謝辞",
     "the verification script (series3_verification.py) is distributed together "
     "with this PDF"),
]

for paper, where, quote in PROMISES:
    check("%s %s の記述が紙面にある" % (paper, where), flat(quote) in text[paper],
          quote[:56] + "…")
    check("その記述が ERRATA.md にも引用されている", flat(quote) in errata_flat)

check("謳われている箇所は 6 つで、ERRATA.md もそう述べている",
      "6 箇所" in errata, "三箇所ではありません")

# 実際に無いこと。あったら E3 は成り立ちません。
missing = []
for n in (1, 2, 3):
    name = "series%d_verification.py" % n
    found = [os.path.relpath(os.path.join(dp, f), ROOT)
             for dp, _, fs in os.walk(ROOT) for f in fs
             if f == name and ".git" not in dp]
    missing.append((name, found))
for name, found in missing:
    check("%s がこのリポジトリに無い" % name, not found,
          "見つかった: %s" % found if found else "")

check("配布物は PDF 三本だけ",
      sorted(os.listdir(os.path.join(ROOT, "pdf"))) == sorted(PDFS.values()),
      ", ".join(sorted(os.listdir(os.path.join(ROOT, "pdf")))))

# ------------------------------------------------------------------ E1
section("E1 — 改訂版を指すつもりで初版の DOI を引いている")

OLD, NEW = "10.5281/zenodo.17173703", "10.5281/zenodo.22058624"
for paper in ("Series II", "Series III"):
    check("%s の参考文献に「(Revised Edition). Zenodo. DOI: %s」が印字されている"
          % (paper, OLD),
          "(Revised Edition). Zenodo. DOI: " + OLD in text[paper])
    check("%s は正しい DOI %s をどこにも印字していない" % (paper, NEW),
          NEW not in text[paper])
check("Series I 自身は初版を指して初版の DOI を引いている（こちらは正しい用法）",
      "This edition revises the original preprint (Nemoto, 2025; DOI: "
      + OLD + ")" in text["Series I"])
check("ERRATA.md が両方の DOI を挙げている", OLD in errata and NEW in errata)

# ------------------------------------------------------------------ E2
section("E2 — Series III の参考文献 [2] に DOI が無い")

REF2 = ("Nemoto, T. (2026). The Trinity-Infinity Framework, Series II: Extended "
        "Formalization and Further Illustrative Applications (Revised Edition). Zenodo.")
i = text["Series III"].find(flat(REF2))
check("その参考文献が印字されている", i >= 0)
if i >= 0:
    after = text["Series III"][i + len(flat(REF2)): i + len(flat(REF2)) + 40]
    check("直後に DOI が続いていない", not after.lstrip().startswith("DOI"),
          "直後の文字列「%s」" % after[:36])
check("ERRATA.md が補うべき DOI を挙げている", "10.5281/zenodo.22058777" in errata)

# ------------------------------------------------------- 最終更新の日付
section("日付")

head = re.search(r"最終更新: (\d{4})年(\d{1,2})月(\d{1,2})日", errata)
check("最終更新の日付が書いてある", bool(head))
if head:
    stamp = tuple(int(g) for g in head.groups())
    inner = [tuple(int(g) for g in m)
             for m in re.findall(r"(\d{4})年(\d{1,2})月(\d{1,2})日", errata)]
    newest = max(inner)
    check("最終更新が、本文に書かれたどの日付よりも古くない", stamp >= newest,
          "最終更新 %d年%d月%d日 / 本文の最新 %d年%d月%d日" % (stamp + newest))

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
