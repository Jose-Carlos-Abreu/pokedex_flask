import csv
from pathlib import Path

CSV_PATH = Path("app/data/favorites.csv")

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


def salvar_favorito(user_id, pokemon_id):
    arquivo_existe = CSV_PATH.exists()

    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not arquivo_existe:
            writer.writerow(["user_id", "pokemon_id"])

        writer.writerow([user_id, pokemon_id])


def remover_favorito(user_id, pokemon_id):
    if not CSV_PATH.exists():
        return

    linhas = []

    with open(CSV_PATH, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not (
                int(row["user_id"]) == user_id and
                int(row["pokemon_id"]) == pokemon_id
            ):
                linhas.append(row)

    with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "pokemon_id"])
        writer.writeheader()
        writer.writerows(linhas)
