import requests

# Ollama API configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# Toggle this to False when you want to use the real LLM
TEST_MODE = False


def explain_fertilizer(
    crop,
    soil,
    temperature,
    humidity,
    nitrogen,
    phosphorus,
    potassium,
    fertilizer
):
    """
    Generate explanation for fertilizer recommendation.

    Args:
        crop (str): Crop type
        soil (str): Soil type
        temperature (float): Temperature in Celsius
        humidity (float): Humidity percentage
        nitrogen (float): Nitrogen level
        phosphorus (float): Phosphorus level
        potassium (float): Potassium level
        fertilizer (str): Recommended fertilizer

    Returns:
        str: Explanation text
    """

    # Simple explanation for development/testing
    if TEST_MODE:
        return (
            f"For {crop} grown in {soil} soil under {temperature}°C temperature "
            f"and {humidity}% humidity, the nutrient levels (N:{nitrogen}, "
            f"P:{phosphorus}, K:{potassium}) indicate that {fertilizer} "
            f"is an appropriate fertilizer to support healthy crop growth."
        )

    try:

        prompt = f"""
Crop: {crop}
Soil Type: {soil}

Environmental Conditions:
Temperature: {temperature}°C
Humidity: {humidity}%

Soil Nutrient Levels:
Nitrogen: {nitrogen}
Phosphorus: {phosphorus}
Potassium: {potassium}

Recommended Fertilizer: {fertilizer}

Explain briefly (2–3 sentences) why this fertilizer is suitable for the crop.
"""

        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 120,
                "temperature": 0.3
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        result = response.json()
        explanation = result.get("response", "").strip()

        if not explanation:
            return f"Recommended fertilizer: {fertilizer}"

        return explanation

    except requests.Timeout:
        return f"AI explanation timed out. Recommended fertilizer: {fertilizer}"

    except requests.RequestException as e:
        return f"Unable to generate explanation. Recommended fertilizer: {fertilizer}. Error: {str(e)}"

    except Exception as e:
        return f"Unexpected error generating explanation. Recommended fertilizer: {fertilizer}. Error: {str(e)}"