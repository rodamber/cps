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
        return matmul(self, x)

    def __pow__(self, x):
        """Hilbert space outer product."""
        assert isinstance(x, Vector)
        assert self.array.shape == x.array.shape

        v0 = self.array.reshape(-1, 1)  # n x 1 matrix
        v1 = x.array.reshape(1, -1)  # 1 x n matrix

        return Matrix(np.dot(v0, v1.conj()))

    def __mod__(self, x):
        """Tensor product."""
        return tensor(self, x)

    def __repr__(self):
        return self.array.__str__()

    def __eq__(self, x):
        """Element-wise equality."""
        assert isinstance(x, Vector)
        return (self.array == x.array).all()


class Matrix:
    def __init__(self, *elems, m=None, n=None, reshape=True):
        """Construct a mn-matrix from a list, tuple or a numpy array."""
        assert len(elems) > 0

        if len(elems) == 1 and isinstance(elems[0], np.ndarray):
            self.array = elems[0]
        else:
            self.array = np.array(elems)

        if reshape:
            if m is None:
                m = self.array.shape[0]
            if n is None:
                n = self.array.shape[1]
            self.array = self.array.reshape(m, n)

    def __add__(self, x):
        """Element-wise addition."""
        assert isinstance(x, Matrix)
        return Matrix(self.array + x.array, reshape=False)

    def __mul__(self, x):
        """Matrix scalar product + matrix vector product + matrix matrix
        product. """
        return matmul(self, x)

    def __mod__(self, x):
        """Tensor product."""
        return tensor(self, x)

    def __repr__(self):
        return self.array.__str__()

    def __eq__(self, x):
        """Element-wise equality."""
        assert isinstance(x, Matrix)
        return (self.array == x.array).all()


def matmul(x, y):
    # Matrix scalar product.
    if isinstance(x, Matrix) and isinstance(y, numbers.Number):
        return Matrix(x.array * y)
    elif isinstance(x, numbers.Number) and isinstance(y, Matrix):
        return Matrix(x * y.array)

    # Vector scalar product.
    elif isinstance(x, Vector) and isinstance(y, numbers.Number):
        return Vector(x.array * y)
    elif isinstance(x, numbers.Number) and isinstance(y, Vector):
        return Vector(x * y.array)

    # Hilbert space vector inner product.
    elif isinstance(x, Vector) and isinstance(y, Vector):
        assert x.array.shape == y.array.shape
        return np.dot(x.array.conjugate(), y.array)

    # Matrix product.
    elif isinstance(x, Matrix) and isinstance(y, Vector):
        # Number of columns of the matrix must equal the number of rows of
        # the vector.
        assert x.array.shape[1] == y.array.shape[0]
        return Matrix(np.dot(x.array.conjugate(), y.array.reshape(-1, 1)))
    elif isinstance(x, Vector) and isinstance(y, Matrix):
        # Number of columns of the vector must equal the number of rows of
        # the matrix.
        assert x.array.shape[0] == y.array.shape[0]
        return Matrix(np.dot(x.array.reshape(1, -1).conjugate(), y.array))
    elif isinstance(x, Matrix) and isinstance(y, Matrix):
        # Number of columns of the left matrix must equal the number of
        # rows of the right matrix.
        assert x.array.shape[1] == y.array.shape[0]
        return Matrix(np.dot(x.array.conjugate(), y.array))

    else:
        raise TypeError("can't multiply " + type(x).__name__ + " by " +
                        type(y).__name__)


def tensor(x, y):
    if isinstance(x, Vector) and isinstance(y, Vector):
        return Vector.from_array(np.kron(x.array, y.array))
    elif isinstance(x, Vector) and isinstance(y, Matrix):
        return Matrix(np.kron(x.array, y.array))
    elif isinstance(x, Matrix) and isinstance(y, Vector):
        return Matrix(np.kron(x.array, y.array.reshape(-1, 1)))
    elif isinstance(x, Matrix) and isinstance(y, Matrix):
        return Matrix(np.kron(x.array, y.array))
    else:
        raise TypeError("tensor: arguments must by of type Vector or Matrix.")
