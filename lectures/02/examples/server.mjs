import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderPage } from './generation/page.mjs';

const root = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.PORT || 4183);
const types = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.md': 'text/plain; charset=utf-8'
};
const server = http.createServer(async (request, response) => {
  try {
    const url = new URL(request.url, 'http://localhost');
    if (url.pathname === '/favicon.ico') {
      response.writeHead(204).end();
      return;
    }
    if (url.pathname === '/materials/week2-examples.zip') {
      response.setHeader('Content-Type', 'application/zip');
      response.end(
        await readFile(path.join(root, '../materials/week2-examples.zip'))
      );
      return;
    }
    if (
      url.pathname === '/generation/ssr.html' ||
      url.pathname === '/generation/en/ssr.html'
    ) {
      response.setHeader('Content-Type', 'text/html; charset=utf-8');
      response.end(renderPage(url.pathname.includes('/en/') ? 'en' : 'ko'));
      return;
    }
    const file = path.resolve(root, '.' + decodeURIComponent(url.pathname));
    const relative = path.relative(root, file);
    if (
      relative.startsWith('..') ||
      path.isAbsolute(relative) ||
      relative.split(path.sep).includes('node_modules')
    ) {
      response.writeHead(403).end('Forbidden');
      return;
    }
    const target = (await stat(file)).isDirectory()
      ? path.join(file, 'index.html')
      : file;
    response.setHeader(
      'Content-Type',
      types[path.extname(target)] || 'text/plain; charset=utf-8'
    );
    response.setHeader('Cache-Control', 'no-store');
    response.end(await readFile(target));
  } catch {
    response.writeHead(404).end('Not found');
  }
});
server.listen(port, '127.0.0.1', () =>
  console.log('Examples: http://localhost:' + port)
);
