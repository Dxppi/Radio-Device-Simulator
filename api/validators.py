import numbers
from api.settings import MIN_FREQ, MAX_FREQ


def normalize_json_body(data, allow_empty: bool = False):
    if data is None and allow_empty:
        return True, {}, None
    if not isinstance(data, dict):
        return False, "Request body must be JSON object", "INVALID_BODY"
    return True, data, None


def validate_frequency_payload(data):
    freq = data.get("frequency")
    if freq is None:
        return False, "Field 'frequency' is required", "MISSING_FREQUENCY"

    if not isinstance(freq, numbers.Real):
        return False, "Field 'frequency' must be a number", "INVALID_TYPE"

    if not (MIN_FREQ <= freq <= MAX_FREQ):
        return (
            False,
            f"Frequency must be between {MIN_FREQ} and {MAX_FREQ} MHz",
            "INVALID_FREQUENCY",
        )

    return True, freq, None


def validate_power_payload(data):
    power = data.get("power")
    if power is None:
        return False, "Field 'power' is required", "MISSING_POWER"

    if not isinstance(power, numbers.Real):
        return False, "Field 'power' must be a number", "INVALID_TYPE"

    return True, power, None
