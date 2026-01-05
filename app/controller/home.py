from flask import Blueprint, request, render_template, abort, jsonify
from flask_login import current_user
from app.models.home import carregar_pokemons, buscar_pokemon_por_nome, listar_tipos, buscar_pokemons_por_prefixo
from app.models.favorite import listar_favoritos
import csv
import os

home_bp = Blueprint("home", __name__)

POKEMONS_POR_PAGINA = 200

@home_bp.route('/')
def home():
    pokemons = carregar_pokemons()
    tipos = listar_tipos()

    favoritos = set()
    if current_user.is_authenticated:
        favoritos = listar_favoritos(current_user.id)

    team_ids = set()
    if current_user.is_authenticated:
        caminho = os.path.join('app', 'data', 'teams.csv')
        if os.path.exists(caminho):
            with open(caminho, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('usuario_id') == str(current_user.id):
                        poks = row.get('pokemons', '')
                        if poks:
                            for pid in poks.split(';'):
                                if pid:
                                    team_ids.add(int(pid))
                        break

    search = request.args.get('search', '').lower()
    tipo_selecionado = request.args.get('tipo', '').lower()
    
    if search:
        pokemons = [
            p for p in pokemons
            if search in p['nome'].lower() or search == str(p['id'])
        ]

    if tipo_selecionado:
        pokemons = [
            p for p in pokemons
            if tipo_selecionado in (p['tipo1'], p['tipo2'])
        ]

    page = request.args.get('page', 1, type=int)
    inicio = (page - 1) * POKEMONS_POR_PAGINA
    fim = inicio + POKEMONS_POR_PAGINA

    total_paginas = (len(pokemons) - 1) // POKEMONS_POR_PAGINA + 1

    return render_template(
        'home.html',
        pokemons=pokemons[inicio:fim],
        tipos=tipos,
        favoritos=favoritos,
        team_ids=team_ids,
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

@home_bp.route("/api/pokemons/search")
def api_search_pokemons():
    query = request.args.get("q", "").strip()

    if len(query) < 2:
        return jsonify([])

    resultados = buscar_pokemons_por_prefixo(query)
    return jsonify(resultados)

