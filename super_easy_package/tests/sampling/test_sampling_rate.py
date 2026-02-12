import pytest
from tests.sampling.sampling_utils import get_supported_sampling_rates


@pytest.mark.sampling
@pytest.mark.parametrize(
    "fw_version, expected_rates",
    [
        ("1.7.6", [256]),
        ("2.1.2", [256]),
        ("2.2.4", [256]),
        ("2.2.6", [256]),
        ("2.3.5", [128]),
        ("2.4.6", [128,256])
    ]
)
def test_sampling_by_fw(app_env, fw_version, expected_rates):
    app_env["fw_version"] = fw_version

    actual_rates = get_supported_sampling_rates(app_env)

    assert actual_rates == expected_rates, (
        f"Sampling mismatch | "
        f"fw={fw_version}, "
        f"expected={expected_rates}, "
        f"actual={actual_rates}"
    )