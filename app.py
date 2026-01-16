from flask import Flask

from api.devices_routes import register_device_routes

application = Flask(__name__)


@application.route("/")
def welcome():
    return "Welcome to the RadioApi!"


register_device_routes(application)

if __name__ == "__main__":
    application.run(debug=True)
