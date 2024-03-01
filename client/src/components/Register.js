import React, { useRef } from "react";
import chat from '../assets/chat.png';
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const Register = () => {
  const firstNameRef = useRef();
  const lastNameRef = useRef();
  const usernameInputRef = useRef();
  const passwordInputRef = useRef();
  const history = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    const requestBody = {
      firstname: firstNameRef.current.value,
      lastname: lastNameRef.current.value,
      username: usernameInputRef.current.value,
      password: passwordInputRef.current.value,
    };

    axios.post('https://chat-app-flask.onrender.com/register', requestBody);
    history('/');
  }

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <form
        style={{
          width: 400,
          border: "1px solid",
          backgroundColor: "#cad5df",
          borderRadius: "5mm",
          padding: "20px",
        }}
        onSubmit={handleSubmit}
      >
        <img
          src={chat}
          style={{
            width: "100%",
            height: "auto",
            borderRadius: "5mm",
            marginBottom: "20px",
          }}
          alt="Chat"
        />
        <div className="mb-3">
          <label htmlFor="firstName" className="form-label">First Name</label>
          <input
            required
            type="text"
            className="form-control"
            id="firstName"
            placeholder="First Name.."
            ref={firstNameRef}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="lastName" className="form-label">Last Name</label>
          <input
            required
            type="text"
            className="form-control"
            id="lastName"
            placeholder="Last Name.."
            ref={lastNameRef}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Username</label>
          <input
            required
            type="username"
            className="form-control"
            id="email"
            placeholder="Username.."
            ref={usernameInputRef}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            required
            type="password"
            className="form-control"
            id="password"
            placeholder="Password.."
            ref={passwordInputRef}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
        <p className="mt-3">
          Already have an account? <Link to="/">LOGIN</Link>
        </p>
      </form>
    </div>
  );
}

export default Register;
