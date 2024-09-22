function toggleOtherInput(selectElement, inputId) {
    const otherInput = document.getElementById(inputId);
    if (selectElement.value === "Other") {
        otherInput.style.display = "block";
    } else {
        otherInput.style.display = "none";
    }
}

function toggleOtherSkill() {
    var skillSelect = document.getElementById('skill1');
    var otherSkillGroup = document.getElementById('other-skill-group');
    otherSkillGroup.style.display = skillSelect.value === 'Other' ? 'block' : 'none';
}

function handleAddSkill() {
    // Logic to handle adding the skill
    var skillForm = document.getElementById('computerSkillsForm');
    // Process form data, then close modal
    $('#computerSkillsModal').modal('hide');
}

function toggleOtherSoftSkill() {
    var skillSelect = document.getElementById('softskill1');
    var otherSkillGroup = document.getElementById('other-soft-skill-group');
    otherSkillGroup.style.display = skillSelect.value === 'Other' ? 'block' : 'none';
}

function handleAddSoftSkill() {
    // Logic to handle adding the soft skill
    var softSkillForm = document.getElementById('softSkillsForm');
    // Process form data, then close modal
    $('#softSkillsModal').modal('hide');
}

document.getElementById('saveChangesBtn').addEventListener('click', function() {
    // Gather input values
    const idnumber = document.getElementById("idnumber").value;
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const gender = document.getElementById("gender").value;
    const maritalStatus = document.getElementById("marital_status").value;
    const dob = document.getElementById("dob").value;

    // Create a data object
    const data = {
        idnumber,
        first_name: firstName,
        last_name: lastName,
        email,
        phone,
        gender,
        marital_status: maritalStatus,
        dob
    };

    // Send data to the server using Fetch API
    fetch('/api/update-personal-details', { // Adjust URL as needed
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Update the displayed personal details
        document.getElementById("displayName").innerText = `${data.first_name} ${data.last_name}`;
        document.getElementById("displayEmail").innerText = data.email;
        document.getElementById("displayPhone").innerText = data.phone;

        // Hide the modal
        $('#personalDetailsModal').modal('hide');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
});

// Add event listener for delete button
document.getElementById('deleteButton').addEventListener('click', function() {
    const confirmation = confirm("Are you sure you want to delete your account?");
    if (confirmation) {
        fetch('/api/delete-account', { // Adjust URL as needed
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Account deleted successfully.");
                // Optionally, redirect or refresh the page
                window.location.reload();
            } else {
                throw new Error('Failed to delete account');
            }
        })
        .catch(error => {
            console.error('There was a problem with the delete operation:', error);
        });
    }
});
