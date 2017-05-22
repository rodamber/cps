#!/usr/bin/env python3

from random import randint
from math import gcd, ceil, sqrt


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
    while x**r % N != 1:
        r += 1

    assert x**r % N == 1
    return r


def prime(n):
    """Primality test by trial division."""
    if n == 2:
        return True
    elif n < 2 or n % 2 == 0:
        return False
    else:
        return not any(n % x == 0 for x in range(3, ceil(sqrt(n)), 2))


def factorize(N):
    """Shor's algorithm."""
    factors = []

    while not prime(N):
        while N % 2 == 0:
            factors.append(2)
            N //= 2

        if N == 1:
            break

        x = randint(2, N - 1)
        d = gcd(x, N)

        if d != 1:  # Then d is a factor of N.
            factors.append(d)
            N //= d
        else:
            r = __order(x, N)
            y = r // 2

            if r % 2 == 0 and 1 < y < N - 1:
                f1 = gcd(y - 1, N)
                f2 = gcd(y + 1, N)

                factors.append(f1)
                factors.append(f2)

                N //= f1
                N //= f2

    factors.append(N)
    return factors
