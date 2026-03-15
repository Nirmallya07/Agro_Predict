# AGRO_PREDICT - Fertilizer Recommendation System

A machine learning-based fertilizer recommendation system that uses soil type, crop type, nutrient levels, and weather data to provide personalized fertilizer recommendations with AI-powered explanations.

## Features

- Machine learning model using Random Forest Classifier
- Real-time weather data integration via OpenWeather API
- AI explanations using local Ollama LLM
- Web-based frontend for easy use
- RESTful API backend

## Installation

1. Clone or download the project files.

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama is installed and running locally:
   - Install Ollama from https://ollama.ai/
   - Pull the llama3 model: `ollama pull llama3`
   - Start Ollama server: `ollama serve`

## Usage

1. **Train the model:**
   ```bash
   python ml/train_model.py
   ```

2. **Run the Flask backend server:**
   ```bash
   python backend/app.py
   ```

3. **Open the frontend:**
   - Open `frontend/index.html` in your web browser
   - Or serve it via a local web server

## API Usage

The backend provides a `/predict` endpoint that accepts POST requests with the following JSON format:

```json
{
  "crop_type": "Wheat",
  "soil_type": "Loamy",
  "nitrogen": 20,
  "phosphorus": 10,
  "potassium": 8,
  "latitude": 28.61,
  "longitude": 77.20
}
```

Response:
```json
{
  "fertilizer": "Urea",
  "explanation": "AI-generated explanation..."
}
```

## Project Structure

```
AGRO_PREDICT/
├── data/
│   └── data_core.csv          # Training dataset
├── models/                    # Saved ML models and encoders
├── ml/
│   ├── train_model.py         # Model training script
│   ├── preprocess.py          # Data preprocessing utilities
│   └── predict.py             # Prediction functions
├── backend/
│   ├── app.py                 # Flask API server
│   ├── weather.py             # Weather API integration
│   └── llm_explain.py         # AI explanation generation
├── frontend/
│   ├── index.html             # Web interface
│   ├── app.js                 # Frontend JavaScript
│   └── style.css              # Styling
├── config/
│   └── fertilizer_info.json   # Fertilizer information
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Dataset Format

The `data/data_core.csv` should contain the following columns:
- Soil Type (categorical)
- Crop Type (categorical)
- Nitrogen (numeric)
- Phosphorus (numeric)
- Potassium (numeric)
- Temperature (numeric, in Celsius)
- Humidity (numeric, percentage)
- Fertilizer Name (categorical, target variable)

## Notes

- Ensure the OpenWeather API key is valid and has sufficient quota
- The Ollama server must be running on localhost:11434
- The model assumes the dataset includes weather features for training