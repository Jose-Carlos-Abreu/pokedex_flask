from flask import Blueprint, request, render_template, abort
from flask_login import current_user
from app.models.home import carregar_pokemons, buscar_pokemon_por_nome
import csv

home_bp = Blueprint("home", __name__)

POKEMONS_POR_PAGINA = 200

@home_bp.route('/')
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

@home_bp.route("/pokemon/<int:pokemon_id>")
def pokemon_detail(pokemon_id):
    pokemon = None
    evolutions = []

    with open("app/data/pokemons.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if int(row["id"]) == pokemon_id:
                pokemon = row
                break

    if not pokemon:
        abort(404)

    # PROCESSAR EVOLUÇÕES
    if pokemon.get("evolucoes"):
        nomes = pokemon["evolucoes"].split("|")

        for nome in nomes:
            evo = buscar_pokemon_por_nome(nome)
            if evo:
                evolutions.append(evo)

    return render_template(
        "pokemon_detail.html",
        pokemon=pokemon,
        evolutions=evolutions
    )