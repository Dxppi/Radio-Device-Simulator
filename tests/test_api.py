import pytest

from api.settings import DEFAULT_FREQUENCY, DEFAULT_POWER, MAX_FREQ, MIN_FREQ


def assert_common_response(
    response, expected_status, expected_success, expected_message, error_code=None
):
    assert response.status_code == expected_status
    data = response.get_json()
    assert data["success"] is expected_success
    assert data["message"] == expected_message
    if error_code is not None:
        assert data["error_code"] == error_code


def test_create_device_defaults(client):
    response = client.post("/devices", json={})
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["frequency"] == DEFAULT_FREQUENCY
    assert data["data"]["power"] == DEFAULT_POWER


def test_create_device_invalid_body(client):
    response = client.post("/devices", json=["bad"])
    assert_common_response(
        response, 400, False, "Request body must be JSON object", "INVALID_BODY"
    )


def test_create_device_invalid_frequency(client):
    response = client.post("/devices", json={"frequency": MIN_FREQ - 1, "power": 10})
    assert_common_response(
        response,
        400,
        False,
        f"Frequency must be between {MIN_FREQ} and {MAX_FREQ} MHz",
        "INVALID_FREQUENCY",
    )


def test_create_device_invalid_power(client):
    response = client.post("/devices", json={"frequency": 2400, "power": "loud"})
    assert_common_response(
        response, 400, False, "Field 'power' must be a number", "INVALID_TYPE"
    )


@pytest.mark.parametrize(
    "frequency, expected_status, expected_success, expected_message",
    [
        (MIN_FREQ, 200, True, f"Frequency set to {MIN_FREQ} MHz"),
        (MAX_FREQ, 200, True, f"Frequency set to {MAX_FREQ} MHz"),
        (
            MIN_FREQ - 1,
            400,
            False,
            f"Frequency must be between {MIN_FREQ} and {MAX_FREQ} MHz",
        ),
        (
            MAX_FREQ + 1,
            400,
            False,
            f"Frequency must be between {MIN_FREQ} and {MAX_FREQ} MHz",
        ),
    ],
)
def test_set_frequency_boundaries(
    client,
    connected_device,
    frequency,
    expected_status,
    expected_success,
    expected_message,
):
    device_id = connected_device
    response = client.post(
        f"/devices/{device_id}/set_frequency",
        json={"frequency": frequency},
    )
    assert_common_response(
        response, expected_status, expected_success, expected_message
    )


def test_set_frequency_requires_body(client, connected_device):
    response = client.post(f"/devices/{connected_device}/set_frequency")
    assert_common_response(
        response, 400, False, "Request body must be JSON object", "INVALID_BODY"
    )


def test_set_frequency_requires_connected(client):
    response = client.post("/devices", json={"frequency": 2400, "power": 10})
    device_id = response.get_json()["data"]["device_id"]
    response = client.post(
        f"/devices/{device_id}/set_frequency", json={"frequency": 2500}
    )
    assert_common_response(
        response, 409, False, "Device is not connected", "NOT_CONNECTED"
    )


def test_set_power_success(client):
    response = client.post("/devices", json={"frequency": 2400, "power": 10})
    device_id = response.get_json()["data"]["device_id"]
    response = client.post(f"/devices/{device_id}/set_power", json={"power": 5.5})
    assert_common_response(response, 200, True, "Power set to 5.5")


def test_measure_signal_requires_connected(client):
    response = client.post("/devices", json={"frequency": 2400, "power": 10})
    device_id = response.get_json()["data"]["device_id"]
    response = client.post(f"/devices/{device_id}/measure_signal")
    assert_common_response(
        response, 409, False, "Device is not connected", "NOT_CONNECTED"
    )


def test_devices_list(client):
    response = client.get("/devices")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["items"] == []

    r1 = client.post("/devices", json={"frequency": 2400, "power": 10})
    r2 = client.post("/devices", json={"frequency": 2500, "power": 5})
    id1 = r1.get_json()["data"]["device_id"]
    id2 = r2.get_json()["data"]["device_id"]

    response = client.get("/devices")
    data = response.get_json()
    items = data["data"]["items"]
    assert [item["device_id"] for item in items] == [id1, id2]


def test_delete_device(client):
    response = client.post("/devices", json={"frequency": 2400, "power": 10})
    device_id = response.get_json()["data"]["device_id"]

    response = client.delete(f"/devices/{device_id}")
    assert_common_response(response, 200, True, "Device deleted")

    response = client.delete(f"/devices/{device_id}")
    assert_common_response(response, 404, False, "Device not found", "NOT_FOUND")
