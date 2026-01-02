from flask import Blueprint, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app.models.favorite import salvar_favorito, remover_favorito, listar_favoritos

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