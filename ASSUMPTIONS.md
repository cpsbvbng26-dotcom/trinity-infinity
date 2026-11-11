# 前提の一覧 —— どれを外すと、どの結論が崩れるか

三篇の定理が置いている前提を、番号を付けて並べます。
前提は紙面の文から取りました。外したときに何が起きるかは、
[trinity-operator の展望](https://github.com/cpsbvbng26-dotcom/trinity-operator/blob/main/roadmap/README.md)と、
このリポジトリの記録から取りました。
ここで新しく評価を加えたものはありません。

三篇の結論は、Series I の定理1の形でまとめられます。
f は S を S に写し、変位をちょうど α 倍にします。
そのため唯一の不動点があり、どの初期値からも誤差が `αⁿ` 以下で減ります。

## 一覧

| 番号 | 前提 | 紙面の文 | 外すと | 崩れる結論 | 出典 |
| --- | --- | --- | --- | --- | --- |
| 1 | 要素は三つ | Series I：`three-component state` | 要素を n 個にする | 崩れない。Series III が任意の `n ≥ 2` で同じ証明が通ることを示した | Series III：`No step uses n=3` |
| 2 | 状態空間は単位立方体 | Series I：`Let the state space be S` | 外から始める | 崩れない。±50 の範囲から始めても同じ極限に着く | [verification/README.md](verification/README.md) の B |
| 3 | 座標を回す写像は等長 | Series I：`using that σ is an isometry`<br>Series III：`hence orthogonal, hence an isometry` | Q を一般の行列にする | 「変位がちょうど α 倍」と「誤差が初手から減る」が崩れる。収束と唯一性は `ρ(DQ) < 1` なら残る | 展望の段 0。[trinity-operator の README](https://github.com/cpsbvbng26-dotcom/trinity-operator#区別が効く場面) |
| 4 | 混合率は一様なスカラ | Series I：`a blending parameter α ∈ (0,1)` | 座標ごとに変える | 縮小定数と収束の速さの一致が崩れる。`‖DQ‖₂` は最大値、`ρ(DQ)` は相乗平均になる | Series II：`generalize to an anisotropic blend`。[ERRATA.md](ERRATA.md) の N9 |
| 5 | 基準点は状態に依らない | Series I：`Uniqueness here depends on integrating toward a fixed anchor p that does not depend on the current state` | 状態自身の平均へ寄せる | 唯一性が崩れる。極限が初期値に依存する | Series I：`the recursion converges in a single step to a limit that depends on the initial state` |
| 6 | 毎段が同じ作用素 | Series I：`The recursion operator is f` | 段 2：毎段が同じ作用素 | 収束が崩れる。各段が縮小でも、切り替えると発散しうる | 展望の段 2 |
| 7 | 切り替えは決定的 | （紙面に無い。段 2 の設定の前提） | 段 3：切り替えが決定的 | 「収束」が一つに決まらない。二乗平均とほとんど確実の二つに割れる | 展望の段 3 |
| 8 | 統合は線形 | Series I：`f(T) = α σ(T) + (1−α)p` | 段 4：統合が線形 | 唯一性が崩れる。不動点が複数になる | 展望の段 4 |
| 9 | 要素は有限個 | Series III：`Let n ≥ 2` | 段 5：要素が有限個 | 「任意の n で同じ」が極限へ渡らない。`ρ` は渡らず、`‖A‖` は渡る | 展望の段 5 |
| 10 | 影響行列は巡回置換 | Series I：`Define the cyclic permutation` | 段 6：影響行列が巡回置換 | 一点の均衡では崩れない。作用素として見ると、像の次元が `n(n−1)` から `n` に落ちる | 展望の段 6 |

## 読み方

前提 1 と 2 は、外しても何も崩れません。
定理が使っていない前提です。

前提 3 と 4 を外しても、`ρ(DQ) < 1` なら収束の結論は残ります。
崩れるのは、収束を言うための議論のほうです。
三篇は作用素ノルムで収束を言いました。
作用素ノルムで言えるのは十分条件までで、必要十分条件はスペクトル半径です。

前提 5、6、8 を外すと、唯一性か収束そのものが崩れます。
前提 9 を外すと、有限の n で言えたことが極限へ渡りません。
前提 5 は、2025 年の初版で実際に崩れていたものです。

前提 7 は三篇の前提ではありません。
展望の段 2 で前提 6 を外したあとに、新しく現れた前提です。

## 載せていないもの

展望の段 1 は、右辺 `W = I` の決め打ちを外しています。
これは `certificate.py` の決め打ちで、三篇の前提ではありません。
そのため、この一覧には入れていません。

## 検査

`python3 verification/check_pages.py` が、この表を当たります。
紙面の文は、三篇の PDF から取り出した文字列に一字一句あるかを見ます。
「段 k：」で始まる欄は、trinity-operator の README の展望の表と同じ語かを見ます。
番号が 1 から欠けずに並んでいるかも見ます。
