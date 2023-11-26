from flask import Flask, jsonify, request
from controller import Controller
from dotenv import load_dotenv
import os

app = Flask(__name__)
ctr = Controller()
# .env 파일 로드
load_dotenv()
id = os.getenv("ID")
api_key = os.getenv("API_KEY")

@app.route('/operator_input', methods=['POST'])
def operator_input():
    data = request.get_json()
    
    map_input = data["map_input"]
    start_input = data["start_input"]
    spot_input = data["spot_input"]
    color_input = data["color_input"]
    hazard_input = data["hazard_input"]

    ret = ctr.operator_input(map_input, start_input, spot_input, color_input, hazard_input)
    return jsonify(ret)

@app.route('/voice_recognization', methods=['POST'])
def voice_recognization():
    print(ctr.add_on.get_map_info())
    data = request.get_json()

    ret = ctr.voice_recognization(id, api_key)
    return ret
    
if __name__ == '__main__':
    app.run(debug=True)
