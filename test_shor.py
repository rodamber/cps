import shor


def test_shor():
    import numpy as np

    limit = 100
    for x in range(2, limit):
        factors = shor.factorize(x)

        assert np.prod(factors) == x
        assert all(shor.prime(f) for f in factors)
