function search() {
    const searchInput = document.getElementById('search-input').value.trim();
    if (searchInput) {
        let recentSearches = JSON.parse(sessionStorage.getItem('recentSearches')) || [];
        if (!recentSearches.includes(searchInput)) {
            recentSearches.unshift(searchInput);
            if (recentSearches.length > 10) {
                recentSearches.pop();
            }
            sessionStorage.setItem('recentSearches', JSON.stringify(recentSearches));
        }
        window.location.href = '/feed/search?team=&keyword=' + searchInput;
    }
}

function displayRecentSearches() {
    const recentSearches = JSON.parse(sessionStorage.getItem('recentSearches')) || [];
    const recentSearchesContainer = document.getElementById('recent-searches');
    recentSearchesContainer.innerHTML = '';
    recentSearches.forEach(search => {
        const searchItem = document.createElement('li');
        searchItem.style.cursor = 'pointer';
        searchItem.textContent = search;
        searchItem.onclick = function () {
            window.location.href = '/feed/search?team=&keyword=' + search;
        };
        recentSearchesContainer.appendChild(searchItem);
    });
}

function filterMyIssues() {
    window.location.href = '/feed/my_issues';
}

function sortIssues(order) {
    // Implement sorting functionality
}

window.onload = function () {
    displayRecentSearches();
};