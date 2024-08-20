function closeNotification() {
    const notification = document.querySelector('.notification');
    if (notification) {
        notification.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const saveButton = document.querySelector('.button.save');
    saveButton.addEventListener('click', function () {
        // 여기에 필요한 클라이언트 측 유효성 검사를 추가할 수 있.
    });
});