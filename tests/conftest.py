import pytest
from tests.sampling.sampling_utils import get_supported_sampling_rates

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

	# •	SDK 초기화	•	BLE 연결 / 해제
	# •	테스트용 계정
	# •	API 토큰 발급
	# •	Appium Driver 생성
	# •	FW / Sampling rate 설정
 