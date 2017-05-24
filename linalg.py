#!/usr/bin/env python3

import numpy as np
import numbers


class Vector:
    """Represents an n-dimensional vector."""

    def __init__(self, *elems):
        """Construct a vector from variadic arguments or from a sequence. It's
        internally represented as a numpy array."""
        if hasattr(type(elems[0]), '__iter__'):
            self.array = np.array(elems[0])
        else:
            self.array = np.array(elems)

    @staticmethod
    def from_array(array):
        """Construct a vector from a numpy array."""
        assert len(array.shape) == 1

        v = vec()
        v.array = array

        return v

    def __getitem__(self, i):
        return self.array[i]

    def __setitem__(self, i, x):
        self.array[i] = x

    def __len__(self):
        return self.array.__len__()

    @property
    def norm(self):
        return np.linalg.norm(self.array)

    def __add__(self, x):
        """Element-wise addition."""
        assert isinstance(x, Vector)
        return Vector.from_array(self.array + x.array)

    def __mul__(self, x):
        """Vector scalar product + Hilbert space vector inner product + vector
        matrix product. """
        assert isinstance(x, numbers.Number) or \
            isinstance(x, Vector) or \
            isinstance(x, Matrix)
        return matmul(self, x, outer=False)

    def __pow__(self, x):
        """Hilbert space outer product."""
        assert isinstance(x, Vector)
        return matmul(self, x, outer=True)

    def __xor__(self, x):
        """Tensor product."""
        return tensor(self, x)

    def __repr__(self):
        return self.array.__str__()

    def __eq__(self, x):
        """Element-wise equality."""
        assert isinstance(x, Vector)
        return (self.array == x.array).all()


class Matrix:
    """Represents an mn-dimensional matrix."""

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
        return mat(self.array + x.array, reshape=False)

    def __mul__(self, x):
        """Matrix scalar product + matrix vector product + matrix matrix
        product. """
        return matmul(self, x)

    def __xor__(self, x):
        """Tensor product."""
        return tensor(self, x)

    def __repr__(self):
        return self.array.__str__()

    def __eq__(self, x):
        """Element-wise equality."""
        assert isinstance(x, Matrix)
        return (self.array == x.array).all()


def matmul(x, y, outer=False):
    """Matrix/vector scalar/inner/outer/matrix product."""

    # Matrix scalar product.
    if isinstance(x, Matrix) and isinstance(y, numbers.Number):
        return mat(x.array * y)
    elif isinstance(x, numbers.Number) and isinstance(y, Matrix):
        return mat(x * y.array)

    # Vector scalar product.
    elif isinstance(x, Vector) and isinstance(y, numbers.Number):
        return vec(x.array * y)
    elif isinstance(x, numbers.Number) and isinstance(y, Vector):
        return vec(x * y.array)

    # Hilbert space vector outer product.
    elif outer and isinstance(x, Vector) and isinstance(y, Vector):
        assert x.array.shape == y.array.shape

        ax = x.array.reshape(-1, 1)  # n x 1 matrix
        ay = y.array.reshape(1, -1)  # 1 x n matrix

        return mat(np.dot(ax, ay.conj()))

    # Hilbert space vector inner product.
    elif isinstance(x, Vector) and isinstance(y, Vector):
        assert x.array.shape == y.array.shape
        return np.dot(x.array.conjugate(), y.array)

    # Matrix product.
    elif isinstance(x, Matrix) and isinstance(y, Vector):
        # Number of columns of the matrix must equal the number of rows of
        # the vector.
        assert x.array.shape[1] == y.array.shape[0]
        return mat(np.dot(x.array.conjugate(), y.array.reshape(-1, 1)))
    elif isinstance(x, Vector) and isinstance(y, Matrix):
        # Number of columns of the vector must equal the number of rows of
        # the matrix.
        assert x.array.shape[0] == y.array.shape[0]
        return mat(np.dot(x.array.reshape(1, -1).conjugate(), y.array))
    elif isinstance(x, Matrix) and isinstance(y, Matrix):
        # Number of columns of the left matrix must equal the number of
        # rows of the right matrix.
        assert x.array.shape[1] == y.array.shape[0]
        return mat(np.dot(x.array.conjugate(), y.array))

    else:
        raise TypeError("can't multiply " + type(x).__name__ + " by " +
                        type(y).__name__)


def tensor(x, y):
    """Kronecker/tensor product."""

    if isinstance(x, Vector) and isinstance(y, Vector):
        return Vector.from_array(np.kron(x.array, y.array))
    elif isinstance(x, Vector) and isinstance(y, Matrix):
        return mat(np.kron(x.array, y.array))
    elif isinstance(x, Matrix) and isinstance(y, Vector):
        return mat(np.kron(x.array, y.array.reshape(-1, 1)))
    elif isinstance(x, Matrix) and isinstance(y, Matrix):
        return mat(np.kron(x.array, y.array))
    else:
        raise TypeError("tensor: arguments must by of type Vector or Matrix.")


# Shorter names for stuff


def vec(*elems):
    """Convenience vector constructor with shorter name."""
    return Vector(*elems)


def mat(*elems, m=None, n=None, reshape=True):
    """Convenience matrix constructor with shorter name."""
    return Matrix(*elems, m=m, n=n, reshape=reshape)


def conj(x):
    """Conjugate of x."""
    return x.conjugate()
