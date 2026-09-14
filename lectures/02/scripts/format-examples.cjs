const fs = require('node:fs');
const path = require('node:path');
const prettier = require('../../../packages/web-deck/node_modules/prettier');
const options = require('../../../packages/web-deck/code-format.json');
const root = path.resolve(__dirname, '../examples');
async function format(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', 'dist'].includes(entry.name)) continue;
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) { await format(file); continue; }
    if (!/\.(html|css|js|jsx|mjs|json)$/.test(file) || /(?:source-data\.js|package-lock\.json)$/.test(file)) continue;
    fs.writeFileSync(file, await prettier.format(fs.readFileSync(file, 'utf8'), { ...options, printWidth: 80, filepath: file }));
  }
}
format(root).then(() => console.log('Formatted all example source files.')).catch(error => { console.error(error); process.exitCode = 1; });
