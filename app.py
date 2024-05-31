from flask import Flask, render_template, jsonify, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_lat_long(city):
    db_file = 'weather_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT Latitude, Longitude FROM coordinates WHERE City=?", (city,))
    result = cursor.fetchone()
    conn.close()
    # print(result)
    if result is not None:
        return result
    else:
        return None,None
    

def get_data_for_date(date):
    db_file = 'weather_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    table_name = f"weather_data_{date.replace('-', '_')}"
    try:
        cursor.execute(f"SELECT * FROM {table_name} ")
        rows = cursor.fetchall()
        

        
        if rows:
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            
            print (data[-1])
            # print(data)
            # Dodawanie Latitude i Longitude dla każdego miasta
            for entry in data:
                city = entry.get('City')
                if city:  # Sprawdzamy, czy nazwa miasta nie jest pusta ani None
                    latitude, longitude = get_lat_long(city)
                    if latitude is not None and longitude is not None:
                        entry['Latitude'] = latitude
                        entry['Longitude'] = longitude
                        # print(type(latitude))
                    else:
                        entry['Latitude'] = ""
                        entry['Longitude'] = ""
                else:
                    print("City name is missing for one of the entries.")
        else:
            print("No data found for the given date and limit.")
            data = []
        
    except Exception as e:
        print(f"Error accessing table {table_name}: {e}")
        data = []
    
    conn.close()

    return data





@app.route('/')
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)

@app.route('/data')
def data():
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    weather_data = get_data_for_date(date)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
