from flask import Flask, jsonify
from flask_cors import CORS
from GetOwlData import get_owl_data, get_owl_data_periodical, get_owl_data_periodical_last_updated, post_owl_data_new, delete_old_owl_data
from time import sleep
from threading import Lock

app = Flask(__name__)

DAYS = 15
DAYS_IMAGE = 10
DAYS_GARDEN = 30
DAYS_WEIGHT = 90
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "credentials": True}})

pump_lock = Lock()
picture_lock = Lock()

# BEEHIVE ONE

@app.route('/temperature_left')
def get_temperature_left():
    temperature_left = get_owl_data("kip_test_temperature_0", "temperature_0")
    return jsonify({"temperature": [temperature_left]})

@app.route('/temperature_left_periodical')
def get_temperature_left_periodical():
    temperature_left = get_owl_data_periodical("kip_test_temperature_0", "temperature_0", DAYS)
    return jsonify({"temperature_periodical": [temperature_left]})

@app.route('/temperature_middle')
def get_temperature_middle():
    temperature_middle = get_owl_data("kip_test_temperature_1", "temperature_1")
    return jsonify({"temperature": [temperature_middle]})

@app.route('/temperature_middle_periodical')
def get_temperature_middle_periodical():
    temperature_middle = get_owl_data_periodical("kip_test_temperature_1", "temperature_1", DAYS)
    return jsonify({"temperature_periodical": [temperature_middle]})

@app.route('/temperature_right')
def get_temperature_right():
    temperature_right = get_owl_data("kip_test_temperature_2", "temperature_2")
    return jsonify({"temperature": [temperature_right]})

@app.route('/temperature_right_periodical')
def get_temperature_right_periodical():
    temperature_right = get_owl_data_periodical("kip_test_temperature_2", "temperature_2", DAYS)
    return jsonify({"temperature_periodical": [temperature_right]})

@app.route('/weight')
def get_weight():
    weight = get_owl_data("kip_test_weight", "weight")
    return jsonify({"weight": [weight]})

@app.route('/weight_periodical')
def get_weight_periodical():
    weight = get_owl_data_periodical("kip_test_weight", "weight", DAYS_WEIGHT)
    return jsonify({"weight_periodical": [weight]})

@app.route('/humidity_internal')
def get_humidity_internal():
    humidity_internal = get_owl_data("kip_test_humidity_1", "humidity_1")
    return jsonify({"humidity_internal": [humidity_internal]})

@app.route('/humidity_internal_periodical')
def get_humidity_internal_periodical():
    humidity_internal = get_owl_data_periodical("kip_test_humidity_1", "humidity_1", DAYS)
    return jsonify({"humidity_internal_periodical": [humidity_internal]})

@app.route('/picture')
def get_picture():
    picture = get_owl_data("kip_test_picture", "picture")
    return jsonify({"picture": [picture]})

@app.route('/picture_periodical')
def get_picture_periodical():
    picture_periodical = get_owl_data_periodical_last_updated("kip_test_picture", "picture", DAYS_IMAGE)
    return jsonify({"picture_periodical": [picture_periodical]})

@app.route('/sound')
def get_sound():
    sound = get_owl_data("kip_test_sound", "sound")
    return jsonify({"sound": [sound]})

@app.route('/sound_anomaly')
def get_sound_anomaly():
    sound_anomaly = get_owl_data("kip_test_sound_anomaly", "anomaly")
    return jsonify({"sound_anomaly": [sound_anomaly]})

@app.route('/take_picture', methods=['POST'])
def take_picture():
    with picture_lock:  # Ensures isolation
        try:
            delete_old_owl_data("kip_test_take_picture", 0)
            post_owl_data_new("kip_test_take_picture", "status", "on")
            sleep(5)  
            delete_old_owl_data("kip_test_take_picture", 0)
            post_owl_data_new("kip_test_take_picture", "status", "off")
            return jsonify({"status": "Taking Picture"}), 200
        except Exception as e:
            # Rollback mechanism if an error occurs
            delete_old_owl_data("kip_test_take_picture", 0)
            post_owl_data_new("kip_test_take_picture", "status", "off")
            return jsonify({"status": "Failed to take picture", "error": str(e)}), 500

# BEEHIVE TWO

@app.route('/temperature_left_2')
def get_temperature_left_2():
    temperature_left = get_owl_data("kip_test_2_temperature_0", "temperature_0")
    return jsonify({"temperature": [temperature_left]})

@app.route('/temperature_left_2_periodical')
def get_temperature_left_2_periodical():
    temperature_left = get_owl_data_periodical("kip_test_2_temperature_0", "temperature_0", DAYS)
    return jsonify({"temperature_periodical": [temperature_left]})


@app.route('/temperature_middle_2')
def get_temperature_middle_2():
    temperature_middle = get_owl_data("kip_test_2_temperature_1", "temperature_1")
    return jsonify({"temperature": [temperature_middle]})

@app.route('/temperature_middle_2_periodical')
def get_temperature_middle_2_periodical():
    temperature_middle = get_owl_data_periodical("kip_test_2_temperature_1", "temperature_1", DAYS)
    return jsonify({"temperature_periodical": [temperature_middle]})

@app.route('/temperature_right_2')
def get_temperature_right_2():
    temperature_right = get_owl_data("kip_test_2_temperature_2", "temperature_2")
    return jsonify({"temperature": [temperature_right]})

@app.route('/temperature_right_2_periodical')
def get_temperature_right_2_periodical():
    temperature_right = get_owl_data_periodical("kip_test_2_temperature_2", "temperature_2", DAYS)
    return jsonify({"temperature_periodical": [temperature_right]})

@app.route('/weight_2')
def get_weight_2():
    weight = get_owl_data("kip_test_2_weight", "weight")
    return jsonify({"weight": [weight]})

@app.route('/weight_2_periodical')
def get_weight_2_periodical():
    weight = get_owl_data_periodical("kip_test_2_weight", "weight", DAYS_WEIGHT)
    return jsonify({"weight_periodical": [weight]})

@app.route('/humidity_internal_2')
def get_humidity_internal_2():
    humidity_internal = get_owl_data("kip_test_2_humidity_1", "humidity_1")
    return jsonify({"humidity_internal": [humidity_internal]})

@app.route('/humidity_internal_2_periodical')
def get_humidity_internal_2_periodical():
    humidity_internal = get_owl_data_periodical("kip_test_2_humidity_1", "humidity_1", DAYS)
    return jsonify({"humidity_internal_periodical": [humidity_internal]})

@app.route('/picture_2')
def get_picture_2():
    picture = get_owl_data("kip_test_2_picture", "picture")
    return jsonify({"picture": [picture]})

@app.route('/picture_2_periodical')
def get_picture_2_periodical():
    picture_periodical = get_owl_data_periodical_last_updated("kip_test_2_picture", "picture", DAYS_IMAGE)
    return jsonify({"picture_periodical": [picture_periodical]})

@app.route('/sound_2')
def get_sound_2():
    sound = get_owl_data("kip_test_2_sound", "sound")
    return jsonify({"sound": [sound]})

@app.route('/sound_anomaly_2')
def get_sound_2_anomaly():
    sound_anomaly = get_owl_data("kip_test_2_sound_anomaly", "anomaly")
    return jsonify({"sound_anomaly": [sound_anomaly]})

# Garden


@app.route('/garden_temperature')
def get_garden_temperature():
    temperature_water = get_owl_data("kip_greenhouse_temperature", "temperature")
    return jsonify({"temperature": [temperature_water]})

@app.route('/garden_temperature_periodical')
def get_garden_temperature_periodical():
    temperature_water = get_owl_data_periodical("kip_greenhouse_temperature", "temperature", DAYS_GARDEN)
    return jsonify({"temperature_periodical": [temperature_water]})

@app.route('/garden_humidity')
def get_garden_humidity():
    humidity_relative = get_owl_data("kip_greenhouse_humidity", "humidity")
    return jsonify({"humidity": [humidity_relative]})

@app.route('/garden_humidity_periodical')
def get_garden_humidity_periodical():
    humidity_relative = get_owl_data_periodical("kip_greenhouse_humidity", "humidity", DAYS_GARDEN)
    return jsonify({"humidity_periodical": [humidity_relative]})

@app.route('/garden_ph')
def get_garden_ph():
    ph = get_owl_data("kip_greenhouse_ph_level", "ph_level")
    return jsonify({"ph": [ph]})

@app.route('/garden_ph_periodical')
def get_garden_ph_periodical():
    ph = get_owl_data_periodical("kip_greenhouse_ph_level", "ph_level", DAYS_GARDEN)
    return jsonify({"ph_periodical": [ph]})

@app.route('/garden_conductivity')
def get_garden_electrical_conductivity():
    conductivity = get_owl_data("kip_greenhouse_electrical_conductivity", "electrical_conductivity")
    return jsonify({"conductivity": [conductivity]})

@app.route('/garden_conductivity_periodical')
def get_garden_electrical_conductivity_periodical():
    conductivity = get_owl_data_periodical("kip_greenhouse_electrical_conductivity", "electrical_conductivity", DAYS_GARDEN)
    return jsonify({"conductivity_periodical": [conductivity]})

@app.route('/garden_water_level')
def get_garden_water_level():
    water_level = get_owl_data("kip_greenhouse_water_level", "water_level")
    return jsonify({"water_level": [water_level]})

@app.route('/garden_picture_analyzed')
def get_garden_analyzed_picture():
    picture_analyzed = get_owl_data("kip_greenhouse_picture_analyzed", "picture_analyzed")
    return jsonify({"picture_analyzed": [picture_analyzed]})

@app.route('/garden_analyzed_labels')
def get_garden_analyzed_labels():
    labels_analyzed = get_owl_data("kip_greenhouse_picture_labels", "labels")
    return jsonify({"labels": [labels_analyzed]})

@app.route('/run_pump', methods=['POST'])
def run_pump():
    with pump_lock:  # Ensures isolation
        try:
            delete_old_owl_data("kip_greenhouse_pump_activate", 0)
            post_owl_data_new("kip_greenhouse_pump_activate", "activate", "on")
            sleep(10)  # Activate pump for 1 minute
            delete_old_owl_data("kip_greenhouse_pump_activate", 0)
            post_owl_data_new("kip_greenhouse_pump_activate", "activate", "off")
            return jsonify({"status": "Pump activated"}), 200
        except Exception as e:
            # Rollback mechanism if an error occurs
            delete_old_owl_data("kip_greenhouse_pump_activate", 0)
            post_owl_data_new("kip_greenhouse_pump_activate", "activate", "off")
            return jsonify({"status": "Pump activation failed", "error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=8000)
