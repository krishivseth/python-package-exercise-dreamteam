"""Turn a password score into a roast at the heat level you pick."""

from .scoring import _is_common, score_password


LEVELS = ("mild", "spicy", "savage")
LONG_LENGTH = 64

# Special cases get their own roast before the score tiers are checked.
SPECIAL_ROASTS = {
    "mild": {
        "blank": "An empty password is a welcome mat, not a lock.",
        "common": "That password is on every hacker's top ten list. Pick something less famous.",
        "repeat": "One key, pressed over and over. Your keyboard has other buttons, I promise.",
        "long": "This password is longer than most terms of service. Respect, and also why?",
    },
    "spicy": {
        "blank": "You left the password blank. Bold move for someone with a bank account.",
        "common": "Congrats, you picked the same password as half the internet and your uncle.",
        "repeat": "Did your cat fall asleep on the keyboard, or is this on purpose?",
        "long": "Nobody is cracking this, including you at 3am when you forget it.",
    },
    "savage": {
        "blank": "No password at all. Hackers would feel bad, if they had feelings.",
        "common": "Hackers don't even brute force this one. They just say it out loud.",
        "repeat": "Typing one letter on repeat isn't a password, it's a cry for help.",
        "long": "You didn't make a password, you wrote a memoir. Please seek a password manager.",
    },
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


def _special_case(password: str) -> str | None:
    if not password.strip():
        return "blank"
    if _is_common(password):
        return "common"
    if len(password) > 1 and len(set(password)) == 1:
        return "repeat"
    if len(password) > LONG_LENGTH:
        return "long"
    return None


def roast_password(password: str, level: str = "mild") -> str:
    """Return a joke that matches how weak the password scores.

    level picks how harsh the roast is: "mild", "spicy", or "savage", in any
    case and with surrounding spaces ignored. Blank, common, single-character
    and very long passwords get their own roasts. Non-string passwords or
    levels raise TypeError, and unknown levels raise ValueError. The roast
    never repeats the password.
    """
    score = score_password(password)
    if not isinstance(level, str):
        raise TypeError("level must be a string")
    level = level.strip().lower()
    if level not in LEVELS:
        raise ValueError("level must be one of: " + ", ".join(LEVELS))

    case = _special_case(password)
    if case is not None:
        return SPECIAL_ROASTS[level][case]
    for limit, roast in ROASTS[level]:
        if score <= limit:
            return roast
    return ROASTS[level][-1][1]
