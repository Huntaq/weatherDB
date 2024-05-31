import requests
import csv
import os
from datetime import datetime
from geopy.geocoders import Nominatim

def get_lat_long(city):
    geolocator = Nominatim(user_agent="geoapiExercises1")
    location = geolocator.geocode(city)
    if location:
        return city,location.latitude, location.longitude
    else:
        return None, None

def get_weather_data(city):
    api_key = '5241a398dcf1bc7bbaee5ceeb1574eab'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if "name" in data:
        city_name = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        temp_celsius = data["main"]["temp"]
        humidity_percent = data["main"]["humidity"]
        dew_point = temp_celsius - ((100 - humidity_percent) / 5)
        visibility = data.get("visibility", "N/A")

        return [city_name, country, temperature, weather_desc, wind_speed, pressure, humidity, dew_point, visibility]
    else:
        print(f"City {city} not found or data not available.")
        return None

if __name__ == "__main__":
    cities = [
        "London", "Paris", "Berlin", "Madrid", "Rome", "Athens", "Warsaw", "Vienna", "Amsterdam", "Brussels",
        "Lisbon", "Oslo", "Stockholm", "Helsinki", "Copenhagen", "Dublin", "Budapest", "Prague", "Bratislava",
        "Ljubljana", "Zagreb", "Belgrade", "Sofia", "Bucharest", "Vilnius", "Riga", "Tallinn", "Valletta",
        "Nicosia", "Reykjavik", "Luxembourg", "Monaco", "Andorra la Vella", "San Marino", "Vatican City", "Bern",
        "Minsk", "Tirana", "Chisinau", "Podgorica", "Skopje", "Sarajevo", "Tbilisi", "Yerevan", "Baku", "Ankara",
        "Kiev", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen",
        "Leipzig", "Bremen", "Dresden", "Hanover", "Nuremberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld",
        "Bonn", "Münster", "Karlsruhe", "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Mönchengladbach",
        "Braunschweig", "Chemnitz", "Kiel", "Aachen", "Halle", "Magdeburg", "Freiburg", "Krefeld", "Lübeck",
        "Oberhausen", "Erfurt", "Mainz", "Rostock", "Kassel", "Hagen", "Saarbrücken", "Hamm", "Mülheim", "Potsdam",
        "Ludwigshafen", "Oldenburg", "Leverkusen", "Osnabrück", "Solingen", "Heidelberg", "Herne", "Neuss", "Darmstadt",
        "Paderborn", "Regensburg", "Ingolstadt", "Würzburg", "Wolfsburg", "Ulm", "Heilbronn", "Pforzheim", "Göttingen",
        "Bottrop", "Trier", "Recklinghausen", "Reutlingen", "Bremerhaven", "Koblenz", "Bergisch Gladbach", "Jena",
        "Remscheid", "Erlangen", "Moers", "Siegen", "Hildesheim", "Salzgitter", "Cottbus", "Kaiserslautern", "Gütersloh",
        "Schwerin", "Witten", "Gera", "Iserlohn", "Ludwigsburg", "Esslingen", "Tübingen", "Flensburg", "Zwickau",
        "Villingen-Schwenningen", "Giessen", "Konstanz", "Dessau", "Worms", "Rosenheim", "Offenbach", "Kempten",
        "Baden-Baden", "Langenfeld", "Wilhelmshaven", "Nordhausen", "Norderstedt", "Garbsen", "Wolfenbüttel",
        "Fulda", "Hof", "Landshut", "Aschaffenburg", "Neuwied", "Dormagen", "Bayreuth", "Hürth", "Brandenburg",
        "Neubrandenburg", "Görlitz", "Gladbeck", "Lüdenscheid", "Castrop-Rauxel", "Bitterfeld-Wolfen", "Landau",
        "Frechen", "Kaufbeuren", "Straubing", "Grevenbroich", "Marl", "Bamberg", "Langenhagen", "Aalen", "Hameln",
        "Meerbusch", "Bad Homburg", "Düren", "Hürth", "Schwabach", "Waiblingen", "Plauen", "Herten", "Lörrach",
        "Velbert", "Ahaus", "Bruchsal", "Schwerte", "Sindelfingen", "Elmshorn", "Herford", "Strausberg", "Hockenheim",
        "Kamp-Lintfort", "Baunatal", "Lindau", "Löhne", "Bühl", "Unna", "Limburg", "Neunkirchen", "Minden", "Hennef",
        "Wismar", "Passau", "Dachau", "Biberach", "Gummersbach", "Backnang", "Homburg", "Pinneberg", "Ravensburg",
        "Heidenheim", "Nordhorn", "Borken", "Sankt Ingbert", "Freising", "Dülmen", "Kitzingen", "Stade", "Warendorf",
        "Rüsselsheim", "Lehrte", "Griesheim", "Bad Kreuznach", "Kleve", "Rheine", "Neumünster", "Coburg", "Aschersleben",
        "Schwäbisch Hall", "Königs Wusterhausen", "Lüdinghausen", "Husum", "Schleswig", "Starnberg", "Alzey",
        "Halberstadt", "Salzwedel", "Delmenhorst", "Mühldorf", "Celle", "Oelde", "Olpe", "Papenburg", "Werne", "Eisenach",
        "Neuruppin", "Weißenfels", "Friedberg", "Rastatt", "Stolberg", "Goch", "Nettetal", "Düren", "Pulheim", "Bocholt",
        "Bergheim", "Neuss", "Hamm", "Marl", "Lippstadt", "Ahlen", "Unna", "Bad Salzuflen", "Siegen", "Ratingen", "Wesel",
        "Gelsenkirchen", "Witten", "Hilden", "Grevenbroich", "Langenfeld", "Dorsten", "Kamen", "Bergkamen", "Sankt Augustin",
        "Rheda-Wiedenbrück", "Oberhausen", "Eschweiler", "Mettmann", "Bad Honnef", "Schwelm", "Herzogenrath", "Viersen",
        "Neukirchen-Vluyn", "Kerpen", "Geilenkirchen", "Erkelenz", "Geldern", "Greven", "Haan", "Meerbusch", "Vlotho",
        "Bad Oeynhausen", "Ibbenbüren", "Oerlinghausen", "Harsewinkel", "Versmold", "Gütersloh", "Rietberg", "Beckum",
        "Ennigerloh", "Warendorf", "Datteln", "Coesfeld", "Lüdinghausen", "Dülmen", "Haltern", "Oer-Erkenschwick", "Selm",
        "Gladbeck", "Castrop-Rauxel", "Recklinghausen", "Herten", "Marl", "Dortmund", "Schwerte", "Unna", "Werne", "Hamm",
        "Bochum", "Witten", "Hattingen", "Herne", "Gelsenkirchen", "Oberhausen", "Bottrop", "Mülheim", "Essen", "Velbert",
        "Wuppertal", "Solingen", "Remscheid", "Wiesbaden", "Rüsselsheim", "Bad Homburg", "Oberursel", "Bad Soden", "Kelkheim",
        "Flörsheim", "Hattersheim", "Hofheim", "Kriftel", "Niedernhausen", "Raunheim", "Schwalbach", "Eschborn", "Bad Vilbel",
        "Maintal", "Karben", "Nidderau", "Friedberg", "Büdingen", "Butzbach", "Hanau", "Seligenstadt", "Hainburg", "Obertshausen",
        "Mühlheim", "Rodgau", "Dietzenbach", "Dreieich", "Neu-Isenburg", "Langen", "Egelsbach", "Erzhausen", "Griesheim",
        "Weiterstadt", "Pfungstadt", "Seeheim-Jugenheim", "Bensheim", "Lorsch", "Heppenheim", "Biblis", "Lampertheim", "Viernheim",
        "Hirschhorn", "Eberbach", "Wald-Michelbach", "Beerfelden", "Michelstadt", "Erbach", "Reichelsheim", "Bürstadt", "Grünstadt",
        "Frankenthal", "Ludwigshafen", "Schifferstadt", "Speyer", "Hockenheim", "Ketsch", "Schwetzingen", "Brühl", "Leimen",
        "Nußloch", "Sandhausen", "Wiesloch", "Walldorf", "St. Leon-Rot", "Rauenberg", "Mannheim", "Viernheim", "Weinheim",
        "Weinheim", "Wiesloch", "Worms", "Bensheim", "Lorsch", "Heppenheim", "Biblis", "Lampertheim", "Viernheim", "Hirschhorn",
        "Eberbach", "Wald-Michelbach", "Beerfelden", "Michelstadt", "Erbach", "Reichelsheim", "Bürstadt", "Grünstadt", "Frankenthal",
        "Ludwigshafen", "Schifferstadt", "Speyer", "Hockenheim", "Ketsch", "Schwetzingen", "Brühl", "Leimen", "Nußloch", "Sandhausen",
        "Wiesloch", "Walldorf", "St. Leon-Rot", "Rauenberg", "Mannheim", "Viernheim", "Weinheim"
    ]

    
    data_to_save = []

    # Save data to .CSV
    current_date = datetime.now().strftime("%Y-%m-%d")
    data_folder = 'data'
    csv_file_name = f"weather_data_{current_date}.csv"
    csv_file_path = os.path.join(data_folder, csv_file_name)

    # Create data directory if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Check if the file already exists
    if os.path.exists(csv_file_path):
        print(f"The file {csv_file_name} already exists in the {data_folder} folder.")
    else:
        for city in cities:
            weather_data = get_weather_data(city)
            if weather_data:
                data_to_save.append(weather_data)
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["City", "Country", "Temperature (°C)", "Weather Description", "Wind Speed (m/s)",
                                 "Pressure (hPa)", "Humidity (%)", "Dew Point (°C)", "Visibility (m)"])
            csv_writer.writerows(data_to_save)

        print(f"Data saved to file: {csv_file_path}")
    
    if os.path.exists(os.path.join(data_folder, "cords.csv")):
        print(f"The file cords.csv already exists in the {data_folder} folder.")

    else:
        data_to_save = []
        for city in cities:
            weather_data = get_lat_long(city)
            if weather_data:
                data_to_save.append(weather_data)
        with open(os.path.join(data_folder, "cords.csv"), 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["City", "Latitude", "Longitude"])
            csv_writer.writerows(data_to_save)

        print(f"Data saved to file: cords.csv")
    
    



