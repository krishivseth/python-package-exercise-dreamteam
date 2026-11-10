import string


def crack_time(password: str, guesses_per_second: int = 1_000_000_000) -> float:
    """Estimate the average seconds needed to guess a password by brute force."""
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not password:
        raise ValueError("password must contain at least one character")
    if type(guesses_per_second) is not int:
        raise TypeError("guesses_per_second must be an integer")
    if guesses_per_second <= 0:
        raise ValueError("guesses_per_second must be positive")

    character_groups = (
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation + " ",
    )

    password_chars = set(password)
    pool_size = sum(
        len(group) for group in character_groups if password_chars.intersection(group)
    )
    known_chars = set("".join(character_groups))
    pool_size += len(password_chars - known_chars)

    possible_guesses = pool_size ** len(password)
    try:
        return (possible_guesses + 1) / (2 * guesses_per_second)
    except OverflowError:
        return float("inf")
