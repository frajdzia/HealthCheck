function validateSignup(event) { //function created to validate the signup form before submission
  const firstname = document.getElementById("firstname").value; //getting first name
  const lastname = document.getElementById("lastname").value;   // getting last name
  const email = document.getElementById("email").value;         //getting email
  const username = document.getElementById("username").value;   //getting username
  const password = document.getElementById("password").value;   //getting password

  if (!firstname || !lastname || !email || !username || !password) { //if first name, last name, email, username, and password is not filled
      event.preventDefault();     //prevent the form submission
      alert("Please fill out the form.");   //tell user to fill form if form is incomplete
  } else {
      window.location.href = homeUrl;     //go to homeUrl(dashboard) if all is filled
  }
}

function validateLogin(event) {     //function created to validate the login form before submision
  const username = document.getElementById("username").value;     //gettingc and validating username
  const password = document.getElementById("password").value;     //getting and validating password

  if (!username || !password) {   //if username or password is not filled
    event.preventDefault();     //prevent the form
      alert("Please fill out the form.");   //tell user to fill form if form is incomplete
  } else {
      window.location.href = homeUrl;       //go to homeUrrl(dashboard) if all is filled.
  }
}

function validatePassword(event) {    //function created to validate the forget password form before submission
  const username = document.getElementById("username").value; //getting username
  const password = document.getElementById("password").value; //getting password
  const code = document.getElementById("code").value; //getting code
  const phoneno = document.getElementById("phoneno").value; //getting phone number
  

  if (!username || !password || !code || !phoneno) {
      event.preventDefault(); //if username, passowrd, code, and phone no is not filled
      alert("Please fill out the form."); //tell user to fill form if form is incomplete
  } else {
      window.location.href = homeUrl;   //go to homeUrl(dashboard) if all is filled
  }
}

