"""Straightforward scoring rules for the password roasting game."""

import string


COMMON_PASSWORDS = frozenset({
    "password", "password1", "password123", "password123!", "123456",
    "12345678", "123456789", "1234567890", "qwerty", "qwerty123",
    "abc123", "admin", "letmein", "welcome", "iloveyou", "monkey",
    "dragon", "football", "baseball", "sunshine", "princess", "login",
})


def _is_common(password: str) -> bool:
    """Catch listed passwords and simple disguises such as P@ssword2026!."""
    lowered = password.casefold().strip()
    substitutions = str.maketrans({"@": "a", "$": "s", "0": "o"})
    normalized = lowered.translate(substitutions)
    base = lowered.rstrip(string.digits + string.punctuation).translate(substitutions)
    return any(
        value in COMMON_PASSWORDS
        or value.rstrip(string.digits + string.punctuation) in COMMON_PASSWORDS
        for value in (lowered, normalized, base)
    )


def _has_sequence(password: str) -> bool:
    """Find runs of four letters, digits, or adjacent keys, in either direction."""
    lowered = password.casefold()
    sequences = (string.ascii_lowercase, "01234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm")
    for sequence in sequences:
        for direction in (sequence, sequence[::-1]):
            for start in range(len(direction) - 3):
                if direction[start:start + 4] in lowered:
                    return True
    return False


def _has_repetition(password: str) -> bool:
    """Find repeated characters or a short pattern repeated across the password."""
    lowered = password.casefold()
    if any(lowered[i] == lowered[i + 1] == lowered[i + 2]
           for i in range(len(lowered) - 2)):
        return True
    for size in range(1, len(lowered) // 2 + 1):
        if len(lowered) % size == 0 and lowered[:size] * (len(lowered) // size) == lowered:
            return True
    return False


def score_password(password: str) -> int:
    """Return a heuristic score from 0 to 100, for entertainment.

    Length earns 3 points per character up to 60. Lowercase, uppercase,
    digits, and symbols each earn 10 points. Repetition costs 25 points;
    sequences cost 20. Fewer than 8 characters caps the score at 30, and
    fewer than 12 caps it at 60. Common passwords score at most 10.
    Empty or whitespace-only input scores zero; other non-strings raise
    TypeError. Whitespace earns no points. Nothing is saved or transmitted.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    characters = [c for c in password if not c.isspace()]
    if not characters:
        return 0

    score = min(len(characters) * 3, 60)
    score += 10 * sum((
        any(c.islower() for c in characters),
        any(c.isupper() for c in characters),
        any(c.isdecimal() for c in characters),
        any(not c.isalnum() for c in characters),
    ))
    if _has_repetition(password):
        score -= 25
    if _has_sequence(password):
        score -= 20
    if len(characters) < 8:
        score = min(score, 30)
    elif len(characters) < 12:
        score = min(score, 60)
    if _is_common(password):
        score = min(score, 10)
    return max(0, min(score, 100))
