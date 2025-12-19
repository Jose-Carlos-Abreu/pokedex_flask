import csv
from pathlib import Path

CSV_PATH = Path("app/data/pokemons.csv")

def carregar_pokemons():
    pokemons = []

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pokemons.append({
                "id": int(row["id"]),
                "nome": row["nome"],
                "tipo1": row["tipo1"],
                "tipo2": row["tipo2"],
                "imagem": row["imagem"],
                "altura": row["altura"],
                "peso": row["peso"]
            })

    return pokemons

def buscar_pokemon_por_nome(nome):
    nome = nome.strip().lower()

    with open("app/data/pokemons.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["nome"].lower() == nome:
                return {
                    "id": int(row["id"]),
                    "nome": row["nome"],
                    "imagem": f"/static/images/pokemons/{row['imagem']}"
                }

    return None
