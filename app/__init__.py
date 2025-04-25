# Import core Flask extensions for database, login, and CSRF protection
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Initialize global extension instances to be configured in the app factory
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    This function acts as the application factory. It sets up core app configurations,
    initializes extensions such as SQLAlchemy, Flask-Login, and CSRF protection,
    and registers application blueprints for routing.

    Returns:
        Flask: A fully configured Flask application instance.
    """
    app = Flask(__name__)

    # Application configuration settings
    app.config['SECRET_KEY'] = 'dV2X+6Frh8g2x9dNLU/DzUWFU5gkmyP9ob4rXieo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:expensetracker@expensetracker.crm4oyaco2kc.us-west-2.rds.amazonaws.com:3306/expenseTracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import and register route blueprints
    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Import models for user loading
    from .models import User

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        """
        Callback function for Flask-Login to load a user by ID.

        Params:
            user_id (str): The user's unique ID (as a string).

        Returns:
            User: The user object retrieved from the database.
        """
        return User.query.get(int(user_id))

    return app
