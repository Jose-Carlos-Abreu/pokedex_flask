from flask import Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.favorite import salvar_favorito

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/<int:pokemon_id>", methods=["POST"])
def toggle(pokemon_id):
    if not current_user.is_authenticated:
        flash("Faça login para favoritar um Pokémon.", "error")
        return redirect(url_for("usuarios.login"))

    salvar_favorito(current_user.id, pokemon_id)
    flash("Pokémon favoritado!", "success")
    return redirect(url_for("home.home"))