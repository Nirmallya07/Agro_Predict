import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
df = pd.read_csv('data/data_core.csv')

# Rename columns to match expected format
df = df.rename(columns={
    'Temparature': 'Temperature',
    'Phosphorous': 'Phosphorus',
    'Soil_type': 'Soil Type',
    'Crop_type': 'Crop Type',
    'Fertilizer': 'Fertilizer Name'
})

# Encode categorical features
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fert = LabelEncoder()

df['Soil Type'] = le_soil.fit_transform(df['Soil Type'])
df['Crop Type'] = le_crop.fit_transform(df['Crop Type'])
df['Fertilizer Name'] = le_fert.fit_transform(df['Fertilizer Name'])

# Features and target
X = df[['Soil Type', 'Crop Type', 'Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity']]
y = df['Fertilizer Name']

# Train Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Save model and encoders
joblib.dump(model, 'models/fertilizer_model.pkl')
joblib.dump(le_soil, 'models/le_soil.pkl')
joblib.dump(le_crop, 'models/le_crop.pkl')
joblib.dump(le_fert, 'models/le_fert.pkl')

print("Model trained and saved successfully!")