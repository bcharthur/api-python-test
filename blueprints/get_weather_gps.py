# blueprints/get_weather_gps.py
from flask import Blueprint, request, jsonify
import logging
from python.get_weather_gps import get_weather_gps

get_weather_gps_bp = Blueprint('get_weather_gps_bp', __name__)


@get_weather_gps_bp.route('/api/get-weather-gps', methods=['GET'])
def get_weather_gps_route():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    logging.info(f"[GET_WEATHER_GPS] Requête reçue avec latitude={lat}, longitude={lon}")

    if not lat or not lon:
        logging.warning("[GET_WEATHER_GPS] Latitude et/ou longitude manquantes dans la requête.")
        return jsonify({'status': 'error', 'message': 'Latitude et longitude manquantes.'}), 400

    try:
        latitude = float(lat)
        longitude = float(lon)
    except ValueError as e:
        logging.error(f"[GET_WEATHER_GPS] Conversion des paramètres échouée: {e}")
        return jsonify({'status': 'error', 'message': 'Latitude et longitude doivent être des nombres valides.'}), 400

    try:
        weather = get_weather_gps(latitude, longitude)
        logging.info(
            f"[GET_WEATHER_GPS] Données météorologiques récupérées pour les coordonnées ({latitude}, {longitude}): {weather}")
        return jsonify({'status': 'success', 'weather': weather})
    except Exception as e:
        logging.exception(f"[GET_WEATHER_GPS] Erreur lors de la récupération des données météo: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
