import { readFileSync } from "node:fs";
import { parse } from "smol-toml";

export function parseToml(text) {
  return parse(text);
}

export function readToml(file) {
  return parse(readFileSync(file, "utf8"));
}
