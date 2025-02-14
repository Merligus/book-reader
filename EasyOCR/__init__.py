# flask libs to serve
from flask import Flask, request
from flask_session import Session
from flask_cors import CORS

# analysis lib
from EasyOCR.OCR import OCR

# system libs
import os
import warnings

# system setting
warnings.filterwarnings("ignore")
if "flask_key" in os.environ:
    flask_key_str = os.environ["flask_key"]
else:
    flask_key_str = "flask_key_str"
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

# load analysis model
ocr_model = OCR(debug=False)


# ******************************************
# endpoint
# ******************************************
@app.route("/", methods=["POST", "GET"])
def analysis():
    # check if image is valid to analyse
    json = {}
    if "image" in request.json:
        json["text"] = ocr_model(request.json["image"])

    return json


if __name__ == "__main__":
    app.run(debug=False)
