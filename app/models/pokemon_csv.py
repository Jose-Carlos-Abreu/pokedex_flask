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