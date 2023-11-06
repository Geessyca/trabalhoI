import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    if (config.url !== '/login') {
      const username = localStorage.getItem("@Auth:access_email");
      const password = localStorage.getItem("@Auth:access_token");
      if (username && password) {
        const credentials = `${username}:${password}`;
        const encodedCredentials = btoa(credentials);
        config.headers.Authorization = `Basic ${encodedCredentials}`;
      }
    }
    return config; // Ensure to return the config in all cases
  },
  (error) => {
    return Promise.reject(error);
  }
);
