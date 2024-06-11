from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

def get_lat_long(city):
    db_file = 'weather_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT Latitude, Longitude FROM coordinates WHERE LOWER(City) = ?", (city.lower(),))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result
    else:
        return None, None

def get_data_for_date(date):
    db_file = 'weather_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    table_name = f"weather_data_{date.replace('-', '_')}"
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if rows:
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            
            for entry in data:
                city = entry.get('City')
                if city:
                    latitude, longitude = get_lat_long(city)
                    if latitude is not None and longitude is not None:
                        entry['Latitude'] = latitude
                        entry['Longitude'] = longitude
                    else:
                        entry['Latitude'] = ""
                        entry['Longitude'] = ""
        else:
            data = []
        
    except Exception as e:
        print(f"Error accessing table {table_name}: {e}")
        data = []
    
    conn.close()
    return data

def get_data_for_date_range(start_date, end_date, city):
    db_file = 'weather_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    data = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        table_name = f"weather_data_{current_date.strftime('%Y_%m_%d')}"
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE LOWER(City) = ?", (city.lower(),))
            rows = cursor.fetchall()
            
            if rows:
                columns = [desc[0] for desc in cursor.description]
                day_data = [dict(zip(columns, row)) for row in rows]
                data.extend(day_data)
        except Exception as e:
            print(f"Error accessing table {table_name}: {e}")
        
        current_date += timedelta(days=1)
    
    conn.close()
    return data

@app.route('/')
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)

@app.route('/data')
def data():
    date = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    city = request.args.get('city')
    
    if date:
        weather_data = get_data_for_date(date)
    elif start_date and end_date and city:
        weather_data = get_data_for_date_range(start_date, end_date, city)
    else:
        weather_data = []
    
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
