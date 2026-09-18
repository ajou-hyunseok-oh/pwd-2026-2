const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const prettier = require('../../../packages/web-deck/node_modules/prettier');
const options = require('../../../packages/web-deck/code-format.json');
const root = path.resolve(__dirname, '..');
(async () => {
  execFileSync('python', [path.join(__dirname, 'lesson-body.py')], { stdio: 'inherit' });
  const filename = path.join(root, 'materials/lesson-body.json');
  const body = JSON.parse(fs.readFileSync(filename, 'utf8'));
  const parsers = { javascript: 'babel', typescript: 'typescript', tsx: 'typescript', html: 'html', json: 'json' };
  for (const slide of Object.values(body.slides)) {
    for (const panel of slide.panels) {
      if (panel.kind !== 'code') continue;
      if (parsers[panel.language]) {
        panel.code = (await prettier.format(panel.code, { ...options, parser: parsers[panel.language], printWidth: 56 })).trimEnd();
      }
    }
  }
  fs.writeFileSync(filename, JSON.stringify(body, null, 2) + '\n');
  execFileSync('python', [path.join(__dirname, 'build-draft.py')], { stdio: 'inherit' });
})().catch((error) => { console.error(error); process.exitCode = 1; });
