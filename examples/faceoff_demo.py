"""Demonstrate every public function using made-up passwords."""

from password_roaster import (
    compare_passwords,
    crack_time,
    generate_password,
    password_feedback,
    roast_password,
    score_password,
)


def main():
    print("Password report (fictional inputs only)")
    for label, password in (("Short", "Go7!"), ("Common", "password"),
                            ("Stronger", "VelvetOtter7!"), ("Blank", "")):
        print(f"{label}: {score_password(password)}/100")
        print("Feedback:", " ".join(password_feedback(password)))
        for level in ("mild", "spicy", "savage"):
            print(f"{level.title()} roast: {roast_password(password, level=level)}")
        print()

    print("Face-offs")
    pairs = [('Go7!', 'VelvetOtter7!'), ('VelvetOtter7!', 'Go7!'), ('Go7!', 'Hi8?')]
    for first, second in pairs:
        result = compare_passwords(first, second)
        print(f"Password 1: {result['first_score']}/100")
        print(f"Password 2: {result['second_score']}/100")
        if result['winner'] == 'tie':
            print("It's a tie!")
        elif result['winner'] == 'first':
            print('Password 1 wins!')
        else:
            print('Password 2 wins!')
        print()

    print("Face-off with roasts")
    result = compare_passwords("Go7!", "VelvetOtter7!", roast=True)
    print("Password 1:", result["first_roast"])
    print("Password 2:", result["second_roast"])
    print()

    print("Generated examples (do not use these displayed values as real passwords)")
    for label, options in (
        ("Default password", {}),
        ("20-character password", {"length": 20}),
        ("Password without symbols", {"symbols": False}),
        ("Default passphrase", {"words": True}),
        ("Four-word passphrase", {"length": 4, "words": True}),
        ("Passphrase without symbols", {"length": 4, "words": True, "symbols": False}),
    ):
        print(f"{label}: {generate_password(**options)}")
    print()

    print("Toy cracking-time estimates for a fictional short password")
    for unit in ("seconds", "coffee_breaks", "movies", "semesters"):
        estimate = crack_time("Go7!", unit=unit)
        print(f"{unit}: {estimate:.6g}")
    print("Seconds at one million guesses per second:",
          crack_time("Go7!", guesses_per_second=1_000_000))
    print()

    print("Invalid input examples")
    for function, args in (
        (score_password, (None,)),
        (roast_password, ("Go7!", "unknown")),
        (password_feedback, (None,)),
        (compare_passwords, ("Go7!", None)),
        (generate_password, (0,)),
        (crack_time, ("",)),
    ):
        try:
            function(*args)
        except (TypeError, ValueError) as error:
            print(f"{function.__name__}: {error}")


if __name__ == '__main__':
    main()
