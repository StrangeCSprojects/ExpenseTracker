# Import the Flask application factory and database instance from the app package
from app import create_app, db

# Create a configured Flask app instance using the application factory
app = create_app()

# Set the WSGI-compatible entry point for deployment tools like Zappa
application = app

# Create all database tables within the application context
with app.app_context():
    db.create_all()
    print("Database tables created.")

