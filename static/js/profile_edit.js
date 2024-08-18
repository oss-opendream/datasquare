document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('profile-upload');
    const uploadButton = document.querySelector('.button.upload');
    const deleteButton = document.querySelector('.delete');
    const userThumb = document.querySelector('.user-thumb img');

    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                userThumb.src = e.target.result;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    deleteButton.addEventListener('click', function() {
        userThumb.src = "/static/images/default_avatar.svg";
        fileInput.value = "";
    });

    function closeNotification() {
        const notification = document.querySelector('.notification');
        if (notification) {
            notification.style.display = 'none';
        }
    }

    const closeNotificationButton = document.querySelector('.notification .right');
    if (closeNotificationButton) {
        closeNotificationButton.addEventListener('click', closeNotification);
    }
});