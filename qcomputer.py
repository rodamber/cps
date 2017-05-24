#!/usr/bin/env python3


class Qureg:
    """Represents a quantum register with arbitrary width (number of
    qubits)."""

    def __init__(self, initval, width):
        pass

    def measure(self):
        pass


# 1-qubit gates


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
