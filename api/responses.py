from flask import jsonify


def make_response(success: bool, message: str, data=None, error_code=None, status=200):
    body = {"success": success, "message": message}
    if data is not None:
        body["data"] = data
    if error_code is not None:
        body["error_code"] = error_code
    return jsonify(body), status
