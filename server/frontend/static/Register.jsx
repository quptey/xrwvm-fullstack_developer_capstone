import React, { useState } from "react";
import "./Register.css";

/** User registration form for the Best Cars Django application. */
const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const gohome = () => {
    window.location.href = "/";
  };

  const register = async (event) => {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      const response = await fetch(`${window.location.origin}/djangoapp/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, firstName, lastName, email, password }),
      });

      const data = await response.json();

      if (response.ok && data.userName && !data.error) {
        sessionStorage.setItem("username", data.userName);
        window.location.href = "/";
        return;
      }

      if (data.error === "Already Registered") {
        setErrorMessage("This username is already registered. Please choose another username.");
      } else {
        setErrorMessage(data.error || "Registration failed. Please check your details and try again.");
      }
    } catch (error) {
      setErrorMessage("Could not connect to the registration service. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register_page">
      <div className="register_container">
        <div className="register_header">
          <h1 className="register_title">Create an account</h1>
          <button className="register_close" type="button" onClick={gohome} aria-label="Close registration">
            ×
          </button>
        </div>

        <p className="register_subtitle">Register to share your dealership experience.</p>

        <form onSubmit={register} className="register_form">
          <label htmlFor="register-username">Username</label>
          <input
            id="register-username"
            name="username"
            type="text"
            autoComplete="username"
            value={userName}
            onChange={(event) => setUserName(event.target.value)}
            required
          />

          <label htmlFor="register-first-name">First name</label>
          <input
            id="register-first-name"
            name="first_name"
            type="text"
            autoComplete="given-name"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            required
          />

          <label htmlFor="register-last-name">Last name</label>
          <input
            id="register-last-name"
            name="last_name"
            type="text"
            autoComplete="family-name"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            required
          />

          <label htmlFor="register-email">Email</label>
          <input
            id="register-email"
            name="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            name="password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          {errorMessage && <p className="register_error" role="alert">{errorMessage}</p>}

          <button className="register_submit" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Registering…" : "Register"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
