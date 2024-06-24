document.addEventListener("DOMContentLoaded", function() {
  // Parse shift start and end times
  const shiftStartTimeString = document.getElementById('shift_start').value; // Example: Shift starts at 9:00 AM
  const shiftEndTimeString = document.getElementById('shift_end').value; // Example: Shift ends at 5:00 PM
  const status = document.getElementById('status').value;
  const link = document.getElementById('links').value;

  const shiftStartTime = new Date(shiftStartTimeString);
  const shiftEndTime = new Date(shiftEndTimeString);
 
  let x = 0
  // Function to update countdown timer
  function updateCountdown() {
    const now = new Date();
    
    if (status == "Inactive") {    
          if (now < shiftStartTime) {
            // Shift has not started yet
            const timeUntilStart = shiftStartTime - now;
            document.getElementById('countdownHeader').textContent = 'Shift starts in ';
            setCountdown(timeUntilStart);
            document.getElementById('startShiftButton').disabled = true;
          } else if (now >= shiftStartTime && now < shiftEndTime) {
            // Shift is ongoing
            const timeUntilEnd = shiftEndTime - now;
            document.getElementById('countdownHeader').textContent = 'You have 10 mins before marked as late';
            setCountdown(timeUntilEnd);
            document.getElementById('startShiftButton').disabled = false;
          } else if (now > shiftEndTime){
            // Shift has ended
            const nextShiftStartTime = new Date(shiftStartTime);
            nextShiftStartTime.setDate(nextShiftStartTime.getDate() + 1); // Next day
            const timeUntilNextShift = nextShiftStartTime - now;
            document.getElementById('countdownHeader').textContent = 'Your Done for today, Next Shift Starts in ';
            setCountdown(timeUntilNextShift);
           const startShiftButton = document.getElementById('startShiftButton');
            startShiftButton.style.cursor = "not-allowed";
            startShiftButton.disabled = true;
            if (x == 0){
              sendShiftEndRequest(link);
              x = 1
             
            }

          }
    }else if(status == "Active"){

          const now = new Date();
          if (now > shiftEndTime){
             sendShiftEndRequest(link);
          }
          const timeUntilEnd = shiftEndTime - now;
          document.getElementById('countdownHeader').textContent = 'Shift ends in ';
          setCountdown(timeUntilEnd);
          document.getElementById('startShiftButton').disabled = true;
          document.getElementById('startShiftButton').textContent = "shift in progress";
      }
  }

  // Function to set and update the countdown display
  function setCountdown(time) {
    const countdownElement = document.getElementById('countdown');
    
    const hours = Math.floor(time / (1000 * 60 * 60));
    const minutes = Math.floor((time % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((time % (1000 * 60)) / 1000);
    document.getElementById('hours').textContent = formatTime(hours);
    document.getElementById('minutes').textContent = formatTime(minutes);
    document.getElementById('seconds').textContent = formatTime(seconds);
    
    
    // Update countdown every second
    setTimeout(updateCountdown, 1000);
  }

  function formatTime(time) {
    return time < 10 ? `0${time}` : time;
}

  // Initial call to set up the countdown
  updateCountdown();

  // Event listener for the start shift button
  
    
  
});


function attend(path) {
  window.location.href = path;
  showFlashMessage("Shift session started successfully", "success");
}

function sendShiftEndRequest(link) {
   fetch(link, {
      method: 'GET'
    })
    .then(response => {
            return response.json();
        })
        .then(data => {
          if (data.status === "error") {
              handleErrors(data.errors);
          } else if (data.status === "success") {
            showFlashMessage(data.message, "info");
            status = "Inactive";  
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
