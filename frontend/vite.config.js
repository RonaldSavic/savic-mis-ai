import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

const platformCommonPath = fileURLToPath(
  new URL("../../Savic-Platform-main/frontend/packages/savic-common", import.meta.url),
);
const appNodeModulesPath = fileURLToPath(new URL("./node_modules", import.meta.url));

// The app calls /api/... on its own origin. In development Vite forwards
// those calls to the backend, so there is no CORS to set up and the
// refresh-token cookie works. API_TARGET picks the backend:
//   http://localhost:8000  this project's backend (docker compose up), the default
//   http://localhost:8080  the platform release ZIP, for platform pages only
const apiTarget = process.env.API_TARGET || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  // platform-common is temporarily linked from the local Platform source
  // until its v1.1.0 Git tag is published. Keep resolution at this app's
  // node_modules so the linked package uses the same React/i18n peers.
  resolve: {
    preserveSymlinks: true,
    dedupe: ["react", "react-dom"],
    alias: [
      {
        find: /^react$/,
        replacement: `${appNodeModulesPath}/react`,
      },
      {
        find: /^react-dom$/,
        replacement: `${appNodeModulesPath}/react-dom`,
      },
      {
        find: /^i18next$/,
        replacement: `${appNodeModulesPath}/i18next`,
      },
      {
        find: /^react-i18next$/,
        replacement: `${appNodeModulesPath}/react-i18next`,
      },
      {
        find: /^lucide-react$/,
        replacement: `${appNodeModulesPath}/lucide-react`,
      },
      {
        find: /^@savic-technologies-pvt-ltd\/platform-common\/i18n$/,
        replacement: `${platformCommonPath}/src/i18n.js`,
      },
      {
        find: /^@savic-technologies-pvt-ltd\/platform-common\/styles$/,
        replacement: `${platformCommonPath}/src/styles/index.css`,
      },
      {
        find: /^@savic-technologies-pvt-ltd\/platform-common$/,
        replacement: `${platformCommonPath}/src/index.js`,
      },
    ],
  },
  // react-i18next reaches html-parse-stringify through the locally linked
  // Platform package. Prebundle its CommonJS dependency so the dev server
  // provides the default export expected by html-parse-stringify.
  optimizeDeps: {
    include: ["html-parse-stringify", "void-elements"],
  },
  server: {
    port: 5173,
    strictPort: true,
    proxy: { "/api": apiTarget },
  },
});
