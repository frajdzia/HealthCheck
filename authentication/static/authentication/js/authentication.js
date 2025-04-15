function validateSignup(event) {
  const firstname = document.getElementById("firstname").value;
  const lastname = document.getElementById("lastname").value;
  const email = document.getElementById("email").value;
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!firstname || !lastname || !email || !username || !password) {
      event.preventDefault();
      alert("Please fill out the form.");
  } else {
      window.location.href = homeUrl;
  }
}

function validateLogin(event) {

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    event.preventDefault();
      alert("Please fill out the form.");
  } else {
      window.location.href = homeUrl;
  }
}

function validatePassword(event) {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const code = document.getElementById("code").value;
  const phoneno = document.getElementById("phoneno").value;
  

  if (!username || !password || !code || !phoneno) {
      event.preventDefault();
      alert("Please fill out the form.");
  } else {
      window.location.href = homeUrl;
  }
}
