import React, { useState } from "react";
import "./Register.css";
import Header from "../Header/Header";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register_url = window.location.origin + "/djangoapp/register";

  const gohome = () => {
    window.location.href = window.location.origin;
  };

  const register = async (e) => {
    e.preventDefault();
    const res = await fetch(register_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userName: userName,
        password: password,
        firstName: firstName,
        lastName: lastName,
        email: email,
      }),
    });
    const json = await res.json();
    if (json.status) {
      sessionStorage.setItem("username", json.userName);
      sessionStorage.setItem("firstname", firstName);
      sessionStorage.setItem("lastname", lastName);
      window.location.href = window.location.origin;
    } else if (json.error === "Already Registered") {
      alert("The user with same username is already registered");
      window.location.href = window.location.origin;
    }
  };

  return (
    <div>
      <Header />
      <div className="register_container">
        <div className="header">
          <span className="text">Sign-up</span>
          <a href="/" onClick={gohome} className="close_link" aria-label="Close">×</a>
        </div>
        <form onSubmit={register}>
          <div className="inputs">
            <div className="input">
              <label htmlFor="username">Username</label>
              <input id="username" type="text" name="username" placeholder="Username" className="input_field" required onChange={(e) => setUserName(e.target.value)} />
            </div>
            <div className="input">
              <label htmlFor="first_name">First Name</label>
              <input id="first_name" type="text" name="first_name" placeholder="First Name" className="input_field" required onChange={(e) => setFirstName(e.target.value)} />
            </div>
            <div className="input">
              <label htmlFor="last_name">Last Name</label>
              <input id="last_name" type="text" name="last_name" placeholder="Last Name" className="input_field" required onChange={(e) => setLastName(e.target.value)} />
            </div>
            <div className="input">
              <label htmlFor="email">Email</label>
              <input id="email" type="email" name="email" placeholder="Email" className="input_field" required onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className="input">
              <label htmlFor="psw">Password</label>
              <input id="psw" name="psw" type="password" placeholder="Password" className="input_field" required onChange={(e) => setPassword(e.target.value)} />
            </div>
          </div>
          <div className="submit_panel">
            <input className="submit" type="submit" value="Register" />
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
