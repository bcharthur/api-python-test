# python/get_info.py
import yt_dlp
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)

def get_video_info(url):
    """
    Récupère les informations de la vidéo YouTube, y compris le titre.
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'video')
        return {
            "title": title,
        }
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des informations de la vidéo : {e}")
        raise
