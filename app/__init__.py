from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

# Initialize
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login" # type: ignore
login_manager.login_message_category = "info"


def create_app(config_class="Development"):
    app = Flask(__name__)

    # Load config
    from app.config import config_by_name
    app.config.from_object(config_by_name[config_class])

    # Initialize with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    
    # Models for migrations

    # Simple index for testing
    @app.route("/")
    def index():
        return "Budget Tracker is running!"

    return app
