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

## 調べた法令

- 著作権法（第21条、第23条）
- 個人情報保護法（第2条）
- arXiv のライセンスの案内（info.arxiv.org/help/license/）

## 取り寄せられなかった文

- SSRN の利用規約は取り寄せていません。
- Zenodo の記録は作業環境から開けず、取り寄せの仕事でも記録の頁は取り寄せていません。

## 弁護士について

この点検は Claude が行いました。
弁護士は、この点検を見ていません。
