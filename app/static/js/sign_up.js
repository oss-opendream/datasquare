// 필요하면 쓰는..?

// document.addEventListener('DOMContentLoaded', function () {
//     // DOM이 완전히 로드된 후 실행.

//     const fileInput = document.getElementById('profile_image');
//     const fileButton = document.querySelector('.button');

//     // 커스텀 버튼 클릭 시 숨겨진 파일 입력을 트리거.
//     fileButton.addEventListener('click', function () {
//         fileInput.click();
//     });

//     // 파일이 선택되면 버튼 텍스트를 파일 이름으로 업데이트.
//     fileInput.addEventListener('change', function () {
//         if (this.files && this.files[0]) {
//             const fileName = this.files[0].name;
//             fileButton.querySelector('.button-text').textContent = fileName;
//         }
//     });
// });

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

    //error 요소
    const Error = document.createElement('div');
    Error.style.color = 'red';
    Error.style.marginTop = '5px';
    Error.style.fontSize = '16px';
    Error.style.width = '100%'; 

    // 필드에 error 메시지 추가
    password2Field.parentNode.appendChild(Error);

    form.addEventListener('submit', function(event) {

        // 비밀번호와 비밀번호 확인이 일치하지 않으면 폼 제출을 막고 경고 표시
        if (passwordField.value !== password2Field.value) {
            event.preventDefault(); // 폼 제출 막기
            Error.textContent = '비밀번호가 일치하지 않습니다.';

            // 페이지를 경고 메시지가 있는 위치로 스크롤
            password2Field.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            errorDiv.textContent = ''; // 에러 메시지 지우기
        }


    });

});