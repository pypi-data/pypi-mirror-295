from kikan import Vector


def test_vector_sum():
    assert Vector(1, 2, 3.14) + Vector(4, 3, 0) == Vector(5, 5, 3.14)
