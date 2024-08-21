document.addEventListener('DOMContentLoaded', function () {
    // 알림 버튼 기능
    const notificationButton = document.querySelector('.notifications-container');
    if (notificationButton) {
        notificationButton.addEventListener('click', function () {
            const notificationPopup = document.getElementById('notificationPopup');
            if (notificationPopup) {
                notificationPopup.style.display = notificationPopup.style.display === 'none' ? 'block' : 'none';
            }
        });
    }

    // 설정 버튼 기능
    const settingsButton = document.querySelector('.user-actions img[alt="Settings"]');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            alert('설정 페이지로 이동합니다.');
        });
    }

    // 로그아웃 버튼 기능
    const logoutButton = document.querySelector('.user-actions img[alt="Logout"]');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            if (confirm('정말 로그아웃 하시겠습니까?')) {
                alert('로그아웃 되었습니다.');
            }
        });
    }
});