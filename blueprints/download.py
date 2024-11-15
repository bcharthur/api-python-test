# blueprints/download.py

from flask import Blueprint, request, jsonify, send_file, current_app
import logging
import yt_dlp
import os

download_bp = Blueprint('download_bp', __name__)

@download_bp.route('/api/download', methods=['GET'])
def download_video():
    ytb_url = request.args.get('ytb_url')
    logging.info(f"[DOWNLOAD] Requête reçue avec ytb_url={ytb_url}")

    if not ytb_url:
        logging.warning("[DOWNLOAD] Paramètre 'ytb_url' manquant.")
        return jsonify({'status': 'error', 'message': 'Paramètre ytb_url manquant.'}), 400

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(current_app.root_path, 'downloads', '%(id)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,  # Activez les logs de yt-dlp pour le débogage
            'no_warnings': True,
            'restrictfilenames': True,  # Assure des noms de fichiers sécurisés
        }

        logging.info("[DOWNLOAD] Démarrage du téléchargement avec yt-dlp...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(ytb_url, download=True)
            # Récupérer le chemin absolu du fichier téléchargé
            download_path = info_dict.get('filepath', None)
            if not download_path:
                # Fallback si 'filepath' n'est pas présent
                video_id = info_dict.get('id', 'video')
                ext = info_dict.get('ext', 'mp4')
                download_path = os.path.join(current_app.root_path, 'downloads', f"{video_id}.{ext}")
                logging.info(f"[DOWNLOAD] Vidéo téléchargée avec succès: {download_path}")
            else:
                logging.info(f"[DOWNLOAD] Vidéo téléchargée avec succès: {download_path}")

        # Vérifier si le fichier existe
        if not os.path.exists(download_path):
            logging.error(f"[DOWNLOAD] Le fichier téléchargé n'existe pas: {download_path}")
            return jsonify({'status': 'error', 'message': 'Le fichier téléchargé est introuvable.'}), 500

        # Récupérer le nom du fichier
        filename = os.path.basename(download_path)
        logging.info(f"[DOWNLOAD] Nom du fichier à envoyer: {filename}")

        # Vérifier les permissions de lecture
        if not os.access(download_path, os.R_OK):
            logging.error(f"[DOWNLOAD] Le fichier téléchargé n'est pas accessible en lecture: {download_path}")
            return jsonify({'status': 'error', 'message': 'Le fichier téléchargé n\'est pas accessible.'}), 500

        # Retourner le fichier téléchargé
        logging.info(f"[DOWNLOAD] Envoi du fichier: {download_path}")
        return send_file(download_path, as_attachment=True)

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"[DOWNLOAD] yt-dlp Error: {e}")
        return jsonify({'status': 'error', 'message': 'Erreur lors du téléchargement avec yt-dlp.'}), 500
    except Exception as e:
        logging.exception(f"[DOWNLOAD] Erreur lors du téléchargement de la vidéo: {e}")
        return jsonify({'status': 'error', 'message': 'Erreur lors du téléchargement de la vidéo.'}), 500
