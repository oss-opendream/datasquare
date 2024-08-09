document.addEventListener('DOMContentLoaded', function () {
    const notificationButton = document.getElementById('notificationButton');
    const notificationPopup = document.getElementById('notificationPopup');

    notificationButton.addEventListener('click', function (e) {
        e.stopPropagation();
        notificationPopup.style.display = notificationPopup.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function (e) {
        if (!notificationPopup.contains(e.target) && e.target !== notificationButton) {
            notificationPopup.style.display = 'none';
        }
    });
});