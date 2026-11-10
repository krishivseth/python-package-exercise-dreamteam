"""Compare two passwords using the same scoring rules."""

from .scoring import score_password


def compare_passwords(first: str, second: str) -> dict:
    """Return both scores and a winner: first, second, or tie."""
    first_score = score_password(first)
    second_score = score_password(second)

    winner = "tie"
    if first_score > second_score:
        winner = "first"
    elif second_score > first_score:
        winner = "second"

    return {"first_score": first_score, "second_score": second_score, "winner": winner}
