from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to the RadioApi!"


@app.route("/set_frequency", methods=["POST"])
def welcome1():
    return "set_frequency"


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
