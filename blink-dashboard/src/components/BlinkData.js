import React, { useEffect, useState } from "react";
import { fetchBlinks, fetchMe } from "../api";
import { Bar, Line } from "react-chartjs-2";
import { Chart, CategoryScale, LinearScale, BarElement,  PointElement, LineElement, TimeScale, Tooltip, Legend } from "chart.js";
import "chartjs-adapter-date-fns";

Chart.register(CategoryScale, LinearScale, BarElement,  PointElement, LineElement, TimeScale, Tooltip, Legend);
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
      <div className="analytics-section">
        <div className="analytics-card">
          <h2>Blinks per Session</h2>
          <Bar
            data={{
              labels: blinks.map((b, i) => `Session ${i + 1}`),
              datasets: [
                {
                  label: "Blinks",
                  data: blinks.map((b) => b.blink_count),
                  backgroundColor: "#1A237E",
                },
              ],
            }}
            options={{
              responsive: false,
              plugins: { legend: { display: false } },
              scales: { y: { beginAtZero: true } },
            }}
            width={450}
            height={220}
          />
        </div>
        <div className="analytics-card">
          <h2>Blinks Over Time</h2>
          <Line
            data={{
              labels: blinks.map((b) => new Date(b.from_timestamp)),
              datasets: [
                {
                  label: "Blinks",
                  data: blinks.map((b) => b.blink_count),
                  borderColor: "#00838F",
                  backgroundColor: "rgba(0,131,143,0.2)",
                  tension: 0.3,
                },
              ],
            }}
            options={{
              responsive: false,
              plugins: { legend: { display: false } },
              scales: {
                x: {
                  type: "time",
                  time: { unit: "day" },
                  title: { display: true, text: "Date" },
                },
                y: { beginAtZero: true, title: { display: true, text: "Blinks" } },
              },
            }}
            width={450}
            height={220}
          />
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
              {[...blinks]
                .sort((a, b) => new Date(b.from_timestamp) - new Date(a.from_timestamp))
                .map((b) => (
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