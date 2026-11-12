#!/usr/bin/env python3
"""散文が名乗る件数、依存、ワークフロー、窓口と様式、要旨、言語モデルの開示を当たる。

    python3 verification/check_meta.py

pypdf が要る（正誤表の監査を回して、その件数を数えるため）。ほかは標準ライブラリで動く。

見るもの。
  1. 散文が名乗る検証の件数。四本を実際に回して数え、README・verification/README.md・
     CLAUDE.md・CI の仕事の名前が名乗る数と突き合わせる（決めごと 5）。
  2. 依存。台本が読み込むのは標準ライブラリと NumPy と pypdf だけで、
     requirements.txt と CI もその二つしか入れない。
  3. ワークフロー。一番上で権限を読むだけに絞り、外部のアクションをコミットの値で固定する。
  4. 安全の窓口（SECURITY.md）と、誤りの知らせの様式。
  5. 保存版の要旨。日本語と英語の段落が、同じ数の文で並んでいる。キーワードが引用情報と同じ。
  6. 言語モデルの開示の表（道具・使ったところ・確かめた人）。
"""

import ast
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

passed, failures = 0, []


def check(label, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print("  PASS  " + label + (("  " + detail) if detail else ""))
    else:
        failures.append(label)
        print("  FAIL  " + label + (("  " + detail) if detail else ""))


def read(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return ""
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


README = read("README.md")
VREADME = read(os.path.join("verification", "README.md"))
CLAUDE = read("CLAUDE.md")
VERIFY = read(os.path.join(".github", "workflows", "verify.yml"))
CFF = read("CITATION.cff")
ZENODO = json.loads(read(".zenodo.json") or "{}")


def last_match(script, pattern):
    proc = subprocess.run([sys.executable, os.path.join("verification", script)], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    m = re.search(pattern, proc.stdout.decode("utf-8", "replace"))
    return m.groups() if m else None


# ------------------------------------------------------------ 1. 件数
print("\n1. 散文が名乗る検証の件数（決めごと 5）")
# 正規表現は、横断の検査（cpsbvbng26-dotcom の ecosystem.json）と同じもの。
th = last_match("independent_check.py", r"(\d+) checks, (\d+) passed")
au = last_match("claims_audit.py", r"(\d+) 項目 —— MATCH (\d+) / CONSISTENT (\d+) / MISMATCH (\d+)")
er = last_match("check_errata.py", r"(\d+) 件すべて通りました。")
ro = last_match("check_route.py", r"(\d+) 件すべて通りました。")
check("四本を回して件数を数えられる", all((th, au, er, ro)),
      "定理 %s・数値 %s・正誤表 %s・経路 %s" % (th and th[0], au and au[0], er and er[0], ro and ro[0]))
if all((th, au, er, ro)):
    T, P, E, R = int(th[0]), int(au[0]), int(er[0]), int(ro[0])
    claims = [
        ("README の英語の欄（定理）", README, r"`python3 verification/independent_check\.py` \((\d+) checks\)", T),
        ("README の英語の欄（数値）", README, r"`claims_audit\.py` \((\d+)\)", P),
        ("README の英語の欄（正誤表）", README, r"`check_errata\.py` \((\d+), needs pypdf\)", E),
        ("README の英語の欄（経路）", README, r"`check_route\.py` \((\d+)\)", R),
        ("README の「上の二本」の和", README, r"上の二本は NumPy のみを必要とし、乱数種を固定しています。(\d+) 項目すべてが通ります。", T + P),
        ("verification/README.md の表（定理）", VREADME, r"^\| `independent_check\.py` \|[^|]*\| (\d+) \|$", T),
        ("verification/README.md の表（数値）", VREADME, r"^\| `claims_audit\.py` \|[^|]*\| (\d+) \|$", P),
        ("verification/README.md の表（経路）", VREADME, r"^\| `check_route\.py` \|[^|]*\| (\d+) \|$", R),
        ("verification/README.md の実行例（定理）", VREADME, r"python3 independent_check\.py\s+# (\d+) 項目", T),
        ("verification/README.md の実行例（数値）", VREADME, r"python3 claims_audit\.py\s+# (\d+) 項目", P),
        ("verification/README.md の実行例（経路）", VREADME, r"python3 check_route\.py\s+# (\d+) 項目", R),
        ("verification/README.md の内訳（総数）", VREADME, r"(\d+) 項目のうち \d+ が `MATCH`", P),
        ("verification/README.md の内訳（MATCH）", VREADME, r"\d+ 項目のうち (\d+) が `MATCH`", int(au[1])),
        ("verification/README.md の内訳（CONSISTENT）", VREADME, r"、(\d+) が `CONSISTENT`、", int(au[2])),
        ("verification/README.md の内訳（MISMATCH）", VREADME, r"`MISMATCH` は (\d+) です。", int(au[3])),
        ("CLAUDE.md の一覧（定理）", CLAUDE, r"independent_check\.py\s+# 定理 (\d+) 項目", T),
        ("CLAUDE.md の一覧（数値）", CLAUDE, r"claims_audit\.py\s+# 印字された数値 (\d+) 項目", P),
        ("CLAUDE.md の一覧（正誤表）", CLAUDE, r"check_errata\.py\s+# 正誤表の監査 (\d+) 項目", E),
        ("CI の仕事の名前", VERIFY, r"name: 定理 (\d+) 項目 / 印字された数値 \d+ 項目", T),
    ]
    for label, text, pattern, want in claims:
        got = re.findall(pattern, text, re.M)
        check("%s が実際の %d と合う" % (label, want), got == [str(want)], "名乗り %s" % got)

# verification/README.md の冒頭は、表に挙げたスクリプトの本数を名乗る。表に行を足せばずれる。
_rows = re.findall(r"^\| `[^`]+\.py` \|", VREADME, re.M)
_named = re.findall(r"検証のスクリプトが (\d+) 本入っています", VREADME)
check("verification/README.md が名乗るスクリプトの本数が、表の行の数 %d と合う" % len(_rows),
      len(_rows) > 0 and _named == [str(len(_rows))], "名乗り %s" % _named)

# ------------------------------------------------------------ 2. 依存
print("\n2. 依存")
local, pyfiles = set(), []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "_sibling", "venv")]
    for f in filenames:
        if f.endswith(".py"):
            local.add(f[:-3])
            pyfiles.append(os.path.join(dirpath, f))
allowed = set(sys.stdlib_module_names) | {"numpy", "pypdf"} | local
foreign = []
for path in sorted(pyfiles):
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module]
        for n in names:
            if n.split(".")[0] not in allowed:
                foreign.append("%s: %s" % (os.path.relpath(path, ROOT), n))
check("読み込むのは標準ライブラリと NumPy と pypdf と、このリポジトリの台本だけ",
      not foreign, "; ".join(foreign[:4]) if foreign else "%d 本" % len(pyfiles))
reqs = [l.split(">")[0].split("=")[0].split("<")[0].strip()
        for l in read("requirements.txt").split("\n") if l.strip() and not l.startswith("#")]
check("requirements.txt が挙げるのは numpy と pypdf の二つだけ", reqs == ["numpy", "pypdf"], repr(reqs))
pips = re.findall(r"run:\s*pip install ([^\n]+)", VERIFY)
check("CI が入れるのは requirements.txt の中身だけ", pips == ["-r requirements.txt"], repr(pips))
manifests = [f for f in ("pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "package.json",
                         "environment.yml") if os.path.exists(os.path.join(ROOT, f))]
check("依存を書き足すほかの場所（pyproject.toml・package.json など）を置いていない", not manifests,
      ", ".join(manifests))

# ------------------------------------------------------------ 3. ワークフロー
print("\n3. ワークフローの権限と、外部のアクションの固定")
WF_DIR = os.path.join(ROOT, ".github", "workflows")
for f in sorted(os.listdir(WF_DIR)):
    if not f.endswith((".yml", ".yaml")):
        continue
    wf = read(os.path.join(".github", "workflows", f))
    top = re.search(r"^permissions:\n((?:  \S[^\n]*\n)+)", wf, re.M)
    perms = dict(re.findall(r"^  ([a-z-]+):\s*(\S+)", top.group(1), re.M)) if top else {}
    check("%s の権限が、一番上で読むだけ（contents: read）に絞られている" % f,
          perms == {"contents": "read"}, repr(perms))
    check("%s は仕事の単位で権限を広げていない" % f,
          not re.search(r"^    permissions:", wf, re.M) and "write-all" not in wf)
    uses = re.findall(r"uses:\s*(\S+)([^\n]*)", wf)
    bad = [u + c for u, c in uses
           if not u.startswith("./")
           and not (re.match(r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$", u) and re.match(r"^ # v\d", c))]
    check("%s の外部のアクションが、すべてコミットの値と版の注釈で固定されている（%d 個）" % (f, len(uses)),
          bool(uses) and not bad, "; ".join(bad))

# ------------------------------------------------------------ 4. 窓口と様式
print("\n4. 安全の窓口（SECURITY.md）と、誤りの知らせの様式")
SECURITY = read("SECURITY.md")
check("SECURITY.md があり、日本語と英語の欄を持つ",
      SECURITY.startswith("# 安全の問題の知らせ方 / Reporting a security issue\n")
      and "\n## 日本語\n" in SECURITY and "\n## English\n" in SECURITY)
# 2026-11-12。GitHub の非公開の報告は有効になっていない。在る窓口（ORCID の記録のメール）だけを書く。
check("SECURITY.md が、メールの窓口（ORCID の記録）と、GitHub の非公開の報告が無いことと、PDF を直さず正誤表で直すことを書いている",
      "[ORCID の記録](https://orcid.org/0009-0000-1406-0547)にあるメールアドレス" in SECURITY
      and "このリポジトリでは有効になっていません" in SECURITY and "is not enabled for this repository" in SECURITY
      and "Report a vulnerability" not in SECURITY
      and "直すのは正誤表の側です。" in SECURITY)
ERR = read(os.path.join(".github", "ISSUE_TEMPLATE", "error-report.yml"))
check("誤りの知らせの様式があり、erratum のラベルを付ける", "labels: [erratum]" in ERR)
for field in ("where", "printed", "correct", "basis", "found_by"):
    mf = re.search(r"id: %s\n(.*?)(?=\n  - type:|\Z)" % field, ERR, re.S)
    check("誤りの知らせの欄 %s があって必須" % field, mf is not None and "required: true" in mf.group(1))

# ------------------------------------------------------------ 5. 要旨と語
print("\n5. 保存版の要旨（日本語と英語）と、キーワード")


def paras(html):
    return re.findall(r"<p>(.*?)</p>", html, re.S)


def is_ja(t):
    return re.search(r"[぀-ヿ]", t) is not None


desc = ZENODO.get("description", "")
ja_p = [p for p in paras(desc) if is_ja(p)]
en_p = [p for p in paras(desc) if not is_ja(p)]
check("要旨の段落が日本語と英語で同じ数", bool(ja_p) and len(ja_p) == len(en_p),
      "%d・%d" % (len(ja_p), len(en_p)))
for i, (j, e) in enumerate(zip(ja_p, en_p), 1):
    nj = len([x for x in j.split("。") if x.strip()])
    ne = len([x for x in re.split(r"(?<=[.!?])\s+", e.strip()) if x.strip()])
    check("要旨の第 %d 段落の文の数が日本語と英語で同じ" % i, nj == ne, "%d・%d" % (nj, ne))
check("英語の要旨も、二つの条件と、残った縮小写像論法と、撤回の記録を書いている",
      bool(en_p) and "two conditions" in en_p[0] and "contraction-mapping argument" in en_p[0]
      and "Retracted claims" in en_p[0])
kw_block = re.search(r"^keywords:\n((?:  - [^\n]+\n)+)", CFF, re.M)
cff_kw = re.findall(r"^  - (.+)$", kw_block.group(1), re.M) if kw_block else []
check("CITATION.cff と .zenodo.json のキーワードが同じ並び",
      bool(cff_kw) and cff_kw == ZENODO.get("keywords"), "%d 語" % len(cff_kw))

# ------------------------------------------------------------ 6. 開示の表
print("\n6. 言語モデルの開示の表")
head = "| 道具 | 使ったところ | 確かめた人 |\n| --- | --- | --- |\n"
i = README.find(head)
rows = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \|$", README[i + len(head):].split("\n\n")[0], re.M) \
    if i >= 0 else []
check("README の「言語モデルの利用」に、道具・使ったところ・確かめた人の表がある",
      i > README.find("## 言語モデルの利用") > 0 and len(rows) > 0, "%d 行" % len(rows))
check("表の道具が、どれも作り手を括弧で添えている",
      bool(rows) and all(re.search(r"（[A-Za-z]+）$", r[0]) for r in rows), ", ".join(r[0] for r in rows))
check("表が、初版を生成した道具と、その記録の場所（E4）を挙げている",
      any(r[0] == "ChatGPT（OpenAI）" and "`E4`" in r[2] for r in rows))
check("README が言語モデルを著作者にしていない", "言語モデルは著作者ではありません。" in README)

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
