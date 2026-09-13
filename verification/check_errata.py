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
import re
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
      "この項目は解決しない" in audit.document_text())

# E6 —— バナッハが本文で使われ、参考文献欄に無いこと。
# 数え上げるだけなので機械で当たれる。参考文献欄は最後の References 以降とする。
_ref_heads = ("References", "参考文献")
_e6 = []
for _sid in ("I", "II", "III"):
    _text = audit._source_text(_sid)
    _i = max(_text.rfind(_h) for _h in _ref_heads)
    if _i < 0:
        _e6.append(_sid + " の参考文献欄が見つからない")
        continue
    _body, _refs = _text[:_i], _text[_i:]
    if "Banach" not in _body:
        _e6.append(_sid + " の本文が Banach を名指ししていない")
    if "Banach" in _refs:
        _e6.append(_sid + " の参考文献欄に Banach がある")
check("E6 —— 三本とも本文で Banach を使い、参考文献欄には無い",
      not _e6, "、".join(_e6) if _e6 else "3 本とも")

# E8 —— Series I が分野を名指しし、三本のどの欄にもその分野の文献が無いこと。
# **名指しは本文に、引用は欄に。**どちらか片方では、この項目の前提が立たない。
_野 = "consensus dynamics in distributed systems"
_合意 = ("DeGroot", "Friedkin", "Johnsen", "Abelson", "Hegselmann", "Krause",
       "Proskurnikov", "consensus", "opinion dynamic")
_e8 = []
if _野 not in audit._source_text("I"):
    _e8.append("Series I が分野を名指ししていない")
for _sid in ("I", "II", "III"):
    _text = audit._source_text(_sid)
    _i = max(_text.rfind(_h) for _h in _ref_heads)
    _refs = _text[_i:] if _i >= 0 else ""
    _hit = [n for n in _合意 if n.lower() in _refs.lower()]
    if _hit:
        _e8.append(_sid + " の参考文献欄に " + "、".join(_hit))
check("E8 —— Series I が分野を名指しし、三本とも欄にその分野が無い",
      not _e8, "、".join(_e8) if _e8 else "3 本とも")

# **照合はまだ付いていない。**付いていないことを、付いたかのように書かない。
_doc = audit.document_text()
check("E8 —— 照合が付いたことと、その書誌が書いてある",
      "## E8 — " in _doc
      and "### 照合 —— 重なった。そして、年号が二つある" in _doc
      and "Friedkin, N. E., & Johnsen, E. C. (1990)" in _doc
      and "Friedkin, N. E., & Johnsen, E. C. (1999)" in _doc
      and "10.1080/0022250X.1990.9990069" in _doc
      and "Advances in Group Processes*, 16, 1–29" in _doc
      and "`W` を巡回置換に限った既知の収束結果である" in _doc)

# **年号を一つにまとめない。**スカラーは 1990、対角は 1999。
# 主張の単位で当てないと、E8 の直しそのものが帰属の不精密を抱える。
check("E8 —— どの系列がどちらの年に当たるかを分けてある",
      "**Series I**（等方、`α` が一つ） | **Friedkin & Johnsen (1990)**" in _doc
      and "**Series II**（異方、座標ごとに `aᵢ`） | **Friedkin & Johnsen (1999)**" in _doc
      and "**スカラーと対角が、そのまま対応している**" in _doc)

# **収束の述べ方は同じではない。**字面で ρ を期待すると、誤った理由で落ちる。
check("E8 —— 収束の述べ方が級数形だと書いてある",
      "**収束の述べ方は、同じではない。**" in _doc
      and "幾何級数を直接足し上げて" in _doc
      and "**ノイマン級数である。**" in _doc
      and "矢印の向きも、二枚で逆である" in _doc)

# Series I 自身がノイマン級数を標準の道具として引いている。これは紙面から取れる。
_ni = "Neumann series" in audit._source_text("I")
check("E8 —— Series I がノイマン級数を引いていることが、紙面と合う",
      _ni and "Series I はそのノイマン級数を、自分で引いている" in _doc,
      "紙面にある" if _ni else "紙面に Neumann series が無い")

# **確かめた等級を三つに分けた。**他者の証言を、自分で確かめたことと同じ顔で並べない。
check("E8 —— 確かめた等級を三つに分けてある",
      "**紙面**（凍結された PDF から機械で取れる）" in _doc
      and "**検索で確認。原典には当たっていない**" in _doc
      and "**他者の証言**（原典を読んだと述べる者から受け取った。こちらは読んでいない）" in _doc
      and "**原典未読の札は外れていない。**" in _doc)

# **参考文献欄の抜けより重いのは、文献上の位置を述べる節の抜けである。**
# Series II 第1.1節は「どの文献の上にいるか」に答えるために置かれている。
_ii = audit._source_text("II")
_i11 = _ii.find("Position in the Literature")
_節 = _ii[_i11:_i11 + 700] if _i11 >= 0 else ""
_中 = [n for n in _合意 if n.lower() in _節.lower()]
check("E8 —— Series II の文献の節に、合意形成動学が無い",
      _i11 >= 0 and not _中,
      "節が見つからない" if _i11 < 0 else ("節に " + "、".join(_中) if _中 else "無い"))
check("E8 —— その節のことを正誤表が書いている",
      "Series II 第1.1節の題は `Position in the Literature` である" in _doc
      and "文献上の位置を述べる節そのものから" in _doc
      and "参考文献欄の抜けより重い" in _doc)

# **「全く同じではない」は、新規性を取り戻す道に見える。**そこを先に塞ぐ。
# 違いは二つが狭いほうへ、一つが広いほうへ。広いほうは定理にならない。
check("E8 —— 違いの向きを書いてある",
      "**同じではない。だが、違いの向きが悪い。**" in _doc
      and "収束の議論は `u` が何であるか" in _doc
      and "**一般化ではなく、名前の付け替えである。**" in _doc
      and "「違いがあるから新規である」は、ここでは成り立たない" in _doc)

# **確かめた範囲を、確かめていない範囲より広く書かない。**
# 式と書誌は検索で取れた。原典の本文は見ていない。そこを混ぜない。
check("E8 —— 原典に当たっていないと書いてある",
      "**検索で確認。原典には当たっていない**" in _doc
      and "こちらは読んでいない" in _doc
      and "外れるのは、本文をこちらで読んだときである" in _doc)

# 照合は正誤表の奥だけでなく、種別の表と経路にも出ていること。
_rd = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
_rt = open(os.path.join(ROOT, "ROUTE.md"), encoding="utf-8").read()
check("E8 —— 種別の表と経路が、照合先と原典未読を指している",
      all(x in _rd for x in ("Friedkin–Johnsen", "`E8`", "**原典未読**"))
      and all(x in _rt for x in ("Friedkin–Johnsen", "ERRATA E8", "**原典未読**")))

# README の英語欄は、日本語の本文と同じ DOI を、同じ位置づけで述べていなければ
# ならない。翻訳は二重管理になり、片方だけが古くなる。ここで縛る。
_en = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
_en = _en[_en.find("<summary><b>In English</b>"):]
_en = _en[:_en.find("</details>")]
_want = ["10.5281/zenodo.22058624", "10.5281/zenodo.22058777", "10.5281/zenodo.22058964"]
_bad = [d for d in _want if d not in _en]
_old = "10.5281/zenodo.17173703"
_superseded = "superseded" in _en and _old in _en
_notauthor = "AI is not an author" in _en
_notpeer = "not peer-reviewed" in _en
check("README の英語欄が、三本の DOI と旧版の扱いを述べている",
      not _bad and _superseded and _notauthor and _notpeer,
      "欠け: " + ", ".join(_bad) if _bad else
      ("旧版 superseded %s / AI is not an author %s / not peer-reviewed %s"
       % (_superseded, _notauthor, _notpeer)))

# 散文に「NN 項目」と書いたら、その NN を機械で確かめる。
# 実際に一度ずれている —— 51 と書いたまま中身が 60 になっていた。
# この検査自身も一件として数えるので、+1 する。
# ------------------------------------------------- arXiv へ出す紙面
# **散文が名乗る頁数と表題は、出す紙面そのものと突き合わせる。**
# 依頼のメールと投稿のコメント欄に載る数なので、ずれれば相手に嘘を言うことになる。
print("\narXiv へ出す紙面")

_submit = open(os.path.join(ROOT, "ARXIV-SUBMIT.md"), encoding="utf-8").read()
_series_i = os.path.join(ROOT, "pdf", "trinity-infinity-series-i-revised.pdf")
sys.modules.setdefault("cryptography", None)
from pypdf import PdfReader as _PdfReader
_reader = _PdfReader(_series_i)
_pages = len(_reader.pages)

_claimed_pages = [int(v) for v in
                  re.findall(r"添付の PDF\((\d+) ページ\)", _submit)
                  + re.findall(r"attached \((\d+) pages\)", _submit)
                  + re.findall(r"^(\d+) pages\. Expository", _submit, re.M)]
check("手順が名乗る頁数が、出す PDF の実際の頁数と一致する",
      len(_claimed_pages) == 3 and all(v == _pages for v in _claimed_pages),
      "実際 %d 頁 / 宣言 %s" % (_pages, _claimed_pages))

_title = re.search(r"\| Title \| `([^`]+)`", _submit)
_page1 = re.sub(r"\s+", " ", _reader.pages[0].extract_text() or "")
check("コメント欄に添える表題が、紙面の一頁目と一致する",
      _title is not None
      and _title.group(1).replace(" (Revised Edition)", "") in _page1,
      _title.group(1)[:48] + "…" if _title else "表題の欄が無い")

_CURRENT_DOI = "10.5281/zenodo.22058624"
_WITHDRAWN_DOI = "10.5281/zenodo.17173703"
check("添える DOI が、撤回された初版でなく改訂版である",
      _CURRENT_DOI in _submit and _WITHDRAWN_DOI not in _submit)

_comment = _submit[_submit.find("### コメント欄に入れる文面"):_submit.find("### その他の欄")]
check("コメント欄の文面が、三つの不備を述べている",
      all(w in _comment for w in ("series1_verification.py",
                                  "generated by a language model",
                                  "Friedman (1971)")))
check("コメント欄の文面が、新しい結果が無いことを述べている",
      "contains no new result" in _comment)

TOTAL = len(results) + len(extra) + 1
CLAIMS = [
    ("README.md", r"PDF から文字を取り出して突き合わせる \| (\d+) \|"),
    ("README.md", r"突き合わせる（(\d+) 項目）"),
    ("README.md", r"`check_errata\.py` \((\d+), needs pypdf\)"),
    ("verification/README.md", r"`check_errata\.py` \|[^|]*\| (\d+) \|"),
    ("verification/README.md", r"python3 check_errata\.py\s+# (\d+) 項目"),
    ("verification/README.md", r"突き合わせる（(\d+) 項目）"),
    (".github/workflows/verify.yml", r"正誤表の監査 (\d+) 項目"),
]
claimed = []
missing = []
for rel, pat in CLAIMS:
    text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    found = re.findall(pat, text)
    if not found:
        missing.append(rel + " の「" + pat + "」")
    claimed += [(rel, int(v)) for v in found]
wrong = [r + " が " + str(v) for r, v in claimed if v != TOTAL]
check("散文が名乗る件数が、実際に走った件数と一致する",
      not wrong and not missing,
      "実際 %d 件 / %s" % (TOTAL, ", ".join(wrong + missing) or "宣言 %d 箇所すべて一致" % len(claimed)))

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
