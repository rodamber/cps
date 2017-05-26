import math
import cmath


class QuMem:
    def __init__(self, t, n):
        self.t = t  # left width
        self.n = n  # right width

        self.amplitudes = []
        self.left = []
        self.right = []

        for left in range(2**t):
            for right in range(2**n):
                self.amplitudes.append(0)
                self.left.append(left)
                self.right.append(right)
        self.amplitudes[0] = 1

    def measure(self):
        from numpy import random
        return random.choice(
            self.left, p=list(map(lambda x: abs(x)**2, self.amplitudes)))

    def __len__(self):
        return len(self.amplitudes)

    def __iter__(self):
        for x in zip(self.amplitudes, self.left, self.right):
            yield x

    def __repr__(self):
        s = ""
        for ampl, left, right in self:
            s += "{:.4f} |{},{}> + ".format(ampl, left, right)
        return s[:-3]

    def hadamard(self):
        for i, (_, left, right) in enumerate(self):
            if right == 0:
                self.amplitudes[i] = 1 / math.sqrt(2**self.t)
        return self

    def mod_exp(self, x, N):
        for i, (amp, left, right) in enumerate(self):
            self.right[i] = pow(x, left, N)
        return self

    def qft(self):
        new_amplitudes = []
        N = 2**self.t

        w__ = cmath.exp(2 * math.pi * 1j / N)
        for k, _ in enumerate(self):
            w_k = w__**k
            s = 0
            for j in range(N):
                wjk = w_k**j
                s += wjk * self.amplitudes[j]
            new_amplitudes.append(s / math.sqrt(N))
        self.amplitudes = new_amplitudes
        return self


def denominator(x, qmax):
    """Finds the denominator q of the best rational approximation p/q for x
    with q < qmax."""
    y = x
    q0, q1, q2 = 0, 1, 0

    while True:
        z = y - math.floor(y)  # decimal part of y
        if z < 0.5 / qmax**2:
            return q1

        y = 1 / z
        q2 = math.floor(y) * q1 + q0

        if q2 >= qmax:
            return q1

        q0, q1 = q1, q2


def shor(N, x):
    print("Running Shor's algorithm.")
    print("Random base =", x)

    while True:
        n = N.bit_length()
        t = math.ceil(math.log(N**2, 2))  # s.t. N**2 <= 2**t < 2 * N**2

        measured = QuMem(t, n).hadamard().mod_exp(x, N).qft().measure()

        if measured == 0:
            print("Measured 0. Trying again.")
        else:
            q = denominator(measured / 2**t, N)
            print("Denominator of the best approximation:", q)

            for i in range(1, math.ceil(N / q)):
                mod = pow(x, i * q, N)

                print("{}^{} mod {} = {}".format(x, q, N, mod))

                if mod == 1:
                    print("Found the period:", i * q)
                    return i * q

            print(s + "Failed to find the period.")
            return 0
