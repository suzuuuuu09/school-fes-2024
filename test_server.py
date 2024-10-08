from flask import *
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("data/test.json") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=8888)