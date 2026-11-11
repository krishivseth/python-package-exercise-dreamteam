import string
import pytest

from password_roaster.generator import SYMBOLS, WORDS, generate_password
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
    for length in ("16", 16.0, True, [16]):
        with pytest.raises(TypeError):
            generate_password(length)


def test_rejects_non_boolean_symbols():
    for symbols in ("yes", 1, None, 0):
        with pytest.raises(TypeError):
            generate_password(16, symbols)


def test_length_none_uses_the_defaults():
    assert len(generate_password(None)) == 16
    assert len(generate_password(None, words=True).split("-")) == 5
    assert len(generate_password(words=False)) == 16


def test_passphrase_default_has_five_words():
    phrase = generate_password(words=True)
    parts = phrase.split("-")
    assert len(parts) == 5
    assert all(part in WORDS for part in parts)
    assert phrase == phrase.lower()


def test_passphrase_respects_word_count():
    for count in (4, 6, 9, 12):
        parts = generate_password(count, words=True).split("-")
        assert len(parts) == count
        assert all(part in WORDS for part in parts)


def test_passphrase_never_repeats_a_word():
    for _ in range(100):
        parts = generate_password(12, words=True).split("-")
        assert len(set(parts)) == len(parts)


def test_passphrase_without_symbols_uses_capitalized_words():
    phrase = generate_password(4, symbols=False, words=True)
    assert phrase.isalpha()
    assert phrase[0].isupper()
    assert sum(c.isupper() for c in phrase) == 4
    pieces = []
    for c in phrase:
        if c.isupper():
            pieces.append(c.lower())
        else:
            pieces[-1] += c
    assert all(piece in WORDS for piece in pieces)


def test_passphrase_avoids_weaknesses_and_scores_well():
    for symbols in (True, False):
        for _ in range(100):
            phrase = generate_password(4, symbols=symbols, words=True)
            assert not _has_repetition(phrase)
            assert not _has_sequence(phrase)
            assert not _is_common(phrase)
            assert score_password(phrase) >= 65


def test_passphrases_are_different_each_time():
    phrases = {generate_password(words=True) for _ in range(25)}
    assert len(phrases) == 25


def test_passphrase_rejects_word_count_out_of_range():
    for count in (3, 0, -1, 13, 16):
        with pytest.raises(ValueError):
            generate_password(count, words=True)




def test_passphrase_rejects_bad_types():
    for count in ("5", 5.0, True, [5]):
        with pytest.raises(TypeError):
            generate_password(count, words=True)
    for words in ("yes", 1, 0, None):
        with pytest.raises(TypeError):
            generate_password(5, words=words)


def test_word_list_is_clean():
    assert len(WORDS) == len(set(WORDS))
    assert len(WORDS) >= 200
    assert all(word.isalpha() and word.islower() for word in WORDS)
