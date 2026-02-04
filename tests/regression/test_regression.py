import pytest

@pytest.mark.regression
def test_regression_basic():
    assert 2 * 2 == 4
    assert 3 + 5 == 8
    assert 10 - 4 ==6
    