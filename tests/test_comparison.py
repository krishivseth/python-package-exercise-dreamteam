import pytest

from password_roaster import compare_passwords


@pytest.mark.parametrize('first, second, expected', [
    ('VelvetOtter7!', 'Go7!', {'first_score': 79, 'second_score': 30, 'winner': 'first'}),
    ('Go7!', 'VelvetOtter7!', {'first_score': 30, 'second_score': 79, 'winner': 'second'}),
    ('Go7!', 'Go7!', {'first_score': 30, 'second_score': 30, 'winner': 'tie'}),
    ('Go7!', 'Hi8?', {'first_score': 30, 'second_score': 30, 'winner': 'tie'}),
    ('', '', {'first_score': 0, 'second_score': 0, 'winner': 'tie'}),
    ('', 'Go7!', {'first_score': 0, 'second_score': 30, 'winner': 'second'}),
    ('password', 'PASSWORD', {'first_score': 10, 'second_score': 10, 'winner': 'tie'}),
])
def test_comparison(first, second, expected):
    assert compare_passwords(first, second) == expected


@pytest.mark.parametrize('value', [None, 42, True, b'secret', [], {}])
@pytest.mark.parametrize('position', ['first', 'second'])
def test_invalid_input(value, position):
    first, second = 'Go7!', 'Hi8?'
    if position == 'first':
        first = value
    else:
        second = value
    with pytest.raises(TypeError, match='password must be a string'):
        compare_passwords(first, second)


def test_comparison_does_not_expose_passwords(capsys):
    first, second = 'FictionalOtter7!', 'MadeUpRaven8?'
    result = compare_passwords(first, second)
    assert first not in str(result)
    assert second not in str(result)
    captured = capsys.readouterr()
    assert captured.out == captured.err == ''
