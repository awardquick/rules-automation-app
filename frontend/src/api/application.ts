import apiClient from "./client";
import type { ApplicationCreate, ApplicationResponse } from "../types/application";

export const submitApplication = async (appData: ApplicationCreate): Promise<ApplicationResponse> => {
  const response = await apiClient.post("/applications", appData);
  return response.data;
};