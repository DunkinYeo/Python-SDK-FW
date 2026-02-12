def parse_version(version: str):
    return tuple(map(int, version.split(".")))


def get_supported_sampling_rates(app_env) -> list[int]:
    fw = parse_version(app_env["fw_version"])

    if fw >= (2, 2, 6):
        return [128, 256]
