import pytest

from password_roaster import score_password
from password_roaster.scoring import _has_repetition, _has_sequence, _is_common


@pytest.mark.parametrize('password, expected', [
    ('', 0), (' \t\n', 0), ('a', 13), ('Go7!', 30),
    ('Velvet7', 30), ('Velvet7!', 60), ('VelvetMoon7', 60),
    ('VelvetOtter7!', 79), ('VelvetOtter7!Moonrise', 100),
    ('sillygoose', 40), ('password', 10), ('P@ssword2026!', 10),
    ('abcabcabcabc', 21), ('Z9!abcdefghijk', 62),
    ('aaaaaaaa', 9), ('0000', 0),
])
def test_scores(password, expected):
    assert score_password(password) == expected


@pytest.mark.parametrize('password', ['VelvetOtter7!', 'Go7!', 'sillygoose'])
def test_spaces_do_not_earn_length_or_symbol_points(password):
    assert score_password(' ' + password + ' ') == score_password(password)


@pytest.mark.parametrize('password', [None, 42, True, b'secret', [], {}])
def test_invalid_input(password):
    with pytest.raises(TypeError, match='password must be a string'):
        score_password(password)


@pytest.mark.parametrize('password, expected', [
    ('password', True), ('PASSWORD', True), ('P@ssword2026!', True),
    (' pa$$word99! ', True), ('123456', True), ('welcome!!', True),
    ('VelvetOtter7!', False), ('passwordsandwich', False), ('', False),
])
def test_common_password_detection(password, expected):
    assert _is_common(password) is expected


@pytest.mark.parametrize('password, expected', [
    ('abcd', True), ('DCBA', True), ('safe4567!', True),
    ('QWERT', True), ('lkjh', True), ('7890', True),
    ('abc', False), ('VelvetOtter7!', False), ('', False),
])
def test_sequence_detection(password, expected):
    assert _has_sequence(password) is expected


@pytest.mark.parametrize('password, expected', [
    ('aaa', True), ('safeXXX7!', True), ('abABab', True),
    ('xyzxyz', True), ('aa', True), ('a', False), ('', False),
    ('VelvetOtter7!', False), ('ababX', False),
])
def test_repetition_detection(password, expected):
    assert _has_repetition(password) is expected


@pytest.mark.parametrize('password', [
    'a' * 200, 'VelvetOtter7!Moonrise' * 10, '🔒' * 100, '密碼７!',
])
def test_scores_stay_in_range(password):
    assert 0 <= score_password(password) <= 100


def test_character_variety_improves_score():
    assert score_password('velvetotter') < score_password('Velvetotter')
    assert score_password('Velvetotter') < score_password('Velvetotte7')
    assert score_password('VelvetOtter7!') > score_password('VelvetOtter7x')
