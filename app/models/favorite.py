import csv
from pathlib import Path

CSV_PATH = Path("app/data/favorites.csv")

def salvar_favorito(user_id, pokemon_id):
    arquivo_existe = CSV_PATH.exists()

    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not arquivo_existe:
            writer.writerow(["user_id", "pokemon_id"])

        writer.writerow([user_id, pokemon_id])

def listar_favoritos(user_id):
    favoritos = set()

    if not CSV_PATH.exists():
        return favoritos

    with open(CSV_PATH, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["user_id"]) == user_id:
                favoritos.add(int(row["pokemon_id"]))

    return favoritos