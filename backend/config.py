# Configuration settings for different environments

import os

class Config:
    DEBUG = False
    TESTING = False
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # API settings
    API_VERSION = 'v1'
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # CORS settings
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    # Gemini API configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_API_SECRET = os.environ.get('GEMINI_API_SECRET')

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
