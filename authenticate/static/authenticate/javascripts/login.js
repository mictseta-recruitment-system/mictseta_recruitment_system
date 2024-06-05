
document.addEventListener('DOMContentLoaded', (event) => {
    const sign_in = document.getElementById('btn-signin');

    
    function handle_sign_in_button_click() {
        const lemail = document.getElementById("lemail").value;
        const lpassword = document.getElementById("lpassword").value;

        const data1 = {
          email: lemail,
          password: lpassword,
        };
        fetch("http://127.0.0.1:8000/auth/sign_in/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
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
                window.location.href = "/auth/";

            } else if (data.status === "warning") {
                showFlashMessage(data.message, "warning");
                window.location.href = "/auth/";
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }
   
   const sign_up = document.getElementById('btn-signup');

    
    function handle_sign_up_button_click() {
        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const password2 = document.getElementById("password2").value;
        const linkedin = document.getElementById("linkedin").value;
        const website = document.getElementById("website").value;
        const job_title = document.getElementById("job_title").value;
        const employer = document.getElementById("employer").value;
        const year_expereince = document.getElementById("year_expereince").value;
        const industry = document.getElementById("industry").value;
        const carear_level = document.getElementById("carear_level").value;
        const desired_job = document.getElementById("desired_job").value;
        const job_location = document.getElementById("job_location").value;
        const idnumber = document.getElementById("idnumber").value;
        const phone = document.getElementById("phone").value;
        const address1 = document.getElementById("address1").value;
        const address2 = document.getElementById("address2").value;
        const city = document.getElementById("city").value;
        const province = document.getElementById("province").value;
        const postal_code = document.getElementById("postal_code").value;


        const data2 = {
            first_name: first_name,
            last_name : last_name,
            email: email,
            username : username,
            password : password,
            password2 :password2,
            idnumber:idnumber,
            phone :phone
        };
        fetch("http://127.0.0.1:8000/auth/sign_up/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
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
                window.location.href = "/authenticates/";
                showFlashMessage(data.message, "success");

            } else if (data.status === "warning") {
                window.location.href = "/authenticates/";
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }

    const forgot_pass = document.getElementById('btn-forgot');

    
    function handle_forgot_button_click() {
        const femail = document.getElementById("femail").value;
        

        const data1 = {
          email: femail,
        };
        fetch("http://127.0.0.1:8000/auth/reset_password_link/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
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
                window.location.href = "/auth/reset_link";

            } else if (data.status === "warning") {
                showFlashMessage(data.message, "warning");
                window.location.href = "/auth/";
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }
   

    sign_up.addEventListener('click', handle_sign_up_button_click)
    sign_in.addEventListener('click', handle_sign_in_button_click)
    forgot_pass.addEventListener('click', handle_forgot_button_click)



 });








function handleErrors(errors) {
  for (const key in errors) {
    //to ensure it makes the container Empty before displaying the next error 
document.getElementById('flash-message-container').innerHTML=``;
//the next error
    if (errors.hasOwnProperty(key)) {
      const error = errors[key];
      if (Array.isArray(error)) {
        error.forEach((errorMessage) => {
          showFlashMessage(`${errorMessage}`, "danger");
        });
      } else {
        showFlashMessage(`${key}: ${error}`, "danger");
      }
    }
  }
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
