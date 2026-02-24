import pytest
from tests.appium.driver import get_driver


@pytest.fixture(scope='module')
def driver():
    d = get_driver()
    yield d
    try:
        d.quit()
    except Exception:
        pass


def test_app_launch(driver):
    # Basic smoke test: verify a session was created
    assert driver.session_id is not None
