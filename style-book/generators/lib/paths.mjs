import { fileURLToPath } from "node:url";
import { join } from "node:path";

export const ROOT = fileURLToPath(new URL("../../", import.meta.url));

export function repoPath(...segments) {
  return join(ROOT, ...segments);
}
