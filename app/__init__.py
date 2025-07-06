from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
     app = Flask(__name__)
     app.config.from_object(Config) 
     db.init_app(app)

     #Registering the blue print
     from app.routes.auth_routes import authentication_bp
     app.register_blueprint(authentication_bp)
     
     from app.routes.dashboard_routes import dashboard_bp
     app.register_blueprint(dashboard_bp)
     return app