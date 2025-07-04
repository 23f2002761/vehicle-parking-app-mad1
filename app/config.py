import os

class Config:
    SECRET_KEY = 'your_secret_key'  # You can make this anything
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parking_app.db'  # SQLite DB file
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Just turns off a warning
