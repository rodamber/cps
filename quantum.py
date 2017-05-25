#!/usr/bin/env python3

import math
import cmath


class QuMem:
    """Represents quantum memory with arbitrary width (number of qubits)."""

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
        """In the Shor algorithm we apply the Hadamard gate to the first t bits
        of the memory. This simulates that by (1) setting the amplitude of all
        the states where the last n bits are different from zero, and (2)
        giving the same amplitude to the other states."""

        # FIXME: Review the documentation.
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

        for k, _ in enumerate(self):
            s = 0
            for j in range(N):
                wjk = cmath.exp(2 * math.pi * 1j * j * k / N)
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


def shor(N, x):
    n = N.bit_length()
    t = math.ceil(math.log(N**2, 2))  # s.t. N**2 <= 2**t < 2 * N**2

    measured = QuMem(t, n).hadamard().mod_exp(x, N).qft().measure()

    if measured == 0:
        print("Measured 0. Trying again.")
        shor(N, x)
    else:
        print("Measured", measured)

    r = denominator(measured / 2**t, N)

    if pow(x, r, N) == 1:
        print("Found period:", x, "^", r, "mod", N, "= 1")
        return r
    else:
        shor(N, x)
