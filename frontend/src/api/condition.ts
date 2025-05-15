import type { Condition } from "../types/condition";
import apiClient from "./client";
import axios from "axios";

export const getConditions = async () => {
  try {
    const response = await apiClient.get("/condition-types");
    return response.data;
  } catch (error) {
    console.error('Error fetching conditions:', error);
    if (axios.isAxiosError(error)) {
      console.error('Request URL:', error.config?.url);
      console.error('Response status:', error.response?.status);
      console.error('Response data:', error.response?.data);
    }
    throw error;
  }
};

export const addCondition = async (condition: Condition) => {
  try {
    const response = await apiClient.post("/condition-types", condition);
    return response.data;
  } catch (error) {
    console.error('Error adding condition:', error);
    if (axios.isAxiosError(error)) {
      console.error('Request URL:', error.config?.url);
      console.error('Response status:', error.response?.status);
      console.error('Response data:', error.response?.data);
    }
    throw error;
  }
};


