
# from controller import Controller
# controller = Controller()
# controller.run()
from flask import Flask, jsonify, request
from controller import Controller

app = Flask(__name__)

@app.route('/operator_input', methods=['POST'])
def operator_input():
    data = request.get_json()
    
    map_input = data["map_input"]
    start_input = data["start_input"]
    spot_input = data["spot_input"]
    color_input = data["color_input"]
    hazard_input = data["hazard_input"]

    ret = Controller.operator_input(map_input, start_input, spot_input, color_input, hazard_input)
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True)
