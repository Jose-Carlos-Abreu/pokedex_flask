from flask import Blueprint, request, session, render_template, redirect, url_for
from models.home import get_all_pokemon_suggestions, formatar_pokemon, fetch_pokemon_detail
from flask_login import LoginManager, login_required, current_user
import requests
from concurrent.futures import ThreadPoolExecutor
import math

app = Blueprint("home", __name__)

POKEMONS_POR_PAGINA = 12
POKEMON_NAMES_URL = "https://pokeapi.co/api/v2/pokemon?limit=10000" 

SUGESTOES_COM_IMAGEM = get_all_pokemon_suggestions()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nome_buscado = request.form.get('nome_pokemon').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{nome_buscado}"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            session['search_result'] = formatar_pokemon(resposta.json())
            session.pop('error', None)
        else:
            session['error'] = "Pokémon não encontrado."
            session.pop('search_result', None)
            
        return redirect(url_for('home.home', logado=current_user.is_authenticated))
    
    if session.get('search_result') or session.get('error'):
        pokemons = []
        erro = session.get('error')
        
        if session.get('search_result'):
            pokemons.append(session['search_result'])

        session.pop('search_result', None)
        session.pop('error', None)
        
        return render_template('home.html', 
                               pokemons=pokemons, 
                               erro=erro, 
                               sugestoes_com_imagem=SUGESTOES_COM_IMAGEM, 
                               page=1, 
                               total_paginas=1,
                               logado=current_user.is_authenticated) 

    pokemons = []
    erro = None
    total_pokemons = 0
    
    page = request.args.get('page', 1, type=int) 
    offset = (page - 1) * POKEMONS_POR_PAGINA

    url_bloco = f"https://pokeapi.co/api/v2/pokemon?limit={POKEMONS_POR_PAGINA}&offset={offset}"
    resp_bloco = requests.get(url_bloco)
    
    if resp_bloco.status_code == 200:
        dados_bloco = resp_bloco.json()
        total_pokemons = dados_bloco['count']
        
        urls_detalhe = [item['url'] for item in dados_bloco['results']]

        with ThreadPoolExecutor(max_workers=POKEMONS_POR_PAGINA) as executor:
            resultados_raw = executor.map(fetch_pokemon_detail, urls_detalhe)
            pokemons = [p for p in resultados_raw if p is not None]
    else:
        total_pokemons = 0
        erro = "Não foi possível carregar o catálogo de Pokémons."

    total_paginas = math.ceil(total_pokemons / POKEMONS_POR_PAGINA) if total_pokemons > 0 else 1
    
    return render_template('home.html', 
                           pokemons=pokemons, 
                           erro=erro, 
                           sugestoes_com_imagem=SUGESTOES_COM_IMAGEM,
                           page=page,
                           total_paginas=total_paginas,
                           logado=current_user.is_authenticated)
