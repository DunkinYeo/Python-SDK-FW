import pytest

@pytest.mark.regression
def test_regression_basic():
    assert 2 * 2 == 4