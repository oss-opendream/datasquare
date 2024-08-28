function addRow() {
    const tableBody = document.getElementById('team-table-body');
    const newRow = document.createElement('tr');

    newRow.innerHTML = `
    <td><input type="text" name="team_names"></td>
    <td>
        <button type="button" onclick="removeRow(this)">Remove</button>
    </td>
    `;
    tableBody.appendChild(newRow);
}

function removeRow(button) {
    const row = button.parentNode.parentNode;
    row.remove();
}

document.querySelector('form').addEventListener('submit', function(event) {
    // 폼 내의 모든 team_names 필드를 가져옴
    const teamNames = document.querySelectorAll('input[name="team_names"]');
    const namesSet = new Set();
    let hasDuplicate = false;

    // 중복된 값을 찾음
    teamNames.forEach(function(input) {
        const name = input.value.trim();
        if (name !== "" && namesSet.has(name)) {
            hasDuplicate = true;
        } else {
            namesSet.add(name);
        }
    });

    if (hasDuplicate) {
        // 중복된 값이 있으면 오류 다이얼로그를 출력하고 폼 제출을 막음
        event.preventDefault();
        document.getElementById('DuplicatedTeamNameDialog').showModal();
    }
});