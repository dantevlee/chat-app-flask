import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import ChatPage from "./components/ChatPage";
import LoginForm from "./components/LoginForm";
import Register from "./components/Register";
import "bootstrap/dist/css/bootstrap.min.css";
import './App.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  return (
    <div className="App">
      <Router>
        <Routes>
          <Route
            path="/chat"
            element={isLoggedIn ? <ChatPage setIsLoggedIn={setIsLoggedIn} /> : <Navigate to="/" />}
          />
          <Route
            path="/"
            element={isLoggedIn ? <Navigate to="/chat" /> : <LoginForm setIsLoggedIn={setIsLoggedIn} />}
          />
          <Route path="/register" element={<Register />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
