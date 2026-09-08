# 正誤

三本の PDF には手を入れない方針である。**本文を書き換える代わりに、見つかった不備をここに記録する。**
どれも定理・証明・数値には影響しない。影響するのは、読者が正しい版に辿り着けるかどうかである。

最終更新: 2026年9月8日

---

## E1 — Series II と Series III が、改訂版 Series I を初版の DOI で引用している

**重大度: 高（読者が誤った版に辿り着く）**

| | |
| --- | --- |
| 該当 | Series II 参考文献 [1]、Series III 参考文献 [1] |
| 印字 | `Nemoto, T. (2026). ... (Revised Edition). Zenodo. DOI: 10.5281/zenodo.17173703.` |
| 正 | `DOI: 10.5281/zenodo.22058624` |

`10.5281/zenodo.17173703` は **2025年の初版**、つまりこの系列が訂正の対象としているものの DOI である。
書誌情報は `(Revised Edition)` かつ `(2026)` と、改訂版を指している。**年・版と DOI が食い違っている。**

Series I 自身の冒頭は「原型（Nemoto, 2025; DOI: 10.5281/zenodo.17173703）を改訂する」と書いており、
こちらは正しい用法である。誤っているのは、II と III が**改訂版を指すつもりで初版の番号を書いている**点である。

この誤りをそのまま辿った読者は、II と III が「これを一般化する」と述べている定理の、
**撤回された方の版**を読むことになる。

---

## E2 — Series III の参考文献 [2]（Series II）に DOI がない

**重大度: 中**

| | |
| --- | --- |
| 該当 | Series III 参考文献 [2] |
| 印字 | `Nemoto, T. (2026). The Trinity-Infinity Framework, Series II: Extended Formalization and Further Illustrative Applications (Revised Edition). Zenodo.` |
| 正 | 末尾に `DOI: 10.5281/zenodo.22058777` を補う |

`Zenodo.` で終わっており、識別子がない。同じ参考文献欄の [1] には DOI が付いているので、
書式の不統一でもある。

---

## E3 — 各論文が同梱を謳う検証スクリプトは、存在しない

**重大度: 中（再現性の主張が、そのままでは果たされていない）**

三本とも、検証スクリプトが PDF と一緒に配布されていると述べている。**謝辞だけではない。
紙面を数え直したところ、合計 6 箇所あった。**

| 論文 | 箇所 | 印字されている記述（原文のまま） |
| --- | --- | --- |
| Series I | 第2節 | We verified both cases computationally (script series1_verification.py, included with this submission) |
| Series I | 謝辞 | the verification script (series1_verification.py) is distributed together with this PDF so the two results can be reproduced independently |
| Series II | 要旨 | All numerical claims are computed and included as a companion script |
| Series II | 第7節 | the companion script series2_verification.py, distributed with this PDF, reproduces every number reported |
| Series II | 謝辞 | the verification script (series2_verification.py) is distributed together with this PDF |
| Series III | 謝辞 | the verification script (series3_verification.py) is distributed together with this PDF |

**六箇所とも、指しているファイルは存在しない。** 配布物は PDF のみで、著者の手元にも残っていない
（2026年9月6日、著者に確認）。

以前この表には謝辞の三箇所しか載せていなかった。**約束は三度ではなく六度している。**
Series I 第2節の「included with this submission」と Series II 要旨の「included as a companion script」は、
謝辞よりも本文に近い場所にあり、読者がそこで再現を期待する記述である。数え落としていた
（2026年9月7日、`verification/check_errata.py` を書いて紙面から数え直したときに判明）。

以前この項目は「配布物に含まれていない」と書いていた。それだと「どこかにはあるかもしれない」と
読める。**そうではない。読者が入手できる場所は、どこにもない。**

つまり、**謝辞の記述は事実ではない。** 三本の論文の数値を、記述どおりの手段で確かめることは
できない。

**このリポジトリでの扱い。** 書き直したものを「これがそれである」と称して置くことはしない。
代わりに [`verification/claims_audit.py`](verification/claims_audit.py) を**別に**書いた。
**三本の紙面に印字されている数値を一つずつ計算し直し、印字された値と並べて表示す。**
31 項目すべてが一致する。

**これは同梱スクリプトの代わりではない。** 独立に書かれた突き合わせである。元のスクリプトが
何を計算していたかは、もう誰にも分からない。**分かるのは、紙面の数値が計算し直しても出る、
ということだけである。**

この項目は解決しない。**果たされなかった約束として残す。**

---

## E4 — 初稿の出所が、三本のどこにも書かれていない

**重大度: 高**

三本の開示文は、**改訂**について Claude の関与を述べている。

> This revision was prepared with drafting and mathematical-formalization assistance from Claude (Anthropic)

**「revision（改訂）」と書いてある。**

**初稿がどう作られたかは、三本のどこにも書かれていない。**

### 実際の経緯

**著者が持っていたのは、`Ⅲ∞` が指定する範囲までである** —— **三つのものを、
果てまで反復する**。`Ⅲ` は変数の個数（`n = 3`）を、`∞` は反復して極限をとることを
決めている。**対象の型は、記号がほぼ決めていた。**

**決めていないもののほうが多い。**写像そのもの（巡回置換と、固定した基準点への
凸結合）も、不動点が存在することも、収束することも、定理も、`Ⅲ∞` からは何も
出ない。**そこを当てはめたのは言語モデル（ChatGPT / OpenAI）で、その出力が
2025年10月の初版になった。**

**型は記号が、中身は言語モデルが。**これが線である。

### 記号の数学的な半分は、撤回された側である

`Ⅲ∞` のうち、数学的に中身があるのは `Ⅲ`（＝ 3）である。**それが、あとで意味が
無いと証明された側**である —— Series III が「任意の `n ≥ 2` で同じ証明が通る」と
示した。

一方 `∞` の側 —— **反復の極限** —— は残った。この系列で生き残った唯一の
数学的事実は、まさに**反復した先に一意の不動点がある**という主張である。

**`Ⅲ` は撤回され、`∞` は残った。**

```
記号 Ⅲ∞
  → 言語モデルに「これで数式を作れないか」と問う
  → 出力が初稿
  → 新規の枠組みとして公開（2025-10）
```

三本の開示文は Claude しか挙げておらず、**OpenAI も ChatGPT も一度も現れない。**

### なぜこれが効くか

この系列の中心にあるのは作用素 `x ← DQx + (I − D)p` である。**それが言語モデルの
出力である**という事実は、開示文が述べている「改訂の起草を手伝った」とは
まったく別の重さを持つ。

書かれていることは本当である。**書かれていないことがある**というだけである。
**不実記載ではなく、欠落である。**

これは撤回された内容の説明にもなる。再現できるコードのない「98.7%」、
ゲーム理論から気候政策まで広がる適用範囲、読むとおりには通らない証明 ——
**いずれも生成された文章に特徴的な形**で、人が捏造したのではなく、生成された
ものが検証されずに残ったものである。

### 規則には違反していない

三本はいずれも**自己登録のプレプリント**である。出版社も、投稿規程も、審査も、
契約もない。**当時、開示義務は存在しなかった。**

規範そのものは 2023 年前半から存在していたが、それらは投稿する論文に
掛かるものである。**この項目は違反の記録ではなく、記載の欠落の記録である。**

### 経路

段階ごとの記録は [ROUTE.md](ROUTE.md) にある。

**この項目は解決しない。**PDF は凍結されており、直せるのはこの正誤表のほうである。

---

## 正誤ではないが、記録しておくこと

### N1 — Series I 定理1の不等号は、実際には等号

Series I の定理1は `‖Tₙ − T*‖ ≤ αⁿ‖T₀ − T*‖` と書いている。証明は正しく、不等号は**成り立つ**。
ただし作用素の線形部分は α × 等長写像なので、**実際には等号が成り立つ**
（[`verification/independent_check.py`](verification/independent_check.py) と
[`claims_audit.py`](verification/claims_audit.py) の両方で確認、24反復まで差 10⁻¹⁵ 以内）。

主張が弱く書かれているだけで、誤りではない。定理の言い方として、より強い形が無償で手に入る。

### N2 — Series II 定理1の「タイトな上界」は、作用素ノルムそのもの

Series II は縮小定数 maxᵢ aᵢ を「the bound tight」と述べ、証明は最大値を達成する座標に沿ってタイトだと
説明している。これも正しいのであるが、より簡潔に言える。スペクトルノルムはユニタリ不変なので
**`‖DQ‖₂ = ‖D‖₂ = maxᵢ aᵢ`**。上界ではなく、作用素ノルムそのものである。

### N3 — 「98.7%」の出所の書き方

Series I 第2節 Remark 1 は、この数字を「the original Series II numerical-validation section」に
帰している。Series III 第4節は、同じ数字を初期草稿群の主張として一般的に挙げている。
どちらも撤回された同じ主張を指しているが、**出所の書き方が二本のあいだで揃っていない。**

---

## 見つけ方

E1・E2 は三本の参考文献欄を突き合わせて見つけた。E3 は配布ファイルの一覧と、著者への確認である。

**この文書が「印字されている」と述べていることは、[`verification/check_errata.py`](verification/check_errata.py)
が PDF から文字を取り出して突き合わせている。** 紙面には手を入れないので、動くとすれば正誤表の側である。
引用が一字でも合わなくなれば、そこで落ちる。E3 の六箇所を数え落としていたことも、これを書いて分かった。
N1・N2 は [`verification/independent_check.py`](verification/independent_check.py) が、
証明を独立に実装した副産物として示したものである。

**この文書自体は査読ではない。** 見つかったものを記録しただけで、
「これ以外に不備がない」という主張ではない。
