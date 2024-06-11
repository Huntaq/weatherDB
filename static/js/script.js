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
            var cityFilter = document.getElementById('city').value.toLowerCase();
            data.forEach(item => {
                if (item.Latitude !== '' && item.Longitude !== '') {
                    if (cityFilter === '' || item.City.toLowerCase().includes(cityFilter)) {
                        let popupContent = `<b>${item.City}, ${item.Country}</b><br>`;
                        if (document.getElementById('temperature').checked) {
                            popupContent += `Temperature: ${item['Temperature_°C']}°C <br>`;
                        }
                        if (document.getElementById('humidity').checked) {
                            popupContent += `Humidity: ${item['Humidity_Pct']}%<br>`;
                        }
                        if (document.getElementById('windSpeed').checked) {
                            popupContent += `Wind Speed: ${item['Wind_Speed_m_per_s']} m/s<br>`;
                        }
                        if (document.getElementById('pressure').checked) {
                            popupContent += `Pressure: ${item['Pressure_hPa']} hPa<br>`;
                        }
                        if (document.getElementById('dewPoint').checked) {
                            popupContent += `Dew Point: ${item['Dew_Point_°C']}°C<br>`;
                        }
                        if (document.getElementById('visibility').checked) {
                            popupContent += `Visibility: ${item['Visibility_m']} m`;
                        }
                        
                        L.marker([item.Latitude, item.Longitude]).addTo(map)
                            .bindPopup(popupContent);
                    }
                }
            });
        });
}

function calculateAverage(startDate, endDate, city) {
    fetch(`/data?start_date=${startDate}&end_date=${endDate}&city=${city}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                var validData = data.filter(item => !isNaN(parseFloat(item['Temperature_°C'])) && !isNaN(parseFloat(item['Humidity_Pct'])) && !isNaN(parseFloat(item['Wind_Speed_m_per_s'])) && !isNaN(parseFloat(item['Pressure_hPa'])) && !isNaN(parseFloat(item['Dew_Point_°C'])) && !isNaN(parseFloat(item['Visibility_m'])));
                
                if (validData.length > 0) {
                    var avgTemp = validData.reduce((acc, item) => acc + parseFloat(item['Temperature_°C']), 0) / validData.length;
                    var avgHumidity = validData.reduce((acc, item) => acc + parseFloat(item['Humidity_Pct']), 0) / validData.length;
                    var avgWindSpeed = validData.reduce((acc, item) => acc + parseFloat(item['Wind_Speed_m_per_s']), 0) / validData.length;
                    var avgPressure = validData.reduce((acc, item) => acc + parseFloat(item['Pressure_hPa']), 0) / validData.length;
                    var avgDewPoint = validData.reduce((acc, item) => acc + parseFloat(item['Dew_Point_°C']), 0) / validData.length;
                    var avgVisibility = validData.reduce((acc, item) => acc + parseFloat(item['Visibility_m']), 0) / validData.length;
                    
                    var maxTemp = Math.max(...validData.map(item => parseFloat(item['Temperature_°C'])));
                    var minTemp = Math.min(...validData.map(item => parseFloat(item['Temperature_°C'])));

                    alert(`Average Data for ${city} from ${startDate} to ${endDate}:\n
                        Temperature: ${avgTemp.toFixed(2)}°C\n
                        Humidity: ${avgHumidity.toFixed(2)}%\n
                        Wind Speed: ${avgWindSpeed.toFixed(2)} m/s\n
                        Pressure: ${avgPressure.toFixed(2)} hPa\n
                        Dew Point: ${avgDewPoint.toFixed(2)}°C\n
                        Visibility: ${avgVisibility.toFixed(2)} m\n
                        Highest Temperature: ${maxTemp.toFixed(2)}°C\n
                        Lowest Temperature: ${minTemp.toFixed(2)}°C`);
                } else {
                    alert(`No valid data available for ${city} from ${startDate} to ${endDate}`);
                }
            } else {
                alert(`No data available for ${city} from ${startDate} to ${endDate}`);
            }
        });
}


document.getElementById('slider').addEventListener('input', function() {
    var date = this.value;
    loadData(date);
});

document.querySelectorAll('#filters input[type=checkbox]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        var date = document.getElementById('slider').value;
        loadData(date);
    });
});

document.getElementById('city').addEventListener('input', function() {
    var date = document.getElementById('slider').value;
    loadData(date);
});

document.getElementById('calculateAverage').addEventListener('click', function() {
    var startDate = document.getElementById('startDate').value;
    var endDate = document.getElementById('endDate').value;
    var city = document.getElementById('city').value.toLowerCase();
    if (startDate && endDate && city) {
        calculateAverage(startDate, endDate, city);
    } else {
        alert('Please enter a valid city and date range');
    }
});
