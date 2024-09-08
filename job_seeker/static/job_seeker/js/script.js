

    function handle_update_profile_info_button_click() {
        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
      
        const email = document.getElementById("email").value;
        const idnumber = document.getElementById("idnumber").value;
        const phone = document.getElementById("phone").value;
        const maritial_status = document.getElementById("maritial_status").value;
        const race = document.getElementById("race").value;
        const disability = document.getElementById("disability").value;
        const linkedin_profile = document.getElementById("linkedin_profile").value;
        const personal_website = document.getElementById("personal_website").value;
        


        const data2 = {
            
            linkedin_profile : linkedin_profile,
            personal_website : personal_website,
            first_name : first_name,
            last_name : last_name,
            email : email,
            phone :  phone ,  
            idnumber : idnumber,
            maritial_status : maritial_status,
            race : race,
            disability : disability,
           
        };
       
        fetch("http://127.0.0.1:8000/profile/update/profile_information/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(data2),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
             console.log(data.errors)
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
                
                showFlashMessage(data.message, "success");

            } else if (data.status === "warning") {
                
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }
  function handle_update_qualification_button_click() {
       
        const highest_qualification = document.getElementById("highest_qualification").value;
        const field_of_study = document.getElementById("field_of_study").value;
        const institution = document.getElementById("institution").value;
        const year_obtained = document.getElementById("year_obtained").value;
         const status = document.getElementById("status").value;
        const grade = document.getElementById("grade").value;
       
        const personal_information = {

            highest_qualification : highest_qualification,
            field_of_study : field_of_study,
            institution : institution, 
            year_obtained : year_obtained, 
            grade : grade,
             status : status
        };
        

        fetch("http://127.0.0.1:8000/profile/update/update_qualification/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(personal_information),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
             console.log(data.errors)
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
                location.reload();
                showFlashMessage(data.message, "success");

            } else if (data.status === "warning") {
      
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }
    
  function handle_update_language_button_click() {
       
        const language = document.getElementById("language").value;
        const reading = document.getElementById("reading").value;
        const writing = document.getElementById("writing").value;
        const speaking = document.getElementById("speaking").value;
        
        const language_information = {
            language : language,
            reading_proficiency : reading,
            writing_proficiency : writing,
            speaking_proficiency : speaking,
        };
        
        fetch("http://127.0.0.1:8000/profile/update/language_information/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(language_information),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
             console.log(data.errors)
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
               
                showFlashMessage(data.message, "success");
                 location.reload();
            } else if (data.status === "warning") {
      
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }

  function handle_update_skill_button_click() {
       
        const skill = document.getElementById("skill1").value;
        const level = document.getElementById("level").value;
        
        const skill_information = {
            skill : skill,
            level : level,
        };
        
        fetch("http://127.0.0.1:8000/profile/update/skill_information/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(skill_information),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "error") {
             console.log(data.errors)
              if (data.errors) {
                handleErrors(data.errors);
              } else {
                showFlashMessage("An unknown error occurred", "danger");
              }
            } else if (data.status === "success") {
               
                showFlashMessage(data.message, "success");
                 location.reload();
            } else if (data.status === "warning") {
      
                showFlashMessage(data.message, "warning");
            }
          })
          .catch((error) => {
            showFlashMessage("An unexpected error occurred", "danger");
            console.error("Error:", error);
          });
    }


function uploadDocument(d_type) {
 
    if(d_type === 'license'){
      const form = document.getElementById('license-upload-form');
      formData = new FormData(form);
    }
     if(d_type === 'id'){
      const form = document.getElementById('id-upload-form');
      formData = new FormData(form);
    }
     if(d_type === 'passport'){
      const form = document.getElementById('passport-upload-form');
      formData = new FormData(form);
    }
    
    console.log(formData);

    fetch('http://127.0.0.1:8000/profile/update/upload_supporting_document/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if needed
        }
    })
    .then(response => response.json())
    .then(data => {
      if (data.errors) {
                handleErrors(data.errors);
              }
        if (data.status === 'success') {
            showFlashMessage('document uploaded successfully ', "success");
            location.reload()
        } else {
          
            showFlashMessage('Error uploading document: ' + JSON.stringify(data.errors), "danger");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage(error, "danger");
    });
}



    // Setting the auto Progress
    function updateProgress(percentage) {
      const progressCircle = document.querySelector('.progress-circle');
      progressCircle.style.setProperty('--percentage', percentage);
      progressCircle.querySelector('span').textContent = percentage + '%';
  } 
  setTimeout(() => {
      updateProgress(50);
  }, 2000);


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
        showFlashMessage(` ${error}`, "danger");
      }
    }
  }
}