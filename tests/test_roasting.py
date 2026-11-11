import pytest

from password_roaster import roast_password
from password_roaster.roasting import BLANK_ROASTS, LEVELS, ROASTS


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password', ['', ' ', ' \t\n'])
def test_blank_input(password, level):
    assert roast_password(password, level) == BLANK_ROASTS[level]


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password, index', [
    ('password', 0), ('P@ssword2026!', 0), ('0000', 0),
    ('a', 1), ('abcabcabcabc', 1), ('Go7!', 1),
    ('sillygoose', 2), ('Velvet7!', 2),
    ('VelvetOtter7!', 3),
    ('VelvetOtter7!Moonrise', 4),
])
def test_roast_matches_score(password, index, level):
    assert roast_password(password, level) == ROASTS[level][index][1]


@pytest.mark.parametrize('password', ['', 'password', 'Go7!', 'VelvetOtter7!Moonrise'])
def test_default_level_is_mild(password):
    assert roast_password(password) == roast_password(password, 'mild')


def test_every_level_has_its_own_lines():
    seen = set()
    for level in LEVELS:
        assert len(ROASTS[level]) == 5
        assert ROASTS[level][-1][0] == 100
        for limit, roast in ROASTS[level]:
            assert roast not in seen
            seen.add(roast)
        assert BLANK_ROASTS[level] not in seen
        seen.add(BLANK_ROASTS[level])


def test_ceilings_go_up_inside_each_level():
    for level in LEVELS:
        last = -1
        for limit, roast in ROASTS[level]:
            assert limit > last
            last = limit


def test_weaker_password_gets_harsher_roast():
    for level in LEVELS:
        assert roast_password('password', level) != roast_password('VelvetOtter7!Moonrise', level)


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password', ['sillygoose', 'VelvetOtter7!', 'Go7!'])
def test_roast_never_repeats_password(password, level):
    roast = roast_password(password, level)
    assert isinstance(roast, str)
    assert password not in roast


@pytest.mark.parametrize('password', [None, 42, True, b'secret', []])
def test_invalid_password(password):
    with pytest.raises(TypeError, match='password must be a string'):
        roast_password(password)


@pytest.mark.parametrize('level', ['hot', 'Mild', '', 'extra savage'])
def test_unknown_level(level):
    with pytest.raises(ValueError, match='level must be one of'):
        roast_password('sillygoose', level)


@pytest.mark.parametrize('level', [None, 1, True, ['mild']])
def test_non_string_level(level):
    with pytest.raises(TypeError, match='level must be a string'):
        roast_password('sillygoose', level)


def test_bad_password_checked_before_level():
    with pytest.raises(TypeError, match='password must be a string'):
        roast_password(None, 'hot')
