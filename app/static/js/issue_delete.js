document.addEventListener('DOMContentLoaded', function () {

    // 이슈 삭제 버튼 기능
    const issueDeleteButton = document.querySelector('.issue-delete-button');
    if (issueDeleteButton) {
        issueDeleteButton.addEventListener('click', function () {
            if (confirm('정말 삭제 하시겠습니까?')) {
                alert('삭제 되었습니다.');
            }
        });
    }
});