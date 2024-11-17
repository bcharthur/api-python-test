# blueprints/get_musique.py

import os
import logging
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from yt_dlp import YoutubeDL
from python.get_musique import download_audio
import copy

get_musique_bp = Blueprint('get_musique', __name__)

# Configuration des options yt_dlp pour extraire uniquement l'audio
YTDL_OPTIONS_AUDIO = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',  # Vous pouvez choisir un autre format comme 'm4a'
        'preferredquality': '192',
    }],
}

@get_musique_bp.route('/api/get_audio', methods=['GET'])
def get_audio():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    # Définir le répertoire de cache pour les musiques
    cache_dir = os.path.join(current_app.root_path, 'musique')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        logging.info(f"[get_musique] Dossier 'musique' créé à {cache_dir}")

    # Supprimer les anciennes musiques dans le cache
    try:
        for filename in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"[get_musique] Supprimé: {file_path}")
    except Exception as e:
        logging.error(f"[get_musique] Erreur lors de la suppression des anciennes musiques: {e}")
        return jsonify({'error': 'Erreur lors de la gestion du cache'}), 500

    # Copier les options et définir 'outtmpl' pour enregistrer dans 'cache_dir'
    ytdl_options = copy.deepcopy(YTDL_OPTIONS_AUDIO)
    ytdl_options['outtmpl'] = os.path.join(cache_dir, '%(id)s.%(ext)s')  # Enregistrer dans 'musique'

    # Utiliser yt_dlp pour extraire et télécharger l'audio
    try:
        audio_filepath = download_audio(url, cache_dir, ytdl_options)
        if not audio_filepath or not os.path.exists(audio_filepath):
            logging.error(f"[get_musique] Échec du téléchargement de l'audio pour l'URL: {url}")
            return jsonify({'error': 'Échec du téléchargement de l\'audio'}), 500

        # Déterminer le nom de fichier pour servir
        filename = os.path.basename(audio_filepath)
        audio_url_cached = f"/musique/{filename}"
        return jsonify({'audio_url': audio_url_cached}), 200

    except Exception as e:
        logging.error(f"[get_musique] Erreur lors de l'extraction des informations: {e}")
        return jsonify({'error': 'Erreur lors de l\'extraction des informations de la vidéo'}), 500

@get_musique_bp.route('/musique/<path:filename>', methods=['GET'])
def serve_audio(filename):
    cache_dir = os.path.join(current_app.root_path, 'musique')
    return send_from_directory(cache_dir, filename, as_attachment=True)
