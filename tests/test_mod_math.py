from core.mod_math import extended_gcd, extended_gcd_table, mod_inverse


def test_extended_gcd_identity():
    gcd_value, x, y = extended_gcd(17, 3120)
    assert 17 * x + 3120 * y == gcd_value == 1


def test_tc01_and_tc02_mod_inverse():
    assert mod_inverse(7, 160) == 23
    assert mod_inverse(17, 3120) == 2753


def test_extended_gcd_table_tracks_coefficients():
    rows = extended_gcd_table(20, 3)
    row_with_one = next(row for row in rows if row["r"] == 1)
    assert row_with_one["s"] * 20 + row_with_one["t"] * 3 == 1
    assert row_with_one["t"] % 20 == 7
