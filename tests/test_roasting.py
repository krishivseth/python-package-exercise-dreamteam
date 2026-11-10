import pytest

from password_roaster import roast_password
from password_roaster.roasting import BLANK_ROAST, ROASTS, STRONG_ROAST


@pytest.mark.parametrize('password', ['', ' ', ' \t\n'])
def test_blank_input(password):
    assert roast_password(password) == BLANK_ROAST


@pytest.mark.parametrize('password, index', [
    ('password', 0), ('P@ssword2026!', 0), ('0000', 0),
    ('a', 1), ('abcabcabcabc', 1), ('Go7!', 1),
    ('sillygoose', 2), ('Velvet7!', 2),
    ('VelvetOtter7!', 3),
])
def test_roast_matches_score(password, index):
    assert roast_password(password) == ROASTS[index][1]


def test_strong_password():
    assert roast_password('VelvetOtter7!Moonrise') == STRONG_ROAST


def test_weaker_password_gets_harsher_roast():
    assert roast_password('password') != roast_password('VelvetOtter7!Moonrise')


@pytest.mark.parametrize('password', ['sillygoose', 'VelvetOtter7!', 'Go7!'])
def test_roast_never_repeats_password(password):
    roast = roast_password(password)
    assert isinstance(roast, str)
    assert password not in roast


@pytest.mark.parametrize('password', [None, 42, True, b'secret', []])
def test_invalid_input(password):
    with pytest.raises(TypeError, match='password must be a string'):
        roast_password(password)
