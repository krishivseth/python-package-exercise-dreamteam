import string
import pytest

from password_roaster.generator import SYMBOLS, generate_password
from password_roaster.scoring import (
    _has_repetition,
    _has_sequence,
    _is_common,
    score_password,
)


def test_returns_string_of_default_length():
    password = generate_password()
    assert isinstance(password, str)
    assert len(password) == 16
    assert not any(c.isspace() for c in password)




def test_respects_requested_length():
    for length in (12, 13, 20, 64, 128):
        assert len(generate_password(length)) == length


def test_symbols_on_includes_a_symbol():
    password = generate_password(16, symbols=True)
    allowed = set(string.ascii_letters + string.digits + SYMBOLS)
    assert any(c in SYMBOLS for c in password)
    assert set(password) <= allowed


def test_symbols_off_has_only_letters_and_digits():
    password = generate_password(16, symbols=False)
    assert password.isalnum()
    assert not any(c in SYMBOLS for c in password)
    assert password.isascii()


def test_contains_every_character_type():
    for symbols in (True, False):
        password = generate_password(16, symbols=symbols)
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)


def test_avoids_weaknesses_the_scorer_punishes():
    for symbols in (True, False):
        for _ in range(50):
            password = generate_password(12, symbols=symbols)
            assert not _has_repetition(password)
            assert not _has_sequence(password)
            assert not _is_common(password)


def test_scores_full_marks_for_its_settings():
    cases = [
        (12, True, 76),
        (16, True, 88),
        (20, True, 100),
        (12, False, 66),
        (16, False, 78),
        (30, False, 90),
    ]
    for length, symbols, expected in cases:
        assert score_password(generate_password(length, symbols)) == expected




def test_passwords_are_different_each_time():
    passwords = {generate_password() for _ in range(25)}
    assert len(passwords) == 25


def test_rejects_length_out_of_range():
    for length in (11, 0, -5, 129, 1000):
        with pytest.raises(ValueError):
            generate_password(length)




def test_rejects_non_integer_length():
    for length in ("16", 16.0, None, True, [16]):
        with pytest.raises(TypeError):
            generate_password(length)


def test_rejects_non_boolean_symbols():
    for symbols in ("yes", 1, None, 0):
        with pytest.raises(TypeError):
            generate_password(16, symbols)
