import pytest

from password_roaster import password_feedback


@pytest.mark.parametrize('password', ['', ' \t\n'])
def test_blank_input(password):
    assert password_feedback(password) == ['Enter a password.']


@pytest.mark.parametrize('password, tip', [
    ('P@ssword2026!', 'Avoid common passwords and simple changes to them.'),
    ('Go7!', 'Use at least 12 characters, not counting spaces.'),
    ('R7!T2?M9#K4%', 'Add a lowercase letter.'),
    ('r7!t2?m9#k4%', 'Add an uppercase letter.'),
    ('VelvetOtter!?', 'Add a number.'),
    ('VelvetOtter79', 'Add a symbol.'),
    ('abcabcabcabc', 'Avoid repeated characters or patterns.'),
    ('Z9!abcdefghijk', 'Avoid sequences like abcd, 1234, or qwerty.'),
])
def test_tips_match_weakness(password, tip):
    assert tip in password_feedback(password)


def test_multiple_tips():
    assert password_feedback('moss') == [
        'Use at least 12 characters, not counting spaces.',
        'Add an uppercase letter.',
        'Add a number.',
        'Add a symbol.',
    ]


def test_length_boundary():
    assert password_feedback('VelvetOttr7') == [
        'Use at least 12 characters, not counting spaces.', 'Add a symbol.',
    ]
    assert password_feedback('VelvetOttr7!') == ['No obvious weaknesses found.']


def test_spaces_do_not_count_as_length_or_symbols():
    assert password_feedback(' VelvetOtter7 ') == password_feedback('VelvetOtter7')


@pytest.mark.parametrize('password', [None, 42, True, b'secret', [], {}])
def test_invalid_input(password):
    with pytest.raises(TypeError, match='password must be a string'):
        password_feedback(password)


def test_feedback_does_not_expose_password(capsys):
    password = 'FictionalOtter7!'
    assert all(password not in tip for tip in password_feedback(password))
    captured = capsys.readouterr()
    assert captured.out == captured.err == ''
