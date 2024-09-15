from flask import *
import json

with open("test.json") as f:
    data = json.load(f)

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=8888)