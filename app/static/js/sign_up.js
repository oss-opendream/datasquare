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