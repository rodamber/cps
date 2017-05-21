#!/usr/bin/env python3

import string
from sympy import Symbol

from linalg import conj, vec, mat, tensor

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z \
    = [Symbol(x) for x in string.ascii_lowercase]


def test_mul():
    assert vec(a, b) * vec(c, d) == c * conj(a) + d * conj(b)

    assert vec(e, f) * mat(a, b, c, d, m=2, n=2) == \
        mat(a * conj(e) + c * conj(f),
            b * conj(e) + d * conj(f), m=1, n=2)

    assert mat(a, b, c, d, m=2, n=2) * vec(e, f) == \
        mat(conj(a) * e + conj(b) * f,
            conj(c) * e + conj(d) * f, m=2, n=1)

    assert mat(a, b, c, d, m=2, n=2) * mat(e, f, g, h, m=2, n=2) == \
        mat(conj(a) * e + conj(b) * g, conj(a) * f + conj(b) * h,
            conj(c) * e + conj(d) * g, conj(c) * f + conj(d) * h, m=2, n=2)


def test_outer_product():
    assert vec(a, b) ** vec(c, d) == \
        mat(a * conj(c), a * conj(d),
            b * conj(c), b * conj(d), m=2, n=2)


def test_tensor_product():
    assert tensor(vec(a, b), vec(c, d)) == \
        vec(a * c, a * d, b * c, b * d)

    assert tensor(mat(a, b, c, d, m=2, n=2), mat(e, f, g, h, m=2, n=2)) == \
        mat(a * e, a * f, b * e, b * f,
            a * g, a * h, b * g, b * h,
            c * e, c * f, d * e, d * f,
            c * g, c * h, d * g, d * h, m=4, n=4)

    assert tensor(vec(a, b), mat(e, f, g, h, m=2, n=2)) == \
        mat(a * e, a * f, b * e, b * f,
            a * g, a * h, b * g, b * h, m=2, n=4)

    assert tensor(mat(e, f, g, h, m=2, n=2), vec(a, b)) == \
        mat(e * a, f * a,
            e * b, f * b,
            g * a, h * a,
            g * b, h * b, m=4, n=2)


def test_add():
    assert vec(a, b) + vec(c, d) == vec(a + c, b + d)

    assert mat(a, b, c, d, m=2, n=2) + mat(e, f, g, h, m=2, n=2) == \
        mat(a + e, b + f,
            c + g, d + h, m=2, n=2)


def test_eq():
    assert vec(a, b) == vec(a, b)

    assert vec(a, b) != vec(a, f)
    assert vec(a, b) != vec(e, b)
    assert vec(a, b) != vec(e, f)

    assert mat(a, b, c, d, m=2, n=2) == mat(a, b, c, d, m=2, n=2)

    assert mat(a, b, c, d, m=2, n=2) != mat(e, b, c, d, m=2, n=2)
    assert mat(a, b, c, d, m=2, n=2) != mat(a, f, c, d, m=2, n=2)
    assert mat(a, b, c, d, m=2, n=2) != mat(a, b, g, d, m=2, n=2)
    assert mat(a, b, c, d, m=2, n=2) != mat(a, b, c, h, m=2, n=2)
