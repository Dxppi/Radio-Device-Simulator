import numbers
from api.settings import MIN_FREQ, MAX_FREQ


def validate_frequency_payload(data):
    if not isinstance(data, dict):
        return False, "Request body must be JSON object", "INVALID_BODY"

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
