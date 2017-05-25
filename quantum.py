#!/usr/bin/env python3

import math
import cmath
from collections import defaultdict


class QuMem:
    """Represents quantum memory with arbitrary width (number of qubits)."""

    def __init__(self, t, n):
        self.t = t
        self.n = n

        self.amplitudes = {}

        for i in range(2**t):
            for j in range(2**n):
                self.amplitudes[(i, j)] = 0

        self.amplitudes[(0, 0)] = 1

    def measure(self):
        assert False, "measure not implemented"

    def __len__(self):
        return len(self.amplitudes)

    def __repr__(self):
        s = ""

        for k, v in sorted(self.amplitudes.items()):
            i, j = k
            s += "{} |{},{}> + ".format(v, i, j)
        return s[:-3]

    def hadamard(self):
        """In the Shor algorithm we apply the Hadamard gate to the first t bits
        of the memory. This simulates that by (1) setting the amplitude of all
        the states where the last n bits are different from zero, and (2)
        giving the same amplitude to the other states."""
        # FIXME: Review the documentation.
        for k, v in self.amplitudes.items():
            _, j = k
            if j == 0:
                self.amplitudes[k] = 1 / math.sqrt(2**self.t)
            else:
                self.amplitudes[k] = 0
        return self

    def mod_exp(self, x, N):
        amps = defaultdict(int)

        for k, v in self.amplitudes.items():
            i, _ = k
            amps[(i, pow(x, i, N))] += v
        self.amplitudes = amps

        return self

    def qft(self):
        pass


def shor(N, x):
    n = math.ceil(math.log(N, 2))
    t = math.ceil(math.log(N**2, 2))  # s.t. N**2 <= 2**t < 2 * N**2

    mem = QuMem(t, n)

    mem.hadamard(t)
    mem.mod_exp(x, N)
    # mem.inv_qft()
    # mem.measure()

    print(t, n)
    return mem
