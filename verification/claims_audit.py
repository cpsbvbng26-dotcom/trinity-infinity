#!/usr/bin/env python3
"""三本の論文に印字されている数値を、一つずつ計算し直して突き合わせる。

`independent_check.py` は「定理が正しいか」を見るスクリプトでした。
これは別の問いに答えます —— **論文の紙面に印字されている数字は、その通りに出るのか。**

論文本文から数値を書き写し、その隣に計算し直した値を並べます。
判定は次の三つです。

  MATCH     印字された値と計算値が、示した許容差の中で一致する
  CONSISTENT  乱数を使う主張のため一致は求められない。分布の理論値と整合する
  MISMATCH  一致しない

NumPy のみを必要とします。乱数種は固定してあります。
"""

import itertools
import sys

import numpy as np

RNG_SEED = 20260905

rows = []          # (paper, locus, claim, printed, recomputed, verdict)
mismatches = []


def record(paper, locus, claim, printed, recomputed, ok, kind="MATCH"):
    verdict = kind if ok else "MISMATCH"
    rows.append((paper, locus, claim, printed, recomputed, verdict))
    if not ok:
        mismatches.append("%s %s — %s" % (paper, locus, claim))


# ---------------------------------------------------------------- 共通の道具

# σ(T1,T2,T3) = (T3,T1,T2) を表す行列。Series I 第2節の定義そのまま。
P3 = np.array([[0, 0, 1],
               [1, 0, 0],
               [0, 1, 0]], dtype=float)


def cyclic_matrix(n):
    """Series III 第3.1節: (σn(T))i = T(i−1 mod n)。"""
    P = np.zeros((n, n))
    for i in range(n):
        P[i, (i - 1) % n] = 1.0
    return P


def stage_payoffs():
    """Series I 第3節: πC(n)=n+1, πD(n)=n+2。n は協調した相手の人数。"""
    table = []
    for profile in itertools.product("CD", repeat=3):
        pay = []
        for i in range(3):
            n = sum(1 for j in range(3) if j != i and profile[j] == "C")
            pay.append(n + 1 if profile[i] == "C" else n + 2)
        table.append((profile, tuple(pay)))
    return table


def hull_volume(points):
    """3次元の凸包の体積。全ての3点組から支持超平面を拾い、面ごとに扇状に分割する。

    点が8個なので総当たりで足ります（SciPy を持ち込まないため）。
    """
    pts = np.unique(np.asarray(points, dtype=float), axis=0)
    n = len(pts)
    centre = pts.mean(axis=0)
    planes = {}
    for i, j, k in itertools.combinations(range(n), 3):
        a, b, c = pts[i], pts[j], pts[k]
        nor = np.cross(b - a, c - a)
        norm = np.linalg.norm(nor)
        if norm < 1e-9:
            continue
        nor = nor / norm
        off = nor @ a
        vals = pts @ nor - off
        if np.all(vals <= 1e-9):
            pass
        elif np.all(vals >= -1e-9):
            nor, off = -nor, -off
        else:
            continue                      # 支持超平面ではない
        key = tuple(np.round(np.concatenate([nor, [off]]), 9))
        members = set(np.where(np.abs(pts @ nor - off) < 1e-9)[0])
        planes.setdefault(key, set()).update(members)

    volume = 0.0
    for key, members in planes.items():
        idx = sorted(members)
        nor = np.array(key[:3])
        a = pts[idx[0]]
        u = pts[idx[1]] - a
        u = u - (u @ nor) * nor
        u = u / np.linalg.norm(u)
        w = np.cross(nor, u)
        ordered = sorted(idx[1:],
                         key=lambda t: np.arctan2((pts[t] - a) @ w, (pts[t] - a) @ u))
        for x, y in zip(ordered, ordered[1:]):
            volume += abs((a - centre) @ np.cross(pts[x] - a, pts[y] - a)) / 6.0
    return volume, len(planes)


# ================================================================ Series I

alpha = 0.6
p1 = np.array([1.0, 0.0, 0.0])
T_star = np.linalg.solve(np.eye(3) - alpha * P3, (1 - alpha) * p1)
printed = np.array([0.510204, 0.306122, 0.183673])
record("I", "§2 Remark 1",
       "補正した作用素 p=(1,0,0), α=0.6 の不動点",
       "(0.510204, 0.306122, 0.183673)",
       "(%.6f, %.6f, %.6f)" % tuple(T_star),
       np.abs(T_star - printed).max() < 5e-7)

# 反復が本当にその点へ行くか（閉形式を信じずに回す）
rng = np.random.default_rng(RNG_SEED)
worst = 0.0
for _ in range(5):
    x = rng.random(3)
    for _ in range(400):
        x = alpha * (P3 @ x) + (1 - alpha) * p1
    worst = max(worst, np.abs(x - T_star).max())
record("I", "§2 Remark 1",
       "独立な初期値5点がすべて同一点へ収束（差 0.00）",
       "差 0.00",
       "最大差 %.1e" % worst,
       worst < 1e-15)

# Theorem 1 は不等号だが、線形部分が α×等長写像なので等号になる
rng = np.random.default_rng(RNG_SEED + 1)
worst_eq = 0.0
for _ in range(2000):
    x, y = rng.random(3), rng.random(3)
    lhs = np.linalg.norm((alpha * (P3 @ x) + (1 - alpha) * p1)
                         - (alpha * (P3 @ y) + (1 - alpha) * p1))
    worst_eq = max(worst_eq, abs(lhs - alpha * np.linalg.norm(x - y)))
record("I", "§2 Theorem 1",
       "‖f(x)−f(y)‖ ≤ α‖x−y‖（実際には等号）",
       "≤ α‖x−y‖",
       "= α‖x−y‖、差の上限 %.1e" % worst_eq,
       worst_eq < 1e-15)

# 自己言及的な統合。極限は初期値の三成分の平均に等しく、その分布は解析的に分かる。
rng = np.random.default_rng(RNG_SEED + 2)
starts = rng.random((1000, 3))
steps = []
limits = []
for x0 in starts:
    x = x0.copy()
    n = 0
    while True:
        nxt = np.full(3, (P3 @ x).mean())     # I(y) = (ȳ,ȳ,ȳ) との合成
        n += 1
        if np.abs(nxt - x).max() < 1e-15:
            break
        x = nxt
    steps.append(n)
    limits.append(x[0])
limits = np.array(limits)
record("I", "§2 Remark 1",
       "自己言及的な統合は1000試行すべて1段で収束（100%）",
       "100%",
       "%.1f%%" % (100.0 * sum(1 for s in steps if s <= 2) / len(steps)),
       all(s <= 2 for s in steps))

# 極限は U(0,1) の3個の平均。したがって理論値 平均 1/2、標準偏差 1/6。
record("I", "§2 Remark 1",
       "極限の平均 0.4995（一意でないことの証拠）",
       "0.4995",
       "理論値 0.500000、本実行 %.4f" % limits.mean(),
       abs(limits.mean() - 0.5) < 0.02, kind="CONSISTENT")
record("I", "§2 Remark 1",
       "極限の標準偏差 0.1676",
       "0.1676",
       "理論値 %.4f（=1/6）、本実行 %.4f" % (1 / 6, limits.std(ddof=1)),
       abs(0.1676 - 1 / 6) < 0.01, kind="CONSISTENT")
record("I", "§2 Remark 1",
       "極限の範囲 [0.0403, 0.9589]",
       "[0.0403, 0.9589]",
       "本実行 [%.4f, %.4f]（台は [0,1]）" % (limits.min(), limits.max()),
       0.0 <= 0.0403 and 0.9589 <= 1.0, kind="CONSISTENT")

table = stage_payoffs()
record("I", "§3 Table 1",
       "3人2戦略の完全な利得表は 2³ = 8 通り",
       "8 行",
       "%d 行" % len(table),
       len(table) == 8)

expected = {("C", "C", "C"): (3, 3, 3), ("C", "C", "D"): (2, 2, 4),
            ("C", "D", "C"): (2, 4, 2), ("D", "C", "C"): (4, 2, 2),
            ("C", "D", "D"): (1, 3, 3), ("D", "C", "D"): (3, 1, 3),
            ("D", "D", "C"): (3, 3, 1), ("D", "D", "D"): (2, 2, 2)}
got = dict(table)
bad = [k for k in expected if got[k] != expected[k]]
record("I", "§3 Table 1",
       "8行すべての利得が印字どおり",
       "Table 1",
       "一致しない行 %d" % len(bad),
       not bad)

dominates = all(
    got[tuple("D" if j == i else profile[j] for j in range(3))][i]
    > got[tuple("C" if j == i else profile[j] for j in range(3))][i]
    for i in range(3) for profile in itertools.product("CD", repeat=3))
record("I", "§3",
       "一回限りのゲームでは裏切りが強支配",
       "強支配する",
       "する" if dominates else "しない",
       dominates)

pareto = all(a > b for a, b in zip(got[("C", "C", "C")], got[("D", "D", "D")]))
record("I", "§3",
       "(C,C,C) が (D,D,D) をパレート支配",
       "する",
       "する" if pareto else "しない",
       pareto)

# grim trigger: VC = 3/(1−δ), VD = 4 + 2δ/(1−δ)。VC ≥ VD ⟺ δ ≥ 1/2。
grid = np.linspace(1e-6, 1 - 1e-6, 2000001)
sustain = (3 / (1 - grid)) >= (4 + 2 * grid / (1 - grid)) - 1e-12
delta_star = grid[np.argmax(sustain)]
record("I", "§3",
       "協調が持続する閾値 δ* = 1/2",
       "0.5",
       "%.6f" % delta_star,
       abs(delta_star - 0.5) < 1e-5)

basel = float(np.sum(1.0 / np.arange(1, 4000001, dtype=float) ** 2))
record("I", "§5",
       "∑ 1/n² = π²/6（バーゼル問題）",
       "π²/6 = %.9f" % (np.pi ** 2 / 6),
       "%.9f（400万項）" % basel,
       abs(basel - np.pi ** 2 / 6) < 1e-6)

# ================================================================ Series II

a_vec = np.array([0.5, 0.7, 0.3])
p2 = np.array([1.0, 0.0, 0.5])
D = np.diag(a_vec)
T2 = np.linalg.solve(np.eye(3) - D @ P3, (np.eye(3) - D) @ p2)
printed2 = np.array([0.754190, 0.527933, 0.508380])
record("II", "§3.1",
       "異方的な作用素 p=(1,0,0.5), a=(0.5,0.7,0.3) の不動点",
       "(0.754190, 0.527933, 0.508380)",
       "(%.6f, %.6f, %.6f)" % tuple(T2),
       np.abs(T2 - printed2).max() < 5e-7)

rng = np.random.default_rng(RNG_SEED + 3)
worst2 = 0.0
for _ in range(6):
    x = rng.random(3)
    for _ in range(600):
        x = a_vec * (P3 @ x) + (1 - a_vec) * p2
    worst2 = max(worst2, np.abs(x - T2).max())
record("II", "§3.1",
       "独立な初期値6点が最大偏差 1.1×10⁻¹⁶ で同一点へ",
       "1.1×10⁻¹⁶",
       "%.1e" % worst2,
       worst2 < 1e-15)

# 20,000 組の経験的上限（論文は 0.699973）と、作用素ノルムそのもの
rng = np.random.default_rng(RNG_SEED + 4)
X = rng.random((20000, 3))
Y = rng.random((20000, 3))
num = np.linalg.norm((X - Y) @ (D @ P3).T, axis=1)
den = np.linalg.norm(X - Y, axis=1)
emp = float(np.max(num / den))
record("II", "§3.1",
       "20,000 組の経験的な縮小比の上限 0.699973（予測 max aᵢ = 0.7）",
       "0.699973",
       "本実行 %.6f" % emp,
       emp <= 0.7 + 1e-12 and emp > 0.69, kind="CONSISTENT")

op_norm = np.linalg.norm(D @ P3, 2)
record("II", "§3.1",
       "max aᵢ は「タイトな上界」（実際には作用素ノルムそのもの）",
       "タイトな上界 0.7",
       "‖DQ‖₂ = %.12f" % op_norm,
       abs(op_norm - a_vec.max()) < 1e-12)

# 離散時間の安定性 V(x_{n+1}) ≤ max(ai)² V(x_n)
rng = np.random.default_rng(RNG_SEED + 5)
ratios = []
for _ in range(5000):
    x = rng.random(3)
    nxt = a_vec * (P3 @ x) + (1 - a_vec) * p2
    v0 = np.sum((x - T2) ** 2)
    v1 = np.sum((nxt - T2) ** 2)
    if v0 > 1e-18:
        ratios.append(v1 / v0)
record("II", "§3.2",
       "V(xₙ₊₁) ≤ max(aᵢ)² V(xₙ)",
       "≤ %.4f" % (a_vec.max() ** 2),
       "実測の最大比 %.6f" % max(ratios),
       max(ratios) <= a_vec.max() ** 2 + 1e-12)

# minmax
payoff = dict(table)
minmax = []
for i in range(3):
    worst_for_i = -np.inf
    best_of_others = np.inf
    for others in itertools.product("CD", repeat=2):
        best = max(payoff[tuple(("C" if k == i else others[k - (k > i)])
                                for k in range(3))][i],
                   payoff[tuple(("D" if k == i else others[k - (k > i)])
                                for k in range(3))][i])
        best_of_others = min(best_of_others, best)
    minmax.append(best_of_others)
record("II", "§4",
       "各プレイヤーのミニマックス利得は 2（対称性より全員同じ）",
       "2, 2, 2",
       "%s" % (tuple(minmax),),
       minmax == [2, 2, 2])

pts = np.array([p for _, p in table], dtype=float)
vol, nfacets = hull_volume(pts)
record("II", "§4",
       "8つの利得の凸包の体積は 4.00",
       "4.00",
       "%.6f（面 %d 枚）" % (vol, nfacets),
       abs(vol - 4.0) < 1e-9)

extreme = []
for idx in range(len(pts)):
    sub = np.delete(pts, idx, axis=0)
    if hull_volume(sub)[0] < vol - 1e-9:
        extreme.append(idx)
record("II", "§4",
       "8つの利得すべてが端点",
       "8 / 8",
       "%d / 8" % len(extreme),
       len(extreme) == 8)

sums = [sum(p) for _, p in table]
argmax = [i for i, s in enumerate(sums) if s == max(sums)]
record("II", "§4",
       "(3,3,3) は利得の総和を最大にする唯一の頂点",
       "唯一",
       "総和最大は %d 個（%s）" % (len(argmax), table[argmax[0]][1]),
       len(argmax) == 1 and table[argmax[0]][1] == (3, 3, 3))

K = np.array([[2.0, -1, -1], [-1, 2, -1], [-1, -1, 2]])
eig = np.sort(np.linalg.eigvalsh(K))
record("II", "§6",
       "3閉路のグラフラプラシアン K の固有値は 0, 3, 3",
       "0, 3, 3",
       "%.6f, %.6f, %.6f" % tuple(eig),
       np.allclose(eig, [0, 3, 3], atol=1e-9))

alpha_K = 0.25
rho = float(np.max(np.abs(np.linalg.eigvals(alpha_K * K))))
record("II", "§6",
       "α=0.25 のとき ρ(αK) = 0.75 < 1",
       "0.75",
       "%.6f" % rho,
       abs(rho - 0.75) < 1e-9)

K_inf = K @ np.linalg.inv(np.eye(3) - alpha_K * K)
printed_K = np.array([[8.0, -4, -4], [-4, 8, -4], [-4, -4, 8]])
record("II", "§6",
       "K∞ = [[8,−4,−4],[−4,8,−4],[−4,−4,8]]",
       "上記の行列",
       "最大差 %.1e" % np.abs(K_inf - printed_K).max(),
       np.abs(K_inf - printed_K).max() < 1e-12)

partial = np.zeros((3, 3))
term = K.copy()
for _ in range(200):
    partial = partial + term
    term = alpha_K * term @ K
dev = float(np.abs(partial - K_inf).max())
record("II", "§6",
       "200項の部分和と閉形式は 3×10⁻¹⁵ 以内で一致",
       "3×10⁻¹⁵ 以内",
       "%.1e" % dev,
       dev < 3e-15)

# ================================================================ Series III

table3 = []
for n in range(2, 9):
    Pn = cyclic_matrix(n)
    iso = float(np.abs(Pn @ Pn.T - np.eye(n)).max())
    rng = np.random.default_rng(RNG_SEED + 100 + n)
    anchor = rng.random(n)
    Tn = np.linalg.solve(np.eye(n) - 0.6 * Pn, 0.4 * anchor)
    dev = 0.0
    for _ in range(5):
        x = rng.random(n)
        for _ in range(400):
            x = 0.6 * (Pn @ x) + 0.4 * anchor
        dev = max(dev, float(np.abs(x - Tn).max()))
    involution = bool(np.allclose(Pn @ Pn, np.eye(n)))
    table3.append((n, iso, dev, involution))

record("III", "§3.1 Table 1",
       "n = 2〜8 のすべてで PₙPₙᵀ = I（等長写像の誤差 0）",
       "0",
       "最大 %.1e" % max(r[1] for r in table3),
       all(r[1] == 0.0 for r in table3))
record("III", "§3.1 Table 1",
       "n = 2〜8 のすべてで閉形式の不動点へ収束（最大 1.1×10⁻¹⁶）",
       "1.1×10⁻¹⁶",
       "最大 %.1e" % max(r[2] for r in table3),
       max(r[2] for r in table3) < 1e-15)
record("III", "§3.1 Table 1",
       "P² = I となるのは n = 2 のみ",
       "n=2 のみ Yes",
       "Yes は n = %s" % [r[0] for r in table3 if r[3]],
       [r[0] for r in table3 if r[3]] == [2])
# 紙面は「maximum deviation 1.1×10−16 ... for every n ≥ 4; exact for n=2,3」と
# 書き分けている。上の表（乱数種を固定してある）では n=2,3 がちょうど 0 になり、
# 紙面どおりに再現する。**だがこれは丸めがそう落ちただけである。**
#
# 基準点を別に引くと 0 でなくなる。それを見るために、**上の種は動かさずに**
# 別の種でもう一度だけ引く。既存の期待値も種も変えていない。
# 等長写像の誤差 0 のほうは、置換行列の成分が 0 と 1 だけなので本当に厳密である。
# ERRATA の N6 —— この検査が落ちるときは、N6 を書き直す番である。
_probe = {}
for _n in (2, 3):
    _Pn = cyclic_matrix(_n)
    _rng = np.random.default_rng(RNG_SEED + 900 + _n)
    _anchor = _rng.random(_n)
    _Tn = np.linalg.solve(np.eye(_n) - 0.6 * _Pn, 0.4 * _anchor)
    _d = 0.0
    for _ in range(5):
        _x = _rng.random(_n)
        for _ in range(400):
            _x = 0.6 * (_Pn @ _x) + 0.4 * _anchor
        _d = max(_d, float(np.abs(_x - _Tn).max()))
    _probe[_n] = _d
record("III", "§3.1 Table 1",
       "「exact for n=2,3」は算術の性質ではなく、基準点の引き方に依る",
       "exact（紙面。上の表の種では再現する）",
       "別の基準点では n=2: %.3e / n=3: %.3e" % (_probe[2], _probe[3]),
       any(v != 0.0 for v in _probe.values()))

record("III", "§3.2",
       "n = 3 は巡回置換がそれ自身の逆写像にならない最小の n",
       "3",
       "%d" % min(r[0] for r in table3 if not r[3]),
       min(r[0] for r in table3 if not r[3]) == 3)

# 三要素であることは収束に効いていない（Series III の主結論を n を変えて直接確認）
rng = np.random.default_rng(RNG_SEED + 7)
rate_dev = 0.0
for n in range(2, 9):
    Pn = cyclic_matrix(n)
    anchor = rng.random(n)
    Tn = np.linalg.solve(np.eye(n) - 0.6 * Pn, 0.4 * anchor)
    x = rng.random(n)
    d0 = np.linalg.norm(x - Tn)
    for k in range(1, 25):
        x = 0.6 * (Pn @ x) + 0.4 * anchor
        rate_dev = max(rate_dev, abs(np.linalg.norm(x - Tn) - 0.6 ** k * d0))
record("III", "§3.1 Theorem 1",
       "収束の速さは n に依存しない（誤差はちょうど αᵏ 倍）",
       "αᵏ、n に依存しない",
       "24反復までの差の上限 %.1e" % rate_dev,
       rate_dev < 1e-15)

# ================================================================ 出力

TITLES = {
    "I":   "Series I —— 三元の再帰作用素と収束定理",
    "II":  "Series II —— 座標ごとに異なる混合率への一般化",
    "III": "Series III —— 「三である必要はあるのか」",
}

print()
print("論文に印字されている数値の突き合わせ")
print("=" * 62)
for paper in ("I", "II", "III"):
    print()
    print(TITLES[paper])
    print("-" * 62)
    for _, locus, claim, printed_v, recomputed, verdict in rows:
        if _ != paper:
            continue
        print("  %-16s %s" % (locus, claim))
        print("  %-16s 印字   %s" % ("", printed_v))
        print("  %-16s 計算   %s   [%s]" % ("", recomputed, verdict))
        print()

n_match = sum(1 for r in rows if r[5] == "MATCH")
n_cons = sum(1 for r in rows if r[5] == "CONSISTENT")
print("=" * 62)
print("%d 項目 —— MATCH %d / CONSISTENT %d / MISMATCH %d"
      % (len(rows), n_match, n_cons, len(mismatches)))
if mismatches:
    print()
    print("一致しなかった主張:")
    for m in mismatches:
        print("  - " + m)
    sys.exit(1)
print("三本の論文に印字されている数値は、すべて計算し直して確認できました。")
