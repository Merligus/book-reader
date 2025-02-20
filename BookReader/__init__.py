# flask libs to serve
from flask import Flask, request, jsonify
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
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # Get image file from request
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    # Direct access to binary data
    img_bytes = file.read()

    json = {}
    # ocr
    start_t = time.time()
    ocr_response = requests.post("http://localhost:7861/", files={"image": img_bytes})
    end_t = time.time()
    print(f"ocr took {end_t - start_t:.0f} s")
    ocr_json = ocr_response.json()
    print(ocr_json)

    # create body to send to qwen
    body = {"text": ocr_json["text"]}
    start_t = time.time()
    qwen_response = requests.post("http://localhost:7862/", json=body)
    end_t = time.time()
    print(f"qwen took {end_t - start_t:.0f} s")
    qwen_json = qwen_response.json()
    print(qwen_json)

    # create body to send to sdxl
    body = {"image_description": qwen_json["image_description"]}
    start_t = time.time()
    sdxl_response = requests.post("http://localhost:7863/", json=body)
    end_t = time.time()
    print(f"sdxl took {end_t - start_t:.0f} s")
    sdxl_json = sdxl_response.json()
    print(sdxl_json)

    json["image_path"] = sdxl_json["image_path"]
    json["summary"] = qwen_json["summary"]

    return json


if __name__ == "__main__":
    app.run(debug=False)
