from .auth.signup import signup_bp
from .auth.signin import signin_bp  # Import the signin blueprint
from .auth.logout import logout_bp  # Import the logout blueprint
from .admin.auth import admin_auth_bp  # Import the admin auth blueprint
from .admin.exercisescontroller import exercises_bp  # Import the exercises management blueprint
from .admin.storecontroller import store_bp  # Import the store management blueprint
from .admin.trainerscontroller import trainers_bp  # Import the trainers management blueprint
from .careers.routes import careers_bp  # Import the careers blueprint

def register_routes(app):
    # Register authentication blueprints
    app.register_blueprint(signup_bp)
    app.register_blueprint(signin_bp)
    app.register_blueprint(logout_bp)
    
    # Register admin-related blueprints
    app.register_blueprint(admin_auth_bp)  # Admin auth blueprint
    app.register_blueprint(store_bp)  # Store management blueprint
    app.register_blueprint(exercises_bp)  # Exercises management blueprint
    app.register_blueprint(trainers_bp)  # Trainers management blueprint

    # Register other blueprints
   
    app.register_blueprint(careers_bp)  # Register careers blueprint
