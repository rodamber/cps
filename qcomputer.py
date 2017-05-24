#!/usr/bin/env python3

import math
import random


class Qubit:
    # Based on https://gist.github.com/limitedmage/945473

    def __init__(self, a=1, b=0):
        """Initializes a qubit. a is the amplitude of |0> and b is the
        amplitude of |1>. """
        self.zero = a
        self.one = b

        assert self._prob_one()

    def _prob_one(self):
        return math.isclose(abs(self.zero)**2 + abs(self.one)**2, 1)

    def measure(self):
        """Measure the qubit. The qubit will be in state |0> with probability
        self.zero ** 2 and in state |1> with probability self.one ** 2."""

        if random.random() < abs(self.zero)**2:  # Decay to |0>.
            self.zero = 1
            self.one = 0

            return 0
        else:  # Decay to |1>.
            self.zero = 0
            self.one = 1

            return 1

    def hadamard(self, ntimes=1):
        """Apply a hadamard gate ntimes to the qubit."""
        for _ in range(ntimes):
            a = self.zero
            b = self.one

            self.zero = (a + b) / math.sqrt(2)
            self.one = (a - b) / math.sqrt(2)

        assert self._prob_one()
        return self

    def __repr__(self):
        return "{:.10g} |0> + {:.10g} |1>".format(self.zero, self.one)


class TwoQubit:
    # Based on https://gist.github.com/limitedmage/945473

    def __init__(self, qb0=Qubit(), qb1=Qubit()):
        self.zero_zero = a
        self.zero_one = b
        self.one_zero = c
        self.one_one = d

        assert self._prob_one()

    def __init__(self, a=1, b=0, c=0, d=0):
        """Initialize a two-qubit entanglement"""
        self.zero_zero = a
        self.zero_one = b
        self.one_zero = c
        self.one_one = d

        assert self._prob_one()

    def _prob_one(self):
        norm = abs(self.zero_zero)**2 + abs(self.zero_one)**2 + abs(
            self.one_zero)**2 + abs(self.one_one)**2
        return math.isclose(norm, 1)

    def cnot(self):
        """Controlled NOT operation"""
        self.one_zero, self.one_one = self.one_one, self.one_zero
        return self

    def hadamard(self, ntimes=1):
        """Perform Hadamard operation ntimes on first qubit."""
        for _ in range(ntimes):
            a = self.zero_zero
            b = self.zero_one
            c = self.one_zero
            d = self.one_one

            self.zero_zero = (a + c) / math.sqrt(2)
            self.zero_one = (b + d) / math.sqrt(2)
            self.one_zero = (a - c) / math.sqrt(2)
            self.one_one = (b - d) / math.sqrt(2)

        assert self._prob_one()
        return self

    def measure(self):
        """Measure the two-qubit in the computational basis"""
        zero_zero_prob = abs(self.zero_zero)**2
        zero_one_prob = abs(self.zero_one)**2
        one_zero_prob = abs(self.one_zero)**2

        prob = random.random()

        if prob < zero_zero_prob:
            self.zero_zero = 1
            self.zero_one = 0
            self.one_zero = 0
            self.one_one = 0

            return (0, 0)
        elif prob < zero_one_prob:
            self.zero_zero = 0
            self.zero_one = 1
            self.one_zero = 0
            self.one_one = 0

            return (0, 1)
        elif prob < one_zero_prob:
            self.zero_zero = 0
            self.zero_one = 0
            self.one_zero = 1
            self.one_one = 0

            return (1, 0)
        else:
            self.zero_zero = 0
            self.zero_one = 0
            self.one_zero = 0
            self.one_one = 1

            return (1, 1)

    def __repr__(self):
        comp = [self.zero_zero, self.zero_one, self.one_zero, self.one_one]
        comp = [i.real if i.real == i else i for i in comp]
        comp = [str(i) for i in comp]
        comp = ["" if i == "1.0" else i for i in comp]

        ls = []
        if abs(self.zero_zero) > 0:
            ls += [comp[0] + " |00>"]
        if abs(self.zero_one) > 0:
            ls += [comp[1] + " |01>"]
        if abs(self.one_zero) > 0:
            ls += [comp[2] + " |10>"]
        if abs(self.one_one) > 0:
            ls += [comp[3] + " |11>"]

        comp = " + ".join(ls)

        return comp
