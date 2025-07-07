import os
from datetime import datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # API Configuration
    ANIMEKITA_API_BASE = 'https://apps.animekita.org/api/v1.1.6'
    
    # App Configuration
    DEBUG = False
    TESTING = False
    
    # Template Configuration
    TEMPLATES_AUTO_RELOAD = True
    
    # Cache Configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    @staticmethod
    def init_app(app):
        # Add current year to template context
        @app.context_processor
        def inject_current_year():
            return {'current_year': datetime.now().year}

class DevelopmentConfig(Config):
    DEBUG = False
    
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
