# app.py

import os
import logging
from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS

from blueprints.get_weather import get_weather_bp
from blueprints.get_weather_gps import get_weather_gps_bp
from blueprints.download import download_bp
from blueprints.get_title import get_title_bp  # Assurez-vous que ce blueprint existe

from blueprints.create import create_bp
from blueprints.edit import edit_bp
from blueprints.delete import delete_bp
from blueprints.list import list_bp

from flask_mysqldb import MySQL

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,  # Utilisez DEBUG pour plus de détails si nécessaire
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')  # Enregistre les logs dans 'app.log'
    ]
)

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Configuration
DOWNLOAD_FOLDER = os.path.join(app.root_path, 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    os.chmod(DOWNLOAD_FOLDER, 0o755)  # Permissions en lecture/écriture/exécution pour le propriétaire et lecture/exécution pour les autres
    logging.info(f"[APP] Dossier 'downloads' créé à {DOWNLOAD_FOLDER}")

# Enregistrer les Blueprints
app.register_blueprint(get_weather_bp)
app.register_blueprint(get_weather_gps_bp)
app.register_blueprint(download_bp)
app.register_blueprint(get_title_bp)  # Assurez-vous que ce blueprint est défini

app.register_blueprint(create_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(list_bp)

# Ajouter la configuration de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Mettez votre mot de passe MySQL ici
app.config['MYSQL_DB'] = 'db_api_test'

# Initialiser MySQL
mysql = MySQL(app)

# Middleware pour loguer les requêtes
@app.before_request
def log_request_info():
    logging.info(f"Incoming request: {request.method} {request.url}")
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Body: {request.get_data()}")

@app.after_request
def log_response_info(response):
    if not response.direct_passthrough:
        try:
            response_data = response.get_data(as_text=True)
            logging.info(f"Response data: {response_data}")
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des données de la réponse: {e}")
    else:
        logging.info("Response data: [Passthrough mode, non enregistré]")
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/downloads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Remplacez debug=True par False en production
