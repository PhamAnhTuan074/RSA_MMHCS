"""Text conversion, RSA encryption and RSA decryption."""

from __future__ import annotations

import re


def text_to_numbers(plain_text: str) -> list[int]:
    """Encode text into UTF-8 bytes so Vietnamese text is supported."""
    return list(plain_text.encode("utf-8"))


def numbers_to_text(numbers: list[int]) -> str:
    """Decode a list of UTF-8 bytes back into text."""
    try:
        return bytes(numbers).decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Dữ liệu giải mã không tạo thành văn bản UTF-8 hợp lệ.") from exc


def parse_cipher_numbers(raw_text: str) -> list[int]:
    """Parse cipher numbers from comma, whitespace, newline or list-like input."""
    if not raw_text or not raw_text.strip():
        raise ValueError("Vui lòng nhập danh sách bản mã cần giải mã.")

    numbers = [int(match) for match in re.findall(r"-?\d+", raw_text)]
    if not numbers:
        raise ValueError("Không tìm thấy số nào trong bản mã đã nhập.")
    if any(number < 0 for number in numbers):
        raise ValueError("Bản mã RSA phải là các số nguyên không âm.")
    return numbers


def _validate_key(key: dict, exponent_name: str) -> tuple[int, int]:
    if not isinstance(key, dict) or exponent_name not in key or "n" not in key:
        raise ValueError(f"Khóa phải có dạng {{{exponent_name}, n}}.")
    exponent = int(key[exponent_name])
    modulus = int(key["n"])
    if exponent <= 0 or modulus <= 1:
        raise ValueError("Giá trị trong khóa RSA không hợp lệ.")
    return exponent, modulus


def encrypt_text(plain_text: str, public_key: dict) -> dict:
    """Encrypt every UTF-8 byte with the public key."""
    if not plain_text:
        raise ValueError("Vui lòng nhập văn bản cần mã hóa.")

    e, n = _validate_key(public_key, "e")
    message_numbers = text_to_numbers(plain_text)
    if max(message_numbers) >= n:
        raise ValueError(
            "n phải lớn hơn mọi giá trị byte của thông điệp. "
            "Với văn bản UTF-8, nên chọn n > 255."
        )

    cipher_numbers = [pow(message, e, n) for message in message_numbers]
    return {
        "plain_text": plain_text,
        "message_numbers": message_numbers,
        "cipher_numbers": cipher_numbers,
        "public_key": {"e": e, "n": n},
    }


def decrypt_text(cipher_numbers: list[int], private_key: dict) -> dict:
    """Decrypt RSA integers and decode the recovered UTF-8 bytes."""
    if not cipher_numbers:
        raise ValueError("Danh sách bản mã đang rỗng.")

    d, n = _validate_key(private_key, "d")
    message_numbers = [pow(int(cipher), d, n) for cipher in cipher_numbers]
    decrypted_text = numbers_to_text(message_numbers)
    return {
        "cipher_numbers": list(cipher_numbers),
        "message_numbers": message_numbers,
        "decrypted_text": decrypted_text,
        "private_key": {"d": d, "n": n},
    }
