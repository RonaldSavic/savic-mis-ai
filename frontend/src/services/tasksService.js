import { apiClient } from "@savic-technologies-pvt-ltd/platform-common";
import { API_RESOURCE_KEY } from "../constants.js";

// apiClient adds the access token, refreshes it when it expires, and throws
// ApiError with the backend's error code and message on failure.
export const tasksService = {
  list: (params) => apiClient.get(API_RESOURCE_KEY, params),
  create: (body) => apiClient.post(API_RESOURCE_KEY, body),
  update: (id, body) => apiClient.patch(`${API_RESOURCE_KEY}/${id}`, body),
  remove: (id) => apiClient.delete(`${API_RESOURCE_KEY}/${id}`),
};
