var map = L.map('map').setView([51.505, -0.09], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function loadData(date) {
    fetch(`/data?date=${date}`)
        .then(response => response.json())
        .then(data => {
            map.eachLayer((layer) => {
                if (layer.options && layer.options.pane === 'markerPane') {
                    map.removeLayer(layer);
                }
            });
            data.forEach(item => {
                // console.log(item);
                if (item.Latitude!='' && item.Longitude!='') {
                    
                    L.marker([item.Latitude, item.Longitude]).addTo(map)
                        .bindPopup(`<b>${item.City}, ${item.Country}</b><br>
                                    Temperature: ${item['Temperature_°C']}°C <br>
                                    Weather: ${item.Weather_Description}<br>
                                    Wind Speed: ${item.Wind_Speed_m_per_s} m/s<br>
                                    Pressure: ${item['Pressure_hPa']} hPa<br>
                                    Humidity: ${item['Humidity_Pct']}%<br>
                                    Dew Point: ${item['Dew_Point_°C']}°C<br>
                                    Visibility: ${item['Visibility_m']} m`);
                }
            });
        });
}

document.getElementById('slider').addEventListener('input', function() {
    var date = this.value;
    loadData(date);
});
