from core.key_generation import calculate_n, calculate_phi, validate_e


def test_tc01_key_parameters():
    assert calculate_n(17, 11) == 187
    assert calculate_phi(17, 11) == 160
    assert validate_e(7, 160)["valid"]


def test_tc04_invalid_e():
    result = validate_e(10, 160)
    assert not result["valid"]
