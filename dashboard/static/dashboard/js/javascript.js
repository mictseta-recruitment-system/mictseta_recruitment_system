/*function showFlashMessage(message, type) {
  const flashMessageContainer = document.getElementById(
    "flash-message-container"
  );
  const flashMessage = document.createElement("div");
  flashMessage.className = `alert alert-${type} alert-dismissible fade show`;
  flashMessage.role = "alert";
  flashMessage.innerHTML = `
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            `;
  flashMessageContainer.appendChild(flashMessage);
}
*/
const sleep = async (milliseconds) => {
await new Promise(resolve => {
return setTimeout(resolve, milliseconds);
});
};

async function sleeper(jobID, mod, spinner, content) {
  console.log("sleeping");
  await sleep(2300);
  document.getElementById(spinner + jobID).style.display = 'none';
  document.getElementById(content + jobID).style.display = 'block';

  if (mod === 'true') {
    $('#JobToggle'+jobID).modal('hide');
    $('#skillToggle'+jobID).modal('show');
  }
}

/*===================================JOB FUNCTIONS  ===============================================================*/
function addJob() {
  // Replace with your actual endpoint URL
  const url = 'http://127.0.0.1:8000/job/add_job/';

  // Extract values from input fields
  title = document.getElementById('title').value;
  description = document.getElementById('description').value;
  end_date = document.getElementById('end_date').value;

  // Extract values from select fields
  const location = document.getElementById('location').value;
  const salary_range = document.getElementById('salary_range').value;
  const job_type = document.getElementById('job_type').value;

  // Extract value from company_name input field
  company_name = document.getElementById('company_name').value;
  industry = document.getElementById('industry').value;

  // Form JSON data object
  const jsonData = {
    title: title,
    description: description,
    end_date: end_date,
    location: location,
    salary_range: salary_range,
    job_type: job_type,
    industry: industry,
    company_name: company_name
  };

  // Fetch API POST request
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Include CSRF token if needed, adjust as per your Django setup
      'X-CSRFToken': getCookie('csrftoken') // Ensure this function gets the CSRF token
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    // Handle success response
    if (data.status === "error") {
        console.log(data.errors)
  if (data.errors) {
      handleErrors(data.errors);
  } else {
       showFlashMessage("An unknown error occurred", "danger");
    }
  } else if (data.status === "success") {
      title = ""
      description = ""
      end_date = ""
      company_name = ""
      industry = ""
    document.getElementById('addJobPage').style.display = 'none';
    document.getElementById('addJobPageComplete').style.display = 'block';
    showFlashMessage(data.message, "success");

  } else if (data.status === "warning") {
      
     showFlashMessage(data.message, "warning");
  }
  })
  .catch(error => {
    // Handle error
    console.error('Error:', error);
    // Replace with your error handling, such as displaying error messages
    showFlashMessage(error, "danger");
  });

   return false;
}

/********************UPDATE JOB********************/
function updateJob(jobID,spinner,content) {
  // Replace with your actual endpoint URL
  const url = 'http://127.0.0.1:8000/job/update_job/';
  document.getElementById('spinner' + jobID).style.display = 'block';
  document.getElementById('editJob' + jobID).style.display = 'none';

  // Extract values from input fields
  const title = document.getElementById('title'+ jobID).value;
  const description = document.getElementById('description'+ jobID).value;
  const end_date = document.getElementById('end_date'+ jobID).value;

  // Extract values from select fields
  const location = document.getElementById('location'+ jobID).value;
  const salary_range = document.getElementById('salary_range'+ jobID).value;
  const job_type = document.getElementById('job_type'+ jobID).value;

  // Extract value from company_name input field
  const company_name = document.getElementById('company_name'+ jobID).value;
  const industry = document.getElementById('industry'+ jobID).value;

  // Form JSON data object
  const jsonData = {
    title: title,
    description: description,
    end_date: end_date,
    location: location,
    salary_range: salary_range,
    job_type: job_type,
    industry: industry,
    company_name: company_name,
    job_id: jobID 
  };

  // Fetch API POST request
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Include CSRF token if needed, adjust as per your Django setup
      'X-CSRFToken': getCookie('csrftoken') // Ensure this function gets the CSRF token
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    // Handle success response
    if (data.status === "error") {
        console.log(data.errors)
        if (data.errors) {
            handleErrors(data.errors, jobID,spinner);
            sleeper(jobID, 'false',spinner,content);
           
        } else {
             showFlashMessage("An unknown error occurred", "danger");
          }
  } else if (data.status === "success") {
    document.getElementById(spinner + jobID).innerHTML =" ";
    document.getElementById(spinner + jobID).innerHTML =' <i class="fa fa-check fa-5x text-success"></i><p >' +data.message+'</p>';
                
    showFlashMessage(data.message, "success");
    
    sleeper(jobID,'true',spinner,content);
    $('#myModal').modal('show');


  } else if (data.status === "warning") {
    document.getElementById(spinner + jobID).innerHTML =" ";
    document.getElementById(spinner + jobID).innerHTML =' <i class="fa fa-check fa-5x text-warning"></i><p >' +data.message+'</p>';
     showFlashMessage(data.message, "warning");
     sleeper(jobID, 'false',spinner,content)

  }
  })
  .catch(error => {
    // Handle error
    console.error('Error:', error);
    // Replace with your error handling, such as displaying error messages
    showFlashMessage(error, "danger");
  });
}
/*****************************************************************************/

function addJobSkill(jobID, spinner, content, modal) {
  const url = 'http://127.0.0.1:8000/job/add_job_skill/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const skillListElement = document.getElementById('skillList' + jobID);

  const name = document.getElementById('name'+ jobID).value;
  const level = document.getElementById('level'+ jobID).value;
  
  const jsonData = {
    name: name,
    level: level,
    job_post_id: jobID 
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      skillListElement.innerHTML = '';

            // Re-render list items based on updated data
            data.skills.forEach(skill => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${skill.name}</div>
                        ${skill.level}
                    </div>
                    <i class="fa-solid fa-square-minus min-icon"></i>
                `;
                skillListElement.appendChild(listItem);
            });
      sleeper(jobID, 'true', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

function deleteSkill(jobID, spinner, content, modal, skillID) {
  const url = 'http://127.0.0.1:8000/job/delete_job_skill/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const skillListElement = document.getElementById('skillList' + jobID);

  const jsonData = {
    job_skill_id: skillID,
    job_post_id : jobID,
  }

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      skillListElement.innerHTML = '';

            // Re-render list items based on updated data
            data.skills.forEach(skill => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${skill.name}</div>
                        ${skill.level}
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteSkill(${jobID},'spinnerSkill','editSkill','skillToggle',${skill.id})"></i>
                `;
                skillListElement.appendChild(listItem);
            });
      sleeper(jobID, 'true', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

/*****************************************************************************/

function addEducation(jobID, spinner, content, modal) {
  const url = 'http://127.0.0.1:8000/job/add_job_acedemic/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const skillListElement = document.getElementById('educationList' + jobID);

  const level = document.getElementById('Elevel'+ jobID).value;
  const qualification = document.getElementById('qualification'+ jobID).value;
  
  const jsonData = {
    level: level,
    qualification: qualification,
    job_post_id: jobID 
  };
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {

    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      skillListElement.innerHTML = '';

            // Re-render list items based on updated data
            data.educations.forEach(education => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${education.level}</div>
                        ${education.qualification}
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteEducation(${jobID},'spinnerEducation','editEducation','EducationToggle',${education.id})"></i>
                `;
                skillListElement.appendChild(listItem);
            });
      sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

function deleteEducation(jobID, spinner, content, modal, educationID) {
  const url = 'http://127.0.0.1:8000/job/delete_job_acedemic/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const skillListElement = document.getElementById('educationList' + jobID);

  const jsonData = {
    job_academic_id: educationID,
    job_post_id : jobID,
  }

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      skillListElement.innerHTML = '';

            // Re-render list items based on updated data
            data.educations.forEach(education => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${education.level}</div>
                        ${education.qualification}
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteEducation(${jobID},'spinnerEducation','editEducation','EducationToggle',${education.id})"></i>
                `;
                skillListElement.appendChild(listItem);
            });
      sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}
/**************************************************************************************************************************************************************************/


function addExperience(jobID, spinner, content, modal) {
  const url = 'http://127.0.0.1:8000/job/add_job_expereince/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const skillListElement = document.getElementById('experienceList' + jobID);

  const name = document.getElementById('Ename'+ jobID).value;
  const duration = document.getElementById('Eduration'+ jobID).value;
  
  const jsonData = {
    duration: duration,
    name: name,
    job_post_id: jobID 
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      skillListElement.innerHTML = '';

            // Re-render list items based on updated data
            data.experiences.forEach(experience => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${experience.name}</div>
                        ${experience.duration}
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteExperience(${jobID},'spinnerExperience','editExperience','experienceToggle')"></i>
                `;
                skillListElement.appendChild(listItem);
            });
      sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

function deleteExperience(jobID, spinner, content, modal, experienceID) {
  const url = 'http://127.0.0.1:8000/job/delete_job_expereince/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const experinceElement = document.getElementById('experienceList' + jobID);

  const jsonData = {
    job_experience_id: experienceID,
    job_post_id : jobID,
  }

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      experinceElement.innerHTML = '';

            // Re-render list items based on updated data
            data.experiences.forEach(experience => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${experience.name}</div>
                        ${experience.duration}
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteExperience(${jobID},'spinnerExperience','editExperience','experienceToggle',${experience.id})"></i>
                `;
                experinceElement.appendChild(listItem);
            });
      sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

/*****************************************************************************************************************************************************/
function addRequirements(jobID, spinner, content, modal) {
  const url = 'http://127.0.0.1:8000/job/add_job_requirements/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const skillListElement = document.getElementById('requirementsList' + jobID);

  const description = document.getElementById('Rdescription'+ jobID).value;
  
  const jsonData = {
    description: description,
    job_post_id: jobID 
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      skillListElement.innerHTML = '';

            // Re-render list items based on updated data
            data.requirements.forEach(requirement => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${requirement.description}</div>
                       
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteRequirements(${jobID},'spinnerRequirements','editRequirements','requirementsToggle','${requirement.id}')"></i>
                `;
                skillListElement.appendChild(listItem);
            });
      sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

function deleteRequirements(jobID, spinner, content, modal, requirementsID) {
  const url = 'http://127.0.0.1:8000/job/delete_job_requirements/';
  document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';
  const experinceElement = document.getElementById('requirementsList' + jobID);

  const jsonData = {
    job_requirement_id: requirementsID,
    job_post_id : jobID,
  }

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
      experinceElement.innerHTML = '';

            // Re-render list items based on updated data
            data.requirements.forEach(requirement => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start');
                listItem.innerHTML = `
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${requirement.duration}</div>
                       
                    </div>
                    <i class="fa-solid fa-square-minus min-icon" onclick="deleteRequirements(${jobID},'spinnerRequirements','editRequirements','requirementsToggle',${requirement.id})"></i>
                `;
                experinceElement.appendChild(listItem);
            });
      sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal
      
    } else if (data.status === "warning") {
      document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', spinner, content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}
/*************************************************************************************************************************************************************/
function completeJob(jobID, spinner, content, modal) {
  const url = 'http://127.0.0.1:8000/job/complete_job/';
  /*document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';*/
 
  
  const jsonData = {
    job_post_id: jobID 
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
      sleeper(jobID, 'false', spinner, content);
    } else if (data.status === "success") {
      document.getElementById('modal-b' + jobID).innerHTML = '<i class="fa fa-check fa-5x text-success"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "success");
    
      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
      
    } else if (data.status === "warning") {
      document.getElementById('modal-b' + jobID).innerHTML = '<i class="fa fa-check fa-5x text-warning"></i><p>' + data.message + '</p>';
      showFlashMessage(data.message, "warning");
      sleeper(jobID, 'false', 'modal-b', content);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}

/***************************************************************************************************************************************************/
function ApproveJob(jobID) {
  const url = 'http://127.0.0.1:8000/job/approve_job/';
  /*document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';*/
 
  
  const jsonData = {
    job_post_id: jobID 
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
    } else if (data.status === "success") {
      location.reload();
      showFlashMessage(data.message, "success");
    
      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
      
    } else if (data.status === "warning") {
      showFlashMessage(data.message, "warning");
  
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}
/***************************************************************************************************************************************************/
function deleteJob(jobID) {
  const url = 'http://127.0.0.1:8000/job/delete_job/';
  /*document.getElementById(spinner + jobID).style.display = 'block';
  document.getElementById(content + jobID).style.display = 'none';*/
 
  
  const jsonData = {
    job_id: jobID 
  };
  console.log(getCookie('csrftoken'))
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(jsonData)
  })
  .then(response => {
    return response.json();
  })
  .then(data => {
    if (data.status === "error") {
      handleErrors(data.errors, jobID, spinner);
    } else if (data.status === "success") {
      location.reload()
      showFlashMessage(data.message, "success");
    
      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
      
    } else if (data.status === "warning") {
      showFlashMessage(data.message, "warning");
  
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showFlashMessage(error.message, "danger");
  });
}
/*===================================END JOB FUNCTIONS  ===============================================================*/
 function addStaff(){
             const url = 'http://127.0.0.1:8000/profile/add/add_staff/';

            let formData = {
                username: document.getElementById('username').value,
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                idnumber: document.getElementById('idnumber').value,
                job_title: document.getElementById('job_title').value,
                department: document.getElementById('department').value,
                password: document.getElementById('password').value,
                password2: document.getElementById('password2').value,
                super: document.getElementById('super').value,
                staff: document.getElementById('staff').value,
                salary: document.getElementById('salary').value,
                rate: document.getElementById('rate').value,
                start_time: document.getElementById('datetime1').value,
                end_time: document.getElementById('datetime').value
            };

            fetch(url, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(formData)
              })
              .then(response => {
                return response.json();
              })
              .then(data => {
                if (data.status === "error") {
                  handleErrors(data.errors);
                } else if (data.status === "success") {
                  document.getElementById('addStaffPage').style.display = 'none';
                  document.getElementById('addStaffPageComplete').style.display = 'block';
                  showFlashMessage(data.message, "success");
                
                  /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
                  
                } else if (data.status === "warning") {
                  showFlashMessage(data.message, "warning");
              
                }
              })
              .catch(error => {
                console.error('Error:', error);
                showFlashMessage(error.message, "danger");
              });
        }


function UpdateStaff(){
             const url = 'http://127.0.0.1:8000/profile/update/update_staff/';

            let formData = {
                username: document.getElementById('username').value,
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                idnumber: document.getElementById('idnumber').value,
                job_title: document.getElementById('job_title').value,
                department: document.getElementById('department').value,
                super: document.getElementById('super').value,
                staff: document.getElementById('staff').value,
                salary: document.getElementById('salary').value,
                rate: document.getElementById('rate').value,
                start_time: document.getElementById('datetime1').value,
                end_time: document.getElementById('datetime').value
            };

            fetch(url, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(formData)
              })
              .then(response => {
                return response.json();
              })
              .then(data => {
                if (data.status === "error") {
                  handleErrors(data.errors);
                } else if (data.status === "success") {
                  document.getElementById('UpdateStaffPage').style.display = 'none';
                  document.getElementById('UpdateStaffPageComplete').style.display = 'block';
                  showFlashMessage(data.message, "success");
                
                  /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
                  
                } else if (data.status === "warning") {
                  showFlashMessage(data.message, "warning");
              
                }
              })
              .catch(error => {
                console.error('Error:', error);
                showFlashMessage(error.message, "danger");
              });
        }


/*==================================================================================*/
function sendLeave(){
    const url = 'http://127.0.0.1:8000/profile/add/leave/';
    const leaveType = document.getElementById('leave_type').value;
    const message = document.getElementById('message').value;
    const startTime = document.getElementById('start_date').value;
    const endTime = document.getElementById('end_date').value;

    const data = {
        leave_type: leaveType,
        message: message,
        start_date: startTime,
        end_date: endTime,
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // If CSRF token is required
        },
        body: JSON.stringify(data),
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
          if (data.status === "error") {
              handleErrors(data.errors);
          } else if (data.status === "success") {
            showFlashMessage(data.message, "success");
                    
                      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
                      
          } else if (data.status === "warning") {
            showFlashMessage(data.message, "warning");
                  
          }
      })
      .catch(error => {
        console.error('Error:', error);
          showFlashMessage(error.message, "danger");
      });
}


function backup_database(){
   const url = 'http://127.0.0.1:8000/dashboard/backup_db/';
   fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // If CSRF token is required
        }
        
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
          if (data.status === "error") {
              handleErrors(data.errors);
          } else if (data.status === "success") {
            showFlashMessage(data.message, "success");
                    
                      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
                      
          } else if (data.status === "warning") {
            showFlashMessage(data.message, "warning");
                  
          }
      })
      .catch(error => {
        console.error('Error:', error);
          showFlashMessage(error.message, "danger");
      });
}

function restore_database(id){
   const url = 'http://127.0.0.1:8000/dashboard/restore_db/'+id+'/';
   fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // If CSRF token is required
        }
        
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
          if (data.status === "error") {
              handleErrors(data.errors);
          } else if (data.status === "success") {
            showFlashMessage(data.message, "success");
                    
                      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
                      
          } else if (data.status === "warning") {
            showFlashMessage(data.message, "warning");
                  
          }
      })
      .catch(error => {
        console.error('Error:', error);
          showFlashMessage(error.message, "danger");
      });
}

function delete_database(id){
   const url = 'http://127.0.0.1:8000/dashboard/delete_db/'+id+'/';
   fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // If CSRF token is required
        }
        
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
          if (data.status === "error") {
              handleErrors(data.errors);
          } else if (data.status === "success") {
            showFlashMessage(data.message, "success");
                    
                      /*sleeper(jobID, 'false', spinner, content); // Pass 'true' to show skillToggle modal*/
                      
          } else if (data.status === "warning") {
            showFlashMessage(data.message, "warning");
                  
          }
      })
      .catch(error => {
        console.error('Error:', error);
          showFlashMessage(error.message, "danger");
      });
}
// Function to get CSRF token (if needed, adjust as per your Django setup)
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

function handleErrors(errors, jobID, spinner) {
  document.getElementById('flash-message-container').innerHTML = '';
  for (const key in errors) {
    if (errors.hasOwnProperty(key)) {
      const error = errors[key];
      if (Array.isArray(error)) {
        error.forEach((errorMessage) => {
          showFlashMessage(`${key}: ${errorMessage}`, "danger");
          if (spinner){
          document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-exclamation-triangle fa-5x text-danger"></i><p><b>' + `${key}` + '</b>:' + ` ${errorMessage}` + '</p>';
          }
        });
      } else {
        showFlashMessage(`${key}: ${error}`, "danger");
        if (spinner){
           document.getElementById(spinner + jobID).innerHTML = '<i class="fa fa-exclamation-triangle fa-5x text-danger"></i><p><b>' + `${key} ` + '</b> :' + ` ${error}` + '</p>';  
        }
      }
    }
  }
}


function toggleVisibility(divId) {
            // Hide all divs
            const divs = ['profileinformation', 'companyinformation','infopage', 'vacanciesc', 'attendance'];
            divs.forEach(function(id) {
                document.getElementById(id).style.display = 'none';
            });


            
            // Show the selected div
            const div = document.getElementById(divId);
            console.log()
            div.style.display = 'block';
        }

      /*  // Initialize: hide all divs
        window.onload = function() {
            toggleVisibility(null);
        };*/