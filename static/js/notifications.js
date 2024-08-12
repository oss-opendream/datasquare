console.log('Notifications script is running');

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded');
    const notificationButton = document.getElementById('notificationButton');
    const notificationPopup = document.getElementById('notificationPopup');
    const closeNotifications = document.getElementById('closeNotifications');

    console.log('Notification button:', notificationButton);
    console.log('Notification popup:', notificationPopup);
    console.log('Close notifications button:', closeNotifications);

    if (notificationButton && notificationPopup) {
        notificationButton.addEventListener('click', function (e) {
            console.log('Notification button clicked');
            e.stopPropagation();
            notificationPopup.style.display = notificationPopup.style.display === 'none' ? 'block' : 'none';
        });

        if (closeNotifications) {
            closeNotifications.addEventListener('click', function () {
                console.log('Close notifications clicked');
                notificationPopup.style.display = 'none';
            });
        }

        document.addEventListener('click', function (e) {
            if (!notificationPopup.contains(e.target) && e.target !== notificationButton) {
                notificationPopup.style.display = 'none';
            }
        });
    } else {
        console.log('Notification button or popup not found');
    }
});