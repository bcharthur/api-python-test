# blueprints/get_title.py
from flask import Blueprint, request, jsonify
import logging
from python.get_info import get_video_info

get_title_bp = Blueprint('get_title_bp', __name__)

@get_title_bp.route('/api/get-title', methods=['GET'])
def get_title():
    ytb_url = request.args.get('ytb_url')
    logging.info(f"[GET_TITLE] URL reçue: {ytb_url}")
    if not ytb_url:
        return jsonify({'status': 'error', 'message': 'URL web manquante.'}), 400
    try:
        info = get_video_info(ytb_url)
        title = info.get('title', 'Titre non disponible')
        logging.info(f"[GET_TITLE] Titre récupéré: {title}")
        return jsonify({'status': 'success', 'title': title})
    except Exception as e:
        logging.error(f"[GET_TITLE] Erreur: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
