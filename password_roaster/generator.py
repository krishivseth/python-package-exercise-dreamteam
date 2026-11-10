import secrets
import string

from .scoring import _has_repetition, _has_sequence, _is_common


SYMBOLS = "!@#$%^&*-_=+?"


MIN = 12

MAX= 128


def generate_password(length: int = 16, symbols: bool = True) -> str:
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("length must be an integer")
    if not isinstance(symbols, bool):
        raise TypeError("symbols must be True or False")
    if not MIN <= length <= MAX:
        raise ValueError(f"length must be between {MIN} and {MAX}")

    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if symbols:
        groups.append(SYMBOLS)
    pool = "".join(groups)

    while True:
        candidate = "".join(secrets.choice(pool) for _ in range(length))
        if not all(any(c in group for c in candidate) for group in groups):
            continue
        if _has_repetition(candidate) or _has_sequence(candidate) or _is_common(candidate):
            continue
        return candidate
