import joblib
from .preprocess import encode_soil, encode_crop, decode_fertilizer

# Load trained model
model = joblib.load('models/fertilizer_model.pkl')

def predict_fertilizer(crop_type, soil_type, nitrogen, phosphorus, potassium, temperature, humidity):
    """
    Predict fertilizer recommendation based on input features.
    
    Args:
        crop_type (str): Type of crop
        soil_type (str): Type of soil
        nitrogen (float): Nitrogen level
        phosphorus (float): Phosphorus level
        potassium (float): Potassium level
        temperature (float): Temperature in Celsius
        humidity (float): Humidity percentage
    
    Returns:
        str: Recommended fertilizer name
    """
    # Encode categorical inputs
    soil_enc = encode_soil(soil_type)
    crop_enc = encode_crop(crop_type)
    
    # Prepare features array
    features = [[soil_enc, crop_enc, nitrogen, phosphorus, potassium, temperature, humidity]]
    
    # Make prediction
    prediction = model.predict(features)[0]
    
    # Decode prediction to fertilizer name
    fertilizer = decode_fertilizer(prediction)
    
    return fertilizer