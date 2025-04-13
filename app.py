from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your actual OpenWeatherMap API key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    query = request.args.get('query')  # city or pincode
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if query:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={query}&appid={OPENWEATHER_API_KEY}&units=metric'
    elif lat and lon:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric'
    else:
        return jsonify({'error': 'Invalid query'}), 400

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    data = response.json()

    weather_info = {
        'city': data.get('name'),
        'temperature': round(data['main']['temp']),
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'summary': data['weather'][0]['main'],
        'icon': data['weather'][0]['icon'],
        'precipitation': data.get('rain', {}).get('1h', 0)  # fallback to 0 if missing
    }

    return jsonify(weather_info)