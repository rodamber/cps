#!/usr/bin/env python3

from random import randint
from math import gcd, ceil, floor, sqrt

from quantum import shor


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
                r = shor(N, x)
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
