document.addEventListener('DOMContentLoaded', function() {
    const submitCommentBtn = document.getElementById('submit-comment');
    const commentTextarea = document.getElementById('comment');

    submitCommentBtn.addEventListener('click', function() {
        const commentContent = commentTextarea.value.trim();
        if (commentContent) {
            // Here you would typically send an AJAX request to submit the comment
            console.log('Submitting comment:', commentContent);
            // Clear the textarea after submission
            commentTextarea.value = '';
        }
    });
});