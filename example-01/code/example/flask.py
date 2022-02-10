from flask import Flask, request

app = Flask(__name__)

@app.route("/welcome", methods=["GET"])
def action_list():
    return "Hello!"

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)