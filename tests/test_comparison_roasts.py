from unittest.mock import patch

import pytest

from password_roaster import compare_passwords, roast_password


@pytest.mark.parametrize('first, second', [
    ('VelvetOtter7!', 'Go7!'),
    ('Go7!', 'VelvetOtter7!'),
    ('Go7!', 'Hi8?'),
    ('', ' \t\n'),
    ('PASSWORD', 'password'),
    ('密碼７!', 'VelvetOtter7!'),
])
def test_optional_roasts_preserve_scores_and_winner(first, second):
    plain = compare_passwords(first, second)
    assert compare_passwords(first, second, roast=False) == plain
    roasted = compare_passwords(first, second, roast=True)
    assert {key: roasted[key] for key in plain} == plain
    assert set(roasted) == set(plain) | {'first_roast', 'second_roast'}
    assert roasted['first_roast'] == roast_password(first)
    assert roasted['second_roast'] == roast_password(second)


def test_default_and_false_do_not_generate_roasts():
    with patch('password_roaster.comparison.roast_password') as make_roast:
        assert compare_passwords('Go7!', 'Hi8?') == {
            'first_score': 30, 'second_score': 30, 'winner': 'tie',
        }
        assert compare_passwords('Go7!', 'Hi8?', roast=False) == {
            'first_score': 30, 'second_score': 30, 'winner': 'tie',
        }
        make_roast.assert_not_called()


@pytest.mark.parametrize('value', [None, 0, 1, '', 'false', [], {}])
def test_roast_requires_bool(value):
    with pytest.raises(TypeError, match='roast must be a bool'):
        compare_passwords('Go7!', 'Hi8?', roast=value)


@pytest.mark.parametrize('value', [None, 42, True, b'secret', [], {}])
@pytest.mark.parametrize('position', ['first', 'second'])
def test_roast_mode_rejects_invalid_passwords(value, position):
    first, second = 'Go7!', 'Hi8?'
    if position == 'first':
        first = value
    else:
        second = value
    with pytest.raises(TypeError, match='password must be a string'):
        compare_passwords(first, second, roast=True)


def test_roasted_result_does_not_expose_passwords(capsys):
    first, second = 'FictionalOtter7!', 'MadeUpRaven8?'
    result = compare_passwords(first, second, roast=True)
    assert first not in str(result)
    assert second not in str(result)
    captured = capsys.readouterr()
    assert captured.out == captured.err == ''
