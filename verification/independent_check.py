#!/usr/bin/env python3
"""Verification script for "What Survives Verification".

Every numerical claim in the paper is produced by this file. Run it with

    python3 audit_verification.py

Requires numpy only. Deterministic: all randomness is seeded.

The script checks four things.

  A. The residual theorem. For f(x) = a*Q*x + (1-a)*p with Q any linear
     isometry of R^n, the displacement is scaled exactly by a, the fixed
     point is the closed form (1-a)(I-aQ)^{-1}p, and the error decays
     exactly geometrically. Checked for permutations, rotations and
     reflections, from starting points inside and far outside [0,1]^n.

  B. The three inessential features. Same operator with n != 3, with Q
     not a permutation, and with iterates leaving the unit cube.

  C. The anisotropic constant. For the per-coordinate blend of Series II,
     the sharp contraction constant is the largest blend parameter,
     equal to the spectral norm of D*Q.

  D. The original operator's non-uniqueness, reproduced independently of
     the Series I script: self-referential integration leaves every
     constant vector fixed, so the limit depends on the starting point.
"""

import numpy as np

RNG = np.random.default_rng(20260905)
EPS = 1e-12


def report(label, ok, detail=''):
    print('%-58s %s  %s' % (label, 'PASS' if ok else 'FAIL', detail))
    return ok


def random_orthogonal(n):
    """A Haar-distributed orthogonal matrix via QR of a Gaussian matrix."""
    q, r = np.linalg.qr(RNG.normal(size=(n, n)))
    return q * np.sign(np.diag(r))


def cyclic_shift(n):
    return np.roll(np.eye(n), 1, axis=0)


def rotation(n, theta):
    """Rotation by theta in the (0,1) plane, identity elsewhere."""
    q = np.eye(n)
    c, s = np.cos(theta), np.sin(theta)
    q[0, 0], q[0, 1], q[1, 0], q[1, 1] = c, -s, s, c
    return q


def reflection(n):
    q = np.eye(n)
    q[0, 0] = -1.0
    return q


def fixed_point(q, p, a):
    return (1 - a) * np.linalg.solve(np.eye(len(p)) - a * q, p)


def iterate(q, p, a, x0, steps):
    x = x0.copy()
    for _ in range(steps):
        x = a * (q @ x) + (1 - a) * p
    return x


# ---------------------------------------------------------------- A

def check_operator(name, q, n, a, spread, trials=200, steps=400):
    p = RNG.uniform(0, 1, n)
    star = fixed_point(q, p, a)

    f = lambda x: a * (q @ x) + (1 - a) * p

    # exact scaling of displacement, not merely a bound
    worst = 0.0
    for _ in range(trials):
        x = RNG.uniform(-spread, spread, n)
        y = RNG.uniform(-spread, spread, n)
        lhs = np.linalg.norm(f(x) - f(y))
        rhs = a * np.linalg.norm(x - y)
        worst = max(worst, abs(lhs - rhs))

    # convergence to the closed form from far-flung starts
    dev = 0.0
    for _ in range(5):
        x0 = RNG.uniform(-spread, spread, n)
        dev = max(dev, np.linalg.norm(iterate(q, p, a, x0, steps) - star))

    # error decays exactly as a**k
    x0 = RNG.uniform(-spread, spread, n)
    d0 = np.linalg.norm(x0 - star)
    geo = max(abs(np.linalg.norm(iterate(q, p, a, x0, k) - star) - a ** k * d0)
              for k in range(1, 25))

    ok = worst < 1e-12 and dev < 1e-9 and geo < 1e-12
    report('A. %s (n=%d, a=%.2f, start range +-%g)' % (name, n, a, spread), ok,
           'isometry err %.1e | fixed-point dev %.1e | geometric err %.1e'
           % (worst, dev, geo))
    return ok


# ---------------------------------------------------------------- D

def check_self_referential(n=3, trials=1000):
    """The operator as the 2025 text most naturally reads it."""
    limits = []
    steps_needed = []
    for _ in range(trials):
        x = RNG.uniform(0, 1, n)
        prev = None
        for k in range(1, 51):
            x = np.full(n, np.roll(x, 1).mean())      # permute, then blend to the mean
            if prev is not None and np.allclose(x, prev, atol=EPS):
                break
            prev = x.copy()
        limits.append(x[0])
        steps_needed.append(k)
    limits = np.array(limits)
    spread = limits.max() - limits.min()
    ok = spread > 0.5                                  # limits demonstrably differ
    report('D. self-referential blend has no unique fixed point', ok,
           'limit mean %.4f sd %.4f range [%.4f, %.4f]'
           % (limits.mean(), limits.std(), limits.min(), limits.max()))
    return ok


def main():
    results = []
    print('A. The residual theorem: an isometry scaled by a, plus a fixed offset\n')

    for n in (2, 3, 4, 5, 8):
        results.append(check_operator('cyclic permutation', cyclic_shift(n), n, 0.6, 1.0))

    print()
    print('B. Each named structural feature is inessential\n')
    results.append(check_operator('rotation, not a permutation', rotation(4, 0.7), 4, 0.6, 1.0))
    results.append(check_operator('reflection (det = -1)', reflection(5), 5, 0.45, 1.0))
    results.append(check_operator('Haar-random orthogonal', random_orthogonal(6), 6, 0.8, 1.0))
    results.append(check_operator('starts far outside the unit cube',
                                  random_orthogonal(3), 3, 0.6, 50.0))
    results.append(check_operator('n = 2, the case Series III set aside',
                                  cyclic_shift(2), 2, 0.9, 1.0))

    print()
    print('C. The anisotropic constant is the spectral norm of D*Q\n')
    for n, a_vec in ((3, [0.5, 0.7, 0.3]), (5, [0.2, 0.9, 0.4, 0.85, 0.1])):
        a_vec = np.array(a_vec)
        q = cyclic_shift(n)
        d = np.diag(a_vec)
        norm = np.linalg.norm(d @ q, 2)
        emp = 0.0
        for _ in range(20000):
            z = RNG.normal(size=n)
            emp = max(emp, np.linalg.norm(d @ (q @ z)) / np.linalg.norm(z))
        ok = abs(norm - a_vec.max()) < 1e-12 and emp <= a_vec.max() + 1e-12
        results.append(report('C. sharp constant (n=%d)' % n, ok,
                              'spectral norm %.12f | max a_i %.12f | empirical sup %.6f'
                              % (norm, a_vec.max(), emp)))

    print()
    print('D. The claim that did not survive\n')
    results.append(check_self_referential())

    print()
    print('%d checks, %d passed' % (len(results), sum(results)))
    return 0 if all(results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
