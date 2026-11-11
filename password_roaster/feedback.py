"""Simple tips for the weaknesses behind a password's score."""

from .scoring import _has_repetition, _has_sequence, _is_common


def password_feedback(password: str) -> list[str]:
    """Return improvement tips without including the password."""
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    characters = [c for c in password if not c.isspace()]
    if not characters:
        return ["Enter a password."]

    tips = []
    if _is_common(password):
        tips.append("Avoid common passwords and simple changes to them.")
    if len(characters) < 12:
        tips.append("Use at least 12 characters, not counting spaces.")
    if not any(c.islower() for c in characters):
        tips.append("Add a lowercase letter.")
    if not any(c.isupper() for c in characters):
        tips.append("Add an uppercase letter.")
    if not any(c.isdecimal() for c in characters):
        tips.append("Add a number.")
    if not any(not c.isalnum() for c in characters):
        tips.append("Add a symbol.")
    if _has_repetition(password):
        tips.append("Avoid repeated characters or patterns.")
    if _has_sequence(password):
        tips.append("Avoid sequences like abcd, 1234, or qwerty.")
    return tips or ["No obvious weaknesses found."]
