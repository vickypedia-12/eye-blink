import React, { useState } from "react";
import { register } from "../api";

export default function Register({ onRegistered }) {
  const [form, setForm] = useState({
    username: "",
    password: "",
    email: "",
    consent: false,
  });
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (name === "confirmPassword") {
      setConfirmPassword(value);
    } else {
      setForm({
        ...form,
        [name]: type === "checkbox" ? checked : value,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (form.password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    try {
      await register(form);
      onRegistered();
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Username</label>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="Choose a username"
            required
          />
        </div>
        <div className="input-group">
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="Enter your email"
            required
          />
        </div>
        <div className="input-group">
          <label>Password</label>
          <input
            type={showPassword ? "text" : "password"}
            name="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Create a password"
            required
          />
        </div>
        <div className="input-group">
          <label>Confirm password</label>
          <input
            type={showPassword ? "text" : "password"}
            name="confirmPassword"
            value={confirmPassword}
            onChange={handleChange}
            placeholder="Confirm your password"
            required
          />
        </div>
        <div className="checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={showPassword}
              onChange={() => setShowPassword((v) => !v)}
            />
            Show password
          </label>
        </div>
        <div className="checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="consent"
              checked={form.consent}
              onChange={handleChange}
              required
            />
            <span className="checkmark"></span>
            I consent to data collection for research purposes (GDPR compliant)
          </label>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Creating Account..." : "Create Account"}
        </button>
        {error && <div className="error-message">{error}</div>}
      </form>
    </div>
  );
}