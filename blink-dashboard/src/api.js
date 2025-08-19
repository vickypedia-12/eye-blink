import axios from "axios";

// const API_URL = "http://127.0.0.1:8000/api";
const API_URL = "http://fastapi-blink-app-env.eba-tabdyx3u.ap-south-1.elasticbeanstalk.com/api";

export const register = (user) =>
  axios.post(`${API_URL}/auth/register`, user);

export const login = (username, password) =>
  axios.post(
    `${API_URL}/auth/login`,
    new URLSearchParams({
      grant_type: "password",
      username,
      password,
    }),
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );

export const fetchBlinks = (token, userId) =>
  axios.get(`${API_URL}/user/${userId}/blinks`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const fetchMe = (token) =>
  axios.get(`${API_URL}/user/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });