
from utilidades.pokeapi import download_imagem, pega_cadeia_evolucao, pegar_dados_pokemon, pegar_dados_species_pokemon, pegar_fraquezas
from utilidades.pokemons_csv import salvar_csv, validar_linhas

def extrair_campos(pokemon_json, species_json):
    # Extrai somente os campos usados no CSV final.

    id = pokemon_json["id"]
    nome = pokemon_json["name"]

    tipo1 = pokemon_json["types"][0]["type"]["name"]
    tipo2 = pokemon_json["types"][1]["type"]["name"] if len(pokemon_json["types"]) > 1 else ""

    # Pega a url da imagem oficial
    imagem = f"{id}.png"

    altura = pokemon_json["height"]
    peso = pokemon_json["weight"]

    # Categoria "genus" dentro do species_json
    categoria = ""
    for valor in species_json["genera"]:
        if valor["language"]["name"] == "en":
            categoria = valor["genus"]
            break

    lista_evolucoes = pega_cadeia_evolucao(species_json)
    evolucoes = " | ".join(lista_evolucoes)

    lista_habilidades = [habilidade["ability"]["name"] for habilidade in pokemon_json["abilities"]]
    habilidades = "|".join(sorted(lista_habilidades))

    lista_fraquezas = pegar_fraquezas(tipo1, tipo2)
    fraquezas = " | ".join(sorted(lista_fraquezas))

    return {
        "id": id,
        "nome": nome,
        "tipo1": tipo1,
        "tipo2": tipo2,
        "imagem": imagem,
        "altura": altura,
        "peso": peso,
        "categoria": categoria,
        "habilidades": habilidades,
        "evolucoes": evolucoes,
        "fraquezas": fraquezas
    }

def main():
    linha = []

    for pokemon_id in range(1, 100): # Teste inicial apenas com pokemons de Kanto
        print(f"Processando Pokémon {pokemon_id}...")

        pokemon_json = pegar_dados_pokemon(pokemon_id)
        species_json = pegar_dados_species_pokemon(pokemon_id)

        if not pokemon_json or not species_json:
            continue

        dados = extrair_campos(pokemon_json, species_json)
        linha.append(dados)

        url_imagem = pokemon_json["sprites"]["other"]["official-artwork"]["front_default"]
        download_imagem(pokemon_id, url_imagem)

    validar_linhas(linha)
    salvar_csv(linha)

main()