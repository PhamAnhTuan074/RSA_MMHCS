from core.prime_utils import is_prime, validate_prime_pair


def test_is_prime():
    assert is_prime(61)
    assert not is_prime(1)
    assert not is_prime(15)


def test_validate_prime_pair():
    assert validate_prime_pair(61, 53)["valid"]
    assert not validate_prime_pair(17, 17)["valid"]
