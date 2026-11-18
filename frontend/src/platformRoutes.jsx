import {
  AccessMatrixPage,
  ActivityLogPage,
  CitiesPage,
  CompanyLocalePage,
  CompanyThemePage,
  DashboardPage,
  ImportHistoryPage,
  MasterDataReferencePage,
  NotificationTemplatesPage,
  OrgUnitsPage,
  RolesPage,
  ScheduledJobsPage,
  SystemConfigPage,
  TenantsPage,
  UnitsOfMeasurePage,
  UserRolesPage,
} from "@savic-technologies-pvt-ltd/platform-common";

// The platform's own screens. The platform seeds a menu entry for each
// (svcplt.menu_master), and the menu links to these exact paths, so keep
// them unchanged. Remove an entry only if your project hides that menu.
export const platformRoutes = [
  // Either grant opens company management: TENANT_SETTINGS for a company
  // administrator, the reserved PLATFORM_COMPANIES for the platform admin.
  {
    path: "/admin/tenants",
    apiResourceKey: "/api/v1/tenants",
    menuCode: "PLATFORM_COMPANIES",
    element: <TenantsPage />,
  },
  {
    path: "/admin/org-units",
    apiResourceKey: "/api/v1/tenants/org-units",
    element: (user) => <OrgUnitsPage tenantId={user?.companyId} />,
  },
  {
    path: "/rbac/roles",
    apiResourceKey: "/api/v1/rbac/roles",
    element: <RolesPage />,
  },
  {
    path: "/rbac/users",
    apiResourceKey: "/api/v1/rbac/users",
    element: <UserRolesPage />,
  },
  {
    path: "/rbac/access-matrix",
    apiResourceKey: "/api/v1/rbac/access-matrix",
    element: <AccessMatrixPage />,
  },
  {
    path: "/admin/menus",
    apiResourceKey: "/api/v1/rbac/menus",
    element: (
      <p style={{ padding: "1.5rem" }}>The platform has no Menus screen yet.</p>
    ),
  },
  {
    path: "/admin/activity-log",
    apiResourceKey: "/api/v1/activity-log",
    element: <ActivityLogPage />,
  },
  {
    path: "/admin/colour-schema",
    apiResourceKey: "/api/v1/theme/company",
    element: <CompanyThemePage />,
  },
  {
    path: "/admin/system-config",
    apiResourceKey: "/api/v1/config",
    element: <SystemConfigPage />,
  },
  {
    path: "/admin/notification-templates",
    apiResourceKey: "/api/v1/notification-templates",
    element: <NotificationTemplatesPage />,
  },
  {
    path: "/admin/localization-settings",
    apiResourceKey: "/api/v1/locale/company",
    element: <CompanyLocalePage />,
  },
  {
    path: "/dashboard",
    apiResourceKey: "/api/v1/dashboard/layout",
    element: <DashboardPage />,
  },
  {
    path: "/master-data/reference",
    apiResourceKey: "/api/v1/master-data/countries",
    element: <MasterDataReferencePage />,
  },
  {
    path: "/master-data/cities",
    apiResourceKey: "/api/v1/master-data/cities",
    element: <CitiesPage />,
  },
  {
    path: "/master-data/uom",
    apiResourceKey: "/api/v1/master-data/uom",
    element: <UnitsOfMeasurePage />,
  },
  {
    path: "/admin/scheduled-jobs",
    apiResourceKey: "/api/v1/scheduler/jobs",
    element: <ScheduledJobsPage />,
  },
  {
    path: "/admin/imports",
    apiResourceKey: "/api/v1/imports",
    element: <ImportHistoryPage />,
  },
];
