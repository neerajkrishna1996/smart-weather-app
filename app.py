from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

OPENWEATHER_API_KEY = "13d742ea2facda093d57f84e5c7f381a"
GEOAPIFY_API_KEY = "c082c17f817a40cd9b363921260920d9"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.json
    city = data.get('city')
    pincode = data.get('pincode')

    if city:
        query = city
    elif pincode:
        query = pincode
    else:
        return jsonify({'error': 'No city or pincode provided'}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'City not found'}), 404

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Coordinates missing'}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Weather not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
