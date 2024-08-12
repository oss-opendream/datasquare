console.log('Notifications script is running');


console.log(document.getElementById('notificationButton'));
console.log(document.getElementById('notificationPopup'));

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
            console.log('Button clicked');
            e.stopPropagation();
            notificationPopup.style.display = notificationPopup.style.display === 'none' ? 'block' : 'none';
            console.log('Popup display:', notificationPopup.style.display);
        });

        if (closeNotifications) {
            closeNotifications.addEventListener('click', function () {
                console.log('Close notifications clicked');
                notificationPopup.style.display = 'none';
            });
        } else {
            console.log('Close notifications button not found');
        }

        document.addEventListener('click', function (e) {
            if (!notificationPopup.contains(e.target) && e.target !== notificationButton) {
                console.log('Clicked outside notification popup');
                notificationPopup.style.display = 'none';
            }
        });
    } else {
        console.log('Notification button or popup not found');
    }
});