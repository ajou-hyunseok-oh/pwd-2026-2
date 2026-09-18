import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL(".", import.meta.url));
const base = resolve(root);
const mime = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json" };
createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
    const file = resolve(base, `.${pathname === "/" ? "/index.html" : pathname}`);
    if (!file.startsWith(base + sep)) { res.writeHead(403).end(); return; }
    const content = await readFile(file);
    res.writeHead(200, { "Content-Type": `${mime[extname(file)] ?? "text/plain"}; charset=utf-8`, "Cache-Control": "no-store" });
    res.end(content);
  } catch { res.writeHead(404).end("Not found"); }
}).listen(4303, "127.0.0.1", () => console.log("http://127.0.0.1:4303"));
