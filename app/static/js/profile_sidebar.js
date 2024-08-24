document.addEventListener('DOMContentLoaded', function() {
    const sidebarNav = document.getElementById('sidebar-nav');
    const sidebarLinks = [
        { url: '/profile', text: 'Personal' },
        { url: '/profile/team', text: 'Team' },

    ];

    sidebarLinks.forEach(link => {
        const listItem = document.createElement('li');
        const anchor = document.createElement('a');
        anchor.href = link.url;
        anchor.textContent = link.text;
        listItem.appendChild(anchor);
        sidebarNav.appendChild(listItem);
    });
});