from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Stałe dane testowe
test_data = {
    "2024-05-28": [
        {"City": "Warsaw", "Country": "Poland", "Latitude": 52.2297, "Longitude": 21.0122, "Temperature (°C)": 20, "Weather Description": "Sunny", "Wind Speed (m/s)": 3.5, "Pressure (hPa)": 1012, "Humidity (%)": 60, "Dew Point (°C)": 12, "Visibility (m)": 10000},
        {"City": "Berlin", "Country": "Germany", "Latitude": 52.5200, "Longitude": 13.4050, "Temperature (°C)": 18, "Weather Description": "Cloudy", "Wind Speed (m/s)": 4.0, "Pressure (hPa)": 1015, "Humidity (%)": 65, "Dew Point (°C)": 10, "Visibility (m)": 8000},
        {"City": "Paris", "Country": "France", "Latitude": 48.8566, "Longitude": 2.3522, "Temperature (°C)": 22, "Weather Description": "Rainy", "Wind Speed (m/s)": 5.0, "Pressure (hPa)": 1008, "Humidity (%)": 55, "Dew Point (°C)": 14, "Visibility (m)": 6000}
    ],
    "2024-05-29": [
        {"City": "Madrid", "Country": "Spain", "Latitude": 40.4168, "Longitude": -3.7038, "Temperature (°C)": 25, "Weather Description": "Sunny", "Wind Speed (m/s)": 2.5, "Pressure (hPa)": 1010, "Humidity (%)": 40, "Dew Point (°C)": 8, "Visibility (m)": 12000},
        {"City": "Rome", "Country": "Italy", "Latitude": 41.9028, "Longitude": 12.4964, "Temperature (°C)": 24, "Weather Description": "Cloudy", "Wind Speed (m/s)": 3.0, "Pressure (hPa)": 1013, "Humidity (%)": 50, "Dew Point (°C)": 12, "Visibility (m)": 9000},
        {"City": "Vienna", "Country": "Austria", "Latitude": 48.2082, "Longitude": 16.3738, "Temperature (°C)": 19, "Weather Description": "Rainy", "Wind Speed (m/s)": 4.5, "Pressure (hPa)": 1007, "Humidity (%)": 70, "Dew Point (°C)": 13, "Visibility (m)": 7000}
    ]
}

@app.route('/')
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)

@app.route('/data')
def data():
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    return jsonify(test_data.get(date, []))

if __name__ == '__main__':
    app.run(debug=True)
