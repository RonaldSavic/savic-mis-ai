import React from "react";
import ReactDOM from "react-dom/client";
import "@savic-technologies-pvt-ltd/platform-common/i18n";
import "@savic-technologies-pvt-ltd/platform-common/styles";
import { App } from "./App.jsx";

// Register this project's dashboard widgets here, before anything renders:
//   import { registerWidget } from "@savic-technologies-pvt-ltd/platform-common";
//   registerWidget("mis_ai_overdue", OverdueWidget);
// (see docs/module-specs/dashboard.md in the platform repo).

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
