from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

OPENWEATHER_API_KEY = "your_openweathermap_api_key"
GEOAPIFY_API_KEY = "your_geoapify_api_key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    # Get coordinates from Geoapify
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()
    
    if not geo_response['features']:
        return jsonify({'error': 'City not found'}), 404

    coordinates = geo_response['features'][0]['geometry']['coordinates']
    lon, lat = coordinates

    # Get weather from OpenWeatherMap
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()

    if weather_data.get("cod") != 200:
        return jsonify({'error': 'Weather data not found'}), 500

    result = {
        'location': weather_data.get('name'),
        'temperature': weather_data['main']['temp'],
        'humidity': weather_data['main']['humidity'],
        'wind_speed': weather_data['wind']['speed'],
        'weather': weather_data['weather'][0]['main'],
        'icon': weather_data['weather'][0]['icon'],
        'precipitation': weather_data.get('rain', {}).get('1h', 0),
        'summary': weather_data['weather'][0]['description']
    }

    return jsonify(result)

@app.route('/suggest_city', methods=['GET'])
def suggest_city():
    query = request.args.get('query')
    geo_url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={query}&apiKey={GEOAPIFY_API_KEY}&limit=5"
    response = requests.get(geo_url).json()
    suggestions = [feat['properties']['formatted'] for feat in response['features']]
    return jsonify(suggestions)

@app.route('/get_location_weather', methods=['POST'])
def get_location_weather():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Location required'}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()

    if weather_data.get("cod") != 200:
        return jsonify({'error': 'Weather data not found'}), 500

    result = {
        'location': weather_data.get('name'),
        'temperature': weather_data['main']['temp'],
        'humidity': weather_data['main']['humidity'],
        'wind_speed': weather_data['wind']['speed'],
        'weather': weather_data['weather'][0]['main'],
        'icon': weather_data['weather'][0]['icon'],
        'precipitation': weather_data.get('rain', {}).get('1h', 0),
        'summary': weather_data['weather'][0]['description']
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
