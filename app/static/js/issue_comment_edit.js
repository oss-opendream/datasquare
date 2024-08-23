let editingCommentId = null;  // 현재 수정 중인 댓글 ID

function editComment(commentId) {
    if (editingCommentId !== null) {
        alert("You can only edit one comment at a time.");
        return;
    }

    const commentElement = document.getElementById('comment-' + commentId);
    const currentText = commentElement.querySelector('.comment-text').innerText;

    editingCommentId = commentId;  // 현재 수정 중인 댓글 ID 설정

    commentElement.innerHTML = `
        <form onsubmit="return saveComment(event, ${commentId})">
            <input type="text" name="new_text" value="${currentText}" />
            <button type="submit">Save</button>
            <button type="button" onclick="cancelEdit(${commentId}, '${currentText}')">Cancel</button>
        </form>
    `;
}

function saveComment(event, commentId) {
    event.preventDefault();
    const form = event.target;
    const newText = form.new_text.value;

    fetch('/issue_comment/modify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `comment_id=${commentId}&content=${newText}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const commentElement = document.getElementById('comment-' + commentId);
            commentElement.innerHTML = `
                <span class="comment-text">${newText}</span>
                <button onclick="editComment(${commentId})">Edit</button>
                <button onclick="deleteComment(${commentId })">Delete</button>
            `;
            editingCommentId = null;  // 수정 완료 후 초기화
        }
    });
}

function cancelEdit(commentId, originalText) {
    const commentElement = document.getElementById('comment-' + commentId);
    commentElement.innerHTML = `
        <span class="comment-text">${originalText}</span>
        <button onclick="editComment(${commentId})">Edit</button>
        <button onclick="deleteComment(${ commentId })">Delete</button>
    `;
    editingCommentId = null;  // 수정 취소 후 초기화
}