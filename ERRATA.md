# 正誤

三本の PDF には手を入れない方針です。**本文を書き換える代わりに、見つかった不備をここに記録します。**
どれも定理・証明・数値には影響しません。影響するのは、読者が正しい版に辿り着けるかどうかです。

最終更新: 2026年9月5日

---

## E1 — Series II と Series III が、改訂版 Series I を初版の DOI で引用している

**重大度: 高（読者が誤った版に辿り着く）**

| | |
| --- | --- |
| 該当 | Series II 参考文献 [1]、Series III 参考文献 [1] |
| 印字 | `Nemoto, T. (2026). ... (Revised Edition). Zenodo. DOI: 10.5281/zenodo.17173703.` |
| 正 | `DOI: 10.5281/zenodo.22058624` |

`10.5281/zenodo.17173703` は **2025年の初版**、つまりこの系列が訂正の対象としているものの DOI です。
書誌情報は `(Revised Edition)` かつ `(2026)` と、改訂版を指しています。**年・版と DOI が食い違っています。**

Series I 自身の冒頭は「原型（Nemoto, 2025; DOI: 10.5281/zenodo.17173703）を改訂する」と書いており、
こちらは正しい用法です。誤っているのは、II と III が**改訂版を指すつもりで初版の番号を書いている**点です。

この誤りをそのまま辿った読者は、II と III が「これを一般化する」と述べている定理の、
**撤回された方の版**を読むことになります。

---

## E2 — Series III の参考文献 [2]（Series II）に DOI がない

**重大度: 中**

| | |
| --- | --- |
| 該当 | Series III 参考文献 [2] |
| 印字 | `Nemoto, T. (2026). The Trinity-Infinity Framework, Series II: Extended Formalization and Further Illustrative Applications (Revised Edition). Zenodo.` |
| 正 | 末尾に `DOI: 10.5281/zenodo.22058777` を補う |

`Zenodo.` で終わっており、識別子がありません。同じ参考文献欄の [1] には DOI が付いているので、
書式の不統一でもあります。

---

## E3 — 各論文が同梱を謳う検証スクリプトが、配布物に含まれていない

**重大度: 中（再現性の主張が、そのままでは果たされていない）**

三本とも謝辞で、検証スクリプトが PDF と一緒に配布されていると述べています。

| 論文 | 印字されている記述 |
| --- | --- |
| Series I | 「the verification script (`series1_verification.py`) is distributed together with this PDF」 |
| Series II | 「the companion script `series2_verification.py`, distributed with this PDF, reproduces every number reported」 |
| Series III | 「the verification script (`series3_verification.py`) is distributed together with this PDF」 |

**著者の手元に届いた配布物は PDF のみで、三本のスクリプトはいずれも含まれていません。**
（掲載先の記録に添付されているかどうかは、このリポジトリからは確認していません。
確認できたのは、このリポジトリに収めた配布ファイルの中に無いことだけです。）

そのため、論文の数値を読者が確かめる手段が、記述どおりには提供されていません。

**このリポジトリでの扱い。** スクリプトを復元したり書き直したりはしていません
（手元に無いものを「これがそれです」と称して置くことはできません）。
代わりに [`verification/claims_audit.py`](verification/claims_audit.py) を別に書きました。
**三本の紙面に印字されている数値を一つずつ計算し直し、印字された値と並べて表示します。**
31 項目すべてが一致します。同梱スクリプトの代用ではなく、独立した突き合わせです。

元のスクリプトが見つかった場合は、`verification/as-published/` に、書き換えずそのまま収めます。

---

## 正誤ではないが、記録しておくこと

### N1 — Series I 定理1の不等号は、実際には等号

Series I の定理1は `‖Tₙ − T*‖ ≤ αⁿ‖T₀ − T*‖` と書いています。証明は正しく、不等号は**成り立ちます**。
ただし作用素の線形部分は α × 等長写像なので、**実際には等号が成り立ちます**
（[`verification/independent_check.py`](verification/independent_check.py) と
[`claims_audit.py`](verification/claims_audit.py) の両方で確認、24反復まで差 10⁻¹⁵ 以内）。

主張が弱く書かれているだけで、誤りではありません。定理の言い方として、より強い形が無償で手に入ります。

### N2 — Series II 定理1の「タイトな上界」は、作用素ノルムそのもの

Series II は縮小定数 maxᵢ aᵢ を「the bound tight」と述べ、証明は最大値を達成する座標に沿ってタイトだと
説明しています。これも正しいのですが、より簡潔に言えます。スペクトルノルムはユニタリ不変なので
**`‖DQ‖₂ = ‖D‖₂ = maxᵢ aᵢ`**。上界ではなく、作用素ノルムそのものです。

### N3 — 「98.7%」の出所の書き方

Series I 第2節 Remark 1 は、この数字を「the original Series II numerical-validation section」に
帰しています。Series III 第4節は、同じ数字を初期草稿群の主張として一般的に挙げています。
どちらも撤回された同じ主張を指していますが、**出所の書き方が二本のあいだで揃っていません。**

---

## 見つけ方

E1・E2 は三本の参考文献欄を突き合わせて見つけました。E3 は配布ファイルの一覧です。
N1・N2 は [`verification/independent_check.py`](verification/independent_check.py) が、
証明を独立に実装した副産物として示したものです。

**この文書自体は査読ではありません。** 見つかったものを記録しただけで、
「これ以外に不備がない」という主張ではありません。
