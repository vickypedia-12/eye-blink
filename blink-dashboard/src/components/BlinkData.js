import React, { useEffect, useState } from "react";
import { fetchBlinks, fetchMe } from "../api";

export default function BlinkData({ token, onLogout }) {
  const [blinks, setBlinks] = useState([]);
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const me = await fetchMe(token);
        setUser(me.data);
        const res = await fetchBlinks(token, me.data.id);
        setBlinks(res.data);
      } catch (err) {
        setError("Failed to fetch blink data");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [token]);

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Loading your blink data...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1>Welcome back, {user?.username}! 👋</h1>
          <p>Here's your blink tracking data</p>
        </div>
        <button className="btn btn-outline" onClick={onLogout}>
          Logout
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Sessions</h3>
          <div className="stat-number">{blinks.length}</div>
        </div>
        <div className="stat-card">
          <h3>Total Blinks</h3>
          <div className="stat-number">
            {blinks.reduce((sum, b) => sum + b.blink_count, 0)}
          </div>
        </div>
        <div className="stat-card">
          <h3>Average per Session</h3>
          <div className="stat-number">
            {blinks.length ? Math.round(blinks.reduce((sum, b) => sum + b.blink_count, 0) / blinks.length) : 0}
          </div>
        </div>
      </div>

      <div className="blink-table-container">
        <h2>Session History</h2>
        {blinks.length === 0 ? (
          <div className="empty-state">
            <p>No blink data yet. Start the desktop app to begin tracking!</p>
          </div>
        ) : (
          <table className="blink-table">
            <thead>
              <tr>
                <th>Blink Count</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Duration</th>
              </tr>
            </thead>
            <tbody>
              {blinks.map((b) => (
                <tr key={b.id}>
                  <td className="blink-count">{b.blink_count}</td>
                  <td>{new Date(b.from_timestamp).toLocaleString()}</td>
                  <td>{new Date(b.to_timestamp).toLocaleString()}</td>
                  <td>
                    {Math.round((new Date(b.to_timestamp) - new Date(b.from_timestamp)) / 1000)}s
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}