from flask import request

from api.responses import make_response
from api.validators import validate_frequency_payload
from repository.radioDevices import get_device, save_device, insert_device
import numbers


def register_device_routes(app):
    @app.route("/devices", methods=["POST"])
    def create_device():
        data = request.get_json(silent=True) or {}
        frequency = data.get("frequency", 2400)
        power = data.get("power", 10)

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

        if not isinstance(data, dict):
            return make_response(
                False,
                "Request body must be JSON object",
                error_code="INVALID_BODY",
                status=400,
            )

        power = data.get("power")
        if power is None:
            return make_response(
                False,
                "Field 'power' is required",
                error_code="MISSING_POWER",
                status=400,
            )

        if not isinstance(power, numbers.Real):
            return make_response(
                False,
                "Field 'power' must be a number",
                error_code="INVALID_TYPE",
                status=400,
            )

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
