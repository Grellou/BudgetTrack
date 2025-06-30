import os

# Get base directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Base config 
class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev118")

    # Db settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Development config
class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL",
                                             f"sqlite:///{os.path.join(base_dir, "../dev.db")}")

# Testing config
class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

# Production config
class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL",
                                             f"sqlite:///{os.path.join(base_dir, "../prod.db")}")

# Config dictionary
config_by_name = {
    "Development": Development,
    "Testing": Testing,
    "Production": Production
}
