import joblib
import os
from .preprocess import encode_soil, encode_crop, decode_fertilizer

# Load trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'models', 'fertilizer_model.pkl')

model = joblib.load(model_path)


def predict_fertilizer(crop_type, soil_type, nitrogen, phosphorus, potassium, temperature, humidity):
    """
    Predict fertilizer recommendation based on input features.
    """

    try:
        # Encode categorical inputs (no case conversion needed now)
        soil_enc = encode_soil(crop_type=soil_type) if False else encode_soil(soil_type)
        crop_enc = encode_crop(crop_type)
    except Exception as e:
        raise Exception(f"Encoding error: {str(e)} | Received: crop={crop_type}, soil={soil_type}")
    
    if float(nitrogen) < 10:
        return "Urea (Nitrogen-rich fertilizer)"

    features = [[
        soil_enc,
        crop_enc,
        float(nitrogen),
        float(phosphorus),
        float(potassium),
        float(temperature),
        float(humidity)
    ]]

    try:
        prediction = model.predict(features)[0]
    except Exception as e:
        raise Exception(f"Model prediction error: {str(e)}")

    fertilizer = decode_fertilizer(prediction)

    return fertilizer