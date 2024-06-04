document.getElementById('login-form').addEventListener('submit', function(event) {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const data = {
                email: email,
                password: password
            };

            fetch('http://127.0.0.1:8000/auth/sign_in/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'error') {
                    if (data.errors) {
                        handleErrors(data.errors);
                    } else {
                        showFlashMessage('An unknown error occurred', 'danger');
                    }
                } else {
                    showFlashMessage(data.message, 'success');
                }
            })
            .catch(error => {
                showFlashMessage('An unexpected error occurred', 'danger');
                console.error('Error:', error);
            });
        });

function handleErrors(errors) {
            for (const key in errors) {
                if (errors.hasOwnProperty(key)) {
                    const error = errors[key];
                    if (Array.isArray(error)) {
                        error.forEach(errorMessage => {
                            showFlashMessage(`${errorMessage}`, 'danger');
                        });
                    } else {
                        showFlashMessage(`${key}: ${error}`, 'danger');
                    }
                }
            }
        }