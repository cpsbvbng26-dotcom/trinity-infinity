# 法令の点検（2026-11-12）

この頁は、2026-11-12 に Claude が行った法令の点検のうち、trinity-infinity の分の記録です。
対象は、README のライセンスの記載と注記、arXiv に出す計画の規約の点検（ARXIV.md）、推薦を頼む文の雛形（ARXIV-SUBMIT.md）です。
10 のリポジトリに掛かる免責事項の点検と、条文の取り寄せ方は、cpsbvbng26-dotcom の[点検の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)にあります。
この頁は運営者の立場を記録するもので、読む人への法的な助言ではありません。

## やり方

法令が出てくる箇所を一つずつ挙げ、挙げた条の文を、取り寄せた条文と照らしました。
条文は記憶から書いていません。
Sophaxis の取り寄せの仕事を走らせて e-Gov から取り寄せ、cpsbvbng26-dotcom の [verification/statutes.json](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/verification/statutes.json) に写しました。
この頁が挙げる条がどれもその表にあることは、cpsbvbng26-dotcom の `check_ecosystem.js` が確かめます。
判定は、誤り・根拠不足・漏れ・表現・問題なしの五つです。

## 点検の表

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| README「ライセンス」、LICENSE、LICENSE-CODE、CITATION.cff、.zenodo.json | 著作権法第21条、著作権法第23条 | 複製と公衆送信は著作者の権利で、他人に許す範囲は許す者の表示で決まる | LICENSE が CC BY 4.0、LICENSE-CODE が MIT。CITATION.cff と .zenodo.json は CC BY 4.0 | 問題なし | なし |
| README の注記「掲載先（Zenodo）の設定と異なる場合は、掲載先を正とします」 | 著作権法第21条 | 複製と公衆送信は著作者の権利で、他人に許す範囲は許す者の表示で決まる | 三本の PDF にはライセンスの記載が無い。.zenodo.json は CC BY 4.0。Zenodo の記録は作業環境から開けず、設定を確かめていない | 根拠不足 | 記録だけ。Zenodo の記録を確かめられないので、注記は残す |
| ARXIV.md のライセンスの二行 | 著作権法第21条、arXiv のライセンスの案内 | arXiv で選べるライセンス | 「CC BY 4.0 は arXiv の選択肢にある（未確認）」だった。取り寄せた arXiv の案内の Licenses available の最初の行は `CC BY 4.0 : Creative Commons Attribution` | 問題なし | 確かめたことを、取り寄せた語と日を添えて書いた。「規約の記述はいずれも未確認」を「ライセンスの一行を除いて未確認」に改め、`check_route.py` の検査を直した |
| ARXIV.md の SSRN の行 | 著作権法第21条 | SSRN への許諾の性質 | 「SSRN の掲載権は非独占で、著作権は著者が持ったまま（未確認）」と未確認の札が付いている | 根拠不足 | 記録だけ。SSRN の規約は取り寄せていない |
| ARXIV-SUBMIT.md の推薦を頼む文の雛形 | 個人情報保護法第2条 | 特定の個人を識別できる情報 | 宛先は〈氏名〉の空欄で、人の名を書いていない | 問題なし | なし |

## 2026-11-12 の続き：リスクを締めた

同じ日に、利用者が「法的リスクをさらにシメて」と求めました。
上の表で根拠不足としたところと、取り寄せた文だけでは読みが決まらないところを、厳しいほうの読みで見直しました。
厳しいほうの読みでも成り立つ形があり、費用が掛からないときは、その形を採りました。
決めたことは、行ごとに理由と一緒に書きます。
取り寄せられなかった文に頼るところは、この節では扱っていません。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| ARXIV-SUBMIT.md の推薦の依頼 | 個人情報保護法第2条 | 特定の個人を識別できる情報 | 依頼した相手の氏名とメールアドレスを書かないと決めて書いている。雛形の宛先は空欄 | 問題なし | なし |
| ERRATA.md と紙面が名を挙げる研究者 | 刑法第230条 | 公然と事実を摘示して名誉を毀損すること | 名は先行研究の帰属を述べる文に出る。自分の結果が既知の模型の特殊例だと書く向きで、相手の評価を下げる文は無い | 問題なし | なし |
| README の責任の一文 | 民法第709条 | 故意又は過失で他人の権利又は法律上保護される利益を侵害した者は、生じた損害を賠償する | 「責任の範囲は、免責事項に定めています」と書いていた。免責事項は契約ではなく、責任の範囲は法令が決める。今日、免責事項は責任を免除する文をやめた | 表現 | 「責任は、法令の定めるとおりです。説明は免責事項にあります。」に直した。10 のリポジトリで同じ一文にそろえ、cpsbvbng26-dotcom の `check_ecosystem.js` が一字一句を見る。2026-11-12 に Claude が決めました。免責事項が範囲を決めると読める言い方は、どちらの読みでも成り立たないからです |

## 2026-11-12 の続き：取り寄せた周辺の文

上の表で取り寄せられなかった文のうち、同じ日に Sophaxis の取り寄せの仕事が取り寄せたものがあります。
置き場は Sophaxis の main（コミット 6b40d77、PR #218）の `verification/sources-raw.json` です。
取り寄せた文で、上の結論を一つずつ確かめ直しました。
条の文は cpsbvbng26-dotcom の `verification/statutes.json` に写し、`check_ecosystem.js` が Sophaxis の文と一字一句を突き合わせます。
規約は著作物なので、頼った句だけをこの表に引きます。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| ARXIV.md の SSRN の行 | SSRN の利用規約 | SSRN への許諾の性質 | 取り寄せた SSRN の利用規約（2026-11-05 の写し）は、投稿者が Elsevier に与えるライセンスを非独占とし（`non-exclusive`）、知的財産権は投稿者に残ると書く（`you retain ownership of any intellectual property rights`） | 問題なし | ARXIV.md の行の「未確認」を外し、取り寄せた語を添えた。三か所とも CC BY 4.0 という結論は変わらない |

## 2026-11-12 の続き：二度目の見落とし

同じ日に、読むだけの点検を、さらに別の手でもう一度行いました。
上の節が見落としていたものが見つかりました。
前の行は、そのとき何を確かめたかの記録なので、消していません。
法令の文は、cpsbvbng26-dotcom の `verification/statutes.json` に写した取り寄せた文から引きます。
10 のリポジトリに同じものを置く文書の点検は、[cpsbvbng26-dotcom の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)の同じ見出しの節にもあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| SECURITY.md | 民法第709条 | 取り寄せた文は「故意又は過失によって他人の権利又は法律上保護される利益を侵害した者は、これによって生じた損害を賠償する責任を負う」と定める。無い窓口を約して、頼った人に損を生じさせないこと | SECURITY.md は、安全の問題を GitHub の非公開の報告で受けると約していた。GitHub の API は、2026-11-12 に、このリポジトリの非公開の報告を `enabled: false` と返した。これはリポジトリの設定であり、Claude の持つ道具では変えられない | 誤り | 運営者の ORCID の記録にあるメールアドレスで受けると書き直し、GitHub の非公開の報告は有効になっていないと、確かめた日と一緒に書いた。写しは 10 のリポジトリと deposit-check で一字一句同じで、cpsbvbng26-dotcom の `check_ecosystem.js` の 12j が中身を確かめる。2026-11-12 に Claude が決めました。在る窓口は、免責事項がすでに使っている一つだけだからです |
| `verification/check_meta.py` の SECURITY.md の検査 | 民法第709条 | 同上 | 検査は「Report a vulnerability」の語があることを求めていた。無い入口を求める検査だった | 誤り | 検査を、ORCID の記録のメールと、非公開の報告が有効でないことを求め、「Report a vulnerability」が戻れば落ちる向きに替えた。もとの SECURITY.md に戻して、落ちることを確かめた。2026-11-12 に Claude が決めました。検査が求める文を、在る窓口の文に移すためです |

## 2026-11-12 の続き：四度目の見落とし

同じ日に、読むだけの点検を、四度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
前の行は、そのとき何を確かめたかの記録なので、消していません。
誤っていた前の行は、新しい行の中でそう書き、理由を添えます。
法令の文は、cpsbvbng26-dotcom の `verification/statutes.json` に写した取り寄せた文から引きます。
10 のリポジトリと deposit-check に同じ形で置く文の点検は、[cpsbvbng26-dotcom の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)の同じ見出しの節にもあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| README（英語の段と日本語の段）と ARXIV.md の、SSRN の選別の文 | なし（表示の正確さ） | 場が何をするかは、取り寄せた場の頁が言う範囲で書くこと | README は英語の段で「SSRN screening checks scope and format, not correctness.」、日本語の段で「SSRN の選別は主題と体裁を見るものであり、査読ではありません。」と書き、ARXIV.md の表は「通ったのは主題と体裁の門である」と書いていた。取り寄せた SSRN の頁（https://web.archive.org/web/20260822023102id_/https://www.elsevier.support/ssrn/answer/nonscholarly、2026-11-12、SHA-256 `60b3353cb309192ee8714ac40e04f8f8aaa5d44cbaf1fd28ef5fb0501aa1f0a0`）は `SSRN must determine if a paper meets the criteria of scholarly content` と書き、別の頁（https://web.archive.org/web/20260822023102id_/https://www.elsevier.support/ssrn/answer/research-integrity、SHA-256 `a80d8bf7581581a24d7b4a7bc254b0d985e1ea3f8448fb73a4ee8ddfa5bea619`）は `SSRN does not peer review preprints` と書く。主題と体裁を見るとは、取り寄せた頁から引いたどの句も言っていない | 表現 | 三か所を、取り寄せた二つの句が言うことだけに書き直した。cpsbvbng26-dotcom の `verification/screening.js` が、場の名のある段落で選別の動きと中身を同じ文に置く文を、日英独仏伊で止める。`check_ecosystem.js` の 12l が、この README と ARXIV.md にも当てる。2026-11-12 に Claude が決めました。三度目の見落としの節までの点検は、自己紹介の頁だけを探し、このリポジトリの README と ARXIV.md を探していなかったからです |
| README「ライセンス」 | 著作権法第21条 | 取り寄せた文は「著作者は、その著作物を複製する権利を専有する。」と定める（cpsbvbng26-dotcom の `verification/statutes.json`、SHA-256 `a85d04f2fd20d7867d5579bee40676b13405c58ea7fd7eb27f1e7a5a03bda100`）。許せるのは、許す者が権利を持つものだけである。ライセンスの文が、他人の文まで許すと読めないこと | README のライセンスの節は、文書の CC BY 4.0 とコードの MIT だけを書き、引いた他人の文の扱いを書いていなかった。Sophaxis は、最初の見落としの節で同じ一文を足していたが、10 のリポジトリと deposit-check には届いていなかった。上の点検の表の「README「ライセンス」、LICENSE、LICENSE-CODE、CITATION.cff、.zenodo.json」の行は問題なしとしていたが、他人の文の扱いを見ていなかった | 漏れ | README のライセンスの節に「このリポジトリが引き、または引用を確かめるために置いている他人の文は、CC BY 4.0 でも MIT でも許諾しておらず、それぞれの権利者のものです。」を足した。`check_ecosystem.js` の 12l が、10 のリポジトリと deposit-check の README（英語の README を含む）にこの一文があることを見る。2026-11-12 に Claude が決めました。Sophaxis の README と同じ範囲を、同じ形で書くためです |
| CITATION.cff の message と .zenodo.json の notes | 著作権法第21条 | 同上。引用情報の license の欄は、どの部分に掛かるかを書けないので、その範囲を別の欄で書くこと | CITATION.cff と .zenodo.json の license の欄は CC BY 4.0 で、notes は文書と論文が CC BY 4.0、検証のコードが MIT とだけ書いていた。欄が掛かる範囲は書いていなかった。上の点検の表の「README「ライセンス」、LICENSE、LICENSE-CODE、CITATION.cff、.zenodo.json」の行は問題なしとしていたが、欄の掛かる範囲と他人の文を見ていなかった | 表現 | message と notes に、文書と論文が CC BY 4.0、検証のコードが MIT で、license の欄は文書と論文だけに掛かることを書いた。他人の文は許諾していないとも、和英で書いた。`check_ecosystem.js` の 12l が、二つのファイルにこの文があり、置き方が目録の licenceLayout と同じことを見る。2026-11-12 に Claude が決めました。Sophaxis の CITATION.cff が三度目の見落としの節で書いた範囲の文に、10 のリポジトリと deposit-check を揃えるためです |

## 2026-11-12 の続き：六度目の見落とし

読むだけの点検を、六度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
直した日は、日本時間で 2026-11-13 です。
前の行は、そのとき何を確かめたかの記録なので、消していません。
同じ誤りの点検は、[cpsbvbng26-dotcom の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)と、researcher-profile の記録の同じ見出しの節にもあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| ERRATA.md の E8「どの程度のモデルか」の表の、2011 年の行 | なし（表示の正確さ） | 他人の本の著者を、書誌の記録が言うとおりに書くこと | 行は「Cambridge University Press から単著の理論書 *Social Influence Network Theory: …*」と書いていた。Crossref の記録（https://api.crossref.org/works/10.1017/cbo9780511976735 、2026-11-13 に日本時間で読んだ）は、type を「monograph」、author を Noah E. Friedkin（sequence「first」）と Eugene C. Johnsen（sequence「additional」）の二人、publisher を「Cambridge University Press」、issued を 2011-04-18 と返した。単著は一人で書いた本を指すので、記録と食い違っていた | 誤り | 行を「Cambridge University Press から、Noah E. Friedkin と Eugene C. Johnsen の共著の理論書」に直した。直したのは本の説明だけで、E8 が記録している出来事の記述は変えていない。`check_errata.py` の「E8 —— 相手の格を書いてある」が、共著と書くことを求め、Friedkin・Johnsen の名か本の題と同じ行に単著や single-authored があれば落ちる。件数は 111 項目のままです。直す前の行に戻すと落ち、直した行に「（単著）」を足しても落ちることを確かめた。2026-11-13 に Claude が決めました。Crossref の記録が著者を二人と返すからです |

## 2026-11-12 の続き：七度目の見落とし

読むだけの点検を、七度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
直した日は、日本時間で 2026-11-13 です。
前の行は、そのとき何を確かめたかの記録なので、消していません。
同じ誤りの点検は、[cpsbvbng26-dotcom の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)の同じ見出しの節にもあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| ERRATA.md の最終更新 | なし（頁の日付の正確さ） | 頁の最終更新が、その頁の文を変えた最後の日より前でないこと | 最終更新は 2026年11月12日 でした。六度目の見落としで E8 の表を直したコミット 56d0887 は、`git log` を日本時間で読むと 2026-11-13 の 4 時 38 分でした。作業の時計は協定世界時で、最終更新の行を変えていませんでした | 誤り | 2026年11月13日 に改めました。2026-11-13 に Claude が決めました。頁の日付は最後の変更を示すもので、作業の時計の日付ではないからです。cpsbvbng26-dotcom の `check_ecosystem.js` の 12n が、この頁の最終更新を、文を変えた最後のコミットの日本時間の日付と照らします |

## 2026-11-12 の続き：八度目の見落とし

読むだけの点検を、八度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
直した日は、日本時間で 2026-11-13 です。
前の行は、そのとき何を確かめたかの記録なので、消していません。
GitHub の利用規約の I 節は「Some Service features may be subject to additional terms specific to that feature or product as set forth in the GitHub Additional Product Terms.」と書きます。
その追加の規約（GitHub Terms for Additional Products and Features）を、これまでの点検は取り寄せていませんでした。
追加の規約は、`github/site-policy` のコミット `166eb97e485b7de3cd5dbaf8c8d16e4310fda46c` の文を、2026-11-13 に raw.githubusercontent.com から直に取り寄せました。
ファイルの SHA-256 は `c39b5a7fc1953ebd37428db18101726acefb55420f766bcd7d912e1b71ee2ffc` です。
Actions の節は「Additionally, regardless of whether an Action is using self-hosted runners, Actions should not be used for:」と書き、次の二つを挙げます。
一つは「Any activity that places a burden on our servers, where that burden is disproportionate to the benefits provided to users (for example, don't use Actions as a content delivery network or as part of a serverless application, but a low benefit Action could be ok if it’s also low burden); or」です。
もう一つは「If using GitHub-hosted runners, any other activity unrelated to the production, testing, deployment, or publication of the software project associated with the repository where GitHub Actions are used.」です。
同じ節は「Misuse of GitHub Actions may result in termination of jobs, restrictions in your ability to use GitHub Actions, disabling of repositories created to run Actions in a way that violates these Terms, or in some cases, suspension or termination of your GitHub account.」とも書きます。
このリポジトリのワークフローは、どれも GitHub の実行環境（`ubuntu-latest` か `ubuntu-24.04`）で動きます。
そこで、ワークフローを一つずつ、四つの目的（制作・検査・配備・公開）のどれに当たるか、負荷が益に見合うかで読みました。
ワークフローの行は、箇所の欄を `.github/workflows/` のファイルの名で始めます。
実行の時間は、GitHub の API で 2026-11-13 に読んだ直近の実行（多くて 300 件）の中央値です。
GitHub Pages が枝から頁を配るときに GitHub が動かす仕事と、Dependabot の版の更新は、このリポジトリのファイルではないので、表に挙げていません。
引いた文は、cpsbvbng26-dotcom の `verification/statutes.json` の「GitHub の利用規約 I」と「GitHub の追加製品の規約 Actions」に写しました。
同じ点検は、13 のリポジトリの記録の同じ見出しの節にあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| GitHub の追加製品の規約（Actions の節） | GitHub の利用規約 I、GitHub の追加製品の規約 Actions | 使っているサービスの規約を取り寄せて読むこと | 利用規約の I 節は追加の規約を取り込みますが、これまでの点検は追加の規約を読んでいませんでした | 漏れ | 取り寄せ、Actions の節の文を cpsbvbng26-dotcom の `verification/statutes.json` に写しました。Sophaxis の週ごとの見張りにも足しました。2026-11-13 に Claude が決めました。ワークフローの使い方を決める文なので、ほかの規約と同じに読むためです |
| `.github/workflows/verify.yml`（main への push・PR、手で起こすとき） | GitHub の追加製品の規約 Actions | GitHub の実行環境で、リポジトリのソフトウェアのプロジェクトの制作・検査・配備・公開のどれかに当たること。負荷が利用者への益に見合うこと | このリポジトリの検査を回します（定理、印字された数値、正誤表の監査、経路、秘密）。実行の中央値は 18 秒です | 問題なし | 変えていません。検査に当たります |
| 検査（`verification/check_meta.py`） | なし | ワークフローごとの判断を、機械で固めること | ありませんでした | 漏れ | `verification/check_meta.py` に、`.github/workflows/` のどのファイルもこの節の表に行を持ち、無いファイルの行が無いことを確かめる項目を足しました。cpsbvbng26-dotcom の `check_ecosystem.js` の 12o も、13 のリポジトリについて同じことを確かめます。2026-11-13 に Claude が決めました。新しいワークフローを、規約に照らさずに足せないようにするためです |

この表の判定は、漏れ 2、問題なし 1 です。

弁護士は、この節を見ていません。

## 2026-11-13：十七度目の見落とし

ここまでの表は、書いたときのまま残しています。
2026-11-13 に、読むだけの十七度目の点検が、issue の中身が言語モデルに渡ることを挙げました。
このリポジトリの作業は Claude Code で行い、その作業は issue の題と本文を読みます。
読んだものは、Anthropic（米国）の言語モデル Claude に渡ります。
扱いは、cpsbvbng26-dotcom の免責事項の節「issue の中身と言語モデル」と、cpsbvbng26-dotcom の点検の記録の同じ見出しの節にあります。
直した日は、日本時間で 2026-11-13 です。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| `.github/ISSUE_TEMPLATE/error-report.yml` | 個人情報保護法第28条 | 外国にある第三者に個人データを提供する前に、本人の同意を得ること | 同意の欄がありませんでした | 漏れ | 必須の同意の欄を足しました。10 のリポジトリと deposit-check で一字一句同じです。2026-11-13 に Claude が決めました。同意を得る前に中身が渡らないよう、issue を開くときに求めるためです |
| `CLAUDE.md` の共通の決めごと | 個人情報保護法第28条 | 同意の無い中身を渡さないこと | issue の読み方の決めがありませんでした | 漏れ | 決めごと 17 を足しました。issue は同意の欄の英語の文で探して出てきたものだけを読み、一覧を取らず、コメントを読みません。2026-11-13 に Claude が決めました。同意の無い issue の本文を読まずに済む読み方を、作業の決めにするためです |

この表の判定は、漏れ 2 です。

この変更は、同意を得る欄を足し、同意の無い中身を渡さないと決める直しです。
誤りの知らせの様式は、同意しないと issue を開けなくなりました。
同意しない人も、免責事項の宛先へメールで知らせられます。

この節も、弁護士は見ていません。

## 調べた法令

- GitHub の利用規約（I 節）と GitHub の追加製品の規約（Actions の節。2026-11-13 に `github/site-policy` から直に取り寄せた）
- 著作権法（第21条、第23条）
- 個人情報保護法（第2条、第28条）
- 刑法（第230条）
- 民法（第709条）
- arXiv のライセンスの案内（info.arxiv.org/help/license/）
- SSRN の利用規約（2026-11-05 の写し）

## 取り寄せられなかった文

- Zenodo の記録の頁は取り寄せていません。README の「掲載先を正とします」の注記は、そのため残しています。

## 弁護士について

この点検は Claude が行いました。
弁護士は、この点検を見ていません。
