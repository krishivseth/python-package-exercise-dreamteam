"""Show all six package functions using fictional passwords."""

from password_roaster import (
    compare_passwords,
    crack_time,
    generate_password,
    password_feedback,
    roast_password,
    score_password,
)


def main() -> None:
    first = "Go7!"
    second = "VelvetOtter7!"
    print("Password Roaster demo: examples only; do not reuse these passwords.")
    print(f"Password 1: {first}")
    print(f"Password 2: {second}")

    print("\n1. Score both passwords")
    print(f"Password 1: {score_password(first)}/100")
    print(f"Password 2: {score_password(second)}/100")

    print("\n2. Get feedback on password 1")
    for tip in password_feedback(first):
        print(f"- {tip}")

    print("\n3. Compare the passwords, with optional roasts")
    result = compare_passwords(first, second, roast=True)
    print(f"Winner: {result['winner']} password")
    print(f"Password 1 roast: {result['first_roast']}")
    print(f"Password 2 roast: {result['second_roast']}")
    tie = compare_passwords(first, "Hi8?")
    print(f"Compare password 1 with Hi8?: {tie['winner']}")

    print("\n4. Roast password 1 at two heat levels")
    print(f"Mild: {roast_password(first, level='mild')}")
    print(f"Savage: {roast_password(first, level='savage')}")

    print("\n5. Generate new examples")
    print(f"16-character password: {generate_password(length=16)}")
    print(f"5-word passphrase: {generate_password(length=5, words=True)}")

    print("\n6. Estimate brute-force time for password 1")
    for rate in (1_000, 1_000_000):
        estimate = crack_time(first, guesses_per_second=rate)
        print(f"At {rate:,} guesses/second: {estimate:,.1f} seconds")
    breaks = crack_time(first, guesses_per_second=1_000, unit="coffee_breaks")
    print(f"At 1,000 guesses/second: {breaks:.3g} five-minute coffee breaks")
    print("These estimates illustrate the model, not real-world security.")


if __name__ == "__main__":
    main()
