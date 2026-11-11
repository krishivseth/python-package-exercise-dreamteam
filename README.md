# Password Roaster

[![Build and test](https://github.com/krishivseth/python-package-exercise-dreamteam/actions/workflows/tests.yml/badge.svg)](https://github.com/krishivseth/python-package-exercise-dreamteam/actions/workflows/tests.yml)

Scores passwords and roasts the weaknesses. For fun...

## Install and use

With Python 3.13+:

```sh
python -m pip install dreamteam-password-roaster
```

[View the package on PyPI](URL_HERE).

```python
from password_roaster import score_password, roast_password

print(score_password("Password123!"))
print(roast_password("Password123!"))
```

- `score_password(password)` returns 0–100 based on length, character variety,
  common passwords, repetition, and sequences. Blank input scores 0.
- `roast_password(password, level="mild")` returns a joke about how weak the
  password is. `level` sets the heat to `"mild"`, `"spicy"` or `"savage"`, in
  any case, with surrounding spaces ignored. Blank passwords, common passwords,
  passwords made from one repeated character, and passwords over 64 characters
  get special roasts. Other passwords are roasted by score. An unknown level
  raises `ValueError`.

```python
from password_roaster import roast_password

print(roast_password("sillygoose"))
print(roast_password("letmein", level="spicy"))
print(roast_password("VelvetOtter7!", level="savage"))
```

Both accept strings and raise `TypeError` otherwise. Neither stores or sends
passwords. Use made-up passwords when trying the examples.

### Password improvement feedback

`password_feedback(password)` returns a list of improvement tips. It checks
non-whitespace length, missing lowercase or uppercase letters, numbers, symbols,
common passwords, repeated patterns, and sequences. It can return several tips
for one password.

```python
from password_roaster import password_feedback

print(password_feedback("Go7!"))
# ['Use at least 12 characters, not counting spaces.']

print(password_feedback("moss"))
# ['Use at least 12 characters, not counting spaces.', 'Add an uppercase letter.', 'Add a number.', 'Add a symbol.']

print(password_feedback(" \t\n"))
# ['Enter a password.']

print(password_feedback("VelvetOtter7!"))
# ['No obvious weaknesses found.']
```

The input must be a string; other types raise `TypeError`. The function returns
tips without printing or including the supplied password. No obvious weaknesses
is a result of these simple rules, not a security guarantee.

### Compare two passwords

`compare_passwords(first, second, roast=False)` returns a dictionary with
`first_score`, `second_score`, and `winner`. Scores use the same 0–100 rules as
`score_password`. The winner is `"first"`, `"second"`, or `"tie"`; different
passwords can tie when their scores are equal. Both inputs must be strings.

```python
from password_roaster import compare_passwords

print(compare_passwords("VelvetOtter7!", "Go7!"))
# {'first_score': 79, 'second_score': 30, 'winner': 'first'}

print(compare_passwords("Go7!", "VelvetOtter7!"))
# {'first_score': 30, 'second_score': 79, 'winner': 'second'}

print(compare_passwords("Go7!", "Hi8?"))
# {'first_score': 30, 'second_score': 30, 'winner': 'tie'}

print(compare_passwords("", ""))
# {'first_score': 0, 'second_score': 0, 'winner': 'tie'}
```

#### Optional roast messages

Pass `roast=True` to add `first_roast` and `second_roast` to the result. Each
message comes from `roast_password` using its default `"mild"` level. The scores and
winner stay the same. Omitting the option or passing `roast=False` returns only
the original three fields.

```python
from password_roaster import compare_passwords

result = compare_passwords("VelvetOtter7!", "Go7!", roast=True)
print(result["winner"])
# first
print(result["first_roast"])
# Not bad. A hacker would at least have to put down their snack.
print(result["second_roast"])
# This password folds faster than a lawn chair.
```

Non-string passwords raise `TypeError`. The `roast` option must be a boolean;
values such as `"false"`, `0`, or `None` also raise `TypeError`. The function
does not print, store, or transmit the supplied passwords.

### Face-off example

The [face-off demo](examples/faceoff_demo.py) compares fictional passwords and
prints their scores, both possible winners, and a tie without printing the
passwords. From the repository root after installing development dependencies:

```sh
pipenv run python -m examples.faceoff_demo
```

## Development

Run from the repository root:

```sh
python -m pip install pipenv
pipenv sync --dev
pipenv run python -m pytest
pipenv run python -m build
```

Use `python3` on macOS/Linux or `py` on Windows if needed. Pipenv manages the
virtual environment. No environment variables, secrets, or database setup needed.
GitHub Actions builds and tests PRs on Python 3.13 and 3.14.

## Team

- [Ben Zaslavsky](https://github.com/benzaslavsky)
- [Krishiv Seth](https://github.com/krishivseth)
- [Jay Yu](https://github.com/Jayyu2005)
- [Isha Zaheer](https://github.com/izz04)
- [TEMP](https://github.com/temp)
