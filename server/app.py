from flask import Flask, jsonify, request, json
from controller import Controller
from dotenv import load_dotenv
from flask_cors import CORS

import os

app = Flask(__name__)

cors_headers = {
    "origins": "http://localhost:3000",
}
CORS(app, resources={r"/operator-input": cors_headers})
CORS(app, resources={r"/voice-recognization": cors_headers})

ctr = Controller()
# .env 파일 로드
load_dotenv()
id = os.getenv("ID")
api_key = os.getenv("API_KEY")

@app.route('/operator-input', methods=['POST','OPTIONS'])
def operator_input():
    if request.method == 'OPTIONS':
        # OPTIONS 메서드 처리
        return "", 200

    elif request.method == 'POST':
        # POST 메서드 처리
        data = request.get_json()
        
        map_input = data["map_input"]
        start_input = data["start_input"]
        spot_input = data["spot_input"]
        color_input = data["color_input"]
        hazard_input = data["hazard_input"]

        ret = ctr.operator_input(map_input, start_input, spot_input, color_input, hazard_input)

        return jsonify(ret)

@app.route('/voice-recognization', methods=['POST'])
def voice_recognization():
    file_data = request.files
    file_stream = file_data.get('file').stream
    status_data = json.loads(request.form['newroad'])

    ret, err = ctr.voice_recognization(id, api_key, file_stream, status_data)
    if err is None:
        return jsonify({"ret": ret, "status": 0}), 200
    else :
        return jsonify({"ret": ret, "status": -1, "err" : err}), 200


if __name__ == '__main__':
    app.run(debug=True)
