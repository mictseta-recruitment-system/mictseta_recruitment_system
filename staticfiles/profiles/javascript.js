
document.addEventListener('DOMContentLoaded', (event) => {
  const update_address_info = document.getElementById('update_address_info');

    console.log("statrted")
    function handle_update_address_info_button_click() {
        console.log("statrted")
       
        const street_address_line = document.getElementById("street_address_line").value;
       console.log(street_address_line)

        const street_address_line1 = document.getElementById("street_address_line1").value;
        console.log(street_address_line1)
        const city = document.getElementById("city").value;
        console.log(city)
        const province = document.getElementById("province").value;
        console.log(province)
        const postal_code = document.getElementById("postal_code").value;

        console.log(postal_code)
        const address_info = {

            street_address_line : street_address_line,
            street_address_line1 : street_address_line1,
            city : city, 
            province  : province, 
            postal_code : postal_code,
           
        };
        console.log(address_info)

        fetch("http://127.0.0.1:8000/profile/update/address_information/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(address_info),
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
    
   
    
       /*===================================================================================*/
   const update_profile_info = document.getElementById('update_profile_info');

    function handle_update_profile_info_button_click() {
        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const idnumber = document.getElementById("idnumber").value;
        const phone = document.getElementById("phone").value;
        const maritial_status = document.getElementById("maritial_status").value;
        const race = document.getElementById("race").value;
        const disability = document.getElementById("disability").value;

        const data2 = {
            username : username,
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
    
    /*===================================================================================*/ 
    
     const update_qualification = document.getElementById('update_personal_info');

    
    function handle_update_qualification_button_click() {
       
        const highest_qualification = document.getElementById("highest_qualification").value;
        const field_of_study = document.getElementById("field_of_study").value;
        const institution = document.getElementById("institution").value;
        const year_obtained = document.getElementById("year_obtained").value;
        const grade = document.getElementById("grade").value;
       
        const personal_information = {

            highest_qualification : highest_qualification,
            field_of_study : field_of_study,
            institution : institution, 
            year_obtained : year_obtained, 
            grade : grade
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
    /*===================================================================================*/ 
      

    
    update_profile_info.addEventListener('click', handle_update_profile_info_button_click);

    
    update_qualification.addEventListener('click',handle_update_qualification_button_click);
    update_address_info.addEventListener('click', handle_update_address_info_button_click);


 });

function uploadImage() {
    const form = document.getElementById('image-upload-form');
    const formData = new FormData(form);

    fetch('http://127.0.0.1:8000/profile/update/upload_profile_image/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if needed
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showFlashMessage('Image uploaded successfully ', "success");
            location.reload()
        } else {
          
            showFlashMessage('Error uploading image: ' + JSON.stringify(data.errors), "danger");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage(error, "danger");
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
const triggerTabList = document.querySelectorAll('#myTab a')
triggerTabList.forEach(triggerEl => {
  const tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', event => {
    event.preventDefault()
    tabTrigger.show()
  })
})



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