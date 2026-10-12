// An explicitly requested verbatim copy must stay equal to its reviewed source.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const sections = html => [...html.matchAll(/<section\b[^>]*data-wd-slide="[^"]+"[^>]*>[\s\S]*?<\/section>/g)].map(m => m[0]);
const sourceId = section => section.match(/data-wd-slide="([^"]+)"/)[1];
// The formatter may serialize quote entities differently inside escaped code.
const normalize = section => section.replace(' is-active', '')
  .replace(/(<pre\b[^>]*>)([\s\S]*?)(<\/pre>)/g, (_, open, code, close) =>
    open + code.replace(/&#x27;/g, "'").replace(/&quot;/g, '"') + close);

module.exports = function validateImports(html, messages, directory) {
  const imported = sections(html).filter(section => /data-wd-import=/.test(section));
  if (!imported.length) return;
  for (const section of imported) assert.match(section, /data-wd-import="04\/react"/, 'Unknown imported deck');
  const source = path.resolve(directory, '../04');
  const original = sections(fs.readFileSync(path.join(source, 'index.html'), 'utf8'));
  assert.equal(imported.length, original.length, 'Copy the complete Lecture 04 React deck');
  for (let i = 0; i < original.length; i++) {
    const id = sourceId(original[i]);
    assert.ok(imported[i].includes(`data-wd-source-slide="${id}"`), `Imported slide ${i + 1}: original order changed`);
    const restored = imported[i]
      .replace(' data-wd-import="04/react"', '')
      .replace(` data-wd-source-slide="${id}"`, '')
      .replace('data-wd-slide="chapter-01"', 'data-wd-slide="cover"')
      .replaceAll('../04/', '');
    // The user explicitly rewrote Week 5 screens 24–25; the other markup stays exact.
    if (id === 'slide-24') {
      assert.match(imported[i], /data-wd-import-override="vite-template-edit"/);
      assert.match(imported[i], /Hello, World!/);
      assert.match(imported[i], /export default function App/);
      continue;
    }
    if (id === 'slide-23') {
      assert.match(imported[i], /data-wd-import-override="vite-interactive"/);
      assert.match(imported[i], /npm create vite@latest/);
      assert.doesNotMatch(imported[i], /--template react-ts/);
      continue;
    }
    assert.equal(normalize(restored), normalize(original[i]), `Imported ${id}: source content or markup changed`);
  }
  const sandbox = {window: {}};
  vm.runInNewContext(fs.readFileSync(path.join(source, 'lecture-content.js'), 'utf8'), sandbox);
  const corrections = JSON.parse(fs.readFileSync(path.join(directory, 'materials/import-text-corrections.json'), 'utf8'));
  const corrected = new Map();
  for (const correction of corrections) {
    const {source_slide: id, locale, key, before, after} = correction;
    assert.equal(locale, 'en', 'Import text corrections preserve Korean HTML');
    const originalSlide = original.find(section => sourceId(section) === id);
    assert.ok(originalSlide?.includes(`data-wd-i18n="${key}"`), `Correction ${key}: wrong source slide`);
    assert.equal(sandbox.window.LECTURE_CONTENT[locale][key], before, `Correction ${key}: original text changed`);
    assert.ok(typeof after === 'string' && after.trim() && before !== after, `Correction ${key}: empty or unchanged replacement`);
    assert.ok(!corrected.has(`${locale}:${key}`), `Correction ${key}: duplicate replacement`);
    corrected.set(`${locale}:${key}`, after);
  }
  for (const locale of ['ko', 'en']) {
    for (const [key, value] of Object.entries(sandbox.window.LECTURE_CONTENT[locale])) {
      if (key.startsWith('slide_')) assert.equal(messages[locale][key], corrected.get(`${locale}:${key}`) ?? value,
        `Imported ${locale}.${key}: source text changed outside its recorded correction`);
    }
  }
  assert.match(html, /href="\.\.\/04\/lecture\.css"/, 'Reuse the original React slide styles');
  assert.match(html, /href="\.\.\/04\/react-cleanup\.css"/, 'Reuse the original React explanation styles');
  assert.match(html, /src="\.\.\/04\/assets\/react-demos\.js"/, 'Reuse the original React demos');
  for (const file of ['hello-world.png', 'hello-react.png']) {
    assert.deepEqual(fs.readFileSync(path.join(directory, 'materials/images', file)),
      fs.readFileSync(path.join(source, 'materials/images', file)), `Imported demo image changed: ${file}`);
  }
  const map = JSON.parse(fs.readFileSync(path.join(directory, 'materials/slide-map.json'), 'utf8'));
  const entries = map.filter(slide => slide.import_source);
  assert.equal(entries.length, original.length, 'Imported slide map is incomplete');
  entries.forEach((slide, i) => {
    assert.equal(slide.import_source.slide, sourceId(original[i]));
    assert.equal(slide.import_source.number, i + 1);
    assert.equal(slide.number, i + 2, 'Imported React deck must be the first chapter after the cover');
    assert.equal(slide.chapter, 'CHAPTER 01 · React 기초');
    assert.deepEqual(slide.import_text_corrections || [],
      corrections.filter(correction => correction.source_slide === slide.import_source.slide)
        .map(correction => `${correction.locale}:${correction.key}`), 'Imported correction metadata differs');
  });
};
