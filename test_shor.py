import shor


def test_shor():
    import numpy as np

    limit = 1000
    for x in range(2, limit):
        factors = shor.factorize(x)

        assert np.prod(factors) == x, "product({}) != {}".format(factors, x)
        for f in factors:
            assert shor.prime(f), "{} (factor of {}) is not prime!".format(
                f, x)
