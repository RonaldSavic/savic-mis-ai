import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The app calls /api/... on its own origin. In development Vite forwards
// those calls to the backend, so there is no CORS to set up and the
// refresh-token cookie works. API_TARGET picks the backend:
//   http://localhost:8000  this project's backend (docker compose up), the default
//   http://localhost:8080  the platform release ZIP, for platform pages only
const apiTarget = process.env.API_TARGET || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: { "/api": apiTarget },
  },
});
