#!/usr/bin/env python3

import linalg as la

# FIXME: Maybe should use numpy math operations?
import cmath
import math

# import numpy as np
# np.set_printoptions(formatter={'float': lambda x: "{:.2f}\t".format(x)})


class Qureg:
    """Represents a quantum register with arbitrary width (number of
    qubits)."""

    def __init__(self, width=1, initval=0):
        self.width = width
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


# Unitary Operators

identity_op = la.mat(1, 0, \
                     0, 1, m=2, n=2)


def phase_shift_op(phi):
    return la.mat(1, 0, \
                  0, cmath.exp(1j * phi), m=2, n=2)


hadamard_op = mat = la.mat(2**-0.5, 2**-0.5, 2**-0.5, -2**-0.5, m=2, n=2)


def control_phase_op(k):
    return la.mat(1, 0, 0, 0,
                  0, 1, 0, 0,
                  0, 0, 1, 0, \
                  0, 0, 0, cmath.exp(1j * math.pi / 2**k), m=4, n=4)

cnot = la.mat(1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 0, 1, \
              0, 0, 1, 0, m=4, n=4)

# 1-Qubit Gates


def unitary(width, target, mat):
    """Build the unitary operation that will act upon the target qubit."""
    if width == 1:
        return mat

    m = la.mat(1, 1, 1, 1, m=2, n=2)

    for _ in range(target):
        m = la.tensor(m, identity_op)

    if width > 1:
        m = la.tensor(m, mat)

    for _ in range(width - (target + 1)):
        m = la.tensor(m, identity_op)


def gate1(qureg, target, mat):
    qureg.amplitudes *= unitary(qureg.width, target, mat)
    return qureg


def phase_shift_gate(qureg, phi, target=0):
    return gate1(qureg, target, phase_shift_op(phi))


def hadamard(qureg, target=0):
    return gate1(qureg, target, hadamard_op)


# 2-qubit gates


def gate2(qureg, control, target, mat):
    pass


def control_phase_shift(qureg, control, target):
    mat = control_phase_op(control - target)
    return gate2(qureg, control, target, mat)


def control_not(qureg, control, target):
    return gate2(qureg, control, target, cnot)


# Quantum Circuits/Procedures


def mod_exp():
    pass


def inv_qft():
    pass
