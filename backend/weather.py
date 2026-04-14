import requests

# OpenWeather API configuration
API_KEY = '' # Put your API key here
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(latitude, longitude):
    """
    Fetch current weather data for given coordinates.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        tuple: (temperature in Celsius, humidity percentage)
    """
    try:
        # Build API URL
        url = f"{BASE_URL}?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
        
        # Make API request
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse JSON response
        data = response.json()
        
        # Extract temperature and humidity
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        
        return temperature, humidity
    
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch weather data: {str(e)}")
    except KeyError as e:
        raise Exception(f"Invalid weather API response: {str(e)}")
