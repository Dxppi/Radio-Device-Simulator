from flask import request

from api.responses import make_response
from api.validators import validate_frequency_payload
from repository.radioDevices import get_device, save_device, insert_device


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
