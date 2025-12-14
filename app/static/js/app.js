let highlightIndex = -1;

function showSuggestions(value) {
    const container = document.getElementById('suggestions-container');
    const input = document.getElementById('pokemon-input');
    container.innerHTML = ''; 

    highlightIndex = -1; 

    if (value.length < 1) {
        return;
    }

    const filtered = POKEMON_SUGGESTIONS_DATA.filter(poke => 
        poke.name.startsWith(value.toLowerCase())
    );

    const limited = filtered.slice(0, 10); 

    limited.forEach((poke, index) => { 
        const item = document.createElement('div');
        item.classList.add('suggestion-item');
        
        const img = document.createElement('img');
        img.src = poke.imageUrl;
        img.alt = poke.name;
        item.appendChild(img);

        const nameSpan = document.createElement('span');
        nameSpan.innerText = poke.name;
        item.appendChild(nameSpan);

        if (index === 0) {
            item.classList.add('suggestion-highlight');
            highlightIndex = 0; 
        }
        
        item.onmouseover = function() {
            document.querySelectorAll('.suggestion-item').forEach(el => 
                el.classList.remove('suggestion-highlight')
            );
        };
        
        item.onclick = function() {
            input.value = poke.name;
            container.innerHTML = '';
            document.getElementById('search-form').submit();
        };

        container.appendChild(item);
    });
}

function handleKeyDown(event) {
    const input = document.getElementById('pokemon-input');
    const container = document.getElementById('suggestions-container');
    const suggestions = container.querySelectorAll('.suggestion-item');
    const totalSuggestions = suggestions.length;
    
    const removeHighlight = () => {
        suggestions.forEach(item => item.classList.remove('suggestion-highlight'));
    };

    if (event.keyCode === 40 || event.keyCode === 38) {
        if (totalSuggestions === 0) return;

        event.preventDefault(); 
        removeHighlight();

        if (event.keyCode === 40) {
            highlightIndex = (highlightIndex < totalSuggestions - 1) ? highlightIndex + 1 : 0;
        } else if (event.keyCode === 38) {
            highlightIndex = (highlightIndex > 0) ? highlightIndex - 1 : totalSuggestions - 1;
        }

        const currentSuggestion = suggestions[highlightIndex];

        currentSuggestion.classList.add('suggestion-highlight');
        currentSuggestion.scrollIntoView({
            behavior: 'smooth', 
            block: 'nearest'    
        });

        input.value = currentSuggestion.querySelector('span').innerText; 
        
    } 

    else if (event.keyCode === 13) { 
        event.preventDefault(); 
        
        if (highlightIndex > -1 && suggestions[highlightIndex]) {

            suggestions[highlightIndex].click();
            
        } else if (totalSuggestions > 0) {

            suggestions[0].click();
            
        } else {

             document.getElementById('search-form').submit();
        }
    }
}