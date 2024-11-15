// static/js/get-weather.js
document.addEventListener('DOMContentLoaded', function() {
    const getWeatherForm = document.getElementById('getWeatherForm');
    const weatherResultDiv = document.getElementById('weatherResult');

    getWeatherForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche le rechargement de la page
        const deptNumber = document.getElementById('weather_dept').value.trim();
        if (!deptNumber) {
            alert('Veuillez entrer un numéro de département valide.');
            return;
        }

        // Validation simple du numéro de département (01 à 95, 2A, 2B)
        const deptRegex = /^(0[1-9]|[1-8]\d|9[0-5]|2A|2B)$/;
        if (!deptRegex.test(deptNumber)) {
            alert('Veuillez entrer un numéro de département français valide (01 à 95, 2A, 2B).');
            return;
        }

        const encodedDept = encodeURIComponent(deptNumber);
        console.log(`Encoded Department for get-weather: ${encodedDept}`);

        fetch(`/api/get-weather?dept_number=${encodedDept}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const weather = data.weather;
                    weatherResultDiv.innerHTML = `
                        <div class="alert alert-info" role="alert">
                            <h5>Météo pour le Département ${deptNumber} (${weather.department}):</h5>
                            <ul class="list-unstyled">
                                <li><strong>Température:</strong> ${weather.temperature}°C</li>
                                <li><strong>Vitesse du vent:</strong> ${weather.windspeed} km/h</li>
                                <li><strong>Direction du vent:</strong> ${weather.winddirection}°</li>
                                <li><strong>Code météo:</strong> ${weather.weathercode}</li>
                                <li><strong>Heure:</strong> ${weather.time}</li>
                            </ul>
                        </div>
                    `;
                } else {
                    weatherResultDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${data.message}</div>`;
                }
            })
            .catch(err => {
                weatherResultDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${err}</div>`;
            });
    });
});
