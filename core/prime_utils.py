"""Prime-number helpers used by the RSA key generation flow."""

from __future__ import annotations

import math
import random


def is_prime(number: int) -> bool:
    """Return True when number is prime."""
    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0:
        return False

    limit = math.isqrt(number)
    for divisor in range(3, limit + 1, 2):
        if number % divisor == 0:
            return False
    return True


def validate_prime_pair(p: int, q: int) -> dict:
    """Validate the two RSA prime factors and return a UI-friendly result."""
    if not isinstance(p, int) or not isinstance(q, int):
        return {
            "valid": False,
            "message": "p và q phải là số nguyên.",
            "warning": None,
        }
    if p <= 2 or q <= 2:
        return {
            "valid": False,
            "message": "p và q phải là số nguyên tố lớn hơn 2.",
            "warning": None,
        }
    if not is_prime(p) or not is_prime(q):
        return {
            "valid": False,
            "message": "p và q phải là hai số nguyên tố.",
            "warning": None,
        }
    if p == q:
        return {
            "valid": False,
            "message": "p và q phải là hai số nguyên tố khác nhau.",
            "warning": None,
        }

    n = p * q
    warning = None
    if n <= 255:
        warning = (
            "n ≤ 255 nên không đủ lớn để mã hóa mọi byte của văn bản. "
            "Hãy dùng p = 61, q = 53 cho phần demo."
        )
    return {
        "valid": True,
        "message": "p và q hợp lệ.",
        "warning": warning,
    }


def generate_prime(min_value: int = 11, max_value: int = 199) -> int:
    """Generate a random odd prime in the inclusive range."""
    if min_value > max_value:
        raise ValueError("min_value phải nhỏ hơn hoặc bằng max_value.")

    candidates = [
        value
        for value in range(max(3, min_value), max_value + 1)
        if is_prime(value)
    ]
    if not candidates:
        raise ValueError("Không tìm thấy số nguyên tố trong khoảng đã chọn.")
    return random.choice(candidates)
