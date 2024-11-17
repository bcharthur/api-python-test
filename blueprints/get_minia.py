# blueprints/get_minia.py

import os
import logging
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from yt_dlp import YoutubeDL
import requests

get_minia_bp = Blueprint('get_minia', __name__)

# Configuration des options yt_dlp
YTDL_OPTIONS = {
    'format': 'best',
    'noplaylist': True,
    'quiet': True,
    'skip_download': True,
}

@get_minia_bp.route('/api/get_thumbnail', methods=['GET'])
def get_thumbnail():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    # Vérifier si la miniature est déjà en cache
    cache_dir = os.path.join(current_app.root_path, 'minia')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        logging.info(f"[get_minia] Dossier 'minia' créé à {cache_dir}")

    # Utiliser yt_dlp pour extraire les informations de la vidéo
    try:
        with YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            thumbnail_url = info.get('thumbnail')
            if not thumbnail_url:
                return jsonify({'error': 'Miniature non trouvée'}), 404

            # Déterminer le nom de fichier de la miniature
            video_id = info.get('id')
            ext = os.path.splitext(thumbnail_url)[1].split('?')[0]  # Obtenir l'extension sans les paramètres URL
            filename = f"{video_id}{ext}"
            filepath = os.path.join(cache_dir, filename)

            # Vérifier si la miniature est déjà téléchargée
            if not os.path.exists(filepath):
                logging.info(f"[get_minia] Téléchargement de la miniature depuis {thumbnail_url}")
                response = requests.get(thumbnail_url, stream=True)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                else:
                    return jsonify({'error': 'Échec du téléchargement de la miniature'}), 500

            # Retourner l'URL de la miniature
            thumbnail_url_cached = f"/minia/{filename}"
            return jsonify({'thumbnail_url': thumbnail_url_cached}), 200

    except Exception as e:
        logging.error(f"[get_minia] Erreur lors de l'extraction des informations: {e}")
        return jsonify({'error': 'Erreur lors de l\'extraction des informations de la vidéo'}), 500

@get_minia_bp.route('/minia/<path:filename>', methods=['GET'])
def serve_thumbnail(filename):
    cache_dir = os.path.join(current_app.root_path, 'minia')
    return send_from_directory(cache_dir, filename, as_attachment=False)
