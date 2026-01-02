document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".btn-favorite");

    buttons.forEach(button => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();

            const pokemonId = button.dataset.pokemonId;

            try {
                const response = await fetch(`/favorite/toggle/${pokemonId}`, {
                    method: "POST",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const data = await response.json();

                if (data.status === "added") {
                    button.classList.add("active");
                    button.textContent = "⭐ Favoritado";
                }

                if (data.status === "removed") {
                    button.classList.remove("active");
                    button.textContent = "☆ Favoritar";
                }

            } catch (error) {
                console.error("Erro ao favoritar:", error);
            }
        });
    });
});