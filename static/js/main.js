document.addEventListener('DOMContentLoaded', function () {
    // 알림 버튼 기능
    const notificationButton = document.querySelector('.notifications');
    if (notificationButton) {
        notificationButton.addEventListener('click', function () {
            alert('알림 기능은 아직 구현되지 않았습니다.');
        });
    }

    // 설정 버튼 기능
    const settingsButton = document.querySelector('.settings');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            alert('설정 페이지로 이동합니다.');
        });
    }

    // 로그아웃 버튼 기능
    const logoutButton = document.querySelector('.logout');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            if (confirm('정말 로그아웃 하시겠습니까?')) {
                alert('로그아웃 되었습니다.');
            }
        });
    }
});