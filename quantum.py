#!/usr/bin/env python3

import linalg as la

# FIXME: Maybe should use numpy math operations?
import cmath
import math

# FIXME: Lacking documentation.
# FIXME: The bits are in reverse order!


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


hadamard_op = mat = la.mat(1,  1, \
                           1, -1, m=2, n=2) * 2**-0.5


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


def unitary_op(width, target, mat):
    """Build the 2x2 unitary operation that will act upon the target qubit."""
    assert 0 <= target < width

    l = la.mat(1, m=1, n=1)
    for _ in range(target):
        l ^= identity_op

    r = la.mat(1, m=1, n=1)
    for _ in range(width - (target + 1)):
        r ^= identity_op

    return l ^ mat ^ r


def gate1(qureg, target, mat, apply_to_all):
    if apply_to_all:
        for i in range(qureg.width):
            qureg.amplitudes *= unitary_op(qureg.width, i, mat)
    else:
        qureg.amplitudes *= unitary_op(qureg.width, target, mat)

    return qureg


# FIXME: UNTESTED
def phase_shift_gate(qureg, phi, target=0, apply_to_all=False):
    return gate1(qureg, target, phase_shift_op(phi), apply_to_all)


def hadamard_gate(qureg, target=0, apply_to_all=False):
    return gate1(qureg, target, hadamard_op, apply_to_all)


# 2-Qubit Gates
# FIXME: UNTESTED


def gate2(qureg, control, target, mat):
    pass


def control_phase_shift_gate(qureg, control, target):
    mat = control_phase_op(control - target)
    return gate2(qureg, control, target, mat)


def cnot_gate(qureg, control, target):
    return gate2(qureg, control, target, cnot)


# Quantum Circuits/Procedures


def mod_exp():
    pass


def inv_qft():
    pass


# Test


def _nth_bit(x, n):
    return (x >> n) & 1


def _toggle_bit(x, n):
    return x ^ (1 << n)


# FIXME: Can we use this trick with hadamard and phase shift gates?


def _cnot(x, control, target):
    return _toggle_bit(x, target) if _nth_bit(x, control) else x
