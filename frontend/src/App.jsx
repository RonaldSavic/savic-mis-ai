import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useLocation,
  useNavigate,
} from "react-router-dom";
import {
  AuthProvider,
  LocaleProvider,
  LoginPage,
  MenuRenderer,
  NotificationBell,
  ProtectedRoute,
  TenantProvider,
  ThemeProvider,
  useAuth,
  useHasAccess,
  useHasMenuAccess,
  useLocale,
  useReturnTo,
  useTheme,
} from "@savic-technologies-pvt-ltd/platform-common";
import {
  API_RESOURCE_KEY,
  ROUTE_PATH,
  SEMANTIC_API_RESOURCE_KEY,
  SEMANTIC_ROUTE_PATH,
} from "./constants.js";
import { TasksPage } from "./pages/TasksPage.jsx";
import { SemanticSnapshotPage } from "./pages/SemanticSnapshotPage.jsx";
import { platformRoutes } from "./platformRoutes.jsx";

// The app shell: sign-in, the menu (built from the user's grants), and the
// routes. Add each new page of this project as a <Route> below, with the
// route path and API resource key its MenuSpec seeds (backend extension.py).

function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        fontFamily: "system-ui",
        background: "var(--color-background, #fff)",
        color: "var(--color-text-primary, #111827)",
      }}
    >
      <aside
        style={{
          width: 220,
          flexShrink: 0,
          borderRight: "1px solid var(--color-border, #e5e7eb)",
          background: "var(--color-surface, transparent)",
        }}
      >
        <div
          style={{
            padding: "1rem",
            fontWeight: 700,
            color: "var(--color-primary, inherit)",
          }}
        >
          MIS AI
        </div>
        <MenuRenderer onNavigate={(path) => navigate(path)} />
        <PlatformCompaniesLink />
      </aside>
      <main style={{ flex: 1, minWidth: 0 }}>
        <header
          style={{
            display: "flex",
            justifyContent: "flex-end",
            alignItems: "center",
            gap: "1rem",
            padding: "0.75rem 1.5rem",
            borderBottom: "1px solid var(--color-border, #e5e7eb)",
          }}
        >
          <NotificationBell />
          <span style={{ fontSize: "0.875rem" }}>{user?.username}</span>
          <button type="button" onClick={() => logout()}>
            Log out
          </button>
        </header>
        <Routes>
          <Route path="/" element={<Navigate to={ROUTE_PATH} replace />} />

          {/* This project's pages */}
          <Route
            path={ROUTE_PATH}
            element={
              <ProtectedRoute apiResourceKey={API_RESOURCE_KEY}>
                <TasksPage />
              </ProtectedRoute>
            }
          />
          <Route
            path={SEMANTIC_ROUTE_PATH}
            element={
              <ProtectedRoute apiResourceKey={SEMANTIC_API_RESOURCE_KEY}>
                <SemanticSnapshotPage />
              </ProtectedRoute>
            }
          />

          {/* The platform's pages */}
          {platformRoutes.map(({ path, apiResourceKey, menuCode, element }) => (
            <Route
              key={path}
              path={path}
              element={
                <ProtectedRoute
                  apiResourceKey={apiResourceKey}
                  menuCode={menuCode}
                >
                  {typeof element === "function" ? element(user) : element}
                </ProtectedRoute>
              }
            />
          ))}

          <Route
            path="*"
            element={<p style={{ padding: "1.5rem" }}>Not found.</p>}
          />
        </Routes>
      </main>
    </div>
  );
}

// The platform admin holds the reserved PLATFORM_COMPANIES menu, which has no
// route of its own, so the menu doesn't list it. This link stands in for it.
function PlatformCompaniesLink() {
  const navigate = useNavigate();
  const isPlatform = useHasMenuAccess("PLATFORM_COMPANIES", "VIEW");
  const hasTenantSettings = useHasAccess("/api/v1/tenants", "VIEW");
  if (!isPlatform || hasTenantSettings) return null;
  return (
    <nav aria-label="Platform menu" style={{ padding: "0.5rem 1rem" }}>
      <a
        href="/admin/tenants"
        onClick={(e) => {
          e.preventDefault();
          navigate("/admin/tenants");
        }}
        style={{ color: "inherit", textDecoration: "none" }}
      >
        Company Management
      </a>
    </nav>
  );
}

function AuthGate() {
  const { user, initializing } = useAuth();
  const { refresh: refreshTheme } = useTheme();
  const { refresh: refreshLocale } = useLocale();
  const navigate = useNavigate();
  const location = useLocation();
  // Sends the user back to the page they asked for after signing in.
  const consumeReturnTo = useReturnTo({
    user,
    initializing,
    currentPath: location.pathname + location.search,
  });

  // The silent session restore (refresh-token cookie) is still running.
  if (initializing) return <p style={{ padding: "1.5rem" }}>Loading…</p>;

  if (!user) {
    return (
      <LoginPage
        onSuccess={async () => {
          // Theme and locale can only load once signed in.
          await refreshTheme();
          await refreshLocale();
          navigate(consumeReturnTo("/"), { replace: true });
        }}
      />
    );
  }
  return <AppShell />;
}

export function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <TenantProvider>
          <ThemeProvider>
            <LocaleProvider>
              <AuthGate />
            </LocaleProvider>
          </ThemeProvider>
        </TenantProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
