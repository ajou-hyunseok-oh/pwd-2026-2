// Static checks for the nested review deck, which the numbered-deck suite does not scan.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const repo = path.resolve(root, '../../..');
const packageRoot = path.join(repo, 'packages/web-deck');
const prettier = require(path.join(packageRoot, 'node_modules/prettier'));
const ts = require(path.join(packageRoot, 'node_modules/typescript'));
const { HTMLHint } = require(path.join(packageRoot, 'node_modules/htmlhint'));
const options = require(path.join(packageRoot, 'code-format.json'));
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'lecture-content.js'), 'utf8'), sandbox);
const messages = sandbox.window.LECTURE_CONTENT;
const decode = text => text.replace(/&#(x[0-9a-f]+|\d+);|&(amp|lt|gt|quot|apos);/gi, (_, number, name) => number
  ? String.fromCodePoint(number[0].toLowerCase() === 'x' ? parseInt(number.slice(1), 16) : Number(number))
  : ({ amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" })[name]);

(async () => {
  assert.equal((html.match(/data-wd-slide=/g) || []).length, 9);
  assert.match(html, /data-lecture="07"/);
  assert.match(html, /LECTURE 07/);
  assert.match(html, /6주차 실습 리뷰/);
  const slideMap = JSON.parse(fs.readFileSync(path.join(root, 'materials/slide-map.json'), 'utf8'));
  assert.deepEqual(slideMap.map(slide => slide.id), [
    'cover', 'project', 'client', 'middleware', 'mvcs', 'async-query', 'create', 'errors', 'persistence'
  ], 'Follow the list request to completion before creation, errors and storage limits');
  assert.deepEqual(slideMap.slice(2, 6).map(slide => slide.request_flow), [
    {kind:'get', current:[0]}, {kind:'get', current:[1]},
    {kind:'get', current:[2,3]}, {kind:'get', current:[4,5]}
  ], 'Keep the same GET request and complete its response before showing variants');
  const lint = HTMLHint.verify(html, { ...HTMLHint.defaultRuleset, 'doctype-first': true, 'doctype-html5': true, 'attr-no-duplication': true });
  assert.deepEqual(lint, [], 'HTML lint');
  const codeKeys = new Set([...html.matchAll(/<pre[^>]+data-wd-i18n="([^"]+)"/g)].map(m => m[1]));
  for (const match of html.matchAll(/<([a-z][\w-]*)\b[^>]*data-wd-i18n="([^"]+)"[^>]*>([^<]*)<\/\1>/g)) {
    const [, , key, fallback] = match;
    assert.equal(decode(fallback), messages.ko[key], 'Korean HTML fallback: ' + key);
    for (const locale of ['ko', 'en']) assert.ok(messages[locale][key], 'Missing translation: ' + locale + '.' + key);
  }
  for (const [key, value] of Object.entries(messages.ko)) {
    if (!codeKeys.has(key)) {
      assert.doesNotMatch(value, /(?:니다|세요|십시오|는가|인가|을까|일까|하면|다면)(?:[.!?…]|$)/u, 'Slide prose style: ' + key);
    }
  }
  let codeBlocks = 0;
  for (const match of html.matchAll(/<pre\b([^>]*)>([\s\S]*?)<\/pre>/g)) {
    const [, attributes, fallback] = match;
    const key = /data-wd-i18n="([^"]+)"/.exec(attributes)[1];
    const language = /data-wd-code="([^"]+)"/.exec(attributes)[1];
    const value = messages.ko[key];
    assert.equal(messages.en[key], value, 'Source code must match across locales');
    assert.equal(decode(fallback), value);
    if (language === 'typescript') {
      const formatted = (await prettier.format(value, { ...options, parser: 'typescript', printWidth: 58 })).trimEnd();
      assert.equal(formatted, value, 'Common code format: ' + key);
      const diagnostics = ts.createSourceFile(key + '.ts', value, ts.ScriptTarget.Latest, true).parseDiagnostics;
      assert.equal(diagnostics.length, 0, 'TypeScript syntax: ' + key);
    } else assert.equal(language, 'bash');
    codeBlocks++;
  }
  const evidence = JSON.parse(fs.readFileSync(path.join(root, 'materials/runtime-evidence.json'), 'utf8'));
  const hashes = new Map(evidence.sourceFiles.map(file => [file.file, file.sha256]));
  const excerpts = JSON.parse(fs.readFileSync(path.join(root, 'materials/code-excerpts.json'), 'utf8'));
  const serverRoot = process.env.SERVER_ROOT;
  for (const [ident, excerpt] of Object.entries(excerpts)) {
    assert.equal(hashes.get(excerpt.file), excerpt.sha256, 'Source version: ' + ident);
    if (serverRoot) {
      const source = fs.readFileSync(path.join(serverRoot, excerpt.file), 'utf8');
      assert.equal(crypto.createHash('sha256').update(source).digest('hex'), excerpt.sha256);
      for (const selection of excerpt.selections)
        assert.equal(source.split(/\r?\n/).slice(selection.startLine - 1, selection.endLine).join('\n'), selection.text);
    }
  }
  const markup = html.replace(/<pre\b[\s\S]*?<\/pre>/g, '');
  for (const match of markup.matchAll(/(?:src|href)="([^"]+)"/g)) {
    if (/^(?:[a-z]+:|#)/i.test(match[1])) continue;
    assert.ok(fs.existsSync(path.resolve(root, match[1])), 'Missing asset: ' + match[1]);
  }
  assert.equal(evidence.requests.created.status, 201);
  assert.equal(evidence.requests.shared.status, 200);
  assert.equal(evidence.requests.lost.status, 404);
  assert.equal(codeBlocks, 8);
  console.log('Week 07 review: 9 slides in request order, bilingual defaults, 8 source code blocks and runtime evidence checked');
})().catch(error => { console.error(error); process.exitCode = 1; });
