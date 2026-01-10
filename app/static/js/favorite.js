document.addEventListener("DOMContentLoaded", () => {

    /* FAVORITAR NA HOME */
    const stars = document.querySelectorAll(".favorite-star");

    stars.forEach(star => {
        star.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();

            const pokemonId = star.dataset.pokemonId;

            try {
                const response = await fetch(`/favorite/toggle/${pokemonId}`, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                });

                const data = await response.json();

                if (data.status === "added") {
                    star.classList.add("active");
                }

                if (data.status === "removed") {
                    star.classList.remove("active");
                }

            } catch (error) {
                console.error("Erro ao favoritar:", error);
            }
        });
    });

    /* REMOVER NA PÁGINA DE FAVORITOS */
    const removeButtons = document.querySelectorAll(".remove-favorite-x");

    removeButtons.forEach(button => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            const pokemonId = button.dataset.pokemonId;
            const card = document.getElementById(`card-${pokemonId}`);
            const grid = document.getElementById("favorites-grid");
            const header = document.getElementById("favorites-header");

            try {
                const response = await fetch(`/favorite/toggle/${pokemonId}`, {
                    method: "POST",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const data = await response.json();

                if (data.status === "removed" && card) {
                    card.remove();

                    // SE NÃO SOBROU NENHUM CARD
                    if (grid && grid.children.length === 0) {
                    grid.remove();
                    if (header) header.remove();

                    const emptyState = document.createElement("div");
                    emptyState.className = "empty-state";
                    emptyState.innerHTML = `
                        <div class="empty-icon">⭐</div>
                        <h2>Nenhum Pokémon favorito</h2>
                        <p>
                            Você ainda não favoritou nenhum Pokémon.<br>
                            Explore a Pokédex e marque seus favoritos!
                        </p>
                        <a href="/" class="btn-back">
                            ← Voltar para Pokédex
                        </a>
                    `;

                    document.querySelector("main").appendChild(emptyState);
                }
                } else {
                    console.warn("Card não encontrado:", pokemonId);
                }

            } catch (error) {
                console.error("Erro ao remover favorito:", error);
            }
        });
    });

});
