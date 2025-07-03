from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Initialize
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login_page" # type: ignore
login_manager.login_message_category = "info"
csrf = CSRFProtect()


def create_app(config_class="Development"):
    app = Flask(__name__)

    # Load config
    from app.config import config_by_name
    app.config.from_object(config_by_name[config_class])

    # Initialize with app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    from app.routes.auth_routes import bp as AuthBlueprint
    from app.routes.navigation_routes import bp as NavigaionBlueprint
    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(NavigaionBlueprint)
    
    # Models for migrations
    from app.models import user_model

    return app
