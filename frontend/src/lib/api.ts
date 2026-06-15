import axios from "axios";
import { supabase } from "./supabase";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080",
});

api.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

export const detectDisease = async (file: File) => {
  const form = new FormData();
  form.append("image", file);
  const res = await api.post("/api/disease-detect", form);
  return res.data;
};

export const getFertilizerRecommendation = async (data: {
  crop: string; nitrogen: number; phosphorus: number; potassium: number;
  ph: number; temperature: number; humidity: number; rainfall: number;
}) => {
  const res = await api.post("/api/fertilizer", data);
  return res.data;
};

export const getYieldPrediction = async (data: {
  state: string; district: string; crop: string; rainfall: number;
  temperature: number; area: number; fertilizer_usage: number;
}) => {
  const res = await api.post("/api/yield", data);
  return res.data;
};

export const getWeatherAdvice = async (lat: number, lon: number) => {
  const res = await api.get("/api/weather-advice", { params: { lat, lon } });
  return res.data;
};

export const sendChatMessage = async (message: string, language: string = "hi") => {
  const res = await api.post("/api/chat", { message, language });
  return res.data;
};

export default api;
