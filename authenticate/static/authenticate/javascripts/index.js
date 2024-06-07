function showFlashMessage(message, type) {
  const flashMessageContainer = document.getElementById(
    "flash-message-container"
  );
  const flashMessage = document.createElement("div");
  flashMessage.className = `alert alert-${type} alert-dismissible fade show`;
  flashMessage.role = "alert";
  flashMessage.innerHTML = `
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            `;
  flashMessageContainer.appendChild(flashMessage);
}

    // Function to show the update email form and hide the reset password form
    function showResetEmailForm() {
      document.getElementById('resetPasswordContainer').style.display = 'none';
      document.getElementById('resetEmailContainer').style.display = 'block';
  }

  function validateEmailForm() {
    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = document.getElementById('new_password2').value;
    const flashMessage = document.getElementById('flashMessage');

    // Clear any previous flash message
    flashMessage.style.display = 'none';
    flashMessage.innerHTML = '';

    if (newPassword.length <= 5) {
        showFlashMessage("Password must be longer than 5 characters", "danger");
        return false;
    }

    if (newPassword !== confirmPassword) {
        showFlashMessage("Passwords do not match", "danger");
        return false;
    }

    showFlashMessage("Password updated successfully", "success");
    return true;
}

function showFlashMessage(message, type) {
    const flashMessage = document.getElementById('flashMessage');
    flashMessage.style.display = 'block';
    flashMessage.innerHTML = message;

    // Setting the color based on the message type
    if (type === "danger") {
        flashMessage.style.backgroundColor = "red";
    } else if (type === "success") {
        flashMessage.style.backgroundColor = "green";
    }
}

function showResetEmailForm() {
    // Implement the logic for showing the email reset form
}
