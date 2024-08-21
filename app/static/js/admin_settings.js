document.addEventListener('DOMContentLoaded', function () {
    const teamList = document.getElementById('teamList');
    const addTeamBtn = document.getElementById('addTeamBtn');
    const adminSettingsForm = document.getElementById('adminSettingsForm');
    const successMessage = document.getElementById('successMessage');

    function createTeamItem(teamName = '', teamAdmin = '') {
        const teamItem = document.createElement('div');
        teamItem.className = 'team-item';
        teamItem.innerHTML = `
            <input type='text' name='teamName[]' placeholder='Team Name' value='${teamName}' required>
            <input type='text' name='teamAdmin[]' placeholder='Team Administrator' value='${teamAdmin}' required>
            <button type='button' class='remove-team'>-</button>
        `;
        return teamItem;
    }

    addTeamBtn.addEventListener('click', function () {
        teamList.appendChild(createTeamItem());
    });

    teamList.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-team')) {
            e.target.closest('.team-item').remove();
        }
    });

    adminSettingsForm.addEventListener('submit', function (e) {
        e.preventDefault();
        // Here you would typically send the form data to the server
        // For this example, we'll just show the success message
        successMessage.style.display = 'block';
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 3000);
    });

    // Initialize with some example data
    teamList.appendChild(createTeamItem('HR Team', 'John Doe'));
    teamList.appendChild(createTeamItem('IT Team', 'Jane Smith'));
});