"""RSA public-key parameters and validation."""

from __future__ import annotations

import math


def calculate_n(p: int, q: int) -> int:
    return p * q


def calculate_phi(p: int, q: int) -> int:
    return (p - 1) * (q - 1)


def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)


def validate_e(e: int, phi_n: int) -> dict:
    """Validate the RSA public exponent."""
    if not isinstance(e, int):
        return {"valid": False, "message": "e phải là số nguyên."}
    if not 1 < e < phi_n:
        return {
            "valid": False,
            "message": "e phải thỏa mãn 1 < e < phi(n).",
        }
    common_divisor = gcd(e, phi_n)
    if common_divisor != 1:
        return {
            "valid": False,
            "message": (
                f"e không hợp lệ vì gcd({e}, {phi_n}) = {common_divisor}, "
                "khác 1."
            ),
        }
    return {"valid": True, "message": "e hợp lệ và nguyên tố cùng nhau với phi(n)."}


def suggest_e(phi_n: int) -> int:
    """Pick a familiar valid public exponent for an educational demo."""
    for candidate in (65537, 257, 17, 5, 3):
        if validate_e(candidate, phi_n)["valid"]:
            return candidate
    for candidate in range(3, phi_n, 2):
        if validate_e(candidate, phi_n)["valid"]:
            return candidate
    raise ValueError("Không tìm được e phù hợp với phi(n).")
