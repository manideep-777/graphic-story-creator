"""
Configuration settings for the Graphic Story Creator application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
    
    # Flask settings
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    TESTING = False
    
    # Image generation settings
    FLUX_MODEL = "black-forest-labs/FLUX.1-dev"
    DEFAULT_IMAGE_SIZE = (1024, 1024)
    MAX_PROMPT_LENGTH = 500
    
    # Gemini settings
    GEMINI_MODEL = "gemini-1.5-flash"
    OPTIMIZATION_TEMPERATURE = 0.7
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        required_vars = ['GEMINI_API_KEY', 'HUGGINGFACE_API_KEY']
        missing = [var for var in required_vars if not getattr(Config, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
