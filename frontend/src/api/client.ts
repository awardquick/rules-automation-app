import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api", // Update this URL as needed
    headers: {
      "Content-Type": "application/json",
    },
});

export default apiClient;

