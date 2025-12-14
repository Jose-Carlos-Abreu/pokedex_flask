from flask import Blueprint, request, render_template
from flask_login import current_user
from app.models.pokemon_csv import carregar_pokemons

app = Blueprint("home", __name__)

POKEMONS_POR_PAGINA = 100

@app.route('/')
def home():
    pokemons = carregar_pokemons()

    search = request.args.get('search', '').lower()
    tipo = request.args.get('tipo')

    if search:
        pokemons = [
            p for p in pokemons
            if search in p['nome'].lower() or search == str(p['id'])
        ]

    if tipo:
        pokemons = [
            p for p in pokemons
            if tipo in (p['tipo1'], p['tipo2'])
        ]

    page = request.args.get('page', 1, type=int)
    inicio = (page - 1) * POKEMONS_POR_PAGINA
    fim = inicio + POKEMONS_POR_PAGINA

    total_paginas = (len(pokemons) - 1) // POKEMONS_POR_PAGINA + 1

    return render_template(
        'home.html',
        pokemons=pokemons[inicio:fim],
        page=page,
        total_paginas=total_paginas,
        logado=current_user.is_authenticated
    )