from flask import Flask, jsonify
from app.airthings import get_access_token, get_airthings_data, process_sensor_data
# from broadlink import decide_action_and_control
app = Flask(__name__)

access_token = get_access_token()


@app.route('/get_data', methods=['GET'])
def get_data():
    if access_token:
        # Fetch data from Airthings API
        airthings_data = get_airthings_data(access_token)['data']
        if airthings_data:
            suggestions = process_sensor_data(airthings_data)
            print("Airthings Data:", airthings_data)
            return jsonify({'data': airthings_data, 'suggestions': suggestions})
        else:
            print("Failed to retrieve Airthings data")
            return "Failed to retrieve Airthings data"
    else:
        print("Failed to retrieve access token")
        return "Failed to retrieve access token"

    # Decide action and control Broadlink device
    # decide_action_and_control(airthings_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
