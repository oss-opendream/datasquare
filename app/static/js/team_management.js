function addRow() {
    const tableBody = document.getElementById('team-rows');
    const newRow = document.createElement('div');

    newRow.innerHTML = `
        <div class="team-row">
            <input readonly type="hidden" name="profile_ids" value="">
            <input type="text" name="team_names" value="">
            <input type="text" name="team_managers" value="">
            <input type="hidden" name="delete_flags" value="false">
            <button type="button" onclick="removeRow(this)">Remove</button>
        </div>
    `;
    tableBody.appendChild(newRow);
}

function removeRow(button) {
    // 'Remove' 버튼이 클릭된 row를 삭제
    const row = button.closest('.team-row');
    const deleteFlagInput = row.querySelector('input[name="delete_flags"]');
    deleteFlagInput.value = 'true';  // 삭제 플래그를 true로 설정
    row.style.display = 'none';  // row를 숨김 처리
}