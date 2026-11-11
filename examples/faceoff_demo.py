"""Compare made-up passwords and announce the winner."""

from password_roaster import compare_passwords


def main():
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


if __name__ == '__main__':
    main()