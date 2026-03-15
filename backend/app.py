from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import ml modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.weather import get_weather
from ml.predict import predict_fertilizer
from backend.llm_explain import explain_fertilizer

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint for fertilizer prediction.
    
    Expects JSON with:
    - crop_type: str
    - soil_type: str
    - nitrogen: float
    - phosphorus: float
    - potassium: float
    - latitude: float
    - longitude: float
    """
    try:
        data = request.get_json()
        
        # Extract input data
        crop_type = data['crop_type']
        soil_type = data['soil_type']
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        
        # Get weather data
        temperature, humidity = get_weather(latitude, longitude)
        
        # Make fertilizer prediction
        fertilizer = predict_fertilizer(
            crop_type, soil_type, nitrogen, phosphorus, potassium,
            temperature, humidity
        )
        
        # Generate AI explanation
        explanation = explain_fertilizer(
            crop_type, soil_type, temperature, humidity,
            nitrogen, phosphorus, potassium, fertilizer
        )
        
        # Return response
        return jsonify({
            'fertilizer': fertilizer,
            'explanation': explanation,
            'temperature': temperature,
            'humidity': humidity
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)