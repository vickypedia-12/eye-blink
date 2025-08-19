import React, { useState } from "react";
import Register from "./components/Register";
import Login from "./components/Login";
import BlinkData from "./components/BlinkData";
import "./App.css";

function App() {
  const [token, setToken] = useState(null);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleLoginSuccess = (token) => {
    setToken(token);
    setShowLoginModal(false);
  };

  const handleRegisterSuccess = () => {
    setShowRegisterModal(false);
    setShowLoginModal(true);
  };

  const closeModals = () => {
    setShowRegisterModal(false);
    setShowLoginModal(false);
  };

  if (token) {
    return (
        <BlinkData token={token} onLogout={() => setToken(null)} />

    );
  }

  return (
    <>
      {/* Floating Bubbles */}
      <div className="bubbles">
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
      </div>

      <div className="homepage">
        {/* Hero Section */}
        <div className="hero">
          <div className="hero-content">
            <h1>👁️ Blink Tracker</h1>
            <p>Track your eye blinks and monitor your digital wellness</p>
            <div className="hero-buttons">
              <button 
                className="btn btn-primary" 
                onClick={() => setShowRegisterModal(true)}
              >
                Register
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={() => setShowLoginModal(true)}
              >
                Already have an account? Login
              </button>
            </div>
          </div>
        </div>

        {/* How it works Section */}
        <div className="how-it-works">
          <h2>How it works</h2>
          <div className="steps">
            <div className="step">
              <span>1</span>
              <p>Register your account and download the desktop app</p>
            </div>
            <div className="step">
              <span>2</span>
              <p>Track your blinks in real-time while using your computer</p>
            </div>
            <div className="step">
              <span>3</span>
              <p>View detailed analytics and insights on this dashboard</p>
            </div>
          </div>
        </div>

        {/* Registration Modal */}
        {showRegisterModal && (
          <div className="modal-overlay" onClick={closeModals}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={closeModals}>×</button>
              <Register onRegistered={handleRegisterSuccess} />
            </div>
          </div>
        )}

        {/* Login Modal */}
        {showLoginModal && (
          <div className="modal-overlay" onClick={closeModals}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={closeModals}>×</button>
              <Login onLogin={handleLoginSuccess} />
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default App;