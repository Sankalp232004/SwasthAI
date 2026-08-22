"""
SwasthAI - Deterministic Medical Triage System
Flask Application Factory
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    """Application factory."""
    
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from routes.patient_routes import patient_bp
    from routes.doctor_routes import doctor_bp
    from routes.api_routes import api_bp
    from routes.sse_routes import sse_bp
    from routes.superadmin_routes import superadmin_bp
    
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(sse_bp, url_prefix='/sse')
    app.register_blueprint(superadmin_bp, url_prefix='/superadmin')

    # Health check endpoint for Railway/load balancers
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    # Tables are managed by Flask-Migrate (flask db upgrade)
    # Do not use db.create_all() as it conflicts with migrations
    
    return app
