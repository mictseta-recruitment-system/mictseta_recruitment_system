function showFlashMessage(message, type) {
  const flashMessageContainer = document.getElementById(
    "flash-message-container"
  );
  const flashMessage = document.createElement("div");
  flashMessage.className = `alert alert-${type} alert-dismissible fade show .overlay`;
  flashMessage.role = "alert";
  flashMessage.innerHTML = "";
  flashMessage.innerHTML = `
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            `;
  flashMessageContainer.appendChild(flashMessage);
}
