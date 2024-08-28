document.addEventListener("DOMContentLoaded", function() {

    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {

        event.preventDefault(); // 폼 제출 기본 동작 방지
        const emailElement = document.getElementById('email');
        const passwordElement = document.getElementById('password');

        fetch('/signin/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${emailElement.value}&password=${passwordElement.value}`
        })
        .then(response => {
            if (response.ok) {
                // 성공적으로 처리된 경우 리디렉션 URL을 받아서 이동
                return response.json().then(data => {
                    window.location.href = data.redirect_url;
                });
            } else {
                // 에러 처리
                return response.json().then(data => {
                    alert(data.error);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    });
});