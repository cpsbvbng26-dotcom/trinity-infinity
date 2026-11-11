#!/usr/bin/env python3
"""README の札と位置づけ、前提の一覧、年表、保存版の関連識別子を当たる。

    python3 verification/check_pages.py

pypdf が要る（前提の一覧が引く紙面の文を、PDF から取り出して照合するため）。
隣に trinity-operator の写しが要る。場所は環境変数 TRINITY_OPERATOR で渡せる。
渡さなければ、このリポジトリと同じ階層の trinity-operator を読む。
CI は trinity-operator を別に checkout して、その場所を渡している。

見るもの。
  1. README の冒頭の札（種類と状態）と、思考実験としての位置づけの一文。
  2. 学部一年次までの成果で、紙面は凍結している、と書いてあること。
  3. CITATION.cff の type と、.zenodo.json の関連識別子。
  4. ASSUMPTIONS.md の表。紙面の文が PDF に一字一句あるか、展望の段の語が
     trinity-operator の README と同じか、番号が欠けていないか。
  5. TIMELINE.md の表。日付が出典の文書に書いてあるか、古い順か。
"""

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OPERATOR = os.environ.get("TRINITY_OPERATOR") or os.path.join(os.path.dirname(ROOT), "trinity-operator")

passed, failures = 0, []


def check(label, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print("  PASS  " + label + (("  " + detail) if detail else ""))
    else:
        failures.append(label)
        print("  FAIL  " + label + (("  " + detail) if detail else ""))


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def table(text, first=r"\d+"):
    """先頭の欄が first に合う表の行を、欄の並びで返す。"""
    rows = []
    for line in text.split("\n"):
        m = re.match(r"^\|\s*(" + first + r")\s*\|(.*)\|\s*$", line)
        if m:
            rows.append([m.group(1)] + [c.strip() for c in m.group(2).split("|")])
    return rows


README = read(os.path.join(ROOT, "README.md"))
CITATION = read(os.path.join(ROOT, "CITATION.cff"))
ZENODO = json.loads(read(os.path.join(ROOT, ".zenodo.json")))
ASSUMPTIONS = read(os.path.join(ROOT, "ASSUMPTIONS.md"))
TIMELINE = read(os.path.join(ROOT, "TIMELINE.md"))

# 目録（cpsbvbng26-dotcom）が決めた札。ここを変えるときは目録と一緒に変える。
TYPE_JA, STATUS_JA = "思考実験・予想", "凍結"
TYPE_EN, STATUS_EN = "Thought experiment and conjecture", "Frozen"
CFF_TYPE = "dataset"


# ------------------------------------------------------------ 1. 冒頭
print("\n1. README の冒頭")
lines = README.split("\n")
check("見出しの直下（空行を一つ挟んで）に札がある",
      len(lines) > 2 and lines[0].startswith("# ") and lines[1] == ""
      and lines[2] == "種類：%s　状態：%s" % (TYPE_JA, STATUS_JA),
      repr(lines[2]) if len(lines) > 2 else "")
check("英語の欄にも同じ札がある",
      "Type: %s · Status: %s" % (TYPE_EN, STATUS_EN) in README)

head = "\n".join(lines[:12])
pos = re.search(r"^この系列は思考実験（概念モデル）であり、[^\n]*$", head, re.M)
check("冒頭に、思考実験（概念モデル）として位置づける一文がある", pos is not None)
if pos:
    s = pos.group(0)
    check("その一文が、主張することと主張しないことを両方書いている",
          "主張するのは" in s and "主張せず" in s)
    check("その一文は一文のまま（句点が末尾の一つだけ）",
          s.count("。") == 1 and s.endswith("。"), "%d 個" % s.count("。"))

# ------------------------------------------------------------ 2. 学部一年次
print("\n2. 学部一年次までの成果で、紙面は凍結している")
FIRST = "三篇は、学部一年次までに独学で進めた成果です。"
check("README の冒頭に書いてある", FIRST in head)
check("凍結が紙面についての決めだと書いてある",
      "PDF は凍結しており、改変も再生成もしません。" in head
      and "正誤表と検査は、これからも書き足します。" in head)
check("英語の欄にも書いてある",
      "self-study completed by the end of the\nauthor's first undergraduate year" in README
      and "The three PDFs are frozen." in README)
check("年表にも書いてある", FIRST in TIMELINE)
check("英語の欄が、検査の注釈が日本語であることを断っている",
      "comments, docstrings and printed messages are in Japanese" in README)

# ------------------------------------------------------------ 3. 引用情報
print("\n3. CITATION.cff と .zenodo.json")
m = re.search(r"^type:\s*(\S+)\s*$", CITATION, re.M)
check("CITATION.cff の type が %s" % CFF_TYPE, m is not None and m.group(1) == CFF_TYPE,
      m.group(1) if m else "type が無い")

i = README.find("## 三本")
papers = re.findall(r"10\.5281/zenodo\.\d+", README[i:README.find("\n## ", i + 3)]) if i >= 0 else []
papers = sorted(set(papers))
rel = ZENODO.get("related_identifiers", [])
check("README の三本の表から、論文の DOI が三つ読める", len(papers) == 3, ", ".join(papers))
for doi in papers:
    check("保存版が %s を isSupplementTo で指している" % doi,
          any(r.get("identifier") == doi and r.get("relation") == "isSupplementTo" for r in rel))
for r in rel:
    check("関連識別子 %s は README に書いてある番号である" % r.get("identifier"),
          r.get("identifier", "") in README)
    check("関連識別子 %s の関係は isSupplementTo か isDerivedFrom" % r.get("identifier"),
          r.get("relation") in ("isSupplementTo", "isDerivedFrom"), r.get("relation", ""))
check("撤回された初版の DOI を、補う相手に挙げていない",
      all(r.get("identifier") != "10.5281/zenodo.17173703" for r in rel))

# ------------------------------------------------------------ 4. 前提の一覧
print("\n4. ASSUMPTIONS.md")
PDFS = {
    "Series I": "trinity-infinity-series-i-revised.pdf",
    "Series II": "trinity-infinity-series-ii-revised.pdf",
    "Series III": "trinity-infinity-series-iii.pdf",
}


def flat(s):
    return re.sub(r"\s+", " ", s).strip()


TEXT = {}
try:
    from pypdf import PdfReader
    for name, f in PDFS.items():
        reader = PdfReader(os.path.join(ROOT, "pdf", f))
        TEXT[name] = flat("\n".join(p.extract_text() or "" for p in reader.pages))
    check("三篇の PDF から文字を取り出せた", all(TEXT.values()))
except ImportError:
    check("pypdf が入っている", False, "pip install -r requirements.txt")

rows = table(ASSUMPTIONS)
check("前提の表がある", len(rows) > 0, "%d 行" % len(rows))
check("番号が 1 から欠けずに並んでいる",
      [int(r[0]) for r in rows] == list(range(1, len(rows) + 1)))
check("どの行も六つの欄を持つ", all(len(r) == 6 for r in rows))

quotes = []
for r in rows:
    if len(r) != 6:
        continue
    for col in (r[2], r[5]):
        for name, q in re.findall(r"(Series I{1,3})：`([^`]+)`", col):
            quotes.append((r[0], name, q))
check("紙面の文を引いている", len(quotes) > 0, "%d 箇所" % len(quotes))
if TEXT:
    for n, name, q in quotes:
        check("前提 %s：%s に「%s」がある" % (n, name, q[:40]), flat(q) in TEXT.get(name, ""))
for r in rows:
    if len(r) == 6 and not re.search(r"Series I{1,3}：`", r[2]):
        check("前提 %s：紙面の文が無いことを、その欄で断っている" % r[0], "紙面に無い" in r[2])

op_readme_path = os.path.join(OPERATOR, "README.md")
have_op = os.path.exists(op_readme_path)
check("trinity-operator の写しがある", have_op, OPERATOR)
if have_op:
    OP = read(op_readme_path)
    stages = {}
    for line in OP.split("\n"):
        mm = re.match(r"^\|\s*([1-6])\s*\|\s*([^|]+?)\s*\|", line)
        if mm:
            stages[mm.group(1)] = re.sub(r"[`*]", "", mm.group(2))
    check("trinity-operator の README に展望の表（段 1〜6）がある", len(stages) == 6)
    for r in rows:
        if len(r) != 6:
            continue
        mm = re.match(r"段 ([1-6])：(.+)$", r[3])
        if mm:
            check("前提 %s：段 %s の語が展望の表と同じ" % (r[0], mm.group(1)),
                  stages.get(mm.group(1)) == mm.group(2),
                  "展望の表は「%s」" % stages.get(mm.group(1)))
    used = {re.match(r"段 ([1-6])：", r[3]).group(1) for r in rows
            if len(r) == 6 and re.match(r"段 ([1-6])：", r[3])}
    check("段 1 を載せない理由を書いている",
          "1" not in used and "これは `certificate.py` の決め打ちで、三篇の前提ではありません。" in ASSUMPTIONS)
    check("段 2〜6 がすべて表にある", used == {"2", "3", "4", "5", "6"}, ", ".join(sorted(used)))

# ------------------------------------------------------------ 5. 年表
print("\n5. TIMELINE.md")


def forms(date):
    """2026-09-06 は「2026年9月6日」とも書かれる。どちらかが出典にあればよい。"""
    out = [date]
    p = date.split("-")
    if len(p) == 3:
        out.append("%s年%d月%d日" % (p[0], int(p[1]), int(p[2])))
    elif len(p) == 2:
        out.append("%s年%d月" % (p[0], int(p[1])))
    return out


trows = table(TIMELINE, r"\d{4}-\d{2}(?:-\d{2})?")
check("年表の行がある", len(trows) > 0, "%d 行" % len(trows))
dates = [r[0] for r in trows]
check("日付が古い順に並んでいる", dates == sorted(dates))
for r in trows:
    links = re.findall(r"\]\(([^)]+)\)", r[-1])
    if not links:
        check("%s：出典がある" % r[0], False)
        continue
    target = links[0].split("#")[0]
    if target.startswith("https://github.com/cpsbvbng26-dotcom/trinity-operator/blob/main/"):
        path = os.path.join(OPERATOR, target.split("/blob/main/", 1)[1])
    elif target.startswith("http"):
        check("%s：出典がこのリポジトリか trinity-operator の文書" % r[0], False, target)
        continue
    else:
        path = os.path.join(ROOT, target)
    if not os.path.exists(path):
        check("%s：出典 %s がある" % (r[0], target), False)
        continue
    body = read(path)
    check("%s：日付が出典 %s に書いてある" % (r[0], target.replace("https://github.com/cpsbvbng26-dotcom/", "")),
          any(f in body for f in forms(r[0])))

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
