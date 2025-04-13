from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API details
API_KEY = '13d742ea2facda093d57f84e5c7f381a'  # Replace with your actual API key

# Route to show the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch weather data
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data['cod'] == '404':
        return render_template('index.html', error="City not found!")
    
    weather_data = {
        'city': city,
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed'],
        'precipitation': data.get('rain', {}).get('1h', 0),  # Precipitation in the last hour
    }

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
