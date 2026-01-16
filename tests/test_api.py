import pytest

@pytest.mark.parametrize(
    "frequency, expected_status, expected_success, expected_message",
    [
        (800, 200, True,  "Frequency set to 800 MHz"),
        (6000, 200, True, "Frequency set to 6000 MHz"),
        (799, 400, False, "Frequency must be between 800 and 6000 MHz"),
        (6001, 400, False, "Frequency must be between 800 and 6000 MHz"),
    ],
)
def test_set_frequency_boundaries(client, frequency, expected_status, expected_success, expected_message):
    response = client.post("devices/1/set_frequency", json={"frequency": frequency})
    assert response.status_code == expected_status

    data = response.get_json()
    assert data["success"] is expected_success
    assert data["message"] == expected_message
