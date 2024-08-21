document.addEventListener('DOMContentLoaded', function () {
    // 알림 버튼 기능
    const notificationButton = document.querySelector('.header__notification-button');
    if (notificationButton) {
        notificationButton.addEventListener('click', function () {
            const notificationPopup = document.getElementById('header__notification-popup');
            if (notificationPopup) {
                notificationPopup.classList.toggle('header__notification-popup--visible');
            }
        });
    }

    // 설정 버튼 기능
    const settingsButton = document.querySelector('.header__settings-button');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            alert('설정 페이지로 이동합니다.');
        });
    }

    // 로그아웃 버튼 기능
    const logoutButton = document.querySelector('.header__logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            if (confirm('정말 로그아웃 하시겠습니까?')) {
                alert('로그아웃 되었습니다.')
                window.location.href = '/logout';
            }
        });
    }
});