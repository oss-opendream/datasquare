let editingCommentId = null;  // 현재 수정 중인 댓글 ID
let originalText = '';

function editComment(commentId) {
    if (editingCommentId !== null) {
        alert("You can only edit one comment at a time.");
        return;
    }

    const commentElement = document.getElementById('comment-' + commentId);
    const currentText = commentElement.querySelector('.comment-text').innerText;
    originalText = currentText;
    const commentPublisher = commentElement.querySelector('.comment-publisher').innerText;

    editingCommentId = commentId;  // 현재 수정 중인 댓글 ID 설정

    commentElement.innerHTML = `
        <span class="comment-publisher">${commentPublisher}</span>
        <br>
        <input type="text" class="comment-text" value="${currentText}" />
        <button class="btn btn--primary issue-comment-button"
            onclick="saveComment(${commentId})">Save</button>
        <button class="btn btn--primary issue-comment-button"
            onclick="cancelComment(${commentId})">Cancel</button>
        <hr>
    `;
}

function deleteComment(commentId) {
    fetch('/issue_comment/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `comment_id=${commentId}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const commentElement = document.getElementById('comment-' + commentId);
                commentElement.remove();  // 삭제 성공 후 댓글 요소를 제거
            } else {
                alert('Failed to delete comment.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete comment due to an error.');
        });
}

function saveComment(commentId) {

    const commentElement = document.getElementById('comment-' + commentId);
    const currentText = commentElement.querySelector('.comment-text').value;
    const commentPublisher = commentElement.querySelector('.comment-publisher').innerText;

    fetch('/issue_comment/modify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `comment_id=${commentId}&content=${encodeURIComponent(currentText)}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const commentElement = document.getElementById('comment-' + commentId);
                commentElement.innerHTML = `
                <span class="comment-publisher">${commentPublisher}</span>
                <br>
                <span class="comment-text">${currentText}</span>
                <button class="btn btn--primary issue-comment-button"
                    onclick="editComment(${commentId})">Edit</button>
                <button class="btn btn--primary issue-comment-button"
                    onclick="deleteComment(${commentId})">Delete</button>
            `;
                editingCommentId = null;  // 수정 완료 후 초기화
            } else {
                alert('Failed to save the comment.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save comment due to an error.');
        });
}

function cancelComment(commentId) {
    const commentElement = document.getElementById('comment-' + commentId);
    const commentPublisher = commentElement.querySelector('.comment-publisher').innerText;

    commentElement.innerHTML = `
        <span class="comment-publisher">${commentPublisher}</span>
        <br>
        <span class="comment-text">${originalText}</span>
        <button class="btn btn--primary issue-comment-button"
            onclick="editComment(${commentId})">Edit</button>
        <button class="btn btn--primary issue-comment-button"
            onclick="deleteComment(${commentId})">Delete</button>
    `;
    editingCommentId = null;  // 수정 취소 후 초기화
}
