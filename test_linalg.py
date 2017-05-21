#!/usr/bin/env python3


from linalg import *


def test_mul():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    def conj(x):
        return x.conjugate()

    assert Vector(a, b) * Vector(c, d) == \
        c * a.conjugate() + d * b.conjugate()

    assert Vector(e, f) * Matrix(a, b, c, d, m=2, n=2) == \
        Matrix(a * conj(e) + c * conj(f),
               b * conj(e) + d * conj(f), m=1, n=2)

    assert Matrix(a, b, c, d, m=2, n=2) * Vector(e, f) == \
        Matrix(conj(a) * e + conj(b) * f,
               conj(c) * e + conj(d) * f, m=2, n=1)

    assert Matrix(a, b, c, d, m=2, n=2) * Matrix(e, f, g, h, m=2, n=2) == \
        Matrix(conj(a) * e + conj(b) * g, conj(a) * f + conj(b) * h,
               conj(c) * e + conj(d) * g, conj(c) * f + conj(d) * h, m=2, n=2)


def test_pow():
    import string
    from sympy import Symbol

    a, b, c, d = [Symbol(x) for x in string.ascii_letters[:4]]

    def conj(x):
        return x.conjugate()

    assert Vector(a, b) ** Vector(c, d) == \
        Matrix(a * conj(c), a * conj(d),
               b * conj(c), b * conj(d), m=2, n=2)


def test_tensor():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    assert tensor(Vector(a, b), Vector(c, d)) == \
        Vector(a * c, a * d, b * c, b * d)

    assert tensor(Matrix(a, b, c, d, m=2, n=2),
                  Matrix(e, f, g, h, m=2, n=2)) == \
        Matrix(a * e, a * f, b * e, b * f,
               a * g, a * h, b * g, b * h,
               c * e, c * f, d * e, d * f,
               c * g, c * h, d * g, d * h, m=4, n=4)

    assert tensor(Vector(a, b), Matrix(e, f, g, h, m=2, n=2)) == \
        Matrix(a * e, a * f, b * e, b * f,
               a * g, a * h, b * g, b * h, m=2, n=4)

    assert tensor(Matrix(e, f, g, h, m=2, n=2), Vector(a, b)) == \
        Matrix(e * a, f * a,
               e * b, f * b,
               g * a, h * a,
               g * b, h * b, m=4, n=2)


def test_add():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    assert Vector(a, b) + Vector(c, d) == \
        Vector(a + c, b + d)

    assert Matrix(a, b, c, d, m=2, n=2) + Matrix(e, f, g, h, m=2, n=2) == \
        Matrix(a + e, b + f,
               c + g, d + h, m=2, n=2)


def test_eq():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    assert Vector(a, b) == Vector(a, b)

    assert Vector(a, b) != Vector(a, f)
    assert Vector(a, b) != Vector(e, b)
    assert Vector(a, b) != Vector(e, f)

    assert Matrix(a, b, c, d, m=2, n=2) == Matrix(a, b, c, d, m=2, n=2)

    assert Matrix(a, b, c, d, m=2, n=2) != Matrix(e, b, c, d, m=2, n=2)
    assert Matrix(a, b, c, d, m=2, n=2) != Matrix(a, f, c, d, m=2, n=2)
    assert Matrix(a, b, c, d, m=2, n=2) != Matrix(a, b, g, d, m=2, n=2)
    assert Matrix(a, b, c, d, m=2, n=2) != Matrix(a, b, c, h, m=2, n=2)
