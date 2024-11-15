// static/js/get-weather-gps.js

document.addEventListener('DOMContentLoaded', function() {
    const getWeatherGPSBtn = document.getElementById('getWeatherGPSBtn');
    const weatherGPSResultDiv = document.getElementById('weatherGPSResult');

    getWeatherGPSBtn.addEventListener('click', function() {
        // Vérifier si le navigateur supporte la géolocalisation
        if ('geolocation' in navigator) {
            // Désactiver le bouton pendant la récupération
            getWeatherGPSBtn.disabled = true;
            weatherGPSResultDiv.innerHTML = `<div class="alert alert-info" role="alert">Récupération de la localisation...</div>`;

            // Options pour la géolocalisation
            const geoOptions = {
                enableHighAccuracy: true,
                timeout: 10000, // 10 secondes
                maximumAge: 0
            };

            // Demander la position de l'utilisateur
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    // Afficher les coordonnées obtenues (optionnel)
                    weatherGPSResultDiv.innerHTML = `
                        <div class="alert alert-info" role="alert">
                            Coordonnées obtenues: Latitude = ${latitude.toFixed(4)}, Longitude = ${longitude.toFixed(4)}
                        </div>
                    `;

                    // Appeler l'API Flask avec les coordonnées GPS
                    fetch(`/api/get-weather-gps?latitude=${latitude}&longitude=${longitude}`)
                        .then(response => {
                            if (!response.ok) {
                                return response.json().then(errData => { throw new Error(errData.message || 'Erreur lors de la récupération des données météo.'); });
                            }
                            return response.json();
                        })
                        .then(data => {
                            if (data.status === 'success') {
                                const weather = data.weather;
                                weatherGPSResultDiv.innerHTML += `
                                    <div class="alert alert-success" role="alert">
                                        <h5>Météo pour votre localisation :</h5>
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
                                weatherGPSResultDiv.innerHTML += `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${data.message}</div>`;
                            }
                        })
                        .catch(err => {
                            weatherGPSResultDiv.innerHTML += `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${err.message}</div>`;
                        })
                        .finally(() => {
                            // Réactiver le bouton après la récupération
                            getWeatherGPSBtn.disabled = false;
                        });
                },
                function(error) {
                    // Gérer les erreurs de géolocalisation
                    let errorMessage = '';
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            errorMessage = 'Permission de localisation refusée.';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMessage = 'Informations de localisation non disponibles.';
                            break;
                        case error.TIMEOUT:
                            errorMessage = 'Délai de récupération de la localisation dépassé.';
                            break;
                        case error.UNKNOWN_ERROR:
                            errorMessage = 'Une erreur inconnue est survenue.';
                            break;
                    }
                    weatherGPSResultDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${errorMessage}</div>`;
                    // Réactiver le bouton en cas d'erreur
                    getWeatherGPSBtn.disabled = false;
                },
                geoOptions
            );
        } else {
            // Géolocalisation non supportée par le navigateur
            weatherGPSResultDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> La géolocalisation n'est pas supportée par votre navigateur.</div>`;
        }
    });
});
