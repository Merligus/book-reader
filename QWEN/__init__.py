# flask libs to serve
from flask import Flask, request
from flask_session import Session
from flask_cors import CORS

# llm lib
from QWEN.QWEN import QWEN

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

# load llm model
qwen_model = QWEN(debug=False)


# ******************************************
# endpoint
# ******************************************
@app.route("/", methods=["POST", "GET"])
def llm():
    # check if text is valid
    result = {}
    if "text" in request.json:
        result = qwen_model(request.json["text"])
        
    json = {}
    for key in result:
        json[key] = result[key]

    print(json)
    return json


if __name__ == "__main__":
    app.run(debug=False)
