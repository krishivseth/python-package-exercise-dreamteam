import pytest

from password_roaster import roast_password
from password_roaster.roasting import LEVELS, LONG_LENGTH, ROASTS, SPECIAL_ROASTS


LONG_PASSWORD = 'VelvetOtter7!Moonrise' * 4


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password', ['', ' ', ' \t\n'])
def test_blank_input(password, level):
    assert roast_password(password, level) == SPECIAL_ROASTS[level]['blank']


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password', ['password', 'PASSWORD', 'P@ssword2026!', 'qwerty123', ' letmein '])
def test_common_password(password, level):
    assert roast_password(password, level) == SPECIAL_ROASTS[level]['common']


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password', ['aa', 'zzzzzzzz', '!!!!', '0000', 'x' * 70])
def test_single_repeated_character(password, level):
    assert roast_password(password, level) == SPECIAL_ROASTS[level]['repeat']


@pytest.mark.parametrize('level', LEVELS)
def test_long_password(level):
    assert len(LONG_PASSWORD) > LONG_LENGTH
    assert roast_password(LONG_PASSWORD, level) == SPECIAL_ROASTS[level]['long']


def test_long_cutoff_is_exclusive():
    password = ('VelvetOtter7!Moonrise' * 4)[:LONG_LENGTH]
    assert roast_password(password) != SPECIAL_ROASTS['mild']['long']
    assert roast_password(password + 'Q') == SPECIAL_ROASTS['mild']['long']


def test_single_character_is_not_a_repeat():
    assert roast_password('a') == ROASTS['mild'][1][1]


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password, index', [
    ('abcd', 0), ('qwer', 0), ('abab', 0),
    ('a', 1), ('abcabcabcabc', 1), ('Go7!', 1),
    ('sillygoose', 2), ('Velvet7!', 2), ('Tr0ub4dor&3', 2),
    ('VelvetOtter7!', 3),
    ('VelvetOtter7!Moonrise', 4),
])
def test_roast_matches_score(password, index, level):
    assert roast_password(password, level) == ROASTS[level][index][1]


@pytest.mark.parametrize('password', ['', 'password', 'Go7!', 'VelvetOtter7!Moonrise'])
def test_default_level_is_mild(password):
    assert roast_password(password) == roast_password(password, 'mild')


@pytest.mark.parametrize('level', ['Spicy', 'SPICY', ' spicy ', '\tspicy\n'])
def test_level_ignores_case_and_spaces(level):
    assert roast_password('sillygoose', level) == roast_password('sillygoose', 'spicy')


def test_every_level_has_its_own_lines():
    seen = set()
    for level in LEVELS:
        assert len(ROASTS[level]) == 5
        assert ROASTS[level][-1][0] == 100
        assert set(SPECIAL_ROASTS[level]) == {'blank', 'common', 'repeat', 'long'}
        for limit, roast in ROASTS[level]:
            assert roast not in seen
            seen.add(roast)
        for case, roast in SPECIAL_ROASTS[level].items():
            assert roast not in seen
            seen.add(roast)


def test_ceilings_go_up_inside_each_level():
    for level in LEVELS:
        last = -1
        for limit, roast in ROASTS[level]:
            assert limit > last
            last = limit


def test_weaker_password_gets_harsher_roast():
    for level in LEVELS:
        assert roast_password('abcd', level) != roast_password('VelvetOtter7!Moonrise', level)


@pytest.mark.parametrize('level', LEVELS)
@pytest.mark.parametrize('password', ['sillygoose', 'VelvetOtter7!', 'Go7!', 'letmein', 'zzzz', LONG_PASSWORD])
def test_roast_never_repeats_password(password, level):
    roast = roast_password(password, level)
    assert isinstance(roast, str)
    assert password not in roast


@pytest.mark.parametrize('password', [None, 42, True, b'secret', []])
def test_invalid_password(password):
    with pytest.raises(TypeError, match='password must be a string'):
        roast_password(password)


@pytest.mark.parametrize('level', ['hot', '', '   ', 'extra savage', 'mi ld'])
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
