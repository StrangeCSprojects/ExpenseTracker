# Import the application factory and database instance from the app package
from app import create_app, db

# Create a Flask app instance using the application factory
app = create_app()

# Initialize the application context and create all database tables
with app.app_context():
    db.create_all()
    print("Database tables created.")
