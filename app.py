from app import create_app 
import os, subprocess

def executar_preprocessamento():
    csv_ok = os.path.exists("app/data/pokemons.csv")
    imgs_ok = os.path.isdir("app/static/images/pokemons") and len(os.listdir("app/static/images/pokemons")) > 0

    if not csv_ok or not imgs_ok:
        print("\n[AVISO] Gerando CSV e imagens...\n")
        subprocess.run(["python", r"app\scripts\pre_processamento.py"], check=True)

executar_preprocessamento()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)