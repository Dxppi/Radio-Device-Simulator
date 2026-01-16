from flask import Flask

from api.devices_routes import register_device_routes

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to the RadioApi!"


register_device_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
