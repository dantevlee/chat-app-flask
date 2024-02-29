import React, { useRef, useState, Fragment } from "react";
import axios from "axios";
import { Alert } from "react-bootstrap";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import chat from "../assets/chat.png";

const LoginForm = ({ setIsLoggedIn }) => {
  let usernameInputRef = useRef();
  let passwordInputRef = useRef();
  const [error, setError] = useState("");
  const [visitCount, setVisitCount] = useState(1);
  const [isInitialLoad, setIsInitialLoad] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (visitCount === 1) {
      setIsInitialLoad(true);
    }

    const loginBody = {
      username: usernameInputRef.current.value,
      password: passwordInputRef.current.value,
    };

   try {
  const response = await axios.post("http://localhost:5000/login", loginBody);

  if (response.data.message === "Invalid credentials") {
    setError("Invalid credentials. Please check your username and password.");
    setIsInitialLoad(true);
    return;
  }

  if (response.data.message === "User does not exist.") {
    setError("User not found. Please check your username.");
    setIsInitialLoad(true);
    return;
  }

  if (response.status === 200) {
    localStorage.setItem("token", response.data.access_token);
    localStorage.setItem("username", response.data.username)
    setIsInitialLoad(true);
    setIsLoggedIn(true)
  }

} catch (err) {
  setError("An error occurred. Please try again later.");
}
  };

  const removeNotification = () => {
    setIsInitialLoad(false);
    setVisitCount(0);
  };

  return (
    <Fragment>
      {isInitialLoad && (
        <Alert variant="info" onClose={() => removeNotification()} dismissible>
          This server is running on a free instance in the cloud that spins down
          if unused. It may take a few seconds for the first app log-in attempt.
          Thank you for your patience!
        </Alert>
      )}

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
            alt="chit-chit"
            style={{
              maxWidth: "100%",
              height: "auto",
              borderRadius: "5mm",
              marginBottom: "20px",
            }}
          />
          {error && <div className="alert alert-danger">{error}</div>}
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Username
            </label>
            <input
              required
              type="username"
              className="form-control"
              id="email"
              placeholder="Username..."
              ref={usernameInputRef}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              required
              type="password"
              className="form-control"
              id="password"
              placeholder="Password..."
              ref={passwordInputRef}
            />
          </div>

          <button type="submit" className="btn btn-primary">
            Submit
          </button>

          <p className="mt-3">
            Don't have an account? <Link to="/register">REGISTER</Link>
          </p>
        </form>
      </div>
    </Fragment>
  );
};

export default LoginForm;
