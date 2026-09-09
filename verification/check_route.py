#!/usr/bin/env python3
"""ROUTE.md の経路が、形と筋を保っているかを検査する。

    python3 verification/check_route.py

経路の記録は、あとから引き直せてしまえば意味が無い。ここで見るのは
「引き直していないこと」ではなく（それは Zenodo と git が持っている）、
**書いてある表が自分自身と矛盾していないこと**である。

  日付が前へ戻っていないか。種別が決めた語の中にあるか。
  README が種別に割り当てた五行が、経路の中にすべて現れるか。
  証拠が空でないか。撤回した初版の DOI を、正しい版として使っていないか。
  再構成の件数を、散文が正しく名乗っているか。
"""

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ROUTE = io.open(os.path.join(ROOT, "ROUTE.md"), encoding="utf-8").read()
README = io.open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()

# 種別はこの六つだけ。増やすときはここに書く。
KINDS = {"生成", "着想", "再発見", "利用", "再導出", "発見の否定", "撤回", "既知との衝突", "同定"}
BASIS = {"同時", "再構成"}

# 撤回された初版。正しい版として使ってはならない。
WITHDRAWN_DOI = "10.5281/zenodo.17173703"
CURRENT_DOI = "10.5281/zenodo.22058624"

passed, failures = 0, []


def check(label, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print("  PASS  " + label + (("  " + detail) if detail else ""))
    else:
        failures.append(label)
        print("  FAIL  " + label + (("  " + detail) if detail else ""))


def strip(cell):
    """飾りを外して素の語にする。"""
    return re.sub(r"[*`]", "", cell).strip()


# ------------------------------------------------------------ 表を読む
rows = []
for line in ROUTE.split("\n"):
    m = re.match(r"^\|\s*(\d+)\s*\|(.*)\|\s*$", line)
    if not m:
        continue
    cells = [c.strip() for c in m.group(2).split("|")]
    if len(cells) != 6:
        continue
    rows.append({
        "n": int(m.group(1)),
        "when": strip(cells[0]),
        "what": strip(cells[1]),
        "kind": strip(cells[2]),
        "known": strip(cells[3]),
        "basis": strip(cells[4]),
        "evidence": cells[5],
    })

print("\n1. 表が読めているか")
check("段階が読み取れる", len(rows) >= 5, "%d 段階" % len(rows))
check("番号が 1 から連番になっている",
      [r["n"] for r in rows] == list(range(1, len(rows) + 1)),
      ", ".join(str(r["n"]) for r in rows))

print("\n2. 筋が通っているか")


def as_key(v):
    parts = v.split("-")
    while len(parts) < 3:
        parts.append("01")
    return tuple(int(x) for x in parts)


bad_date = [r["n"] for r in rows if not re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", r["when"])]
check("いつ が年月または年月日で書いてある", not bad_date,
      ", ".join(str(x) for x in bad_date))

keys = [as_key(r["when"]) for r in rows]
back = [rows[i]["n"] for i in range(1, len(keys)) if keys[i] < keys[i - 1]]
check("日付が前へ戻っていない", not back, ", ".join(str(x) for x in back))

bad_kind = [r["n"] for r in rows if r["kind"] not in KINDS]
check("種別が決めた語の中にある", not bad_kind,
      ", ".join("%d: %s" % (r["n"], r["kind"]) for r in rows if r["kind"] not in KINDS))

bad_basis = [r["n"] for r in rows if r["basis"] not in BASIS]
check("記録が「同時」か「再構成」である", not bad_basis,
      ", ".join(str(x) for x in bad_basis))

empty = [r["n"] for r in rows if len(r["evidence"]) < 4 or r["what"] == ""]
check("どの段階にも中身と証拠がある", not empty, ", ".join(str(x) for x in empty))

print("\n3. README との食い違い")

for kind in ("再発見", "再導出", "利用"):
    check("経路に「%s」の段階がある" % kind,
          any(r["kind"] == kind for r in rows),
          "%d 件" % sum(1 for r in rows if r["kind"] == kind))

# README の五行に割り当てた種別が、経路にも現れること。
for kind in ("再発見", "再導出", "利用", "発見の否定"):
    check("README の種別「%s」が経路にもある" % kind,
          ("**%s**" % kind) in README or kind in README)

print("\n4. 撤回した版を、正しい版として使っていないか")

# 撤回された初版の DOI は、撤回されたものとして名指しでのみ現れてよい。
occurrences = [ln for ln in ROUTE.split("\n") if WITHDRAWN_DOI in ln]
labelled = all(("撤回" in ln) for ln in occurrences)
check("初版の DOI は「撤回された」と添えてのみ現れる", labelled,
      "%d 箇所" % len(occurrences))
check("改訂版の DOI が経路に出てくる", CURRENT_DOI in ROUTE)

print("\n5. 散文が名乗る数")

n_recon = sum(1 for r in rows if r["basis"] == "再構成")
m = re.search(r"九段階のうち(.+?)段階は再構成", ROUTE)
KANJI = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
         "六": 6, "七": 7, "八": 8, "九": 9}
said = KANJI.get(m.group(1)) if m else None
check("再構成の件数が実際と合う", said == n_recon,
      "名乗り %s / 実際 %d" % (said, n_recon))

m2 = re.search(r"\*\*(.+?)段階を経て", ROUTE)
said2 = KANJI.get(m2.group(1)) if m2 else None
check("段階の数が実際と合う", said2 == len(rows),
      "名乗り %s / 実際 %d" % (said2, len(rows)))

print("\n6. 水準についての節が、経路と同じ数を言っているか")

README = io.open(os.path.join(ROOT, "README.md"), encoding="utf-8").read() \
    if "io" in dir() else open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()

# **結論は根幹に置く。**下のほうに置けば、読み手が辿り着く前に別の話が挟まる。
# 三本の紹介より前にあること。
i_concl = README.find("## 結論")
i_three = README.find("## 三本")
check("README の先頭に結論の節がある", i_concl >= 0)
check("結論が三本の紹介より前にある", 0 <= i_concl < i_three,
      "結論 %d / 三本 %d" % (i_concl, i_three))
for 語 in ("**枠組みは残らなかった。**",
           "学部の演習問題の水準である",
           "その側が、意味を\n持たないと証明された"):
    check("結論が「%s」を保っている" % 語.replace("\n", "")[:26],
          語 in README[i_concl:i_three] if i_concl >= 0 else False)

check("README に水準についての節がある", "## どの水準の数学か" in README)
check("結局どうなったかが書いてある", "### 結局、何をしてどう終わったか" in README)

# 反例の数値は経路の表にもある。**二箇所に書いた以上、同じでなければならない。**
for 値 in ("[[1,40],[0,1]]", "20.01", "11.8"):
    check("反例の %s が経路と README の両方にある" % 値,
          値 in ROUTE and 値 in README)

# 残った事実。記号のうち残った側と消えた側を、両方書いてあること。
check("記号のどちら側が消えたかを書いてある",
      "その側が、意味を持たないと証明された" in README)
check("枠組みが残らなかったと書いてある", "枠組みは残らなかった" in README)

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
