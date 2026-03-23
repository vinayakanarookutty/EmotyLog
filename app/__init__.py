from flask import Flask
import google.generativeai as genai
from .config import Config
from .extensions import mongo, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    mongo.init_app(app)
    bcrypt.init_app(app)

    # Configure AI
    genai.configure(api_key=app.config['GEMINI_API_KEY'])

    # Register Blueprints (Routes)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app