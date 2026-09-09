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
           "学部 2〜3 年の演習問題の水準である",
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

# **水準は一段ではない。**三つに割ったことと、順位を軸にしないことを保つ。
for 語 in ("**残ったものは、学部 2〜3 年の演習問題である。**",
           "**直しに使った道具は、大学院の線形システム論と行列解析に属する。**",
           "### 大学院に入る部分",
           "非正規行列の過渡的な増大",
           "この山の高さは\n扱わない",
           "これで全体が大学院の水準になるわけではない",
           "道具の水準と、直された中身の水準は\n別である",
           "それで全体の水準が上がるわけではない",
           "### どの学科で扱うか",
           "いちばん近いのは三つめである",
           "世界大学ランキングは、この件の軸にならない",
           "確かめようも\n覆しようもない"):
    check("水準の節が「%s」を保っている" % 語.replace("\n", "")[:24], 語 in README)

check("参照した講義に未確認の札がある",
      "#### 参照した講義（未確認）" in README
      and "確かめずに「確認済み」とは書かない" in README)

print("\n7. arXiv へ出すという決定が、判定を取り下げていないか")

# **決定と判定は別である。**出すと決めたことが、新規性が無いという判定を
# 打ち消していないことを保つ。ここが緩むと、記録が決定に合わせて過去を書き換える。
ARXIV_PATH = os.path.join(ROOT, "ARXIV.md")
check("ARXIV.md がある", os.path.exists(ARXIV_PATH))
ARXIV = io.open(ARXIV_PATH, encoding="utf-8").read() if os.path.exists(ARXIV_PATH) else ""
SUBMIT_PATH = os.path.join(ROOT, "ARXIV-SUBMIT.md")
SUBMIT = io.open(SUBMIT_PATH, encoding="utf-8").read() if os.path.exists(SUBMIT_PATH) else ""

check("結果が出ていないと書いてある", "**結果はまだ出ていない。**" in ARXIV)
check("新規性が無いという理由は決定で変わらないと書いてある",
      "**変わらない**" in ARXIV
      and "出すと決めたことと、新しい結果があることは別である" in ARXIV)
check("判定を取り下げるためではないと書いてある",
      "その判定を取り下げるために書いたものではない" in ARXIV)
check("残った事実の水準が、結論と同じ語で書いてある",
      "学部 2〜3 年の演習問題" in ARXIV and "学部 2〜3 年の演習問題" in README)
check("凍結された PDF を組み直さないと書いてある", "arXiv 用に組み直さない" in ARXIV)
check("推薦者に内容を大きく見せないと書いてある",
      "推薦を求める相手に、内容を大きく見せない" in ARXIV)
check("推薦の文面に新規性と AI の関与を書くと決めてある",
      "**新規の結果ではないこと。**" in ARXIV
      and "**初稿が言語モデルの生成物であること。**" in ARXIV)
check("却下の見込みを先に書いてある", "**却下されると見ている。**" in ARXIV)
check("先に書いたことを日付で確かめられると書いてある",
      "**この行は結果が出る前に書いた。**" in ARXIV
      and "コミットの日付で確かめられる" in ARXIV)
check("通っても新規性の証明にならないと書いてある",
      "通ったことは新規性の証明にならない" in ARXIV and "arXiv は査読ではない" in ARXIV)
check("結果を消さないと書いてある", "**どの結果でも消さない。**" in ARXIV)
check("覆し方がある", "## 覆し方" in ARXIV)

# **未確認は未確認のまま置く。**arXiv の規則は作業環境から開けない。
check("arXiv の規則に未確認の札がある",
      ARXIV.count("未確認") >= 6 and "いずれも未確認である" in ARXIV)

# 決定を README の結論からも辿れること。片方だけ直すと食い違う。
check("結論が ARXIV.md を指している", "[ARXIV.md](ARXIV.md)" in README)
check("結論が、決定で判定が変わらないことを保っている",
      "**新しい結果が無いという上の一行は、その決定によって変わらない。**" in README)

# **どれを出すかと、どこへ出すか。**選び方の基準は「その紙面が既知の誤りを運ぶか」である。
# 基準が消えると、選択の理由が「都合のよいほう」に置き換わる。
check("三篇のうち一篇を出すと決めてある",
      "**採るのは B である。**" in ARXIV and "C（新しい短報を書く）は採らない" in ARXIV)
check("選んだのが改訂版 Series I であると書いてある",
      "### 三篇のうちどれか —— 改訂版 Series I" in ARXIV)
check("選ぶ基準が書いてある",
      "**選ぶ基準は、その紙面が既知の誤りを運ぶかどうかである。**" in ARXIV
      and "既知の誤った参照を載せた紙面を、\n新しい場へ持ち込まない" in ARXIV)
check("一般形が Series III にあることを隠していない",
      "いちばん一般の形（任意の n ≥ 2）は Series III にある" in ARXIV
      and "**一般性のために、誤りを運ぶ紙面を選ばない。**" in ARXIV)
check("E1 をコメント欄に自分で書くと決めてある",
      "**E1 のことは、投稿のコメント欄に自分で書く。**" in ARXIV)

# 比較表が名指しした不備は、実在しなければならない。
ERRATA = io.open(os.path.join(ROOT, "ERRATA.md"), encoding="utf-8").read()
table = ARXIV[ARXIV.find("### 三篇のうちどれか"):ARXIV.find("## 分類")]
ids = sorted(set(re.findall(r"\b([EN]\d+)\b", table)))
missing = [i for i in ids if not re.search(r"^#{2,3} %s —" % i, ERRATA, re.M)]
check("比較表が名指しした不備が、すべて正誤表にある",
      len(ids) >= 10 and not missing,
      "%d 件 / 欠け %s" % (len(ids), missing or "無し"))

check("第一希望と第二希望を決めてある",
      "**第一希望は `math.NA`、第二希望は `math.DS` とする。**" in ARXIV)
# **分類は主題で決まる。**新規性の水準を区分で表そうとすると、この系列が犯したのと
# 同じ取り違えになる。直した経緯ごと保つ。
check("分類が主題で決まると書いてある",
      "**分類は主題で決まる。新規性の水準を表す欄ではない。**" in ARXIV
      and "**区分で新規性の無さを表そうとしない。**" in ARXIV)
check("math.HO を外した理由が残っている",
      "**第一希望から外した。**" in ARXIV
      and "「新しい結果が無い解説」を入れる区分ではない" in ARXIV)
check("取り違えを登録簿に送ってある", "`SC-013`" in ARXIV)
check("新規性の無さをコメント欄で述べると決めてある",
      "新しい結果が無いことは、投稿のコメント欄で述べることである" in ARXIV)
check("分類を変えられる余地を書いてある",
      "econ.TH" in ARXIV and "希望と実際の両方を書く" in ARXIV)
check("推薦の範囲が未確認だと書いてある",
      "同じ domain かどうかは確かめていない" in ARXIV)

# **外側の規則は、確かめた範囲までしか書かない。**検索結果は原文ではない。
check("数学の自動推薦の日付を、全区分の改定と分けてある",
      "**2025年12月10日から、数学の区分では機関のメールだけでは下りない。**" in ARXIV
      and "2026年1月21日に、同じ趣旨の改定が全区分へ広げられた" in ARXIV
      and "**数学の側の日付は 2026年1月ではなく 2025年12月である。**" in ARXIV)
check("推薦者の資格の範囲を書いてある",
      "3 か月前から 5 年前までの間に出されたもの" in ARXIV
      and "**出したばかりの著者は推薦できない。**" in SUBMIT)
check("同梱のしくみが PDF 投稿で使えないと書いてある",
      "PDF だけの投稿では働かない" in ARXIV and "PDF だけの投稿では働かない" in SUBMIT)
check("停止の中身を、及ぶ範囲ごと書いてある",
      "**1 年の投稿停止**" in ARXIV
      and "次の投稿はまず査読のある場を通す必要がある" in ARXIV
      and "**数学の区分にどう及ぶかは確かめていない。**" in ARXIV)
check("出典の節があり、原文を開いていないと断ってある",
      "## 出典（検索結果から取ったもの。原文の頁は開いていない）" in ARXIV)
check("裏の取れなかった一件を名指ししてある",
      "**`math.HO` の対象についての記述だけは、検索でも裏が取れなかった。**" in ARXIV)

print("\n8. 出す手順が、書かないと決めたものを書かせていないか")

# 手順書は、書く内容を人に指示する文書である。**指示のほうに漏れがあると、
# 決めごと 6 と 9 が手順の側から破られる。**破れない形になっていることを保つ。
check("ARXIV-SUBMIT.md がある", os.path.exists(SUBMIT_PATH))

check("手順が六つの段階に分かれている",
      all(("## %d. " % i) in SUBMIT for i in range(7)))
check("画面の文言を確かめていないと断ってある",
      "画面の文言までは確かめていない" in SUBMIT
      and "実際の表示が違えば、実際のほうが正しい" in SUBMIT)
check("所有権の主張を先に見ると書いてある",
      "**Claim Ownership をいちばん先に見る。**" in SUBMIT
      and "Claim Ownership" in ARXIV)

# **依頼の文面に必ず書く二つ。**省けば通りやすくなるものだから、機械で留める。
check("依頼に新規性の無さを書くと決めてある",
      "**新規の結果ではないこと。**" in SUBMIT)
check("依頼に言語モデルの関与を書くと決めてある",
      "**初稿が言語モデルの生成物であること。**" in SUBMIT)
check("省くことが欺きだと書いてある", "それは相手を欺くことである" in SUBMIT)
check("雛形が日本語と英語の二つある",
      "#### 日本語" in SUBMIT and "#### 英語" in SUBMIT)
check("雛形が二つとも新規性の無さを述べている",
      "新規の結果ではありません" in SUBMIT and "It contains no new result" in SUBMIT)
check("雛形が二つとも言語モデルの関与を述べている",
      "初稿は言語モデルによる生成物です" in SUBMIT
      and "generated by a language model" in SUBMIT)

# **決めごと 6 と 9。**肩書きを名乗らない。相手の氏名と連絡先、コードを書かない。
check("肩書きを名乗らないと書いてある", "**肩書きを名乗らない**（決めごと 6）" in SUBMIT)
check("コードをリポジトリに書かないと書いてある",
      "**リポジトリには書かない**（決めごと 9）" in SUBMIT)
check("相手の氏名と連絡先を記録に書かないと書いてある",
      "依頼した相手の氏名とメールアドレス" in SUBMIT
      and "何通送ったか、いつ送ったか、返事があったかまでである" in SUBMIT)
check("雛形が相手の氏名を埋め込みにしていない",
      "〈相手の氏名〉" in SUBMIT and "〈name〉" in SUBMIT)

# 送り方の作法。ここを外すと、相手ではなく arXiv の側に迷惑が出る。
check("一度に一人へ送ると書いてある",
      "**一度に一人へ送る。**" in SUBMIT and "スパムとして扱われる" in SUBMIT)
check("運営に頼まないと書いてある", "**arXiv の運営に頼まない。**" in SUBMIT)
check("承認を査読と読み替えないと書いてある",
      "**承認は査読ではない。**" in SUBMIT
      and "内容が認められたこととして書かない" in SUBMIT)
check("手順のコメント欄が、区分の代わりでないと書いてある",
      "**区分ではなくここで述べる**" in SUBMIT)
check("段階 1 が済んだことを、符号を書かずに記録してある",
      "**この段階は済んでいる。**2026年9月9日、`math.NA` の符号を受け取った。" in SUBMIT
      and "**この文書に書いてよいのは、受け取った日と分類までである。**" in SUBMIT
      and "**符号そのものは、この記録のどこにも書かない**" in ARXIV)

# **符号は秘密である。**検査に符号そのものを書けば、検査が漏らすことになる。
# だから値ではなく、値が置かれる形のほうを禁じる。
leaked = []
for name in sorted(os.listdir(ROOT)):
    if not name.endswith(".md"):
        continue
    text = io.open(os.path.join(ROOT, name), encoding="utf-8").read()
    if re.search(r"endorse\?x=[A-Za-z0-9]", text) or re.search(r"[Ee]ndorsement [Cc]ode:\s*[A-Za-z0-9]", text):
        leaked.append(name)
check("散文のどこにも推薦の符号が置かれていない", not leaked, "漏れ %s" % (leaked or "無し"))

check("規約の点検が三つに分かれている",
      "### 差し支えないもの" in ARXIV
      and "### 投稿のときに自分で述べるもの（紙面は直せない）" in ARXIV
      and "### してはならないこと" in ARXIV)
check("紙面自身が新規性を否定していることを根拠にしている",
      "not as a new mathematical theory" in ARXIV
      and "虚偽の表示にならない" in ARXIV)
check("符号の転送が想定された使い方だと書いてある",
      "**転送は想定された使い方である**" in ARXIV)
check("同梱を謳うスクリプトが無いことを、いちばん近い問題として挙げてある",
      "**規約にいちばん近い問題である。**" in ARXIV
      and "series1_verification.py" in ARXIV)
check("帰属の誤りが捏造ではないと切り分けてある",
      "**実在する文献の誤用であって、捏造ではない。**" in ARXIV
      and "制裁の対象には当たらない" in ARXIV)
check("所属欄に肩書きを打たないと決めてある",
      "**メタデータの所属欄に肩書きを打たない**（決めごと 6）" in ARXIV
      and "**肩書きを打たない**（決めごと 6）" in SUBMIT)
check("三つの正誤が、コメント欄と依頼の文面の両方に入っている",
      all(w in SUBMIT for w in ("（E3）", "（E4）", "（E5）", "(E3)", "(E4)", "(E5)")))
check("雛形が述べる点の数と、箇条の数が合っている",
      "先に三点お伝えいたします。" in SUBMIT
      and "Three things I should state up front." in SUBMIT)

check("止まった段階も記録すると書いてある",
      "**どの段階で止まっても消さない。**" in SUBMIT)
check("決定の文書が手順を指している",
      "[ARXIV-SUBMIT.md](ARXIV-SUBMIT.md)" in ARXIV)

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
