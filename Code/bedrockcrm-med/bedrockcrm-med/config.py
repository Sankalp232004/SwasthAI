"""
SwasthAI Configuration
Deterministic Medical Triage System
"""

import os
from datetime import timedelta


class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'swasthai-dev-secret-key-change-in-production')
    
    # Database
    # Railway sometimes provides 'postgres://' but SQLAlchemy requires 'postgresql://'
    _db_url = os.environ.get('DATABASE_URL', 'postgresql://localhost/swasthai')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1) if _db_url.startswith('postgres://') else _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # Public base URL used when no explicit system setting is stored yet.
    APP_BASE_URL = os.environ.get('APP_BASE_URL', 'https://swasthai.roadto405.xyz').rstrip('/')
    
    # Triage Engine Version (for audit trail)
    TRIAGE_ENGINE_VERSION = "1.0.0"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
