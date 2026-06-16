import pytest

from core.rsa_cipher import decrypt_text, encrypt_text, parse_cipher_numbers
from core.rsa_service import generate_keys


def test_tc05_encrypt_decrypt_hello():
    keys = generate_keys(61, 53, 17)
    encrypted = encrypt_text("HELLO", keys["public_key"])
    decrypted = decrypt_text(encrypted["cipher_numbers"], keys["private_key"])
    assert decrypted["decrypted_text"] == "HELLO"


def test_vietnamese_utf8_round_trip():
    keys = generate_keys(61, 53, 17)
    encrypted = encrypt_text("Xin chào", keys["public_key"])
    decrypted = decrypt_text(encrypted["cipher_numbers"], keys["private_key"])
    assert decrypted["decrypted_text"] == "Xin chào"


def test_parse_cipher_numbers_accepts_common_formats():
    assert parse_cipher_numbers("[1345, 3179, 2235]\n1992") == [
        1345,
        3179,
        2235,
        1992,
    ]


def test_parse_cipher_numbers_rejects_empty_or_negative_values():
    with pytest.raises(ValueError):
        parse_cipher_numbers("")
    with pytest.raises(ValueError):
        parse_cipher_numbers("12, -4")
