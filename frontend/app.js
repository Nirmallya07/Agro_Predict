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

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    detectLocationBtn.addEventListener('click', detectLocation);
    form.addEventListener('submit', handleSubmit);
}

// Detect user location using Geolocation API
function detectLocation() {
    if (!navigator.geolocation) {
        showError('Geolocation is not supported by this browser.');
        return;
    }

    detectLocationBtn.disabled = true;
    detectLocationBtn.textContent = 'Detecting...';

    navigator.geolocation.getCurrentPosition(
        function(position) {
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
        function(error) {
            let errorMessage = 'Unable to detect location.';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = 'Location access denied. Please enable location permissions.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = 'Location information is unavailable.';
                    break;
                case error.TIMEOUT:
                    errorMessage = 'Location request timed out.';
                    break;
            }

            showError(errorMessage);
            detectLocationBtn.disabled = false;
            detectLocationBtn.textContent = '📍 Detect My Location';
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 300000
        }
    );
}

// Handle form submission
async function handleSubmit(event) {
    event.preventDefault();

    if (!latitude || !longitude) {
        showError('Please detect your location first.');
        return;
    }

    // Get form data
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

    // Show loading
    showLoading();

    try {
        // Make API request
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Display result
        displayResult(result);

    } catch (error) {
        showError('Failed to get recommendation. Please check if the backend server is running.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Display loading state
function showLoading() {
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

// Hide loading state
function hideLoading() {
    loadingDiv.classList.add('hidden');
}

// Display result
function displayResult(result) {
    fertilizerResult.innerHTML = `
        <div class="fertilizer-card">
            <h3>Recommended Fertilizer: ${result.fertilizer}</h3>
            <p>Current Weather: ${result.temperature}°C, ${result.humidity}% humidity</p>
        </div>
    `;

    explanationResult.innerHTML = `
        <div class="explanation-card">
            <h4>AI Explanation:</h4>
            <p>${result.explanation}</p>
        </div>
    `;

    resultDiv.classList.remove('hidden');
    errorDiv.classList.add('hidden');
}

// Show error message
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
}