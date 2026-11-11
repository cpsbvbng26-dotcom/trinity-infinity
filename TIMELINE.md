# 年表

Series I〜III と、作用素の実装と、黄金比の窓の予想を、一つの表に並べます。
日付はどれも、出典の欄に挙げた文書に書いてあるものです。
月までしか書いていない出来事は、月までで止めています。

三篇は、学部一年次までに独学で進めた成果です。
作用素と予想は、その続きと修正として進めています。

| 日付 | 稿 | 受け継いだもの | 直したもの・足したもの | 出典 |
| --- | --- | --- | --- | --- |
| 2025-10 | 初版（2025 年） | 記号 `Ⅲ∞` | 言語モデルが写像と定理を当てはめ、そのまま初版になった | [ROUTE.md](ROUTE.md) の段階 1 |
| 2026-08 | Series I 改訂版 | 初版の着想 | 統合を、状態に依らない基準点へ寄せる形に直した。作用素を `x ← DQx + (I − D)p` に書き下した | [ROUTE.md](ROUTE.md) の段階 2・3 |
| 2026-08 | Series II 改訂版 | Series I の作用素と定理1 | 混合率を座標ごとに変え、縮小定数を `maxᵢ aᵢ` とした | [ROUTE.md](ROUTE.md) の段階 4 |
| 2026-08 | Series III | Series I・II の定理 | 要素数を n にした。`n = 3` に数学的な意味が無いことを示した | [ROUTE.md](ROUTE.md) の段階 5 |
| 2026-09-06 | trinity-operator | 三篇の作用素 | 収束を決めているのは作用素ノルムではなくスペクトル半径だと示した | [ROUTE.md](ROUTE.md) の段階 7 |
| 2026-09-07 | trinity-operator の証書 | 壊れたバナッハの議論 | リアプノフ方程式から、縮小になるノルムを作った | [ROUTE.md](ROUTE.md) の段階 8 |
| 2026-09-08 | このリポジトリの README | 段階 1〜8 | 作用素を定常反復法と同定し、数学的再発見と規定した | [ROUTE.md](ROUTE.md) の段階 9 |
| 2026-09-18 | 正誤表 E8 | 展望の段 6 | 三篇の作用素が Friedkin–Johnsen の特殊例としてどれだけ小さいかを測った | [ERRATA.md](ERRATA.md) の E8 |
| 2026-09-29 | 系列を閉じた | 三篇 | 理論として伸ばすことをやめた。Series IV は出さない | [README.md](README.md) の「この系列は閉じた」 |
| 2026-10-04 | 繰り返しゲームのノート | 三篇の作用素と、Series II 第4節の例 | 例 `(2,4,2)` が持続しないことを示した。黄金比の窓の予想を置いた | [trinity-operator の games/README.md](https://github.com/cpsbvbng26-dotcom/trinity-operator/blob/main/games/README.md) |
| 2026-10-13 | ノートの論文版（Figshare） | ノートの命題 1〜7 と予想 | 英語の論文版を凍結して置いた | [trinity-operator の games/README.md](https://github.com/cpsbvbng26-dotcom/trinity-operator/blob/main/games/README.md) |
| 2026-11-07 | Zenodo の保存版 1.0.0 | このリポジトリと trinity-operator | 二つのリポジトリをそれぞれ保存した | [CITATION.cff](CITATION.cff) |
| 2026-11-11 | 正誤表 E7 | ノートの命題 3 | Series II 第4節の例の点が支えられないことを、E7 に書き足した | [ERRATA.md](ERRATA.md) の E7 |

## 検査

`python3 verification/check_pages.py` が、この表を当たります。
各行の日付が、出典の欄に挙げた文書に書いてあるかを見ます。
日付が上から古い順に並んでいるかも見ます。
trinity-operator の文書は、隣に置いた trinity-operator の写しから読みます。
