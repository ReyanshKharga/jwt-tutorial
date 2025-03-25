import React, { useState } from "react";

const API_URL = "http://localhost:8000";

const App: React.FC = () => {
  const [message, setMessage] = useState("");

  const login = async () => {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: "admin", password: "password" }),
    });
    const data = await res.json();
    setMessage(data.message);
  };

  const fetchProtected = async () => {
    const res = await fetch(`${API_URL}/protected`, {
      credentials: "include",
    });
    const data = await res.json();
    setMessage(data.message || "Unauthorized");
  };

  const logout = async () => {
    await fetch(`${API_URL}/logout`, {
      method: "POST",
      credentials: "include",
    });
    setMessage("Logged out");
  };

  return (
    <div>
      <h2>Session-Based Auth (Redis)</h2>
      <button onClick={login}>Login</button>
      <button onClick={fetchProtected}>Fetch Protected</button>
      <button onClick={logout}>Logout</button>
      <p>{message}</p>
    </div>
  );
};

export default App;
