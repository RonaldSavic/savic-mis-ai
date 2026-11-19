import { lstat, mkdir, symlink, unlink } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const frontendDirectory = path.resolve(scriptDirectory, "..");
const defaultSource = path.resolve(
  frontendDirectory,
  "..",
  "..",
  "Savic-Platform-main",
  "frontend",
  "packages",
  "savic-common",
);
const source = path.resolve(process.env.SAVIC_PLATFORM_COMMON_PATH || defaultSource);
const link = path.join(
  frontendDirectory,
  "node_modules",
  "@savic-technologies-pvt-ltd",
  "platform-common",
);

try {
  await lstat(path.join(source, "package.json"));
} catch {
  throw new Error(
    `Platform package not found at ${source}. Set SAVIC_PLATFORM_COMMON_PATH to its full path.`,
  );
}

await mkdir(path.dirname(link), { recursive: true });
try {
  const existing = await lstat(link);
  if (!existing.isSymbolicLink()) {
    throw new Error(`Refusing to replace non-link path ${link}.`);
  }
  await unlink(link);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
await symlink(source, link, process.platform === "win32" ? "junction" : "dir");

console.log(`Linked platform-common to ${source}`);
