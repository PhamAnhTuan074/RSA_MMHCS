"""Modular arithmetic for RSA."""

from __future__ import annotations


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return gcd(a, b), x and y where ax + by = gcd(a, b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t


def extended_gcd_steps(a: int, b: int) -> list[dict]:
    """Return each Euclidean division step for visualization."""
    steps: list[dict] = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    index = 1
    while r:
        quotient = old_r // r
        next_r = old_r - quotient * r
        steps.append(
            {
                "Bước": index,
                "Phép chia": f"{old_r} = {quotient} × {r} + {next_r}",
                "q": quotient,
                "r": next_r,
                "x": old_s,
                "y": old_t,
            }
        )
        old_r, r = r, next_r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
        index += 1
    return steps


def extended_gcd_table(a: int, b: int) -> list[dict]:
    """Return the coefficient table where every row satisfies r = s*a + t*b."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    rows = [
        {
            "Bước": 0,
            "q": "-",
            "r": old_r,
            "s": old_s,
            "t": old_t,
            "Biểu diễn": f"{old_r} = {old_s}×{a} + {old_t}×{b}",
        },
        {
            "Bước": 1,
            "q": "-",
            "r": r,
            "s": s,
            "t": t,
            "Biểu diễn": f"{r} = {s}×{a} + {t}×{b}",
        },
    ]

    step = 2
    while r:
        quotient = old_r // r
        next_r = old_r - quotient * r
        next_s = old_s - quotient * s
        next_t = old_t - quotient * t
        expression = (
            "Dừng vì số dư bằng 0"
            if next_r == 0
            else f"{next_r} = {next_s}×{a} + {next_t}×{b}"
        )
        rows.append(
            {
                "Bước": step,
                "q": str(quotient),
                "r": next_r,
                "s": next_s,
                "t": next_t,
                "Biểu diễn": expression,
            }
        )
        old_r, r = r, next_r
        old_s, s = s, next_s
        old_t, t = t, next_t
        step += 1
    return rows


def mod_inverse(e: int, phi_n: int) -> int:
    """Return d where e*d mod phi_n equals one."""
    gcd_value, x, _ = extended_gcd(e, phi_n)
    if gcd_value != 1:
        raise ValueError(
            "Không tồn tại nghịch đảo modulo vì e và phi_n "
            "không nguyên tố cùng nhau."
        )
    return x % phi_n
