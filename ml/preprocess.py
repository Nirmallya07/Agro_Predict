import joblib

# Load encoders
le_soil = joblib.load('models/le_soil.pkl')
le_crop = joblib.load('models/le_crop.pkl')
le_fert = joblib.load('models/le_fert.pkl')

def encode_soil(soil_type):
    """Encode soil type using trained label encoder."""
    return le_soil.transform([soil_type])[0]

def encode_crop(crop_type):
    """Encode crop type using trained label encoder."""
    return le_crop.transform([crop_type])[0]

def decode_fertilizer(encoded_fertilizer):
    """Decode fertilizer prediction back to name."""
    return le_fert.inverse_transform([encoded_fertilizer])[0]