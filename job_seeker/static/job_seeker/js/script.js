

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
    
    // Setting the auto Progress
    function updateProgress(percentage) {
      const progressCircle = document.querySelector('.progress-circle');
      progressCircle.style.setProperty('--percentage', percentage);
      progressCircle.querySelector('span').textContent = percentage + '%';
  } 
  setTimeout(() => {
      updateProgress(50);
  }, 2000);