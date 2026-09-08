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

## E5 — Series I 第3節が、grim trigger の閾値を Fudenberg & Maskin に帰している

**重大度: 中（借りた先が違う）**

| | |
| --- | --- |
| 該当 | Series I 第3節、および参考文献 |
| 印字 | `This is a direct, closed-form application of the folk theorem for repeated games [Fudenberg & Maskin, 1986].` |
| 正 | Friedman, J. (1971). A Non-cooperative Equilibrium for Supergames. *Review of Economic Studies*, 38(1), 1–12 |

第3節がやっているのは、grim trigger を固定して**一回逸脱の誘因制約が binding になる
`δ` を閉形式で出す**ことである。ナッシュ復帰型スーパーゲームの標準論法であり、
Friedman (1971) が出所である。

Fudenberg & Maskin (1986) が示したのは別のことである。割引つきで、次元条件のもとに
**実現可能かつ個人合理的な利得集合の全体**が `δ → 1` で支持される、という
特徴づけである。**特定の戦略に対する閾値を定義していない。**

したがって、印字されている「computing **its** threshold」の `its` が指すものが、
Fudenberg & Maskin には存在しない。

**Series II 第4節での引用は正しい。**そちらは利得集合の特徴づけそのものを使っており、
Fudenberg & Maskin が出所である。**同じ文献が、一方では正しく、一方では誤って
引かれている。**

---

## E6 — バナッハの不動点定理が、三本のどの参考文献欄にも無い

**重大度: 中（いちばん重く借りたものが、いちばん引かれていない）**

| | |
| --- | --- |
| 該当 | Series I・II・III の参考文献欄 |
| 印字 | 本文: `the Banach fixed-point theorem gives existence, uniqueness, and the stated convergence rate`（Series I 定理1の証明）ほか |
| 正 | Banach, S. (1922). Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales. *Fundamenta Mathematicae*, 3, 133–181 |

三本すべてが、定理の証明の中でバナッハの不動点定理を名指しで使っている。
**三本すべての参考文献欄に、その項目が無い。**

| 論文 | 参考文献の件数 | 本文が名指しする定理・成果 | バナッハ |
| --- | --- | --- | --- |
| Series I | 2 | Banach、Löwenheim–Skolem、Henkin、Basel（Euler 1735）、Neumann 級数 | **無い** |
| Series II | 6 | Banach、folk theorem、Neumann 級数、グラフラプラシアン | **無い** |
| Series III | 2 | Banach | **無い** |

Series I は Euler 1735 も本文にのみ年号を置き、参考文献欄に項目が無い。

**この系列の方法は「証明したものと借りたものを区別する」である。**その借りたほうの
主軸が、三本とも欄に現れていない。README の出典 11 件はこの穴を後から埋めているが、
**紙面は埋まっていない。**

---

## E7 — Series II 第4節の例が、その二文前の条件を満たしていない

**重大度: 低（同じ節の中で条件と例が食い違う）**

| | |
| --- | --- |
| 該当 | Series II 第4節 |
| 印字（条件） | `every payoff profile in this hull with all three coordinates strictly above 2 is sustainable` |
| 印字（例） | `profiles such as (2,4,2) and their convex combinations with other individually-rational points are also eventually sustainable` |

`(2,4,2)` は第1座標と第3座標が **2 に等しい**。**「strictly above 2」を満たしていない。**
自分が二文前に置いた条件の外にある点を、その条件が保証する例として挙げている。

ミニマックス利得が 2 であることは同じ節が正しく導いている（`πD(0) = 2`）。
条件のほうも、例のほうも、単独では正しい。**組み合わせが成り立っていない。**

主張の中身は動かない。八点の凸包・体積 4.00・すべてが端点であることは
[`claims_audit.py`](verification/claims_audit.py) で確認済みである。

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

**一歩の話である。**漸近率は別で、そちらは maxᵢ aᵢ より真に小さい。N9 を見ること。

### N3 — 「98.7%」の出所の書き方

Series I 第2節 Remark 1 は、この数字を「the original Series II numerical-validation section」に
帰している。Series III 第4節は、同じ数字を初期草稿群の主張として一般的に挙げている。
どちらも撤回された同じ主張を指しているが、**出所の書き方が二本のあいだで揃っていない。**

### N4 — Series III の「三が特別な唯一の点」は、写像ではなく置換についての事実

Series III 第3.2節は、`n = 3` が構造的に区別される点を一つだけ挙げる。
**巡回置換が自己逆にならない最小の `n` である。**これは正しい。

続けてこう書いている。

> n=3 is the smallest n at which repeatedly permuting the roles is **not simply an
> oscillation between two states**

**これは置換 `σ` についての事実であって、反復 `f` についての事実ではない。**
`n = 2` でも `f` は振動しない。同じ論文の定理1が、`n = 2` を含む任意の `n ≥ 2` で
一意不動点へ幾何収束すると証明している。**力学系としては `n = 2` に退化は無い。**

したがって「the minimal interesting case **for this specific recursive structure**」は、
言い過ぎである。最小なのは**置換にとって**であり、**反復はそこに無関心**である。

誤りではない。読み方によっては通る。ただし**この論文の唯一の構造的主張**であり、
この系列は他の箇所ではこの種の区別に厳密である。ここだけ緩んでいる。

### N5 — 抽出した文字列に、確認できない箇所がある

Series III 第3.2節を PDF から取り出すと `Pn ≠ Pn−1` と出る。文脈からは
`Pₙ ≠ Pₙ⁻¹`（自己逆でない）を意味しているはずで、`Pₙ ≠ Pₙ₋₁`（n 次と n−1 次の
比較）では意味を成さない。

**これが紙面の誤植なのか、抽出の崩れなのかは確かめていない。**この作業環境には
PDF を画像に起こす道具が無く、**組版された頁を見ていない。**上付き・下付きが
抽出時に落ちることは、この系列で既に起きている（README に記載）。

**確かめてから、どちらかに振り分ける。**それまでは、ここに置いておく。

**独立の観察がある。**外部の査読（Stanford Agentic Reviewer、2026年9月）が、
この文書を渡されずに同じ箇所を挙げた —— `Pⁿ is a permutation matrix` が `P_n` の
意味に見えること、`P_n'` に不要なプライムがあること、`10-16` が `10⁻¹⁶` の
崩れであること。**ただしその査読も PDF から文字を取り出して読んでいるので、
同じ崩れを共有している可能性がある。**紙面の誤植であることの証拠にはならない。

### N6 — Series III 表1の「exact for n=2,3」は、算術の性質ではない

Series III 第3.1節は、閉形式の不動点への最大偏差について
`maximum deviation 1.1×10−16, machine precision, for every n ≥ 4; **exact for n=2,3**`
と書いている。

**偽ではない。**[`claims_audit.py`](verification/claims_audit.py) の固定した乱数種では、
`n = 2` も `n = 3` もちょうど `0.000e+00` になり、紙面どおりに再現する。

**だが算術の性質ではない。**基準点を別に引くと 0 でなくなる。
同じ検査の中で、**上の種は動かさずに**別の種で引き直すと `n = 2` で `5.551e-17` が出る。
有理数演算をしているわけではなく、丸めがそう落ちただけである。

**同じ表の中で、二つの 0 の意味が違う。**

| 列 | 0 の意味 |
| --- | --- |
| `isometry error` | **厳密。**置換行列の成分は 0 と 1 だけなので `PPᵀ − I` に誤差が入らない（`n = 2` から `8` まで `‖PPᵀ − I‖_F = 0.0`） |
| `max deviation from T*` | **丸め。**基準点の引き方に依る |

紙面は両方を同じ `0` と `exact` で書いており、**書き分けられていない。**
`within machine precision` と書けば足りた。

外部の査読（Stanford Agentic Reviewer、2026年9月）が、この文書を渡されずに
`exact` の書き方を問うた。**指摘は当たっている** —— ただし理由は査読が述べた
「浮動小数点だから 0 にならないはず」ではない。**このリポジトリの種では 0 になる。**
問題は 0 かどうかではなく、**0 が算術から出ているのか丸めから出ているのかが
書き分けられていないこと**である。

### N7 — Series III が、異方性版を一般の n で定義していない

Series III 定理1の証明は、最後にこう書く。

> The anisotropic version of Series II generalizes identically: for a=(a1,…,an),
> each ai ∈ (0,1), the same argument gives contraction constant maxi(ai).

**作用素そのものを書いていない。**`f(T) = D σₙ(T) + (I − D)p`（`D = diag(a₁,…,aₙ)`）を
明示せずに、縮小定数だけを述べている。Series II は `n = 3` について座標ごとの形で
書いているが、一般の `n` についての式は三本のどこにもない。

**等号と不等号の別も、そこで曖昧になる。**定理1の等式 `‖f(x)−f(y)‖ = α‖x−y‖` は
一様な `α` の場合である。異方性の場合は `‖D z‖ ≤ maxᵢ(aᵢ)‖z‖` で、**等号は
最大値を達成する座標に台が乗るときだけ**成り立つ。Series II 定理1は正しく
`≤` で書いている。Series III の「generalizes identically」は、そこを飛ばしている。

**ノルムも特定していない。**Series I は「under the Euclidean norm」と明記しているが、
Series III の定理1は `‖·‖` としか書かない。置換はどの `ℓᵖ` でも等長なので結論は
変わらないが、紙面には書かれていない。

外部の査読（Stanford Agentic Reviewer、2026年9月）による。

### N8 — Series I が確かめていない二つ

**① grim trigger が subgame perfect であることを述べていない。**

第3節は、経路上の一回逸脱の誘因制約だけを確認している（`VC ≥ VD` ⟺ `δ ≥ 1/2`）。
**罰則の側の信憑性を述べていない。**ここでは全員裏切りが段階ゲームのナッシュ均衡
（`πD(0) = 2` が三人とも最良応答）なので、ナッシュ復帰は信憑性を持ち、実際に
subgame perfect である。**紙面はそう言っていない。**

**独立に二度指摘されている。**こちらの読み直し（2026年9月8日）と、外部の査読
（Stanford Agentic Reviewer、同日）が、互いを知らずに同じ箇所を挙げた。
査読は `does not verify subgame perfection conditions in detail (e.g., one-shot
deviation principle under the specified trigger)` と述べている。

**② `I − αP` が可逆であることを述べていない。**

第2節 Remark 1 は閉形式 `T* = (1−α)(I−αP)⁻¹p` を使うが、**逆行列が存在する理由を
書いていない。**成り立つ —— `P` の固有値は絶対値 1 なので `ρ(αP) = α < 1` であり、
`I − αP` は可逆である。定理1の証明はバナッハだけで閉じているので、閉形式のほうに
一行足りない。

どちらも定理・数値には影響しない。**書かれていない、というだけである。**

### N9 — Series II の縮小率は上界であって、漸近率ではない

**この系列でいちばん重い見落としである。**

Series II 定理1は、不動点が `maxᵢ(aᵢ)ⁿ` の幾何率で到達されると述べる。
**一歩の縮小定数としては正しい**（N2 —— 作用素ノルムそのものである）。
**漸近率としては、ゆるい。**

`n` 巡回では次が厳密に成り立つ。

> `(DQ)ⁿ = (∏ᵢ aᵢ) · I`

`Q` が `n` 巡回で `D = diag(a)` なので、`n` 歩で各座標が全部の `aᵢ` を一度ずつ
掛けて元の位置に戻る。したがって `n` 歩ごとの誤差はちょうど `∏ᵢ aᵢ` 倍になり、
**漸近率はスペクトル半径 `ρ(DQ) = (∏ᵢ aᵢ)^{1/n}`、すなわち幾何平均**である。
`aᵢ` が全部等しいときを除いて、`maxᵢ aᵢ` より**真に小さい。**

論文の `a = (0.5, 0.7, 0.3)` で測った。

| | |
| --- | --- |
| `(DQ)³` | `0.105 · I`（誤差 `0.0e+00`） |
| `ρ(DQ)` | `0.471769398032` = `(0.105)^{1/3}` |
| `‖DQ‖₂ = maxᵢ aᵢ` | `0.700000000000` |
| 比 | `1.4838` |
| 30 反復での実際の誤差比 | `1.63e-10` |
| 紙面が名乗る `max(aᵢ)³⁰` | `2.25e-05` |

**5 桁ゆるい。**

**Series I にこの問題は無い。**`a` が一様なら `D = αI` で `DQ = αQ` は正規行列に
なり、`ρ = ‖·‖₂ = α` が一致する。**異方性にしたときに初めて開く。**

**この系列が訂正したと謳っているのと、同じ種類の混同である。**初版は
作用素ノルムで収束を語り、改訂版はそれを直した。だが改訂版の Series II は、
**収束の速さを作用素ノルムで語り続けている。**誤りではない —— 上界は成り立つ。
**訂正が一段浅い。**

正しい向きの事実は
[trinity-operator](https://github.com/cpsbvbng26-dotcom/trinity-operator) が
実装しており、[作用素のページ](https://cpsbvbng26-dotcom.github.io/cpsbvbng26-dotcom/trinity.html)
がその場で計算する。**紙面に無いのは、そこと繋がっていない。**

外部の査読（Stanford Agentic Reviewer、2026年9月）が、**この文書もリポジトリも
渡されずに `(DP)³ = (a₁a₂a₃)I` を導出した。**機械で当たっている
（[`independent_check.py`](verification/independent_check.py)、15 項目）。

### N10 — Series II が、凸包を実現可能集合とする根拠を述べていない

Series II 第4節は `The feasible set is the convex hull of the eight stage payoffs`
と述べる。**成り立つが、条件が要る** —— 段階利得の凸結合を実現するには、
公開ランダム化装置か、時間平均を許す定式化のどちらかが必要である。
**紙面はどちらも述べていない。**監視構造（完全監視か否か）も明示していない。

外部の査読（Stanford Agentic Reviewer、2026年9月）による。

---

## 見つけ方

E1・E2 は三本の参考文献欄を突き合わせて見つけた。E3 は配布ファイルの一覧と、著者への確認である。
**E5・E6・E7 と N4・N5 は、三本を通しで読み直して見つけた**（2026年9月8日）。
**N8 は、こちらの読み直しと外部の査読が、互いを知らずに同じ箇所を挙げたものである。**
**N9・N10 は外部の査読が出した。**N9 は、この系列でいちばん重い見落としである。
E6 は数え上げるだけなので、機械が当たっている —— 本文がバナッハを名指ししていること、
そして三本の参考文献欄にその項目が無いことを、PDF から取り出して確かめる。

**この文書が「印字されている」と述べていることは、[`verification/check_errata.py`](verification/check_errata.py)
が PDF から文字を取り出して突き合わせている。** 紙面には手を入れないので、動くとすれば正誤表の側である。
引用が一字でも合わなくなれば、そこで落ちる。E3 の六箇所を数え落としていたことも、これを書いて分かった。
N1・N2 は [`verification/independent_check.py`](verification/independent_check.py) が、
証明を独立に実装した副産物として示したものである。

**この文書自体は査読ではない。** 見つかったものを記録しただけで、
「これ以外に不備がない」という主張ではない。
