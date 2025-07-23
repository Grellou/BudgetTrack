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
login_manager.login_view = "auth.login_page"  # type: ignore
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
    from app.routes.navigation_routes import bp as NavigationBlueprint
    from app.routes.category_routes import bp as CategoriesBlueprint
    from app.routes.expense_routes import bp as ExpensesBlueprint
    from app.routes.income_routes import bp as IncomesBlueprint
    from app.routes.dashboard_routes import bp as DashboardBlueprint

    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(NavigationBlueprint)
    app.register_blueprint(CategoriesBlueprint)
    app.register_blueprint(ExpensesBlueprint)
    app.register_blueprint(IncomesBlueprint)
    app.register_blueprint(DashboardBlueprint)

    # Models for migrations
    from app.models import user_model, category_model, expense_model, income_model, credit_model 

    # CLI commands
    @app.cli.command("seed-categories")
    def seed_categories_command():
        from app.utils.seed_data import seed_default_categories

        count = seed_default_categories()
        return f"{count} categories added successfully!"

    return app
