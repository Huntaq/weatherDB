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
                L.marker([item.Latitude, item.Longitude]).addTo(map)
                    .bindPopup(`<b>${item.City}, ${item.Country}</b><br>
                                Temperature: ${item['Temperature (°C)']}°C<br>
                                Weather: ${item['Weather Description']}<br>
                                Wind Speed: ${item['Wind Speed (m/s)']} m/s<br>
                                Pressure: ${item['Pressure (hPa)']} hPa<br>
                                Humidity: ${item['Humidity (%)']}%<br>
                                Dew Point: ${item['Dew Point (°C)']}°C<br>
                                Visibility: ${item['Visibility (m)']} m`);
            });
        });
}

document.getElementById('slider').addEventListener('input', function() {
    var date = this.value;
    loadData(date);
});
