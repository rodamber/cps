#!/usr/bin/env python3

from random import randint
from math import gcd, ceil, floor, sqrt


def __factorize(n):
    """Classical implementation of integer factorization. This is used just to
    test."""

    factors = []
    d = 2
    saved = n

    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)

    from numpy import prod
    assert prod(factors) == saved

    return factors


def __order(x, N):
    # We want to find r such that x**r % N == 1
    assert gcd(x, N) == 1

    r = 2
    while pow(x, r, N) != 1:
        r += 1

    assert pow(x, r, N) == 1
    return r


def prime(n):
    """Primality test by trial division."""

    if n == 2:
        return True
    elif n < 2 or n % 2 == 0:
        return False
    else:
        return not any(n % x == 0 for x in range(3, ceil(sqrt(n)) + 1, 2))


def composite(n):
    return not prime(n)


def found(factors, f):
    if f > 1:
        factors.append(f)


def factorize_helper(N):
    factors = []
    while N > 1 and composite(N):
        while N % 2 == 0:
            found(factors, 2)
            N //= 2
        if N > 1:
            x = randint(2, N - 1)
            d = gcd(x, N)
            if d != 1:  # Then d is a factor of N.
                found(factors, d)
                N //= d
            else:
                r = __order(x, N)
                y = r // 2
                if r % 2 == 0 and 1 < y < N - 1:
                    f1 = gcd(y - 1, N)
                    f2 = gcd(y + 1, N)

                    found(factors, f1)
                    found(factors, f2)

                    N = N // f1 // f2
    found(factors, N)
    return factors


def factorize(N):
    """Shor's algorithm."""
    factors = []
    left = [N]

    for n in left:
        if composite(n):
            left.extend(factorize_helper(n))
        else:
            factors.append(n)

    return factors


def partial_quots(x):
    """Returns the partial quotients of the continued fraction of x."""
    num, den = x.as_integer_ratio()

    quot, mod = divmod(num, den)
    partials = [quot]
    num = mod

    while num > 0:
        quot, mod = divmod(den, num)
        partials.append(quot)
        num, den = mod, num

    return partials


def qth_conv(x, q):
    """Returns the qth convergent to the continued fraction of x."""
    if q == 0:
        return partial_quots(x)[0]

    partials = partial_quots(x)
    acc = partials[q]

    for p in reversed(partials[:q]):
        acc = p + 1 / acc
    return acc


def denominator(x, qmax):
    """Finds the denominator q of the best rational approximation p/q for x
    with q < qmax."""
    y = x
    q0, q1, q2 = 0, 1, 0

    while True:
        z = y - floor(y)  # decimal part of y
        if z < 0.5 / qmax**2:
            return q1

        y = 1 / z
        q2 = floor(y) * q1 + q0

        if q2 >= qmax:
            return q1

        q0, q1 = q1, q2