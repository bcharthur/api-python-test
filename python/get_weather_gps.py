# python/get_weather_gps.py
import requests
import logging

def get_weather_gps(lat, lon):
    """
    Récupère les informations météorologiques basées sur les coordonnées GPS.

    :param lat: Latitude (float)
    :param lon: Longitude (float)
    :return: Dictionnaire contenant les informations météorologiques
    """
    try:
        # Appel à l'API Open-Meteo
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "timezone": "Europe/Paris"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        current_weather = data.get("current_weather")
        if not current_weather:
            raise ValueError("Données météorologiques non disponibles.")

        weather_info = {
            "latitude": lat,
            "longitude": lon,
            "temperature": current_weather.get("temperature"),
            "windspeed": current_weather.get("windspeed"),
            "winddirection": current_weather.get("winddirection"),
            "weathercode": current_weather.get("weathercode"),
            "time": current_weather.get("time")
        }

        logging.info(f"Météo récupérée pour les coordonnées ({lat}, {lon}): {weather_info}")
        return weather_info

    except requests.exceptions.RequestException as e:
        logging.exception(f"Erreur de requête HTTP: {e}")
        raise
    except Exception as e:
        logging.exception(f"Erreur lors de la récupération de la météo: {e}")
        raise
