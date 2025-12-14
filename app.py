from flask import Flask, redirect, url_for
from app.controller.usuario import app as usercontroller
from app.controller.home import app as homecontroller
from flask_login import LoginManager 
from app.models.usuario import db, Usuario
import os, subprocess

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.sqlite3'

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'chave_generica_para_dev_local')

app.register_blueprint(usercontroller, url_prefix="/pokedex/")
app.register_blueprint(homecontroller, url_prefix="/pokedex/")

@app.route('/')
def index():
    return redirect(url_for('home.home'))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'usuarios.login' 

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def executar_preprocessamento():
    csv_ok = os.path.exists("app/data/pokemons.csv")
    imgs_ok = os.path.isdir("app/static/images/pokemons") and len(os.listdir("app/static/images/pokemons")) > 0

    if not csv_ok or not imgs_ok:
        print("\n[AVISO] Gerando CSV e imagens...\n")
        subprocess.run(["python", r"app\static\py\pre_processamento.py"], check=True)

executar_preprocessamento()

if __name__ == '__main__':
    db.init_app(app=app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)