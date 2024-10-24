

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
        const cover_letter = document.getElementById("cover_letter").value;


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
            cover_letter:cover_letter
           
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
       
        const institution = document.getElementById("institution").value;
        const field_of_study = document.getElementById("field").value;
        const nqf_level = document.getElementById("nqf").value;
        const start_date = document.getElementById("start_date").value;
        const end_date = document.getElementById("end_date").value;
         const status = document.getElementById("status").value;
       
        const personal_information = {

            institution : institution, 
            field_of_study : field_of_study,
            nqf_level : nqf_level,
            start_date : start_date, 
            end_date : end_date,
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

  function handle_update_computer_skill_button_click() {
       
        const skill = document.getElementById("skill3").value;
        const level = document.getElementById("level3").value;
        
        const skill_information = {
            skill : skill,
            level : level,
        };
        
        fetch("http://127.0.0.1:8000/profile/update/computer_skill_information/", {
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

  function handle_update_soft_skill_button_click() {
       
        const skill = document.getElementById("softskill1").value;
        const level = document.getElementById("proficiency1").value;
        
        const skill_information = {
            skill : skill,
            level : level,
        };
        
        fetch("http://127.0.0.1:8000/profile/update/soft_skill_information/", {
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

function handle_update_address_button_click() {
       
        const street = document.getElementById("residential_street_address").value;
        const city = document.getElementById("residential_city").value; 
        const province = document.getElementById("residential_province").value;
        const postal_code = document.getElementById("residential_postal_code").value;
        const address = {
            street : street,
            city : city,
            province : province,
            postal_code : postal_code
        };
        
        fetch("http://127.0.0.1:8000/profile/update/address_information/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(address),
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



function handle_update_working_experince_button_click() {
       
        const job_title = document.getElementById("wjob_title").value;
        const company = document.getElementById("wcompany").value; 
        const location = document.getElementById("wlocation").value;
        const start_date = document.getElementById("wstart_date").value;
       var end_date =  document.getElementById("wend_date").value;
        const description = document.getElementById("wdescription").value;
        const checkbox = document.getElementById("myCheckbox");

        if (checkbox.checked) {
            end_date = 'currentley working there ';
        } else {
            end_date = document.getElementById("wend_date").value;
        }
        const working_experince = {
            job_title : job_title,
            company : company,
            location : location,
            start_date : start_date,
            end_date : end_date,
            description : description
        };
        
        fetch("http://127.0.0.1:8000/profile/update/update_working_experince/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(working_experince),
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

function handle_update_reference_button_click() {
       
        const working_expereince = document.getElementById("working_expereince").value;
        const full_name = document.getElementById("full_name").value; 
        const phone = document.getElementById("rphone").value;
        const position = document.getElementById("rposition").value;
        const working_experince = {
            working_expereince : working_expereince,
            full_name : full_name,
            phone : phone,
            position : position,
            
        };
        
        fetch("http://127.0.0.1:8000/profile/update/update_reference/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(working_experince),
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

function uploadDocument(d_type, event) {
   event.preventDefault(); 
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
    
        if (data.status === 'success') {
            showFlashMessage('document uploaded successfully ', "success");
        
        } else {
          
            showFlashMessage('Error uploading document: ' + JSON.stringify(data.errors), "danger");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage(error, "danger");
    });
}

function take_quiz() {
  const url = 'http://127.0.0.1:8000/job/take_quiz/';
  
  const form = document.getElementById('myForm');
 
  const formData = new FormData(form);

  // Example: Convert formData to JSON object if needed
  const formDataObject = {};
  formData.forEach((value, key) => {
    formDataObject[key] = value;
  });

  console.log(formData)

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(formDataObject),
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors);
     
    } else if (data.status === "success") {
   
      showFlashMessage(data.message, "success");
      location.reload();
      showFlashMessage(data.message, "success");
    } else if (data.status === "warning") {
      
      showFlashMessage(data.message, "warning");
     
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
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