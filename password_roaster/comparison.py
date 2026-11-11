"""Compare two passwords using the same scoring rules."""

from .roasting import roast_password
from .scoring import score_password


def compare_passwords(first: str, second: str, roast: bool = False) -> dict:
    """Return both scores and a winner: first, second, or tie.

    Set roast=True to also include first_roast and second_roast messages.
    Scores and the winner are unchanged. Passwords must be strings and
    roast must be a bool; invalid inputs raise TypeError. Nothing is printed.
    """
    if not isinstance(roast, bool):
        raise TypeError("roast must be a bool")

    first_score = score_password(first)
    second_score = score_password(second)

    winner = "tie"
    if first_score > second_score:
        winner = "first"
    elif second_score > first_score:
        winner = "second"

    result = {"first_score": first_score, "second_score": second_score, "winner": winner}
    if roast:
        result["first_roast"] = roast_password(first)
        result["second_roast"] = roast_password(second)
    return result
