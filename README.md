# Trinity-Infinity

[![検証](https://github.com/cpsbvbng26-dotcom/trinity-infinity/actions/workflows/verify.yml/badge.svg)](https://github.com/cpsbvbng26-dotcom/trinity-infinity/actions/workflows/verify.yml)

> [!IMPORTANT]
> **改訂版 Series I を引用するときの DOI は `10.5281/zenodo.22058624` です。**
> Series II と Series III の参考文献欄は、改訂版を指すつもりで
> `10.5281/zenodo.17173703` と書いています。これは**この系列が訂正の対象としている
> 2025年の初版**の DOI です。そのまま辿ると、II と III が「これを一般化する」と
> 述べている定理の、撤回された方の版に着きます。詳細は [ERRATA.md](ERRATA.md) の E1。

三本の系列です。**枠組みを提示した系列ではなく、枠組みが自分を検証にかけて縮んでいく系列**として読むのが正確です。

2025年に発表した最初のプレプリントは、三つの要素が再帰的に統合されて収束するという着想を軸に、
ゲーム理論・数理論理学・機械工学、そして AI アライメントや気候政策への応用まで主張していました。
2026年8月の改訂で、二つの条件を課して書き直しています。

1. **定理は、書かれたとおりに証明できること。** 「趣旨としては証明できる」「直せば証明できる」ではなく、読者が読むとおりに
2. **数値は、同梱するコードが出したものであること。** 記憶している実行結果でも、もっともらしい見積もりでもなく

どちらも厳しい条件ではありません。本来すでに満たされているべきものです。**この系列が記録として意味を持つのは、
それを満たさなかった部分がどれだけあったかのほうです。**

## 三本

| | 内容 | 版 | DOI |
| --- | --- | --- | --- |
| [Series I](pdf/trinity-infinity-series-i-revised.pdf) | 巡回置換つきアフィン反復と、その収束定理。ゲーム理論・論理学・工学への例示 | 改訂版 — 2026年8月 | [**10.5281/zenodo.22058624**](https://doi.org/10.5281/zenodo.22058624)<br>← II・III の参考文献欄はここを誤っています |
| [Series II](pdf/trinity-infinity-series-ii-revised.pdf) | 座標ごとに異なる混合率への一般化。均衡利得集合と、ばね系の完全な計算例 | 改訂版 — 2026年8月 | [10.5281/zenodo.22058777](https://doi.org/10.5281/zenodo.22058777) |
| [Series III](pdf/trinity-infinity-series-iii.pdf) | 「三である必要はあるのか」への回答と、系列全体の回顧 | 2026年8月 | [10.5281/zenodo.22058964](https://doi.org/10.5281/zenodo.22058964) |

本文は PDF のままです。**Markdown への書き起こしはしていません** —— 数式の下付き文字が抽出時に別行へ分解されるため、
起こすには数式を組み直す必要があり、それは論文を変えることになるからです。

## 確立されたこと

三本を通して残った数学的事実は、ひとつです。

> 座標の置換と、固定した基準点への統合とを合成した作用素は縮小写像であり、
> したがってバナッハの不動点定理により、唯一の不動点へ幾何的に収束する。

Series I がこれを三要素・一様な混合率について証明し、Series II が混合率を座標ごとに変えても成り立つことを示し、
Series III が**そもそも三要素である必要がなかったこと**（任意の n ≥ 2 で同じ証明が通る）を示しました。

n = 3 が区別されるのは一点だけです。**巡回置換がそれ自身の逆写像にならない最小の n である**こと。
Series III はこの事実を特定したうえで、それが「三」の文化的・哲学的な含意を正当化しないことを明示的に否定しています。

これ以外の内容は、すべて (a) 他分野の既知の結果を正しく計算した実例か、
(b) 類推または未証明の推測として明示的に印をつけたもの、のいずれかです。

## 数学的再発見として

この系列で起きたことには名前があります。**数学的再発見**です。
そこへ至る九段階は [ROUTE.md](ROUTE.md) に刻んであります。

> **再発見** —— 既に文献にある結果に、**それを知らずに**独立して到達すること。

似た三つを区別しておきます。混同すると評価が狂います。

| | 定義 | この系列 |
| --- | --- | --- |
| **再発見** | 既知であることを知らずに独立到達した | **該当する** |
| **多重発見** | 複数人がほぼ同時に独立到達した（Merton 1961） | 該当しない。数十年から百年遅れている |
| **再導出** | 既知だと知った上で自分で導き直す | 一部が該当（下表） |

再発見そのものは失敗ではありません。**どう置いたかで意味が決まります。**

- ラマヌジャンは孤立した環境で既知の解析の相当部分に独立到達しており、Hardy は
  それを重複と認めた上で評価を変えていません（Hardy 1937, 1940）
- 逆の例が Tai (1994) です。台形公式を新しい「モデル」として発表し、同じ雑誌に
  「これは台形公式である」という指摘が載りました（Monaco & Anderson 1994）。
  問題は中身ではなく、**既知だと書かなかったこと**です

**この系列は、最初 Tai (1994) の側にいて、2026年8月の改訂で自分をもう一方の棚に
移しました。**移したのが第三者ではなく著者自身である点が、この記録の性質を決めています。

### 五行の種別

「すべて再発見」とまとめるのは雑です。**種類が違います。**

| 内容 | 種別 | すでにある名前 |
| --- | --- | --- |
| 作用素 `x ← DQx + (I − D)p` | **再発見** | **アフィン反復**。`x ← Mx + c` の形は**定常反復法**と呼ばれ、Jacobi 法・Gauss–Seidel 法と同じ枠に入る（Varga 2000, Young 1971） |
| 巡回置換が自己逆にならない最小の `n` が 3 | **再発見** | 置換群の初等的な事実 |
| 縮小定数は `maxᵢ aᵢ` | **再導出** | 対角行列と置換行列の積のノルム。その場の計算 |
| 縮小写像なので唯一の不動点へ幾何収束する | **利用** | **バナッハの不動点定理**（Banach 1922）。系列は正しく引用しており、再発見ではない |
| 任意の `n ≥ 2` で同じ証明が通る（III） | **発見の否定** | 新事実ではなく、`n = 3` という区別が最初から無かったことの確認 |

**再発見 2、再導出 1、利用 1、撤回 1。**

### 独学という条件が説明すること、しないこと

**説明すること。**指導教員がいれば「その形は定常反復法である」で初回に終わっています。
文献調査の反射が身についていなければ、**既知かどうかを確かめる工程が構造的に抜け落ちます。**
これは能力の問題ではなく、置かれた条件の問題です。

**説明しないこと。**発表した時点で、確かめる責任は等しく発生します。**独学は原因の
説明であって、免責ではありません。**だから撤回が必要であり、実際に撤回しています。

### 直観が当たった部分と、外れた部分

**当たっていた部分。**「固定した基準点へ寄せる」と「座標を回す」を合成すれば収束する、
という構造の見立ては正しい。**選んだ対象は、筋の良い標準的な対象です。**独立に標準形へ
着地したこと自体は、直観が実在する構造を捉えていたことの証拠になります。

**外れていた部分。**証明が書かれたとおりには通らず（不動点が一意にならない）、
**作用素ノルムとスペクトル半径の区別を落としました。**

外れ方に構造があります。論文の設定では `Q` が置換行列 ＝ 直交、`a` が一様なので
`A = DQ` は正規行列になり、**`ρ(A) = ‖A‖₂` が成り立ちます。**区別しなくても答えが
合ってしまう。**直観が届く範囲の内側では正しく、外側で初めて壊れる**種類の誤りです。

正規でない場合に何が起きるかは
[trinity-operator](https://github.com/cpsbvbng26-dotcom/trinity-operator) で実装しました。
`ρ < 1 ≤ ‖A‖₂` のとき収束はしますが、誤差はいったん増えます
（非正規行列の過渡的増幅。Trefethen & Embree 2005）。

### 歴史的な位置づけ

**数学という分野に対しては、寄与ゼロです。**新しい定理はありません。ここは動きません。

**記録としては、ゼロではありません。**再発見の大半は、誰にも知られず消えるか、
発見として発表されたあと第三者に指摘されるかのどちらかです。科学社会学が扱える材料は
たいてい**外から出た記録**（訂正通知・撤回通知）で、**内から出た記録は構造的に集まりません。**

この系列にあるのは、**著者自身が、日付つきで、機械検証可能な形で、自分の再発見を
再発見だと書いた記録**です。価値は数学の中身ではなく、**材料としての形**の側にあります。

## 新しい数学は含まれていません

以上から結論です。**残った事実に、既存の文献に無いものは一つもありません。**
訂正の側も同じです。`x ← Ax + b` が任意の初期値から収束する必要十分条件が `ρ(A) < 1`
であることも（Varga 2000）、`ρ(A) < 1` なら `A` が縮小になるノルムが存在することも
（Ostrowski / Householder 1964; Horn & Johnson 2013 §5.6）、教科書に載っています。

**誤りを見つけたことに独自性があるのではありません。**教科書と突き合わせたら
合わなかった、というだけです。

**この結論を覆すには**、上の五行のどれか一つについて「これは既存の文献に無い」と
示してください。**一件で覆ります。**

### 出典

> **この一覧は、著者の作業環境から原典に到達して確認したものではありません。**
> 外部への通信が塞がれた環境で書いています。書誌事項の誤りが見つかった場合は
> [ERRATA.md](ERRATA.md) に記録します。**確かめずに「確認済み」とは書きません。**

- Banach, S. (1922). Sur les opérations dans les ensembles abstraits et leur application
  aux équations intégrales. *Fundamenta Mathematicae*, 3, 133–181.
- Hardy, G. H. (1937). The Indian Mathematician Ramanujan. *The American Mathematical
  Monthly*, 44(3), 137–155.
- Hardy, G. H. (1940). *Ramanujan: Twelve Lectures on Subjects Suggested by His Life and
  Work*. Cambridge University Press.
- Horn, R. A., & Johnson, C. R. (2013). *Matrix Analysis* (2nd ed.). Cambridge University
  Press. §5.6.
- Householder, A. S. (1964). *The Theory of Matrices in Numerical Analysis*. Blaisdell.
- Merton, R. K. (1961). Singletons and Multiples in Scientific Discovery: A Chapter in the
  Sociology of Science. *Proceedings of the American Philosophical Society*, 105(5), 470–486.
- Monaco, J. H., & Anderson, R. L. (1994). Tai's Formula Is the Trapezoidal Rule.
  *Diabetes Care*, 17(10), 1224–1225.
- Tai, M. M. (1994). A Mathematical Model for the Determination of Total Area Under Glucose
  Tolerance and Other Metabolic Curves. *Diabetes Care*, 17(2), 152–154.
- Trefethen, L. N., & Embree, M. (2005). *Spectra and Pseudospectra: The Behavior of
  Nonnormal Matrices and Operators*. Princeton University Press.
- Varga, R. S. (2000). *Matrix Iterative Analysis* (2nd ed.). Springer.
- Young, D. M. (1971). *Iterative Solution of Large Linear Systems*. Academic Press.

**内容を引き写してはいません。**「既知である」ことの出典として挙げています。

## 撤回されたこと

改訂前の草稿が主張していて、**改訂版に残らなかったもの**です。各論文が自ら列挙しています。

| 主張 | なぜ残らなかったか |
| --- | --- |
| 収束定理（原型） | 原文の自然な読みでは不動点が一意にならない。全座標が等しい状態がすべて不動点になり、極限は初期値に依存する |
| 「98.7% の試行で確認」 | 再現できるコード・乱数種・停止条件がない。作用素を記述どおり実行すると値も一致しない |
| 三人ゲームの利得表 | 3人2戦略のゲームは 2³ = 8 通り。4セルの表はこのゲームを表現できない |
| リアプノフ微分と LaSalle の原理 | 離散反復に連続時間の道具を当てていた。縮小定数が既知なので、必要な議論は一行で済む |
| AI アライメント・気候政策・ガバナンスへの応用 | 実際の政策過程が固定基準点へ縮小することも、制度を距離空間の点として扱えることも、到達する不動点が望ましいことも、何も示されていない |

Series II は最後の項目について、**主張を成立させるために最低限必要なもの**を挙げています。
実在の過程から距離空間への明示的な写像、その写像が正確だという経験的証拠、そして到達する不動点が
**望ましい**という規範的議論（到達可能であることとは別の話）。この三つが揃っていませんでした。

## なぜ消さずに置いてあるのか

元の DOI は生きたままです。改訂版は、誤りを静かに上書きするのではなく、**何が落ちたかを項目ごとに書いています。**

普通は逆になります。静かに v2 を出すか、他人に指摘されるまで放置されるか。
残った定理は初等的なもので、それは論文自身が認めています。**この系列の価値は定理の大きさではなく、
野心的な枠組みを証明とコードの実行に通したとき何が残るか、という測定のほうにあります。**

## 検証

二本のスクリプトが入っています。**問いが違います。**

| | 問い | 項目 |
| --- | --- | --- |
| [`verification/independent_check.py`](verification/independent_check.py) | **定理は正しいか。** 証明の記述から独立に実装して、同じ結論に達するか | 13 |
| [`verification/claims_audit.py`](verification/claims_audit.py) | **紙面に印字されている数字は、その通りに出るか。** 論文から数値を書き写し、隣に計算し直した値を並べる | 31 |

```
python3 verification/independent_check.py
python3 verification/claims_audit.py
```

どちらも NumPy のみを必要とし、乱数種を固定しています。44 項目すべてが通ります。
**GitHub Actions が push ごとに両方を実行しています** —— 上のバッジが、いま通っているかどうかです。
詳細は [verification/README.md](verification/README.md) を参照してください。

`claims_audit.py` が確かめるのは、たとえば次のようなものです —— Series I の不動点
`(0.510204, 0.306122, 0.183673)`、Series II の異方的な不動点と 8つの利得の**凸包の体積 4.00**、
ばね系の `K∞`、Series III の表1の `P² = I` の列。**論文の数値を一つも信用しないで読み直せます。**

なお、各論文は検証スクリプトを同梱していると謳っていますが、**そのスクリプトは存在しません**。
配布物にも著者の手元にも残っていません（[ERRATA.md](ERRATA.md) の E3）。謳っているのは謝辞だけでは
なく、三本で合計 **6 箇所**です。上の二本は、その代用ではなく別に書いたものです。
**元のスクリプトが何を計算していたかは、もう分かりません。**

その 6 箇所が本当に紙面に印字されているかは、`check_errata.py` が PDF から文字を取り出して
突き合わせます（51 項目）。E1・E2 の引用も、名乗る件数も、未解決の項目が
「解決済み」に書き換わっていないかも、同じように当たります。

条件は [`verification/audit.toml`](verification/audit.toml) に宣言してあり、当たるのは
[errata-check](https://github.com/cpsbvbng26-dotcom/errata-check)（MIT、単一ファイル、v0.1.0、[10.5281/zenodo.22649054](https://doi.org/10.5281/zenodo.22649054)）が
やります。**判定に推論を使いません。**あるか、無いか、一致するか、しないか。
PDF そのものの SHA-256 も宣言してあるので、**一次資料が差し替わればそこで落ちます。**

## ライセンス

© 2026 根本卓哉（Takuya Nemoto）— [CC BY 4.0](LICENSE)。

**注記:** 三本の PDF 自体にはライセンスの記載がありません。著者の他のプレプリントに合わせて CC BY 4.0 としています。
掲載先（Zenodo）の設定と異なる場合は、掲載先を正としてください。

## 引用

三本とも Zenodo に登録され、DOI が付与されています。上の一覧の DOI 欄から辿れます。

```
Nemoto, T. (2026). The Trinity-Infinity Framework: A Conceptual Model with Illustrative
Applications in Game Theory, Mathematical Logic, and Mechanical Engineering
(Revised Edition). Zenodo. https://doi.org/10.5281/zenodo.22058624

Nemoto, T. (2026). The Trinity-Infinity Framework, Series II: Extended Formalization
and Further Illustrative Applications (Revised Edition). Zenodo.
https://doi.org/10.5281/zenodo.22058777

Nemoto, T. (2026). The Trinity-Infinity Framework, Series III: Beyond Three —
A Generalization and Retrospective. Zenodo. https://doi.org/10.5281/zenodo.22058964
```

**改訂前の版**（2025年、この系列が訂正の対象としているもの）は別の DOI をもちます:
[10.5281/zenodo.17173703](https://doi.org/10.5281/zenodo.17173703)。
どちらを参照したのかが読者に分かる形で引用してください。

### 正誤

見つかった不備は [**ERRATA.md**](ERRATA.md) にまとめています。PDF に手を入れない方針のため、
本文を書き換える代わりにここに記録しています。

**いちばん影響が大きいのは E1 です。Series II と Series III の参考文献欄は、
改訂版 Series I を `10.5281/zenodo.17173703` で引用しています。** これは訂正の対象である
2025年の初版の DOI で、改訂版は `10.5281/zenodo.22058624` です。そのまま辿った読者は、
II と III が「これを一般化する」と述べている定理の、**撤回された方の版**を読むことになります。

**改訂版 Series I を参照する場合は `10.5281/zenodo.22058624` を用いてください。**

## AI の利用

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-D97757?style=for-the-badge)](https://claude.com/claude-code)

**論文について。** 三本とも、起草・数学的定式化・計算による検証にあたって Claude（Anthropic）の
助力を得ています。各論文の末尾に、どの作業に用いたかの開示文があります。

**このリポジトリについて。** README の構成と本文、`ERRATA.md`、`CITATION.cff`、および
`verification/` の二本のスクリプトは、Claude Code（Anthropic）を用いて作成し、実行しました。**論文の PDF には手を入れていません** ——
`pdf/` にあるのは配布されたファイルそのものです。README に書いた「確立されたこと」「撤回されたこと」は、
各論文自身の改訂註と回顧の章にもとづく要約であり、こちらで新たに評価を加えたものではありません。

検証スクリプトが報告する数値は、すべて実行して得たものです。いずれの主張についても、
責任は著者（根本卓哉）にあります。AI は著作者ではありません。

**記録から確認できること。** このリポジトリのコミットは `Claude` 名義で、
末尾に作業セッションを示す `Claude-Session:` トレーラが付いています。
`git log --author=Claude` で辿れます。

## 著者

根本卓哉（Takuya Nemoto）
[プロフィール](https://cpsbvbng26-dotcom.github.io/cpsbvbng26-dotcom/) ｜
[ORCID](https://orcid.org/0009-0000-1406-0547)
