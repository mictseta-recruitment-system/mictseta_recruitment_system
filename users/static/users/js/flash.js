function showFlashMessage(message, type) {
    const flashMessageContainer = document.getElementById("flash-message-container");
    const flashMessage = document.createElement("div");
    flashMessage.className = `alert alert-${type} alert-dismissible fade show overlay`;
    flashMessage.role = "alert";
    flashMessage.style.position = "fixed";
    flashMessage.style.top = "70px"; // Moved down
    flashMessage.style.right = "20px";
    flashMessage.style.zIndex = "9999";
    flashMessage.style.minWidth = "320px"; // Reduced width
    flashMessage.style.minHeight = "80px"; // Reduced height
    flashMessage.style.padding = "40px";
    flashMessage.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
    flashMessage.style.opacity = "0";
    flashMessage.style.transform = "translateX(100%)";
    flashMessage.style.transition = "opacity 0.5s ease-out, transform 0.5s ease-out";

    flashMessage.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 4px; background: #ddd;">
            <div id="progress-bar" style="width: 100%; height: 4px; background: #007bff; transition: width 2.5s linear;"></div>
        </div>
    `;
    flashMessageContainer.appendChild(flashMessage);

    // Trigger transition
    setTimeout(() => {
        flashMessage.style.opacity = "1";
        flashMessage.style.transform = "translateX(0)";
        document.getElementById("progress-bar").style.width = "0%";
    }, 100);

    // Set a timeout to remove the flash message after 2.5 seconds and refresh the page
    setTimeout(() => {
        flashMessage.style.opacity = "0";
        flashMessage.style.transform = "translateX(100%)";

        // Remove the element from the DOM after the fade-out transition
        setTimeout(() => {
            flashMessageContainer.removeChild(flashMessage);
            location.reload(); // Refresh the page
        }, 500);
    }, 4500); // Now disappears after 2.5 seconds
}
