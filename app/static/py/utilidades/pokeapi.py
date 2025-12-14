import requests
import os

POKEMON = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES = "https://pokeapi.co/api/v2/pokemon-species/"
IMG_DIR = "app/static/images/pokemons/"

def pegar_dados_pokemon(pokemon_id):
    # Coleta dados principais de um Pokémon.
    url = f"{POKEMON}{pokemon_id}"
    resposta = requests.get(url, timeout=10)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"falha ao recuperar dados {resposta.status_code}, url: {url}")
        return None

def pegar_dados_species_pokemon(pokemon_id):
    # Coleta dados da espécie (categoria, evoluções).
    url = f"{POKEMON_SPECIES}{pokemon_id}"
    resposta = requests.get(url, )
    if resposta.status_code == 200:
        return resposta.json() 
    else:
        print(f"falha ao recuperar dados {resposta.status_code}, url: {url}")
        return None

def download_imagem(pokemon_id, url):
    # Faz o download da imagem oficial do Pokémon e salva localmente em app/static/images/pokemons/<id>.png
    
    if url is None:
        print(f"[ERRO] Pokémon {pokemon_id} sem imagem disponível.")
        return

    os.makedirs(IMG_DIR, exist_ok=True)
    img_caminho = os.path.join(IMG_DIR, f"{pokemon_id}.png")

    try:
        resposta = requests.get(url, timeout=10)

        if resposta.status_code == 200:
            with open(img_caminho, "wb") as f:
                f.write(resposta.content)
            print(f"[IMG] Pokémon {pokemon_id} -> imagem salva em {img_caminho}")
        else:
            print(f"[ERRO] Falha ao baixar imagem do Pokémon {pokemon_id}")

    except Exception as e:
        print(f"[EXC] Erro ao baixar imagem do Pokémon {pokemon_id}: {e}")

def pega_cadeia_evolucao(species_json):
    # Recebe o species_json e retorna uma lista ordenada com todos os Pokémon da cadeia de evolução (por nome).
    
    evolucao_url = species_json["evolution_chain"]["url"]
    if not evolucao_url:
        return []

    try:
        resposta = requests.get(evolucao_url, timeout=10)
        if resposta.status_code == 200:
            evolucao_json = resposta.json()

            cadeia = evolucao_json["chain"]
            evolucao_lista = []

            def andar(cadeia):
                # Percorre recursivamente toda a cadeia.

                evolucao_lista.append(cadeia["species"]["name"])
                for proxima_evolucao in cadeia.get("evolves_to", []): # .get caso encontre retorna evolves_to, se não []
                    andar(proxima_evolucao)

            andar(cadeia)
            return evolucao_lista
        else:
            print(f"falha ao recuperar dados {resposta.status_code}, url: {evolucao_url}")
            return []
    except:
        return []
        
def pegar_fraquezas(tipo1, tipo2=""):
    tipos = [tipo1] + ([tipo2] if tipo2 else [])
    fraquezas = set() # coleção não ordenada de elementos únicos (sem repetição)

    for tipo in tipos:
        url = f"https://pokeapi.co/api/v2/type/{tipo}"
        resposta = requests.get(url, timeout=10)

        if resposta.status_code == 200:
            dados = resposta.json()
            for item in dados["damage_relations"]["double_damage_from"]:
                fraquezas.add(item["name"])
        else:
            print(f"Erro ao consultar tipo {tipo}: {resposta.status_code}")

    return fraquezas