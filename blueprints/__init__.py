# blueprints/__init__.py
from .get_title import get_title_bp
from .download import download_bp
from .get_weather import get_weather_bp

def register_blueprints(app):
    app.register_blueprint(get_title_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(get_weather_bp)
