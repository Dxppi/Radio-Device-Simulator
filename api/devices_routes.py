from flask import request

from api.responses import make_response
from api.settings import DEFAULT_FREQUENCY, DEFAULT_POWER
from api.validators import (
    normalize_json_body,
    validate_frequency_payload,
    validate_power_payload,
)
from repository.radioDevices import (
    delete_device,
    get_device,
    insert_device,
    list_devices,
    save_device,
)


def register_device_routes(app):
    @app.route("/devices", methods=["POST"])
    def create_device():
        data = request.get_json(silent=True)
        ok, value_or_msg, error_code = normalize_json_body(data, allow_empty=True)
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        data = value_or_msg

        frequency = data.get("frequency", DEFAULT_FREQUENCY)
        power = data.get("power", DEFAULT_POWER)

        ok, value_or_msg, error_code = validate_frequency_payload(
            {"frequency": frequency}
        )
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        ok, value_or_msg, error_code = validate_power_payload({"power": power})
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        device_id = insert_device(frequency, power)

        return make_response(
            True,
            "Device created",
            data={"device_id": device_id, "frequency": frequency, "power": power},
            status=201,
        )

    @app.route("/devices/<int:device_id>/set_frequency", methods=["POST"])
    def set_frequency(device_id):
        data = request.get_json(silent=True)

        ok, value_or_msg, error_code = normalize_json_body(data)
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        data = value_or_msg
        ok, value_or_msg, error_code = validate_frequency_payload(data)
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        freq = value_or_msg

        device = get_device(device_id)
        if device is None:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )

        if not device.is_connected:
            return make_response(
                False,
                "Device is not connected",
                error_code="NOT_CONNECTED",
                status=409,
            )

        device.set_frequency(freq)
        save_device(device)

        return make_response(
            True,
            f"Frequency set to {freq} MHz",
            data={"device_id": device.id, "frequency": device.frequency},
            status=200,
        )

    @app.route("/devices/<int:device_id>/connect", methods=["POST"])
    def connect_device(device_id):
        device = get_device(device_id)
        if device is None:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )

        device.connect()
        save_device(device)

        return make_response(
            True,
            "Device connected",
            data={"device_id": device.id, "is_connected": device.is_connected},
            status=200,
        )

    @app.route("/devices/<int:device_id>/disconnect", methods=["POST"])
    def disconnect_device(device_id):
        device = get_device(device_id)
        if device is None:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )

        device.disconnect()
        save_device(device)

        return make_response(
            True,
            "Device disconnected",
            data={"device_id": device.id, "is_connected": device.is_connected},
            status=200,
        )

    @app.route("/devices/<int:device_id>/set_power", methods=["POST"])
    def set_power(device_id):
        data = request.get_json(silent=True)

        ok, value_or_msg, error_code = normalize_json_body(data)
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        data = value_or_msg
        ok, value_or_msg, error_code = validate_power_payload(data)
        if not ok:
            return make_response(False, value_or_msg, error_code=error_code, status=400)

        power = value_or_msg

        device = get_device(device_id)
        if device is None:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )

        device.set_power(power)
        save_device(device)

        return make_response(
            True,
            f"Power set to {power}",
            data={"device_id": device.id, "power": device.power},
            status=200,
        )

    @app.route("/devices/<int:device_id>/measure_signal", methods=["POST"])
    def measure_signal(device_id):
        device = get_device(device_id)
        if device is None:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )

        if not device.is_connected:
            return make_response(
                False,
                "Device is not connected",
                error_code="NOT_CONNECTED",
                status=409,
            )

        device.measure_signal()
        save_device(device)

        return make_response(
            True,
            "Signal measured",
            data={
                "device_id": device.id,
                "last_measurement": (
                    device.last_measurement.isoformat()
                    if device.last_measurement
                    else None
                ),
            },
            status=200,
        )

    @app.route("/devices/<int:device_id>/status", methods=["GET"])
    def device_status(device_id):
        device = get_device(device_id)
        if device is None:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )

        return make_response(
            True,
            "Device status",
            data={
                "device_id": device.id,
                "frequency": device.frequency,
                "power": device.power,
                "is_connected": device.is_connected,
                "last_measurement": (
                    device.last_measurement.isoformat()
                    if device.last_measurement
                    else None
                ),
            },
            status=200,
        )

    @app.route("/devices", methods=["GET"])
    def devices_list():
        devices = list_devices()
        return make_response(
            True,
            "Devices list",
            data={
                "items": [
                    {
                        "device_id": device.id,
                        "frequency": device.frequency,
                        "power": device.power,
                        "is_connected": device.is_connected,
                        "last_measurement": (
                            device.last_measurement.isoformat()
                            if device.last_measurement
                            else None
                        ),
                    }
                    for device in devices
                ]
            },
            status=200,
        )

    @app.route("/devices/<int:device_id>", methods=["DELETE"])
    def device_delete(device_id):
        deleted = delete_device(device_id)
        if not deleted:
            return make_response(
                False,
                "Device not found",
                error_code="NOT_FOUND",
                status=404,
            )
        return make_response(
            True,
            "Device deleted",
            data={"device_id": device_id},
            status=200,
        )
