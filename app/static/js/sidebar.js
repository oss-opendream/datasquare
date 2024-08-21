document.addEventListener('DOMContentLoaded', function() {
    const sidebarNav = document.getElementById('sidebar-nav');
    const sidebarLinks = [
        { url: '/profile/personal', text: 'Personal' },
        { url: '/profile/team', text: 'Team' },
        { url: '/profile/admin', text: 'Admin' },

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