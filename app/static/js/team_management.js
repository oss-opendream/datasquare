function addRow() {
    const tableBody = document.getElementById('team-table-body');
    const newRow = document.createElement('tr');

    newRow.innerHTML = `
        <td><input type="text" name="team_names"></td>
        <td><input type="text" name="team_managers"></td>
        <td>
            <button type="button" onclick="removeRow(this)">Remove</button>
            <input type="hidden" name="profile_ids" value="">
        </td>
    `;
    tableBody.appendChild(newRow);
}

function removeRow(button) {
    const row = button.parentNode.parentNode;
    row.remove();
}