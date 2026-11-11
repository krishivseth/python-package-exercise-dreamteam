import string


def crack_time(
    password: str,
    guesses_per_second: int = 1_000_000_000,
    *,
    unit: str = "seconds",
) -> float:
    """Return a toy brute-force estimate in the requested time unit.

    Supported units:
        seconds: one second
        coffee_breaks: five minutes
        movies: two hours
        semesters: sixteen weeks

    These durations are fixed, playful assumptions.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not password:
        raise ValueError("password must contain at least one character")
    if type(guesses_per_second) is not int:
        raise TypeError("guesses_per_second must be an integer")
    if guesses_per_second <= 0:
        raise ValueError("guesses_per_second must be positive")
    if not isinstance(unit, str):
        raise TypeError("unit must be a string")

    unit_seconds = {
        "seconds": 1,
        "coffee_breaks": 300,
        "movies": 7_200,
        "semesters": 9_676_800,
    }
    if unit not in unit_seconds:
        raise ValueError(
            "unit must be seconds, coffee_breaks, movies, or semesters"
        )

    character_groups = (
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation + " ",
    )

    password_chars = set(password)
    pool_size = sum(
        len(group) for group in character_groups
        if password_chars.intersection(group)
    )
    known_chars = set("".join(character_groups))
    pool_size += len(password_chars - known_chars)

    possible_guesses = pool_size ** len(password)
    try:
        return (possible_guesses + 1) / (
            2 * guesses_per_second * unit_seconds[unit]
        )
    except OverflowError:
        return float("inf")
