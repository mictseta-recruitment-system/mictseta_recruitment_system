
function showFlashMessage(message, type) {
    const flashMessageContainer = document.getElementById("flash-message-container");
    const flashMessage = document.createElement("div");
    flashMessage.className = `alert alert-${type} alert-dismissible fade show .overlay`;
    flashMessage.role = "alert";
    flashMessage.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;
    flashMessageContainer.appendChild(flashMessage);

    // Set a timeout to remove the flash message after 5 seconds
    setTimeout(() => {
        flashMessage.classList.remove("show");
        flashMessage.classList.add("hide");
        
        // Remove the element from the DOM after the fade-out transition
        setTimeout(() => {
            flashMessageContainer.removeChild(flashMessage);
        }, 500); // Adjust this timeout to match the CSS transition duration
    }, 5000); // 5000 milliseconds = 5 seconds
}