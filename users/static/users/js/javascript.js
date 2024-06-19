
function deleteUser(username) {
    
    const url = 'http://127.0.0.1:8000/user/delete_user/';  // Replace with your actual endpoint URL
    const data = {
        username: username,
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Function to get CSRF token
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            location.reload();
            showFlashMessage(result.message, "success");
           
        } else {
            
            showFlashMessage(result.errors, "danger");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage(error, "danger");
        showFlashMessage('An error occurred. Check the console for details.', "danger");
       
    });
}

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