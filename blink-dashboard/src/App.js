import React, { useEffect, useState } from "react";
import Register from "./components/Register";
import Login from "./components/Login";
import BlinkData from "./components/BlinkData";
import "./App.css";


function App() {
  const [token, setToken] = useState(null);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
      const savedToken = localStorage.getItem("token");
      if(savedToken){
        setToken(savedToken);
      }
    }, [])

  const handleLoginSuccess = (token) => {
    setToken(token);
    localStorage.setItem("token", token);
    setShowLoginModal(false);
  };

  const handleLogout = () =>{
    setToken(null);
    localStorage.removeItem("token");
  }

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
        <BlinkData token={token} onLogout={handleLogout} />

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
            <h1>
              <img src="/image.png" alt="Blink Tracker Logo" style={{ height: "2em", verticalAlign: "middle", marginRight: "0.5em" }} />
              Blink Tracker
            </h1>
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
            <div style={{ paddingTop: "2em"}}>
              <a
                href="https://github.com/vickypedia-12/eye-blink/releases/latest/download/main.exe"
                className="btn btn-primary"
                download
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "0.7em", // space between logo and text
                  justifyContent: "center"
                }}
              >
                <img src="/windows-logo.png" alt="Windows" style={{ width: 30, height: 30 }} />
                <span>Windows App</span>
              </a>
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