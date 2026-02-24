import pytest

@pytest.mark.regression
def test_api_basic():
    assert 200 == 200