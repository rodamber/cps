#!/usr/bin/env python3

import cmath
import math
import random


class QuMem:
    def __init__(self, t, n):
        self.t = t  # left width
        self.n = n  # right width

        self.amplitudes = []
        self.left = []
        self.right = []

        for left in range(2**t):
            for right in range(2**n):
                self.amplitudes.append(0)
                self.left.append(left)
                self.right.append(right)
        self.amplitudes[0] = 1

    def measure(self):
        from numpy import random
        return random.choice(
            self.left, p=list(map(lambda x: abs(x)**2, self.amplitudes)))

    def __len__(self):
        return len(self.amplitudes)

    def __iter__(self):
        for x in zip(self.amplitudes, self.left, self.right):
            yield x

    def __repr__(self):
        s = ""
        for ampl, left, right in self:
            s += "{:.4f} |{},{}> + ".format(ampl, left, right)
        return s[:-3]

    def hadamard(self):
        for i, (_, left, right) in enumerate(self):
            if right == 0:
                self.amplitudes[i] = 1 / math.sqrt(2**self.t)
        return self

    def mod_exp(self, x, N):
        for i, (amp, left, right) in enumerate(self):
            self.right[i] = pow(x, left, N)
        return self

    def qft(self):
        new_amplitudes = []
        N = 2**self.t

        w__ = cmath.exp(2 * math.pi * 1j / N)
        for k, _ in enumerate(self):
            w_k = w__**k
            s = 0
            for j in range(N):
                wjk = w_k**j
                s += wjk * self.amplitudes[j]
            new_amplitudes.append(s / math.sqrt(N))
        self.amplitudes = new_amplitudes
        return self


def denominator(x, qmax):
    """Finds the denominator q of the best rational approximation p/q for x
    with q < qmax."""
    y = x
    q0, q1, q2 = 0, 1, 0

    while True:
        z = y - math.floor(y)  # decimal part of y
        if z < 0.5 / qmax**2:
            return q1

        y = 1 / z
        q2 = math.floor(y) * q1 + q0

        if q2 >= qmax:
            return q1

        q0, q1 = q1, q2


def shor(N, a):
    while True:
        n = N.bit_length()
        t = math.ceil(math.log(N**2, 2))  # s.t. N**2 <= 2**t < 2 * N**2

        measure = QuMem(t, n).hadamard().mod_exp(a, N).qft().measure()

        if measure == 0:
            print("| measured zero, trying again ...")
        else:
            c = measure / 2**t
            q = denominator(c, N)
            p = math.floor(q * c + 0.5)
            print("| measured {}, approximation for {} is {}/{}"
                  .format(measure, c, p, q))

            # FIXME: Is this polinomial in n?
            print("| trying multiples of {} ...".format(q))
            for i in range(1, math.ceil(N / q)):
                mod = pow(a, i * q, N)

                print("| {}^{} mod {} = {}".format(a, i * q, N, mod))

                if mod == 1:
                    print("| period of f(x) = {}^x mod {} is {}".format(
                        a, N, i * q))
                    return i * q

            print("| failed to find period")
            return None


def prime(n):
    """Primality test by trial division."""
    if n == 2:
        return True
    elif n < 2 or n % 2 == 0:
        return False
    else:
        return not any(n % x == 0
                       for x in range(3, math.ceil(math.sqrt(n)) + 1, 2))


def odd_prime_power(n):
    if n < 3:
        return False
    factor = 0
    for i in range(3, math.ceil(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            factor = i
            break
    if factor == 0:
        return False
    for i in range(2, math.ceil(math.log(n, factor)) + 1):
        if factor**i == n:
            return True
    return False


def factorize(N):
    assert N > 1

    if N % 2 == 0:
        print(N, "is even")
    elif prime(N):
        print(N, "is prime")
    elif odd_prime_power(N):
        print(N, "is a power of an odd prime")
    else:
        while True:
            a = random.randint(2, N - 1)
            d = math.gcd(a, N)

            print("| picked random a =", a)

            if d != 1:
                print("| got lucky, {} = {} * {}".format(N, d, N // d))
                print("| repeating ...")
            else:
                r = shor(N, a)
                if r is None:
                    print("| trying again ...")
                    continue

                y = r // 2
                if r % 2 == 1:
                    print("| period {} is odd, trying again ...".format(r))
                elif not 1 < y < N - 1:
                    print("| 1 < {} < {} - 1 is false, trying again".format(
                        y, N))
                else:
                    factor = max(math.gcd(y - 1, N), math.gcd(y + 1, N))

                    print("factor is one, trying again ...")
                    continue

                    print("| found factor: {} = {} * {}".format(
                        N, factor, N // factor))
                    return factor
