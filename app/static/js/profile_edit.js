document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('editButton');
    const saveButton = document.getElementById('saveButton');
    const uploadButton = document.getElementById('uploadButton');
    const profileImageInput = document.getElementById('profile_image');
    const profileThumb = document.getElementById('profileThumb');
    const fields = ['name', 'email', 'phone']; // 'department'는 제외

    // 이미지 업로드 버튼 클릭 시 파일 선택
    uploadButton.addEventListener('click', function() {
        profileImageInput.click();
    });

    // 파일 선택 후 미리 보기
    profileImageInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profileThumb.src = e.target.result;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    // Edit 버튼 클릭 시 필드를 편집 가능하게 전환
    editButton.addEventListener('click', function() {
        fields.forEach(field => {
            const element = document.getElementById(field);
            // const inputElement = document.getElementById(`${field}Input`);
            const value = element.textContent.trim();
            element.innerHTML = `<input type="text" id="${field}Input" value="${value}">`;
        });
        editButton.style.display = 'none';
        saveButton.style.display = 'inline-block';
        uploadButton.style.display = 'inline-block'; // Upload 버튼 표시
    });

    // Save 버튼 클릭 시 입력된 값으로 필드 업데이트
    saveButton.addEventListener('click', function() {
        fields.forEach(field => {
            const input = document.getElementById(`${field}Input`);
            const element = document.getElementById(field);
            element.textContent = input.value;
            // textElement.style.display = 'inline'; 
        });
        editButton.style.display = 'inline-block';
        saveButton.style.display = 'none';
        uploadButton.style.display = 'none'; // Upload 버튼 숨기기

        // 폼을 실제로 제출합니다.
        document.querySelector('form').submit();
    });
});
