# flask libs to serve
from flask import Flask, request
from flask_session import Session
from flask_cors import CORS

# sdxl lib
from Lora.SDXL import SDXL

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

# load sdxl model
sdxl_model = SDXL(debug=True)


# ******************************************
# endpoint
# ******************************************
@app.route("/", methods=["POST", "GET"])
def sdxl():
    # check if image is valid to analyse
    json = {}
    if "image_description" in request.json:
        json["image_path"] = sdxl_model(request.json["image_description"])

    print(json)
    return json


if __name__ == "__main__":
    app.run(debug=False)
