import requests
from concurrent.futures import ThreadPoolExecutor
import math

POKEMON_NAMES_URL = "https://pokeapi.co/api/v2/pokemon?limit=10000"

def get_all_pokemon_suggestions():
    print("Iniciando a busca e cache de todos os nomes e URLs de imagem...")
    
    try:
        response = requests.get(POKEMON_NAMES_URL, timeout=10)
        pokemon_list = response.json().get('results', [])
        urls_detalhe = [item['url'] for item in pokemon_list]
    except Exception as e:
        print(f"Erro ao obter lista de nomes base: {e}")
        return []

    suggestions_data = []

    def fetch_suggestion_detail(url):
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'name': data['name'],
                    'imageUrl': data['sprites']['front_default']
                }
        except Exception:
            return None
        return None

    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(fetch_suggestion_detail, urls_detalhe)
        
        for result in results:
            if result:
                suggestions_data.append(result)
                
    print(f"Cache de dados de sugestão concluído. Total: {len(suggestions_data)} Pokémons.")
    return suggestions_data

def formatar_pokemon(dados):
    return {
        'nome': dados['name'].upper(),
        'id': dados['id'],
        'imagem': dados['sprites']['front_default'] or '',
        'tipo': dados['types'][0]['type']['name'].capitalize()
    }

def fetch_pokemon_detail(url):
    try:
        resp_detalhe = requests.get(url, timeout=5)
        if resp_detalhe.status_code == 200:
            return formatar_pokemon(resp_detalhe.json())
    except Exception:
        pass
    return None