document.addEventListener('DOMContentLoaded', function () {
    const notificationButton = document.getElementById('header__notification-button');
    const notificationPopup = document.getElementById('header__notification-popup');
    const deleteAllButton = document.querySelector('.header__notification-delete-all');

    if (notificationButton && notificationPopup) {
        notificationButton.addEventListener('click', function (e) {
            e.stopPropagation();
            notificationPopup.classList.toggle('header__notification-popup--visible');
            if (notificationPopup.classList.contains('header__notification-popup--visible')) {
                updateNotifications();
            }
        });

        document.addEventListener('click', function (e) {
            if (!notificationPopup.contains(e.target) && e.target !== notificationButton) {
                notificationPopup.classList.remove('header__notification-popup--visible');
            }
        });

        deleteAllButton.addEventListener('click', clearAllNotifications);
    }

    updateNotificationCount();
});

function updateNotifications() {
    const notificationList = document.querySelector('.header__notification-list');
    const mockNotifications = [
        { descriptionTop: "Description Top", title: "Title", descriptionBottom: "Description Bottom" },
        { descriptionTop: "Description Top", title: "Title", descriptionBottom: "Description Bottom" },
        { descriptionTop: "Description Top", title: "Title", descriptionBottom: "Description Bottom" },
        { descriptionTop: "Description Top", title: "Title", descriptionBottom: "Description Bottom" }
    ];

    notificationList.innerHTML = mockNotifications.map(notification => `
        <li class="header__notification-item">
            <div class="header__notification-content">
                <p class="header__notification-description-top">${notification.descriptionTop}</p>
                <h4 class="header__notification-title">${notification.title}</h4>
                <p class="header__notification-description-bottom">${notification.descriptionBottom}</p>
            </div>
            <button class="header__notification-delete">×</button>
        </li>
    `).join('');

    notificationList.querySelectorAll('.header__notification-delete').forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            this.closest('.header__notification-item').remove();
            updateNotificationCount();
        });
    });
}

function clearAllNotifications() {
    const notificationList = document.querySelector('.header__notification-list');
    notificationList.innerHTML = '';
    updateNotificationCount();
}

function updateNotificationCount() {
    const notificationCount = document.querySelectorAll('.header__notification-item').length;
    const badge = document.querySelector('.header__notification-badge');
    if (notificationCount > 0) {
        badge.textContent = notificationCount;
        badge.style.display = 'inline';
    } else {
        badge.style.display = 'none';
    }
}