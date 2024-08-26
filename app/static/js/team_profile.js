let originalTeam = '';

function editComment() {

    const nameElement = document.getElementById('team_name');
    const introductionElement = document.getElementById('team_introduction');
    const editButton = document.getElementById('team-profile-view__edit');

    // Replace the <p> element with an <input> element
    const inputElement_name = `<input type="text" class="team-profile-view__name" name="team_name" id="team_name" value="${nameElement.innerText}" />`;
    const inputElement_intro = `<input type="text" class="team-profile-view__introduction" name ="team_intro" id="team_introduction" value="${introductionElement.innerText}" />`;
    originalTeam = nameElement.innerText
    // Replace the <p> element's outerHTML with the new input element's HTML
    nameElement.outerHTML = inputElement_name;
    introductionElement.outerHTML = inputElement_intro;

    editButton.innerHTML =`
    <div class = "team-profile-view__save" id = 'team-profile-view__save'>
        <button id="saveButton" class="edit-button" onclick="saveComment()">Save</button>
    </div>
    `
};

function saveComment() {
    const nameElement = document.getElementById('team_name');
    const introductionElement = document.getElementById('team_introduction');
    const saveButton = document.getElementById('team-profile-view__save');

    fetch('/profile/team', {
        method : 'POST',
        headers :{
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body : `origin_name=${originalTeam}&team_name=${nameElement.value}&team_intro=${introductionElement.value}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status == 'success') {
                nameElement.outerHTML = `<p class="team-profile-view__name" id = "team_name">${nameElement.value}</p>`
                introductionElement.outerHTML = `<p class="team-profile-view__introduction" id = "team_introduction"> ${introductionElement.value}</p>`
                saveButton.outerHTML = `
                <div class = "team-profile-view__edit" >
                    <button id="editButton" class="edit-button" onclick="editComment()">Edit</button>
                </div>
    `;
            } else {
                alert('Failed to save the comment.');
            }
})


};