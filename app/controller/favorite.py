from flask import Blueprint, redirect, url_for, flash, request, jsonify, render_template
from flask_login import current_user, login_required
from app.models.favorite import salvar_favorito, remover_favorito, listar_favoritos
from app.models.home import carregar_pokemons

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/toggle/<int:pokemon_id>", methods=["POST"])
@login_required
def toggle(pokemon_id):
    favoritos = listar_favoritos(current_user.id)

    if pokemon_id in favoritos:
        remover_favorito(current_user.id, pokemon_id)
        return jsonify({
            "status": "removed",
            "pokemon_id": pokemon_id
        })
    else:
        salvar_favorito(current_user.id, pokemon_id)
        return jsonify({
            "status": "added",
            "pokemon_id": pokemon_id
        })

@favorite_bp.route("/favorites")
@login_required
def favorites():
    favoritos_ids = listar_favoritos(current_user.id)

    pokemons = carregar_pokemons()

    favoritos = [
        p for p in pokemons
        if p["id"] in favoritos_ids
    ]

    return render_template(
        "favorites.html",
        pokemons=favoritos
    )