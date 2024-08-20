document.addEventListener('DOMContentLoaded', function () {
    const notificationButton = document.getElementById('header__notification-button');
    const notificationPopup = document.getElementById('header__notification-popup');

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
    }

    updateNotificationCount();
    updateNotifications();
});

function updateNotificationCount() {
    fetch('/api/notification-count')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.header__notification-badge');
            if (data.count > 0) {
                if (badge) {
                    badge.textContent = data.count;
                } else {
                    const newBadge = document.createElement('span');
                    newBadge.className = 'header__notification-badge';
                    newBadge.textContent = data.count;
                    const container = document.querySelector('.header__notification-button');
                    if (container) {
                        container.appendChild(newBadge);
                    }
                }
            } else if (badge) {
                badge.remove();
            }
        })
        .catch(error => {
            console.error('Error updating notification count:', error);
        });
}

function updateNotifications() {
    fetch('/api/notifications')
        .then(response => response.json())
        .then(data => {
            const notificationList = document.querySelector('.header__notification-list');
            if (notificationList) {
                if (data.notifications && data.notifications.length > 0) {
                    notificationList.innerHTML = data.notifications.map(notification => `
                        <div class="header__notification-item">
                            <div class="header__notification-content">
                                <p>${notification.description_top}</p>
                                <h3>${notification.title}</h3>
                                <p>${notification.description_bottom}</p>
                            </div>
                            <div class="header__notification-actions">
                                <button class="header__notification-view-button">이슈로 이동</button>
                                <button class="header__notification-read-button">읽음 처리</button>
                            </div>
                        </div>
                    `).join('');

                    notificationList.querySelectorAll('.header__notification-view-button').forEach(btn => {
                        btn.addEventListener('click', function () {
                            console.log('Move to issue');
                            // 여기에 이슈로 이동하는 로직 추가
                        });
                    });
                    notificationList.querySelectorAll('.header__notification-read-button').forEach(btn => {
                        btn.addEventListener('click', function () {
                            console.log('Mark as read');
                            // 여기에 읽음 처리 로직 추가
                        });
                    });
                } else {
                    notificationList.innerHTML = '<div class="header__notification-item header__notification-item--empty"><p>새로운 알림이 없습니다.</p></div>';
                }
            }
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

setInterval(updateNotificationCount, 60000);