from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from app.config import Config

db = SQLAlchemy()
migrate = Migrate() 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)  

    # Registering the blueprints
    from app.routes.auth_routes import authentication_bp
    app.register_blueprint(authentication_bp)
    
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
    
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from app.routes.__init__ import landing_bp
    app.register_blueprint(landing_bp)

    return app
