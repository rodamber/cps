import shor


def test_shor():
    from numpy import prod

    limit = 21
    assert all(prod(shor.factorize(x)) == x for x in range(2, limit))
