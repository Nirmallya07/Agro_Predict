// Global variables
let latitude = null;
let longitude = null;

// DOM elements
const form = document.getElementById('fertilizerForm');
const detectLocationBtn = document.getElementById('detectLocation');
const locationDisplay = document.getElementById('locationDisplay');
const resultDiv = document.getElementById('result');
const fertilizerResult = document.getElementById('fertilizerResult');
const explanationResult = document.getElementById('explanationResult');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');

// Init
document.addEventListener('DOMContentLoaded', function () {
    setupEventListeners();
});

function setupEventListeners() {
    detectLocationBtn.addEventListener('click', detectLocation);
    form.addEventListener('submit', handleSubmit);
}

// ---------------- LOCATION ----------------
function detectLocation() {
    if (!navigator.geolocation) {
        showError('Geolocation is not supported.');
        return;
    }

    detectLocationBtn.disabled = true;
    detectLocationBtn.textContent = 'Detecting...';

    navigator.geolocation.getCurrentPosition(
        (position) => {
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;

            locationDisplay.innerHTML = `
                <p>📍 Location detected:</p>
                <p>Latitude: ${latitude.toFixed(4)}</p>
                <p>Longitude: ${longitude.toFixed(4)}</p>
            `;

            detectLocationBtn.disabled = false;
            detectLocationBtn.textContent = '📍 Detect My Location';
        },
        (error) => {
            showError('Location error.');
            detectLocationBtn.disabled = false;
        }
    );
}

// ---------------- FORM SUBMIT ----------------
async function handleSubmit(event) {
    event.preventDefault();

    if (!latitude || !longitude) {
        showError('Please detect your location first.');
        return;
    }

    const formData = new FormData(form);

    const data = {
        crop_type: formData.get('cropType'),
        soil_type: formData.get('soilType'),
        nitrogen: parseFloat(formData.get('nitrogen')),
        phosphorus: parseFloat(formData.get('phosphorus')),
        potassium: parseFloat(formData.get('potassium')),
        latitude: latitude,
        longitude: longitude
    };

    showLoading();

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) throw new Error(result.error);

        displayResult(result);

    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// ---------------- SENSOR FUNCTION ----------------
async function useSensor() {
    const btn = event.target;

    btn.disabled = true;
    btn.textContent = "Collecting sensor data...";

    await new Promise(resolve => setTimeout(resolve, 3000));

    try {
        const res = await fetch('http://localhost:5000/sensor-data');
        const data = await res.json();

        document.getElementById('nitrogen').value = data.N;
        document.getElementById('phosphorus').value = data.P;
        document.getElementById('potassium').value = data.K;

    } catch (error) {
        showError("Failed to fetch sensor data");
    }

    btn.disabled = false;
    btn.textContent = "📡 Use Soil Sensor Values";
}

// ---------------- UI ----------------
function showLoading() {
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function displayResult(result) {
    fertilizerResult.innerHTML = `
        <div class="fertilizer-card">
            <h3>Recommended Fertilizer: ${result.fertilizer}</h3>
            <p>Weather: ${result.temperature}°C, ${result.humidity}%</p>
        </div>
    `;

    explanationResult.innerHTML = `
        <div class="explanation-card">
            <p>${result.explanation}</p>
        </div>
    `;

    resultDiv.classList.remove('hidden');
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}