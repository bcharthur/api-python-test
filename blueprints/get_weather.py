# blueprints/get_weather.py
from flask import Blueprint, request, jsonify
import logging
from python.get_weather import get_weather

get_weather_bp = Blueprint('get_weather_bp', __name__)


@get_weather_bp.route('/api/get-weather', methods=['GET'])
def get_weather_route():
    dept_number = request.args.get('dept_number')
    logging.info(f"[GET_WEATHER] Requête reçue avec dept_number={dept_number}")

    if not dept_number:
        logging.warning("[GET_WEATHER] Numéro de département manquant dans la requête.")
        return jsonify({'status': 'error', 'message': 'Numéro de département manquant.'}), 400

    try:
        weather = get_weather(dept_number)
        logging.info(f"[GET_WEATHER] Données météorologiques récupérées pour le département {dept_number}: {weather}")
        return jsonify({'status': 'success', 'weather': weather})
    except Exception as e:
        logging.error(f"[GET_WEATHER] Erreur lors de la récupération des données météo: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
