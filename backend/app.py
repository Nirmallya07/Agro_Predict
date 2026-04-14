from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
from collections import deque
import paho.mqtt.client as mqtt

# Add parent directory to path to import ml modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.weather import get_weather
from ml.predict import predict_fertilizer
from backend.llm_explain import explain_fertilizer

app = Flask(__name__)
CORS(app)

# ---------------- MQTT BUFFER ----------------
npk_buffer = deque(maxlen=10)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        npk_buffer.append(data)
    except Exception as e:
        print("MQTT message error:", e)

mqtt_client = mqtt.Client()

# ✅ SAFE CONNECTION (won’t crash if broker missing)
try:
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.subscribe("soil/npk")
    mqtt_client.loop_start()
    print("✅ MQTT Connected")
except Exception as e:
    print("⚠️ MQTT connection failed:", e)

# ---------------- AVERAGE FUNCTION ----------------
def get_average_npk():
    if not npk_buffer:
        return {"N": 0, "P": 0, "K": 0}

    avg_n = sum(x["N"] for x in npk_buffer) / len(npk_buffer)
    avg_p = sum(x["P"] for x in npk_buffer) / len(npk_buffer)
    avg_k = sum(x["K"] for x in npk_buffer) / len(npk_buffer)

    return {
        "N": round(avg_n, 2),
        "P": round(avg_p, 2),
        "K": round(avg_k, 2)
    }

# ---------------- SENSOR ROUTE ----------------
@app.route("/sensor-data")
def sensor_data():
    return jsonify(get_average_npk())

# ---------------- MAIN PREDICTION ----------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        crop_type = data['crop_type']
        soil_type = data['soil_type']
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        # Weather
        temperature, humidity = get_weather(latitude, longitude)

        # ML Prediction
        fertilizer = predict_fertilizer(
            crop_type, soil_type, nitrogen, phosphorus, potassium,
            temperature, humidity
        )

        # AI Explanation
        explanation = explain_fertilizer(
            crop_type, soil_type, temperature, humidity,
            nitrogen, phosphorus, potassium, fertilizer
        )

        return jsonify({
            'fertilizer': fertilizer,
            'explanation': explanation,
            'temperature': temperature,
            'humidity': humidity
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)