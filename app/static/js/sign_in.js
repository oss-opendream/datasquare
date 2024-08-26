document.addEventListener("DOMContentLoaded", function() {
    // 쿼리 파라미터에서 오류 메시지 가져오기
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');

    if (error) {
        alert(error); // 오류 메시지 팝업 표시
    }

    // 폼과 필드 가져오기
    const form = document.querySelector('form');

    // error 요소
    const errorDiv = document.createElement('div');
    errorDiv.style.color = 'red';
    errorDiv.style.marginTop = '5px';
    errorDiv.style.fontSize = '16px';
    errorDiv.style.width = '100%';

    form.addEventListener('submit', function(event) {

        event.preventDefault(); // 폼 제출 기본 동작 방지
    
        // 폼 데이터 생성
        const formData = new FormData(event.target);
    
        // 폼 데이터 제출
        fetch('/signin/post', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // 서버가 성공적으로 처리한 경우 JSON이 아니라 상태 코드만 반환할 수 있으므로
            if (response.ok) {
                // 성공적으로 처리된 경우 리디렉션
                window.location.href = '/feed';
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

