# python/get_musique.py

import os
import logging
from yt_dlp import YoutubeDL


def download_audio(url, cache_dir, ytdl_options):
    """
    Télécharge l'audio d'une vidéo à partir de son URL et l'enregistre dans le répertoire de cache.

    Args:
        url (str): URL de la vidéo.
        cache_dir (str): Chemin du répertoire de cache.
        ytdl_options (dict): Options pour yt_dlp.

    Returns:
        str: Chemin complet du fichier audio téléchargé ou None en cas d'échec.
    """
    try:
        with YoutubeDL(ytdl_options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Obtenir le chemin du fichier téléchargé
            downloaded_file = info_dict.get('filepath')
            if not downloaded_file:
                # Fallback si 'filepath' n'est pas présent
                downloaded_file = ydl.prepare_filename(info_dict)
                # Postprocessing est déjà effectué par yt_dlp, donc on doit vérifier le format
                # Exemple : si 'preferredcodec' est 'mp3', on change l'extension
                base, ext = os.path.splitext(downloaded_file)
                downloaded_file = f"{base}.mp3"
                if not os.path.exists(downloaded_file):
                    logging.error(f"[download_audio] Fichier audio converti non trouvé: {downloaded_file}")
                    return None
            logging.info(f"[download_audio] Audio téléchargé à {downloaded_file}")
            return downloaded_file
    except Exception as e:
        logging.error(f"[download_audio] Erreur lors du téléchargement de l'audio: {e}")
        return None
