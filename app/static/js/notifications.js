console.log('Notifications script is running');

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded');
    const notificationButton = document.getElementById('notificationButton');
    const notificationPopup = document.getElementById('notificationPopup');

    console.log('Notification button:', notificationButton);
    console.log('Notification popup:', notificationPopup);

    if (notificationButton && notificationPopup) {
        notificationButton.addEventListener('click', function (e) {
            console.log('Notification button clicked');
            e.stopPropagation();
            if (notificationPopup.style.display === 'none' || notificationPopup.style.display === '') {
                notificationPopup.style.display = 'block';
                console.log('Notification popup displayed');
                updateNotifications();
            } else {
                notificationPopup.style.display = 'none';
                console.log('Notification popup hidden');
            }
        });

        document.addEventListener('click', function (e) {
            if (!notificationPopup.contains(e.target) && e.target !== notificationButton) {
                notificationPopup.style.display = 'none';
                console.log('Notification popup closed by outside click');
            }
        });
    } else {
        console.log('Notification button or popup not found');
    }

    updateNotificationCount();
    updateNotifications();
});

function updateNotificationCount() {
    fetch('/api/notification-count')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notifications-container .badge');
            if (data.count > 0) {
                if (badge) {
                    badge.textContent = data.count;
                } else {
                    const newBadge = document.createElement('span');
                    newBadge.className = 'badge';
                    newBadge.textContent = data.count;
                    const container = document.querySelector('.notifications-container');
                    if (container) {
                        container.appendChild(newBadge);
                    } else {
                        console.log('Notifications container not found');
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
            const notificationList = document.querySelector('.notification-list');
            if (notificationList) {
                if (data.notifications && data.notifications.length > 0) {
                    notificationList.innerHTML = data.notifications.map(notification => `
                        <div class="notification-item">
                            <div class="notification-content">
                                <p>${notification.description_top}</p>
                                <h3>${notification.title}</h3>
                                <p>${notification.description_bottom}</p>
                            </div>
                            <div class="notification-actions">
                                <button class="btn-view">이슈로 이동</button>
                                <button class="btn-read">읽음 처리</button>
                            </div>
                        </div>
                    `).join('');

                    // 버튼 이벤트 리스너 추가
                    notificationList.querySelectorAll('.btn-view').forEach(btn => {
                        btn.addEventListener('click', function () {
                            console.log('Move to issue');
                            // 여기에 이슈로 이동하는 로직 추가
                        });
                    });
                    notificationList.querySelectorAll('.btn-read').forEach(btn => {
                        btn.addEventListener('click', function () {
                            console.log('Mark as read');
                            // 여기에 읽음 처리 로직 추가
                        });
                    });
                } else {
                    notificationList.innerHTML = '<div class="notification-item"><p>새로운 알림이 없습니다.</p></div>';
                }
            }
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

setInterval(updateNotificationCount, 60000);