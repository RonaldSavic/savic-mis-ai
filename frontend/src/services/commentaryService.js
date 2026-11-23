import { apiClient } from "@savic-technologies-pvt-ltd/platform-common";
import { COMMENTARY_API_RESOURCE_KEY } from "../constants.js";

export const commentaryService = {
  analyzeVariance: (body) => apiClient.post(COMMENTARY_API_RESOURCE_KEY, body),
  getReadiness: (companyCode, currency, metric) =>
    apiClient.get("/api/v1/mis-ai/commentary/readiness", {
      company_code: companyCode,
      currency,
      metric,
    }),
};
