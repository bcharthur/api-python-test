# python/get_weather.py
import requests
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# Dictionnaire des coordonnées (latitude, longitude) pour les départements français
DEPARTMENTS_COORDINATES = {
    "01": {"name": "Ain", "lat": 46.1667, "lon": 5.6667},
    "02": {"name": "Aisne", "lat": 49.1167, "lon": 3.3},
    "03": {"name": "Allier", "lat": 46.1333, "lon": 3.4167},
    "04": {"name": "Alpes-de-Haute-Provence", "lat": 44.1, "lon": 6.1},
    "05": {"name": "Hautes-Alpes", "lat": 44.5, "lon": 6.1667},
    "06": {"name": "Alpes-Maritimes", "lat": 43.5833, "lon": 7.0833},
    "07": {"name": "Ardèche", "lat": 44.6667, "lon": 4.7667},
    "08": {"name": "Ardennes", "lat": 49.75, "lon": 4.75},
    "09": {"name": "Ariège", "lat": 42.0, "lon": 1.3333},
    "10": {"name": "Aube", "lat": 48.3, "lon": 4.0},
    "11": {"name": "Aude", "lat": 43.25, "lon": 2.3333},
    "12": {"name": "Aveyron", "lat": 44.0, "lon": 2.0},
    "13": {"name": "Bouches-du-Rhône", "lat": 43.3333, "lon": 5.3333},
    "14": {"name": "Calvados", "lat": 49.0, "lon": -0.5},
    "15": {"name": "Cantal", "lat": 45.3333, "lon": 2.0},
    "16": {"name": "Charente", "lat": 45.6667, "lon": 0.5},
    "17": {"name": "Charente-Maritime", "lat": 45.8333, "lon": -1.1667},
    "18": {"name": "Cher", "lat": 47.0, "lon": 2.3333},
    "19": {"name": "Corrèze", "lat": 45.7, "lon": 1.2},
    "20A": {"name": "Corse-du-Sud", "lat": 42.0, "lon": 9.0},
    "20B": {"name": "Haute-Corse", "lat": 42.5, "lon": 9.0},
    "21": {"name": "Côte-d'Or", "lat": 47.0, "lon": 5.0},
    "22": {"name": "Côtes-d'Armor", "lat": 48.15, "lon": -2.7},
    "23": {"name": "Creuse", "lat": 45.1667, "lon": 2.0},
    "24": {"name": "Dordogne", "lat": 45.1667, "lon": 1.25},
    "25": {"name": "Doubs", "lat": 47.3333, "lon": 6.3333},
    "26": {"name": "Drôme", "lat": 44.85, "lon": 5.95},
    "27": {"name": "Eure", "lat": 49.0833, "lon": 1.25},
    "28": {"name": "Eure-et-Loir", "lat": 48.2, "lon": 1.5833},
    "29": {"name": "Finistère", "lat": 48.3333, "lon": -4.3333},
    "30": {"name": "Gard", "lat": 43.8333, "lon": 4.0},
    "31": {"name": "Haute-Garonne", "lat": 43.6, "lon": 1.4333},
    "32": {"name": "Gers", "lat": 43.7, "lon": 0.7},
    "33": {"name": "Gironde", "lat": 44.8333, "lon": -0.5833},
    "34": {"name": "Hérault", "lat": 43.6667, "lon": 3.5},
    "35": {"name": "Ille-et-Vilaine", "lat": 48.1167, "lon": -1.6667},
    "36": {"name": "Indre", "lat": 46.0, "lon": 1.0},
    "37": {"name": "Indre-et-Loire", "lat": 47.4, "lon": 0.7},
    "38": {"name": "Isère", "lat": 45.1667, "lon": 5.7167},
    "39": {"name": "Jura", "lat": 46.6667, "lon": 5.6667},
    "40": {"name": "Landes", "lat": 43.6667, "lon": -1.0},
    "41": {"name": "Loir-et-Cher", "lat": 47.3333, "lon": 1.3333},
    "42": {"name": "Loire", "lat": 45.3, "lon": 4.05},
    "43": {"name": "Haute-Loire", "lat": 45.0, "lon": 3.75},
    "44": {"name": "Loire-Atlantique", "lat": 47.3, "lon": -2.2},
    "45": {"name": "Loiret", "lat": 47.75, "lon": 2.3333},
    "46": {"name": "Lot", "lat": 44.3, "lon": 1.3333},
    "47": {"name": "Lot-et-Garonne", "lat": 44.45, "lon": 0.55},
    "48": {"name": "Lozère", "lat": 44.0, "lon": 3.75},
    "49": {"name": "Maine-et-Loire", "lat": 47.3333, "lon": -0.5},
    "50": {"name": "Manche", "lat": 49.9167, "lon": -1.3333},
    "51": {"name": "Marne", "lat": 49.0, "lon": 4.0},
    "52": {"name": "Haute-Marne", "lat": 48.8333, "lon": 5.0},
    "53": {"name": "Mayenne", "lat": 48.0, "lon": -0.7},
    "54": {"name": "Meurthe-et-Moselle", "lat": 48.7, "lon": 6.2},
    "55": {"name": "Meuse", "lat": 49.1, "lon": 5.3333},
    "56": {"name": "Morbihan", "lat": 47.6667, "lon": -3.0},
    "57": {"name": "Moselle", "lat": 49.0, "lon": 6.2},
    "58": {"name": "Nièvre", "lat": 47.0, "lon": 3.0},
    "59": {"name": "Nord", "lat": 50.9167, "lon": 3.0667},
    "60": {"name": "Oise", "lat": 49.0, "lon": 2.0},
    "61": {"name": "Orne", "lat": 48.1667, "lon": -0.5},
    "62": {"name": "Pas-de-Calais", "lat": 50.9167, "lon": 2.0},
    "63": {"name": "Puy-de-Dôme", "lat": 45.3333, "lon": 3.0},
    "64": {"name": "Pyrénées-Atlantiques", "lat": 43.3333, "lon": -1.5},
    "65": {"name": "Hautes-Pyrénées", "lat": 43.0, "lon": 0.0},
    "66": {"name": "Pyrénées-Orientales", "lat": 42.6667, "lon": 2.0},
    "67": {"name": "Bas-Rhin", "lat": 48.5833, "lon": 7.75},
    "68": {"name": "Haut-Rhin", "lat": 47.75, "lon": 7.25},
    "69": {"name": "Rhône", "lat": 45.75, "lon": 4.85},
    "70": {"name": "Haute-Saône", "lat": 47.6667, "lon": 6.0},
    "71": {"name": "Saône-et-Loire", "lat": 46.3333, "lon": 4.0},
    "72": {"name": "Sarthe", "lat": 48.0, "lon": 0.0},
    "73": {"name": "Savoie", "lat": 45.6667, "lon": 6.1},
    "74": {"name": "Haute-Savoie", "lat": 45.8333, "lon": 6.0833},
    "75": {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    "76": {"name": "Seine-Maritime", "lat": 49.4333, "lon": 1.0833},
    "77": {"name": "Seine-et-Marne", "lat": 48.95, "lon": 2.5833},
    "78": {"name": "Yvelines", "lat": 48.8, "lon": 2.1667},
    "79": {"name": "Deux-Sèvres", "lat": 46.3333, "lon": -0.5},
    "80": {"name": "Somme", "lat": 49.9, "lon": 2.3},
    "81": {"name": "Tarn", "lat": 43.6, "lon": 2.0},
    "82": {"name": "Tarn-et-Garonne", "lat": 44.0, "lon": 1.5},
    "83": {"name": "Var", "lat": 43.5, "lon": 6.1667},
    "84": {"name": "Vaucluse", "lat": 43.8333, "lon": 5.1667},
    "85": {"name": "Vendée", "lat": 46.5, "lon": -1.0},
    "86": {"name": "Vienne", "lat": 46.5833, "lon": 0.3333},
    "87": {"name": "Haute-Vienne", "lat": 45.8333, "lon": 1.3333},
    "88": {"name": "Vosges", "lat": 48.0, "lon": 6.0},
    "89": {"name": "Yonne", "lat": 47.8333, "lon": 3.3333},
    "90": {"name": "Territoire de Belfort", "lat": 47.6333, "lon": 6.8667},
    "91": {"name": "Essonne", "lat": 48.6667, "lon": 2.45},
    "92": {"name": "Hauts-de-Seine", "lat": 48.85, "lon": 2.3},
    "93": {"name": "Seine-Saint-Denis", "lat": 48.9167, "lon": 2.45},
    "94": {"name": "Val-de-Marne", "lat": 48.8, "lon": 2.4333},
    "95": {"name": "Val-d'Oise", "lat": 49.05, "lon": 2.05},
}


def get_weather(department_number):
    """
    Récupère les informations météorologiques pour un département français donné.

    :param department_number: Numéro du département français (str)
    :return: Dictionnaire contenant les informations météorologiques
    """
    try:
        department = DEPARTMENTS_COORDINATES.get(department_number)
        if not department:
            raise ValueError(f"Département {department_number} non trouvé.")

        lat = department["lat"]
        lon = department["lon"]

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
            "department": department["name"],
            "temperature": current_weather.get("temperature"),
            "windspeed": current_weather.get("windspeed"),
            "winddirection": current_weather.get("winddirection"),
            "weathercode": current_weather.get("weathercode"),
            "time": current_weather.get("time")
        }

        logging.info(f"Météo récupérée pour le département {department_number} ({department['name']}): {weather_info}")
        return weather_info

    except Exception as e:
        logging.error(f"Erreur lors de la récupération de la météo: {e}")
        raise
