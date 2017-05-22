#!/usr/bin/env python3


# Used just to test.
def __factorize(n):
    factors = []
    d = 2

    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)

    return factors


def factorize(N):
    """Shor's algorithm."""

    if N == 2:
        return [2]

    from random import randint
    from math import gcd

    x = randint(2, N - 1)
    d = gcd(x, N)

    if d != 1:
        # Then d is a factor of N
        return factorize(N // d) + [d]
    else:
        return __factorize(N)
