# flask libs to serve
from flask import Flask, request
from flask_session import Session
from flask_cors import CORS

# system libs
import requests
import time
import os
import warnings

# system setting
warnings.filterwarnings("ignore")
flask_key_str = os.environ["flask_key"]

print(flask_key_str)

# flask setting
app = Flask(__name__)
SECRET_KEY = flask_key_str
SESSION_TYPE = "filesystem"
app.secret_key = SECRET_KEY
app.session_type = SESSION_TYPE
app.config.from_object(__name__)
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
Session(app)
CORS(app)


# ******************************************
# endpoint
# ******************************************
@app.route("/", methods=["POST", "GET"])
def book_reader():
    # check if image is valid to analyse skin
    json = {}
    if "image" in request.json:
        body = {"image": request.json["image"]}

        # age analysis
        start_t = time.time()
        ocr_response = requests.post("http://localhost:7861/", json=body)
        end_t = time.time()
        print(f"ocr took {end_t - start_t:.0f} s")

        ocr_json = ocr_response.json()
        for item in ocr_json:
            json[item] = ocr_json[item]

    print(json)
    return json


if __name__ == "__main__":
    app.run(debug=False)
