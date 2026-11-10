"""Turn a password score into a roast."""

from .scoring import score_password


BLANK_ROAST = "An empty password is a welcome mat, not a lock."

ROASTS = (
    (10, "Hackers won't need to guess this one. They'll read it off your sticky note."),
    (30, "This password folds faster than a lawn chair."),
    (60, "Your password is the airport sandwich of security. It exists, and that's about it."),
    (80, "Not bad. A hacker would at least have to put down their snack."),
)

STRONG_ROAST = "Strong password. Good luck remembering it after a long weekend."


def roast_password(password: str) -> str:
    """Return a joke that matches how weak the password scores.

    Non-strings raise TypeError. The roast never repeats the password.
    """
    score = score_password(password)
    if not password.strip():
        return BLANK_ROAST
    for limit, roast in ROASTS:
        if score <= limit:
            return roast
    return STRONG_ROAST
