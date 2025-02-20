# flask libs to serve
from flask import Flask, request, jsonify
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
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # Direct access to binary data
    file = request.files['image']
    img_bytes = file.read()
    
    # check if image is valid to analyse
    json = {}
    json["text"] = ocr_model(img_bytes)

    return json


if __name__ == "__main__":
    app.run(debug=False)
