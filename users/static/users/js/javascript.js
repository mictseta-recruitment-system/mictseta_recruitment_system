

function handleErrors(errors) {
  for (const key in errors) {
    //to ensure it makes the container Empty before displaying the next error 
document.getElementById('flash-message-container').innerHTML=``;
//the next error
    if (errors.hasOwnProperty(key)) {
      const error = errors[key];
      if (Array.isArray(error)) {
        error.forEach((errorMessage) => {
          showFlashMessage(`${key}: ${errorMessage}`, "danger");
        });
      } else {
        showFlashMessage(`${key}: ${error}`, "danger");
      }
    }
  }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}