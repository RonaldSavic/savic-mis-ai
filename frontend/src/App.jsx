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
  COMMENTARY_API_RESOURCE_KEY,
  COMMENTARY_ROUTE_PATH,
  ROUTE_PATH,
  SEMANTIC_API_RESOURCE_KEY,
  SEMANTIC_ROUTE_PATH,
} from "./constants.js";
import { TasksPage } from "./pages/TasksPage.jsx";
import { SemanticSnapshotPage } from "./pages/SemanticSnapshotPage.jsx";
import { CommentaryPage } from "./pages/CommentaryPage.jsx";
import { platformRoutes } from "./platformRoutes.jsx";

// The app shell: sign-in, the menu (built from the user's grants), and the
// routes. Add each new page of this project as a <Route> below, with the
// route path and API resource key its MenuSpec seeds (backend extension.py).

function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="mis-shell">
      <aside className="mis-sidebar">
        <div className="mis-brand">
          <span className="mis-brand-mark">M</span>
          <div className="mis-brand-title">MIS AI</div>
          <div className="mis-brand-subtitle">Management intelligence suite</div>
        </div>
        <MenuRenderer onNavigate={(path) => navigate(path)} />
        <PlatformCompaniesLink />
      </aside>
      <main className="mis-main">
        <header className="mis-header">
          <NotificationBell />
          <span className="mis-user">Signed in as <strong>{user?.username}</strong></span>
          <button className="mis-logout" type="button" onClick={() => logout()}>
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
          <Route
            path={COMMENTARY_ROUTE_PATH}
            element={
              <ProtectedRoute apiResourceKey={COMMENTARY_API_RESOURCE_KEY}>
                <CommentaryPage />
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
