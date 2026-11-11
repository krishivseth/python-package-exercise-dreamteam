# Password Roaster

[![Build and test](https://github.com/krishivseth/python-package-exercise-dreamteam/actions/workflows/tests.yml/badge.svg)](https://github.com/krishivseth/python-package-exercise-dreamteam/actions/workflows/tests.yml)

Scores passwords and roasts the weaknesses. For fun...

## Install and use

With Python 3.11+:

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
  any case. Blank, common, single-character and very long passwords get their
  own roasts, and every other password is roasted by its score. An unknown
  level raises `ValueError`.

```python
from password_roaster import roast_password

print(roast_password("sillygoose"))
print(roast_password("letmein", level="spicy"))
print(roast_password("VelvetOtter7!", level="savage"))
```

Both accept strings and raise `TypeError` otherwise. Neither stores or sends
passwords. See [the example](examples/roast_demo.py) for more inputs.

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
- [TEMP](https://github.com/temp)
- [TEMP](https://github.com/temp)
- [TEMP](https://github.com/temp)
