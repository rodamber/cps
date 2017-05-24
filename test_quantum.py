import quantum as qu

import string
from sympy import Symbol

import linalg as la

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z \
    = [Symbol(x) for x in string.ascii_lowercase]


def test_qureg():
    r = qu.Qureg()
    assert r.width == 1
    assert r.measure() == 0
    assert r.__repr__() == "1 |0> + 0 |1>"

    r = qu.Qureg(2)
    assert r.width == 2
    assert r.measure() == 0
    assert r.__repr__() == "1 |0> + 0 |1> + 0 |2> + 0 |3>"

    r = qu.Qureg(2, 1)
    assert r.width == 2
    assert r.measure() == 1
    assert r.__repr__() == "0 |0> + 1 |1> + 0 |2> + 0 |3>"


def test_unitary_op():
    assert qu.unitary_op(1, 0, qu.hadamard_op) == qu.hadamard_op

    assert qu.unitary_op(2, 0, qu.hadamard_op) == \
        la.mat(1, 0,  1,  0,
               0, 1,  0,  1,
               1, 0, -1,  0,
               0, 1,  0, -1, m=4, n=4) * 2**-0.5

    assert qu.unitary_op(2, 1, qu.hadamard_op) == \
        la.mat(1,  1, 0,  0,
               1, -1, 0,  0,
               0,  0, 1,  1,
               0,  0, 1, -1, m=4, n=4) * 2**-0.5

    assert qu.unitary_op(3, 1, qu.hadamard_op) == \
        la.mat(1, 0,  1,   0,  0, 0,  0,   0,
               0, 1,  0,   1,  0, 0,  0,   0,
               1, 0, -1,   0,  0, 0,  0,   0,
               0, 1,  0,  -1,  0, 0,  0,   0,
               0, 0,  0,   0,  1, 0,  1,   0,
               0, 0,  0,   0,  0, 1,  0,   1,
               0, 0,  0,   0,  1, 0, -1,   0,
               0, 0,  0,   0,  0, 1,  0,  -1, m=8, n=8) * 2**-0.5
