import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export default api;

export const getHospitalPatients = async (
  hospitalId: number
) => {
  const response = await api.get(
    `/hospitals/${hospitalId}/patients`
  );

  return response.data;
};