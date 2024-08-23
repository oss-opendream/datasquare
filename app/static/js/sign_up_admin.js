document.addEventListener("DOMContentLoaded", function() {
    // 쿼리 파라미터에서 오류 메시지 가져오기
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');

    if (error) {
        alert(error); // 오류 메시지 팝업 표시
    }

    // 폼과 필드 가져오기
    const form = document.querySelector('form');
    const passwordField = form.querySelector('input[name="password"]');
    const password2Field = form.querySelector('input[name="password2"]');

    // error 요소
    const errorDiv = document.createElement('div');
    errorDiv.style.color = 'red';
    errorDiv.style.marginTop = '5px';
    errorDiv.style.fontSize = '16px';
    errorDiv.style.width = '100%';

    // 필드에 error 메시지 추가
    password2Field.parentNode.appendChild(errorDiv);

    form.addEventListener('submit', function(event) {
        // 비밀번호와 비밀번호 확인이 일치하지 않으면 폼 제출을 막고 경고 표시
        if (passwordField.value !== password2Field.value) {
            event.preventDefault(); // 폼 제출 막기
            errorDiv.textContent = '비밀번호가 일치하지 않습니다.';

            // 페이지를 경고 메시지가 있는 위치로 스크롤
            password2Field.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            errorDiv.textContent = ''; // 에러 메시지 지우기
        }
        
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // 폼 제출 기본 동작 방지
    
        // 폼 데이터 생성
        const formData = new FormData(event.target);
    
        // 폼 데이터 제출
        fetch('/admin', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // 서버가 성공적으로 처리한 경우 JSON이 아니라 상태 코드만 반환할 수 있으므로
            if (response.ok) {
                // 성공적으로 처리된 경우 리디렉션
                window.location.href = '/signin';
            } else {
                // 에러 상태 코드일 경우 JSON 형식으로 응답 읽기
                return response.json().then(data => {
                    // 서버에서 에러 메시지가 반환되면 팝업창 표시
                    alert(data.error);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
