"""Orchestration layer that combines the RSA core modules."""

from __future__ import annotations

from core.key_generation import calculate_n, calculate_phi, validate_e
from core.mod_math import mod_inverse
from core.prime_utils import validate_prime_pair


def generate_keys(p: int, q: int, e: int) -> dict:
    prime_result = validate_prime_pair(p, q)
    if not prime_result["valid"]:
        raise ValueError(prime_result["message"])

    n = calculate_n(p, q)
    phi_n = calculate_phi(p, q)
    e_result = validate_e(e, phi_n)
    if not e_result["valid"]:
        raise ValueError(e_result["message"])

    d = mod_inverse(e, phi_n)
    return {
        "p": p,
        "q": q,
        "n": n,
        "phi_n": phi_n,
        "e": e,
        "d": d,
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
    }
