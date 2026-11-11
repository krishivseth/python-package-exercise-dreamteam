"""Turn a password score into a roast at the heat level you pick."""

from .scoring import score_password


LEVELS = ("mild", "spicy", "savage")

BLANK_ROASTS = {
    "mild": "An empty password is a welcome mat, not a lock.",
    "spicy": "You left the password blank. Bold move for someone with a bank account.",
    "savage": "No password at all. Hackers would feel bad, if they had feelings.",
}

# Each level maps score ceilings to roasts. The first ceiling the score fits under wins.
ROASTS = {
    "mild": (
        (10, "Hackers won't need to guess this one. They'll read it off your sticky note."),
        (30, "This password folds faster than a lawn chair."),
        (60, "Your password is the airport sandwich of security. It exists, and that's about it."),
        (80, "Not bad. A hacker would at least have to put down their snack."),
        (100, "Strong password. Good luck remembering it after a long weekend."),
    ),
    "spicy": (
        (10, "My grandma's flip phone has better security, and it doesn't lock."),
        (30, "A toddler mashing the keyboard would beat this, and get a nap after."),
        (60, "This password does the bare minimum, like a group project member who only made the title slide."),
        (80, "Decent. A hacker would need a coffee refill, not a supercomputer."),
        (100, "Fine, this one's tough. Too bad you'll store it in a file called passwords.txt."),
    ),
    "savage": (
        (10, "This isn't a password, it's a public announcement."),
        (30, "Hackers use this password to warm up before the hard ones."),
        (60, "Mid. Your password peaked in the first try and never recovered."),
        (80, "Almost respectable. Almost. Like a tip that's just under 15 percent."),
        (100, "Strong enough to scare hackers. Shame the account behind it is your Club Penguin."),
    ),
}


def roast_password(password: str, level: str = "mild") -> str:
    """Return a joke that matches how weak the password scores.

    level picks how harsh the roast is: "mild", "spicy", or "savage".
    Non-string passwords or levels raise TypeError, and unknown levels raise
    ValueError. The roast never repeats the password.
    """
    score = score_password(password)
    if not isinstance(level, str):
        raise TypeError("level must be a string")
    if level not in LEVELS:
        raise ValueError("level must be one of: " + ", ".join(LEVELS))
    if not password.strip():
        return BLANK_ROASTS[level]
    for limit, roast in ROASTS[level]:
        if score <= limit:
            return roast
    return ROASTS[level][-1][1]
