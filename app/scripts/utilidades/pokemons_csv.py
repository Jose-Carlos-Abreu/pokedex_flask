import csv
import os

CSV_CAMINHO = "app/data/pokemons.csv"

def salvar_csv(linhas):
    os.makedirs("app/data", exist_ok=True)

    header = ["id","nome","tipo1","tipo2","imagem","altura","peso","categoria","habilidades","evolucoes", "fraquezas"]

    with open(CSV_CAMINHO, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(linhas)

    print(f"[OK] CSV criado em {CSV_CAMINHO}")

def validar_linhas(linhas):
    ids = set() # coleção não ordenada de elementos únicos (sem repetição)
    for linha in linhas:
        if linha["id"] in ids:
            raise Exception(f"ID duplicado detectado: {linha['id']}")
        ids.add(linha["id"])

        for campo in ["id", "nome", "tipo1", "imagem"]:
            if not linha[campo]:
                raise Exception(f"Campo obrigatório vazio: {campo}")

    print("[OK] CSV validado sem erros")