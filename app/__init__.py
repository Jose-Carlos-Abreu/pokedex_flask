from flask import Flask
from config import *
import csv
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "senha_teste" # Chave de sessão (trocar por CHAVE_SECRETA_FLASK)

    from .routes import bp
    app.register_blueprint(bp)

    return app