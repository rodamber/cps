#!/usr/bin/env python3

import linalg as la

import numpy as np
import math
import numbers


def state(x, nqubits=1):
    """
    state(0) <-> |0>
    state(1) <-> |1>
    state(2) <-> |2>
    state(3) <-> |3>
    etc.

    state(0, 3) <-> |0> <-> |00>
    state(1, 3) <-> |1> <-> |01>
    state(2, 3) <-> |2> <-> |10>
    state(3, 3) <-> |3> <-> |11>
    etc.

    Examples
    --------
    >>> for x in [state(y) for y in range(5)]: print(x)
    ...
    [ 1.  0.]
    [ 0.  1.]
    [ 0.  0.  1.  0.]
    [ 0.  0.  0.  1.]
    [ 0.  0.  0.  0.  1.  0.  0.  0.]

    >>> for x in [state(y, 3) for y in range(8)]: print(x)
    ...
    [ 1.  0.  0.  0.  0.  0.  0.  0.]
    [ 0.  1.  0.  0.  0.  0.  0.  0.]
    [ 0.  0.  1.  0.  0.  0.  0.  0.]
    [ 0.  0.  0.  1.  0.  0.  0.  0.]
    [ 0.  0.  0.  0.  1.  0.  0.  0.]
    [ 0.  0.  0.  0.  0.  1.  0.  0.]
    [ 0.  0.  0.  0.  0.  0.  1.  0.]
    [ 0.  0.  0.  0.  0.  0.  0.  1.]
    """
    assert isinstance(x, int)

    if x > 1 and nqubits == 1:
        nqubits = math.floor(math.log(x, 2)) + 1

    st = np.zeros(pow(2, nqubits))
    st[x] = 1

    return la.Vector.from_array(st)


class QBit:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def __str__(self):
        return str(self.alpha) + " * |0> + " + str(self.beta) + " * |1>"


class QState:
    def __init__(self, *amplitudes, nqubits=1):
        assert all(isinstance(x, numbers.Number) for x in amplitudes)

        def is_power_of_two(x):
            return math.log(x, 2).is_integer()

        assert is_power_of_two(len(amplitudes))
        assert len(amplitudes) > 1

        self.amplitudes = la.Vector(amplitudes)
