import pytest
from tests.sampling.sampling_utils import get_supported_sampling_rates


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--target-packets",
        action="store",
        default=None,
        type=int,
        help="Target packet count for long-term stability test (e.g., 3600 for 1 hour, 86400 for 1 day)"
    )


@pytest.fixture
def target_packets(request):
    """Get target packet count from command line option."""
    return request.config.getoption("--target-packets")


@pytest.fixture
def actual_sampling_rate(app_env):
    return get_actual_sampling_rate(app_env)


@pytest.fixture(scope="session")
def app_env():
    return {
        "platform": "Android",
        "app_version": "1.0.8",
        "fw_version": "2.2.6"
    }


@pytest.fixture(scope="function")
def sampling_rate():
    return
 