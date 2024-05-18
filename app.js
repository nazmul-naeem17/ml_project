function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const web_username = "Stack Neverflow";
  const web_password = "414";

  if (username === web_username && password === web_password) {
    window.location.href = "http://127.0.0.1:5000/";
  } else {
    alert("Incorrect Username or Password");
  }
}
