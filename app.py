from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OPENWEATHER_API_KEY = "13d742ea2facda093d57f84e5c7f381a"

def get_weather_data(city_name=None, lat=None, lon=None):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    if city_name:
        params['q'] = city_name
    elif lat and lon:
        params['lat'] = lat
        params['lon'] = lon

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data['name'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'summary': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'precipitation': data.get('pop', 0) * 100  # Fallback if 'pop' is not in data
        }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    city = data.get('city')
    lat = data.get('lat')
    lon = data.get('lon')
    weather = get_weather_data(city_name=city, lat=lat, lon=lon)
    if weather:
        return jsonify(weather)
    return jsonify({'error': 'Weather data not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
