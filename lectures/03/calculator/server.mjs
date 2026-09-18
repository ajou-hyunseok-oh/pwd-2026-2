import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const base = resolve(fileURLToPath(new URL('.', import.meta.url)));
const mime = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
};
const port = Number(process.env.PORT || 4305);
createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    const demo = pathname === '/demo' || pathname === '/demo.html';
    const file = resolve(
      base,
      `.${pathname === '/' || demo ? '/index.html' : pathname}`,
    );
    if (!file.startsWith(base + sep)) {
      res.writeHead(403).end();
      return;
    }
    let content = await readFile(file);
    if (demo)
      content = content
        .toString('utf8')
        .replace('dist/src/main.js', 'dist/solution/main.js')
        .replace('학생용 시작 코드', '완성 예제');
    res.writeHead(200, {
      'Content-Type': `${mime[extname(file)] ?? 'text/plain'}; charset=utf-8`,
      'Cache-Control': 'no-store',
    });
    res.end(content);
  } catch {
    res.writeHead(404).end('Not found');
  }
}).listen(port, '127.0.0.1', () =>
  console.log(`학생용 http://127.0.0.1:${port}
완성 예제 http://127.0.0.1:${port}/demo`),
);
