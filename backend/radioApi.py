from flask import Flask, request, jsonify
import numbers
from settings import MAX_FREQ, MIN_FREQ

app = Flask(__name__)


def make_response(success: bool, message: str, data=None, error_code=None, status=200):
    body = {
        "success": success,
        "message": message,
    }
    if data is not None:
        body["data"] = data
    if error_code is not None:
        body["error_code"] = error_code
    return jsonify(body), status


@app.route("/")
def welcome():
    return "Welcome to the RadioApi!"


@app.route("/set_frequency", methods=["POST"])
def set_frequency():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return make_response(
            False,
            "Request body must be JSON object",
            error_code="INVALID_BODY",
            status=400,
        )

    freq = data.get("frequency")

    if freq is None:
        return make_response(
            False,
            "Field 'frequency' is required",
            error_code="MISSING_FREQUENCY",
            status=400,
        )

    if not isinstance(freq, numbers.Real):
        return make_response(
            False,
            "Field 'frequency' must be a number",
            error_code="INVALID_TYPE",
            status=400,
        )

    if not (MIN_FREQ <= freq <= MAX_FREQ):
        return make_response(
            False,
            f"Frequency must be between {MIN_FREQ} and {MAX_FREQ} MHz",
            error_code="INVALID_FREQUENCY",
            status=400,
        )
    return make_response(
        True,
        f"Frequency set to {freq} MHz",
        data={"frequency": freq},
        status=200,
    )


@app.route("/get_frequency")
def welcome2():
    return "get_frequency"


@app.route("/set_power")
def welcome3():
    return "set_power"


@app.route("/measure_signal")
def welcome4():
    return "measure_signal"


@app.route("/status")
def welcome5():
    return "status"


if __name__ == "__main__":
    app.run(debug=True)
