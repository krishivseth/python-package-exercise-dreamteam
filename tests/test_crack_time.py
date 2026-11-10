import pytest

from password_roaster.crack_time import crack_time


def test_known_estimate():
    assert crack_time("1234", guesses_per_second=100) == pytest.approx(50.005)


def test_doubling_guess_rate_halves_estimate():
    slower = crack_time("1234", guesses_per_second=100)
    faster = crack_time("1234", guesses_per_second=200)
    assert faster == pytest.approx(slower / 2)


def test_mixed_character_groups_increase_estimate():
    assert crack_time("aB3!") > crack_time("abcd")


def test_empty_password():
    with pytest.raises(ValueError, match="at least one character"):
        crack_time("")


@pytest.mark.parametrize("rate", [0, -1])
def test_nonpositive_guess_rate(rate):
    with pytest.raises(ValueError, match="must be positive"):
        crack_time("1234", guesses_per_second=rate)


@pytest.mark.parametrize("rate", [True, 1.5, "100"])
def test_noninteger_guess_rate(rate):
    with pytest.raises(TypeError, match="must be an integer"):
        crack_time("1234", guesses_per_second=rate)


def test_nonstring_password():
    with pytest.raises(TypeError, match="must be a string"):
        crack_time(1234)
