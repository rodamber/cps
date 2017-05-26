#!/usr/bin/env python3
"""Simulation of Shor's algorithm for integer factorization."""

import cmath
import math
import numpy as np
import random


class QuMem:
    """Representation of the memory of the quantum computer."""

    def __init__(self, t, n):
        """Initialize the memory. For Shor's algorithm we have t + n qubits,
        where t is such that N^2 <= 2^t < 2N^2 holds.

        The memory is represented by explicitly saving all the 2^(t+n) possible
        states and their corresponding amplitudes.
        """

        # The amplitudes and the states are represented by three lists where,
        # for each i, 0 <= i < 2^(t+n), amplitudes[i] is the amplitude of the
        # state |fst[i], lst[i]>.
        self.amplitudes = []
        self.fst = []  # Quantum state of the first t qubits.
        self.lst = []  # Quantum state of the last n qubits.

        self.t = t  # fst width
        self.n = n  # lst width

        # Populate the quantum state lists.
        for fst in range(2**t):
            for lst in range(2**n):
                self.amplitudes.append(0)
                self.fst.append(fst)
                self.lst.append(lst)

        # Initialize the memory to the state |0, 0>.
        self.amplitudes[0] = 1

    def measure(self):
        """Measure the first t bits of the memory. Simulated by making a
        weighted random choice of one of the possible states. The weights are
        the squares of the absolute values of their amplitudes."""
        return np.random.choice(
            self.fst, p=list(map(lambda x: abs(x)**2, self.amplitudes)))

    def __len__(self):
        """Equal to 2^(t+n). This is here for convenience."""
        return len(self.amplitudes)

    def __iter__(self):
        """Iterator of the quantum state. This is here for convenience."""
        for x in zip(self.amplitudes, self.fst, self.lst):
            yield x

    def __repr__(self):
        """Represented as a linear combination, a0 |0, 0> + a1 |0, 1> + ... ,
        of all the possible states."""
        s = ""
        for ampl, fst, lst in self:
            s += "{:.4f} |{},{}> + ".format(ampl, fst, lst)
        return s[:-3]


def hadamard(mem):
    """Apply the Hadamard gate to the first t qubits. After this
    application, the memory is in a quantum superposition where the
    measuring probability is equidistributed between the first t qubits."""
    for i, (_, fst, lst) in enumerate(mem):
        if lst == 0:  # The last n qubits remain in state |0>
            mem.amplitudes[i] = 1 / math.sqrt(2**mem.t)
    return mem


def mod_exp(mem, x, N):
    """Apply the operator |j, k> |-> |j, k + x^j mod N>. However, in Shor's
    algorithm k = 0, so we just apply the modular exponentiation."""
    for i, (_, fst, lst) in enumerate(mem):
        mem.lst[i] = pow(x, fst, N)
    return mem


def qft(mem):
    """Apply quantum Fourier transform to the first t qubits."""
    new_amplitudes = []
    N = 2**mem.t

    # Calculate root of unity in two steps, as complex exponentiation is
    # expensive.
    w__ = cmath.exp(2 * math.pi * 1j / N)

    for k, _ in enumerate(mem):
        s = 0
        for j in range(N):
            wjk = w__**(j * k)
            s += wjk * mem.amplitudes[j]
        new_amplitudes.append(s / math.sqrt(N))
    mem.amplitudes = new_amplitudes
    return mem


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
    """Simulation of Shor's algorithm for order finding."""
    assert 1 < a < N

    while True:
        n = N.bit_length()
        t = math.ceil(math.log(N**2, 2))  # s.t. N^2 <= 2^t < 2N^2

        mem = QuMem(t, n)
        hadamard(mem)
        mod_exp(mem, a, N)
        qft(mem)
        measure = mem.measure()

        if measure == 0:
            print("| measured zero, trying again ...")
        else:
            c = measure / 2**t
            q = denominator(c, N)
            p = math.floor(q * c + 0.5)
            print("| measured {}, approximation for {} is {}/{}"
                  .format(measure, c, p, q))

            mod = pow(a, q, N)
            print("| {}^{} mod {} = {}".format(a, q, N, mod))

            if mod == 1:
                print("| got {}".format(q))
                return q
            else:
                print("| failed, trying again ...")


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
    """Test if n is a power of an odd prime."""
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
    """Applies Shor's algorithm to the problem of integer factorization."""
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
                print("| got lucky, {} = {} * {}, trying again...".format(
                    N, d, N // d))
                print("|---------------------------------------------")
            else:
                r = shor(N, a)
                if r is None:
                    print("| trying again ...")
                    print("|-----------------------------------------------")
                    continue

                y = r // 2
                if r % 2 == 1:
                    print("| order {} is odd, trying again ...".format(r))
                    print("|-----------------------------------------------")
                elif not 1 < y < N - 1:
                    print("| 1 < {} < {} - 1 is false, trying again".format(
                        y, N))
                    print("|-----------------------------------------------")
                else:
                    factor = max(math.gcd(y - 1, N), math.gcd(y + 1, N))

                    if factor == 1:
                        print("| factor is one, trying again ...")
                        print("|---------------------------------------------")
                    else:
                        print("| found factor: {} = {} * {}".format(
                            N, factor, N // factor))
                        return factor


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("USAGE: shor.py <input>")
    else:
        print(factorize(int(sys.argv[1])))
