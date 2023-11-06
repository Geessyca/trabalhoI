import { useState } from "react";
import { useAuth } from "../context/auth";
import "../style.css"

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { Login } = useAuth();

  const handleLogin = () => {
    Login({ email, password });
    
  };

  return (
    <div className="login-container">
        <h2>Login</h2>
        <form id="loginForm">
            <input
                onChange={(e) => {
                setEmail(e.target.value);
                }}
                placeholder="Email"
                className="input"
            />
            <input
                onChange={(e) => {
                setPassword(e.target.value);
                }}
                placeholder="Password"
                className="input"
            />
        </form>
        <button className="buttonLogin"onClick={handleLogin}>Login</button>
    </div>
  );
};