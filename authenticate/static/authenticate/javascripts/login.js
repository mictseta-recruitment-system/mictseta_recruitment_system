
    
    function handle_sign_in_button_click() {
        const lemail = document.getElementById("lemail").value;
        const lpassword = document.getElementById("lpassword").value;
        
       /* const forms = document.getElementById("login-form");
        csrftoken = forms.getElementsByTagName("input")[0].value;
        console.log(csrftoken)*/
        const data1 = {
          email: lemail,
          password: lpassword,
          csrfmiddlewaretoken:getCookie('csrftoken') ,
          /*csrftoken:csrftoken,
          jeff:"jeff"*/
        };
        fetch("http://127.0.0.1:8000/auth/sign_in/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken':getCookie('csrftoken') ,
            'csrfmiddlewaretoken':getCookie('csrftoken') ,
            'csrftoken':getCookie('csrftoken')
          },
          body: JSON.stringify(data1),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
                showFlashMessage(data.message, "success");
                window.location.href = "/";

            } else if (data.status === "warning") {
                showFlashMessage(data.message, "warning");
                window.location.href = "/profile/";
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }
   

       /*===================================================================================*/


    function handle_sign_up_button_click() {
      /*  const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;*/
        
        const email = document.getElementById("email").value;
        const idnumber = document.getElementById("idnumber").value;
        const password = document.getElementById("password").value;
        const password2 = document.getElementById("password2").value;
      /*  const phone = document.getElementById("phone").value;*/


        const data2 = {
            /*first_name : first_name,
            last_name : last_name,*/
           /* phone :  phone , */ 
            email : email,
           
            idnumber : idnumber,
            password : password,
            password2 : password2
        };

        fetch("http://127.0.0.1:8000/auth/sign_up/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken') 
          },
          body: JSON.stringify(data2),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
                window.location.href = "/auth/authenticates/";
                showFlashMessage(data.message, "success");

            } else if (data.status === "warning") {
                window.location.href = "/auth/authenticates/";
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
          });
    }

    /*===================================================================================*/ 

     
    /*===================================================================================*/ 




    function handle_forgot_button_click() {
        const femail = document.getElementById("femail").value;
        

        const data1 = {
          email: femail,
        };
        fetch("http://127.0.0.1:8000/auth/reset_password_link/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(data1),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
                showFlashMessage(data.message, "success");
                localStorage.setItem('value', data.link);
                window.location.href = "/auth/reset_link/";

            } else if (data.status === "warning") {
                showFlashMessage(data.message, "warning");
                window.location.href = "";
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
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
          showFlashMessage(`${key}:${errorMessage}`, "danger");
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

var btnSignUp = document.getElementById("btn-sign-up");
var frmSignUp = document.getElementById("wrapper-sign-up");
var frmSignIn = document.getElementById("wrapper-sign-in");
var btnSignIn = document.getElementById("btn-sign-in");

btnSignUp.addEventListener("click", funcDisplaySignUp);
btnSignIn.addEventListener("click", funcDisplaySignIn);

function funcDisplaySignUp(event) {
  event.preventDefault();
  frmSignUp.style.display = "block";
  frmSignIn.style.display = "none";
}

function funcDisplaySignIn(event) {
  event.preventDefault();
  frmSignUp.style.display = "none";
  frmSignIn.style.display = "block";
}
