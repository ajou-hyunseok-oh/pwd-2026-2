const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const prettier = require('prettier');
const { HTMLHint } = require('htmlhint');
const options = require('../code-format.json');

const packageRoot = path.resolve(__dirname, '..');
const lectureRoot = path.resolve(packageRoot, '..', '..', 'lectures');
const write = process.argv.includes('--write');
const parsers = { html: 'html', css: 'css', javascript: 'babel', jsx: 'babel', typescript: 'typescript', tsx: 'typescript', json: 'json' };
const supported = [...Object.keys(parsers), 'bash', 'text'];
const errors = [];
let blocks = 0;
let variants = 0;

function decode(value) {
  const named = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };
  return value.replace(/&(#x[\da-f]+|#\d+|amp|lt|gt|quot|apos);/gi, (_, entity) => {
    if (entity[0] !== '#') return named[entity.toLowerCase()];
    return String.fromCodePoint(entity[1].toLowerCase() === 'x'
      ? parseInt(entity.slice(2), 16) : Number(entity.slice(1)));
  });
}

function encode(value) {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function literal(value) {
  return "'" + value.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
    .replace(/\n/g, '\\n').replace(/\r/g, '\\r') + "'";
}

async function format(value, language, width, label) {
  variants += 1;
  const normalized = value.replace(/\r\n?/g, '\n').trimEnd();
  const formatted = parsers[language]
    ? (await prettier.format(normalized, { ...options, parser: parsers[language], printWidth: width })).trimEnd()
    : normalized.split('\n').map((line) => line.trimEnd()).join('\n');
  if (language === 'html') {
    const fullDocument = /^\s*<!doctype html>/i.test(formatted);
    const diagnostics = HTMLHint.verify(formatted, {
      ...HTMLHint.defaultRuleset,
      'doctype-first': fullDocument,
      'doctype-html5': fullDocument,
      'title-require': fullDocument,
      'space-tab-mixed-disabled': 'space2',
      'attr-no-duplication': true
    });
    for (const item of diagnostics) errors.push(label + ':' + item.line + ': ' + item.message);
  }
  if (language === 'json') JSON.parse(formatted);
  if (!write && value.replace(/\r\n?/g, '\n') !== formatted) errors.push(label + ': run npm run format:code');
  return formatted;
}

async function processDeck(htmlPath) {
  let html = fs.readFileSync(htmlPath, 'utf8');
  const highlighter = html.indexOf('vendor/prism/prism.js');
  const runtime = html.search(/<script\b[^>]*src="[^"]*\/web-deck\.js"/);
  assert.ok(highlighter >= 0 && highlighter < runtime, htmlPath + ': load local Prism before the deck runtime');
  const contentPath = path.join(path.dirname(htmlPath), 'lecture-content.js');
  const contentSource = fs.existsSync(contentPath) ? fs.readFileSync(contentPath, 'utf8') : '';
  const sandbox = { window: {} };
  if (contentSource) vm.runInNewContext(contentSource, sandbox);
  const messages = sandbox.window.LECTURE_CONTENT;
  const replacements = [];
  const translated = new Map();

  for (const match of html.matchAll(/<pre\b([^>]*)>([\s\S]*?)<\/pre>/g)) {
    const [, attributes, markup] = match;
    const label = path.relative(lectureRoot, htmlPath) + ' block ' + (++blocks);
    const language = /data-wd-code="([^"]+)"/.exec(attributes)?.[1];
    assert.ok(supported.includes(language), label + ': declare data-wd-code (' + supported.join(', ') + ')');
    assert.match(attributes, /class="[^"]*\bwd-code\b/, label + ': use the shared wd-code class');
    assert.doesNotMatch(markup, /<[^>]+>/, label + ': escape code; syntax colors are applied by the runtime');
    const width = Number(/data-wd-code-width="(\d+)"/.exec(attributes)?.[1] || options.printWidth);
    assert.ok(width >= 32 && width <= 80, label + ': code width must be 32–80');
    const key = /data-wd-i18n="([^"]+)"/.exec(attributes)?.[1];
    let formatted;
    if (key) {
      assert.ok(messages, label + ': translated code requires lecture-content.js');
      const localized = {};
      for (const locale of ['ko', 'en']) {
        assert.equal(typeof messages[locale]?.[key], 'string', label + ': missing ' + locale + '.' + key);
        localized[locale] = await format(messages[locale][key], language, width, label + ' ' + locale + '.' + key);
      }
      formatted = localized.ko;
      translated.set(key, localized);
      if (!write && decode(markup).replace(/\r\n?/g, '\n') !== formatted) errors.push(label + ': HTML fallback differs from Korean code');
    } else {
      formatted = await format(decode(markup), language, width, label);
    }
    const start = match.index + match[0].indexOf('>') + 1;
    replacements.push({ start, end: start + markup.length, value: encode(formatted) });
  }

  if (!write) return;
  for (const { start, end, value } of replacements.reverse()) html = html.slice(0, start) + value + html.slice(end);
  if (html !== fs.readFileSync(htmlPath, 'utf8')) fs.writeFileSync(htmlPath, html);
  let content = contentSource;
  // Generated decks may use JSON-serialized keys and values.
  let jsonMessages;
  const assignment = /^window\.LECTURE_CONTENT\s*=\s*([\s\S]*?);?\s*$/.exec(contentSource);
  if (assignment) {
    try { jsonMessages = JSON.parse(assignment[1]); } catch { /* Hand-authored JavaScript below. */ }
  }
  for (const [key, localized] of translated) {
    assert.match(key, /^\w+$/);
    if (jsonMessages) {
      for (const locale of ['ko', 'en']) jsonMessages[locale][key] = localized[locale];
      continue;
    }
    let count = 0;
    const pattern = new RegExp("(^[ \\t]*" + key + ":\\s*)'(?:\\\\.|[^'\\\\])*'", 'gm');
    content = content.replace(pattern, (_, prefix) => {
      const locale = ['ko', 'en'][count++];
      assert.ok(locale, 'Duplicate translation key: ' + key);
      return prefix + literal(localized[locale]);
    });
    assert.equal(count, 2, 'Expected KO/EN strings for ' + key);
  }
  if (jsonMessages && translated.size) content = 'window.LECTURE_CONTENT = ' + JSON.stringify(jsonMessages, null, 2) + ';\n';
  if (content !== contentSource) fs.writeFileSync(contentPath, content);
}

(async () => {
  const folders = fs.readdirSync(lectureRoot).filter((name) => /^\d{2}$/.test(name)).sort();
  for (const folder of folders) await processDeck(path.join(lectureRoot, folder, 'index.html'));
  await processDeck(path.join(packageRoot, 'template', 'index.html'));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log('Code examples: ' + blocks + ' blocks / ' + variants + ' language variants ' + (write ? 'formatted' : 'checked') + '; syntax checks passed');
})().catch((error) => { console.error(error.message); process.exitCode = 1; });
