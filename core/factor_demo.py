"""Fast modular exponentiation and small-number factorization demos."""

from __future__ import annotations

import math


def fast_mod_exp(base: int, exponent: int, modulus: int) -> int:
    if exponent < 0:
        raise ValueError("Số mũ phải không âm.")
    if modulus <= 0:
        raise ValueError("Modulo phải lớn hơn 0.")

    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result


def fast_mod_exp_steps(base: int, exponent: int, modulus: int) -> list[dict]:
    """Return square-and-multiply states for each exponent bit."""
    if exponent < 0:
        raise ValueError("Số mũ phải không âm.")
    if modulus <= 0:
        raise ValueError("Modulo phải lớn hơn 0.")

    result = 1
    current_base = base % modulus
    current_exponent = exponent
    steps: list[dict] = []
    index = 1

    if exponent == 0:
        return [
            {
                "Bước": 0,
                "Số mũ": 0,
                "Bit": 0,
                "Hành động": "Kết quả khởi tạo",
                "Cơ số": current_base,
                "Kết quả": 1 % modulus,
            }
        ]

    while current_exponent:
        bit = current_exponent & 1
        before = result
        if bit:
            result = (result * current_base) % modulus
            action = f"{before} × {current_base} mod {modulus}"
        else:
            action = "Bỏ qua phép nhân (bit = 0)"

        steps.append(
            {
                "Bước": index,
                "Số mũ": current_exponent,
                "Bit": bit,
                "Hành động": action,
                "Cơ số": current_base,
                "Kết quả": result,
            }
        )
        current_base = (current_base * current_base) % modulus
        current_exponent >>= 1
        index += 1
    return steps


def fast_mod_exp_detailed_steps(
    base: int,
    exponent: int,
    modulus: int,
) -> list[dict]:
    """Return detailed square-and-multiply rows for teaching the algorithm."""
    if exponent < 0:
        raise ValueError("Số mũ phải không âm.")
    if modulus <= 0:
        raise ValueError("Modulo phải lớn hơn 0.")

    result = 1 % modulus
    current_base = base % modulus
    current_exponent = exponent
    rows: list[dict] = []
    step = 0

    while current_exponent > 0:
        is_odd = current_exponent % 2 == 1
        result_before = result
        base_before = current_base
        if is_odd:
            result = (result * current_base) % modulus
            result_detail = (
                f"({result_before}×{base_before}) mod {modulus} = {result}"
            )
        else:
            result_detail = f"Giữ nguyên {result}"

        current_base = (current_base * current_base) % modulus
        next_exponent = current_exponent // 2
        rows.append(
            {
                "Bước": step,
                "b hiện tại": current_exponent,
                "b ở nhị phân": bin(current_exponent)[2:],
                "Bit cuối": current_exponent % 2,
                "Nhận xét": (
                    "b lẻ - nhân thêm a vào k"
                    if is_odd
                    else "b chẵn - giữ k, chỉ bình phương a"
                ),
                "k trước": result_before,
                "a hiện tại": base_before,
                "k sau bước": result_detail,
                "a cho bước sau": (
                    f"{base_before}² mod {modulus} = {current_base}"
                ),
                "b bước sau": str(next_exponent),
            }
        )
        current_exponent = next_exponent
        step += 1

    rows.append(
        {
            "Bước": step,
            "b hiện tại": 0,
            "b ở nhị phân": "0",
            "Bit cuối": "-",
            "Nhận xét": "Dừng vì b = 0",
            "k trước": result,
            "a hiện tại": current_base,
            "k sau bước": f"Kết quả cuối = {result}",
            "a cho bước sau": "-",
            "b bước sau": "-",
        }
    )
    return rows


def factor_n_demo(n: int, max_attempts: int | None = None) -> dict:
    """Try trial division to illustrate why large RSA moduli are difficult."""
    if n < 4:
        return {
            "success": False,
            "p": None,
            "q": None,
            "attempts": 0,
            "message": "n phải lớn hơn hoặc bằng 4.",
        }

    attempts = 0
    limit = math.isqrt(n)
    divisors = [2, *range(3, limit + 1, 2)]
    for divisor in divisors:
        attempts += 1
        if n % divisor == 0:
            return {
                "success": True,
                "p": divisor,
                "q": n // divisor,
                "attempts": attempts,
                "message": "Đã tìm thấy hai thừa số của n.",
            }
        if max_attempts is not None and attempts >= max_attempts:
            break

    return {
        "success": False,
        "p": None,
        "q": None,
        "attempts": attempts,
        "message": "Không tìm thấy p và q trong giới hạn thử nghiệm.",
    }
