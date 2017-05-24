#!/usr/bin/env python3

import linalg as la


class Qureg:
    """Represents a quantum register with arbitrary width (number of
    qubits)."""

    def __init__(self, width=1, initval=0):
        # Start in the state |initval>
        self.amplitudes = la.vec([0] * 2**width)
        self.amplitudes[initval] = 1

    def measure(self):
        from numpy.random import choice

        bit = choice(len(self.amplitudes), p=self.amplitudes)

        self.amplitudes.array.fill(0)  # Every amplitude becomes zero
        self.amplitudes[bit] = 1

        return bit

    def __repr__(self):
        s = ""
        for i, amp in enumerate(self.amplitudes):
            s += "{:.4g} |{}> + ".format(amp, i)
        return s[:-3]


# 1-qubit gates

# add parameter to apply the gate several times?

# The sum of the squares of the amplitudes must sum to one.
# assert self.amplitudes.norm == 1


def phase_shift(qureg, target, gamma):
    pass


def hadamard(qureg, target):
    pass


# 2-qubit gates


def control_phase_shift(qureg, control, target):
    pass


def control_not(qureg, control, target):
    pass


# Quantum Circuits/Procedures


def mod_exp():
    pass


def inv_qft():
    pass
