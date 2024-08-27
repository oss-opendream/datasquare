function addRow() {
    const tableBody = document.getElementById('team-rows');
    const newRow = document.createElement('div');

    newRow.innerHTML = `
        <div class="team-row">
            <input readonly type="hidden" name="profile_ids" value="">
            <input type="text" name="team_names" value="">
            <input type="hidden" name="team_manager_ids" value="">
            <input type="text" name="team_manager_names" value="" readonly>
            <input type="hidden" name="delete_flags" value="false">
            <button type="button" onclick="removeRow(this)">-</button>
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

function showDialog(teamProfileId, button) {
    fetch(`teams/members/${teamProfileId}`)
        .then(response => response.json())
        .then(members => {
            const memberList = document.getElementById('memberList');
            memberList.innerHTML = ''; // 기존 멤버 목록 초기화
            members.forEach(member => {
                const li = document.createElement('li');
                li.textContent = member.name; // PersonalProfile의 속성 예: name
                const selectButton = document.createElement('button');
                selectButton.textContent = 'Select';
                selectButton.onclick = function () {
                    // 'team_manager_ids'와 'team_manager_names' 필드를 정확히 선택
                    const row = button.closest('.team-row');
                    const managerIdInput = row.querySelector('input[name="team_manager_ids"]');
                    const managerNameInput = row.querySelector('input[name="team_manager_names"]');

                    managerIdInput.value = member.profile_id; // profile_id를 숨겨진 필드에 저장
                    managerNameInput.value = member.name; // name을 표시되는 필드에 저장
                    closeDialog();
                };
                li.appendChild(selectButton);
                memberList.appendChild(li);
            });
            document.getElementById('memberDialog').showModal();
        });
}

function closeDialog(dialog) {
    document.getElementById(dialog).close();
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