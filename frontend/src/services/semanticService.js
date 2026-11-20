import { apiClient } from "@savic-technologies-pvt-ltd/platform-common";
import { SEMANTIC_API_RESOURCE_KEY } from "../constants.js";

export const semanticService = {
  getSnapshot: () => apiClient.get(SEMANTIC_API_RESOURCE_KEY),
};
