#!/usr/bin/env python3

import numpy as np
import numbers


class Vector:
    """Represents an n-dimensional vector."""

    def __init__(self, *elems):
        """Construct a vector from variadic arguments. It's internally
        represented as a numpy array."""
        self.array = np.array(elems)

    @staticmethod
    def from_array(array):
        """Construct a vector from a numpy array."""
        assert len(array.shape) == 1

        v = Vector()
        v.array = array

        return v

    def __add__(self, x):
        """Element-wise addition."""
        assert isinstance(x, Vector)
        return Vector.from_array(self.array + x.array)

    def __mul__(self, x):
        """Vector scalar product + Hilbert space vector inner product + vector
        matrix product. """

        if isinstance(x, numbers.Number):
            return Vector.from_array(self.array * x)

        elif isinstance(x, Vector):
            assert self.array.shape == x.array.shape
            return np.dot(self.array.conjugate(), x.array)

        elif isinstance(x, Matrix):
            # Number of columns of the vector must equal the number of rows of
            # the matrix.
            assert self.array.shape[0] == x.array.shape[0]

            y = self.array.reshape(1, -1)  # n x 1 matrix
            return Matrix(np.dot(y.conjugate(), x.array), reshape=False)

        else:
            raise TypeError("can't multiply Vector by object of type " +
                            type(x).__name__)

    def __pow__(self, x):
        """Hilbert space outer product."""
        assert isinstance(x, Vector)

        v0 = self.array.reshape(-1, 1)  # n x 1 matrix
        v1 = x.array.reshape(1, -1)  # 1 x n matrix

        return np.dot(v0, v1.conj())

    def __repr__(self):
        return self.array.__str__()

    def __eq__(self, x):
        """Element-wise equality."""
        assert isinstance(x, Vector)
        return (self.array == x.array).all()


class Matrix:
    def __init__(self, array, m=1, n=-1, reshape=True):
        """Construct a mn-matrix from a list, tuple or a numpy array."""

        if isinstance(array, np.ndarray):
            self.array = array
        else:
            assert hasattr(type(array), '__iter__')
            self.array = np.array(array)

        if reshape:
            self.array = self.array.reshape(m, n)

    def __add__(self, x):
        """Element-wise addition."""
        assert isinstance(x, Matrix)
        return Matrix(self.array + x.array, reshape=False)

    def __mul__(self, x):
        """Matrix scalar product + matrix vector product + matrix matrix
        product. """

        if isinstance(x, numbers.Number):
            return Matrix(self.array * x)

        elif isinstance(x, Vector):
            # Number of columns of the matrix must equal the number of rows of
            # the vector.
            assert self.array.shape[1] == x.array.shape[0]

            y = x.array.reshape(-1, 1)  # n x 1 matrix
            return Matrix(np.dot(self.array.conjugate(), y), reshape=False)

        elif isinstance(x, Matrix):
            # Number of columns of the left matrix must equal the number of
            # rows of the right matrix.
            assert self.array.shape[1] == x.array.shape[0]
            return Matrix(
                np.dot(self.array.conjugate(), x.array), reshape=False)

        else:
            raise TypeError("can't multiply Matrix by object of type " +
                            type(x).__name__)

    def __repr__(self):
        return self.array.__str__()

    def __eq__(self, x):
        """Element-wise equality."""
        assert isinstance(x, Matrix)
        return (self.array == x.array).all()


def test_add():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    assert Vector(a, b) + Vector(c, d) == \
        Vector(a + c, b + d)

    assert Matrix([a, b, c, d], 2, 2) + Matrix([e, f, g, h], 2, 2) == \
        Matrix([a + e, b + f,
                c + g, d + h], 2, 2)


def test_mul():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    def conj(x):
        return x.conjugate()

    assert Vector(a, b) * Vector(c, d) == \
        c * a.conjugate() + d * b.conjugate()

    assert Vector(e, f) * Matrix([a, b, c, d], 2, 2) == \
        Matrix([a * conj(e) + c * conj(f),
                b * conj(e) + d * conj(f)], 1, 2)

    assert Matrix([a, b, c, d], 2, 2) * Vector(e, f) == \
        Matrix([conj(a) * e + conj(b) * f,
                conj(c) * e + conj(d) * f], 2, 1)

    assert Matrix([a, b, c, d], 2, 2) * Matrix([e, f, g, h], 2, 2) == \
        Matrix([conj(a) * e + conj(b) * g, conj(a) * f + conj(b) * h,
                conj(c) * e + conj(d) * g, conj(c) * f + conj(d) * h], 2, 2)


def test_eq():
    import string
    from sympy import Symbol

    a, b, c, d, e, f, g, h = [Symbol(x) for x in string.ascii_letters[:8]]

    assert Vector(a, b) == Vector(a, b)

    assert Vector(a, b) != Vector(a, f)
    assert Vector(a, b) != Vector(e, b)
    assert Vector(a, b) != Vector(e, f)

    assert Matrix([a, b, c, d], 2, 2) == Matrix([a, b, c, d], 2, 2)

    assert Matrix([a, b, c, d], 2, 2) != Matrix([e, b, c, d], 2, 2)
    assert Matrix([a, b, c, d], 2, 2) != Matrix([a, f, c, d], 2, 2)
    assert Matrix([a, b, c, d], 2, 2) != Matrix([a, b, g, d], 2, 2)
    assert Matrix([a, b, c, d], 2, 2) != Matrix([a, b, c, h], 2, 2)
