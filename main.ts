// gta6-meme-x-01 entry program (Node 22, standard library only).
// The entry itself is the X post named in POST.json at the repo root.
// The grader runs this file; all it must do is hand POST.json to the
// output directory unchanged, where the house gate reads it and then
// fetches the post (first picture + text) from X for the judge.
// Local run: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  console.error("POST.json could not be copied: " + message);
  process.exit(1);
}
