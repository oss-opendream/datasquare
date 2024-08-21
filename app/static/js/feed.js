function search() {
    const searchInput = document.getElementById('search_input').value.trim();

    if (searchInput) {
        // 검색어를 sessionStorage에 저장
        let recentSearches = JSON.parse(sessionStorage.getItem('recentSearches')) || [];

        // 중복 검색어 제거
        if (!recentSearches.includes(searchInput)) {
            recentSearches.unshift(searchInput); // 최근 검색어를 맨 앞에 추가
            if (recentSearches.length > 10) {
                recentSearches.pop(); // 최근 검색어는 최대 10개까지만 유지
            }
            sessionStorage.setItem('recentSearches', JSON.stringify(recentSearches));
        }

        window.location.href = '/feed/search?team=&keyword=' + searchInput;
    }
}

function view_issue(issue_id) {

    if (issue_id) {

        window.location.href = '/issue/view?issue_id=' + issue_id;
    }
}

function displayRecentSearches() {
    const recentSearches = JSON.parse(sessionStorage.getItem('recentSearches')) || [];
    const recentSearchesContainer = document.getElementById('recent-searches');

    recentSearchesContainer.innerHTML = '';
    recentSearches.forEach(search => {
        const searchItem = document.createElement('li');
        searchItem.setAttribute("style", "cursor:pointer;")
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
