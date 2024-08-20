document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('profile-edit__file-input');
    const uploadButton = document.querySelector('.profile-edit__upload-button');
    const deleteButton = document.querySelector('.profile-edit__delete-button');
    const userThumb = document.querySelector('.profile-edit__user-thumb');

    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                userThumb.src = e.target.result;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    deleteButton.addEventListener('click', function () {
        userThumb.src = "/static/images/default_avatar.svg";
        fileInput.value = "";
    });

    function closeNotification() {
        const notification = document.querySelector('.profile-edit__notification');
        if (notification) {
            notification.style.display = 'none';
        }
    }

    const closeNotificationButton = document.querySelector('.profile-edit__notification-close');
    if (closeNotificationButton) {
        closeNotificationButton.addEventListener('click', closeNotification);
    }
});