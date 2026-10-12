// The contract applies to authored 05+ decks; historical decks keep their exceptions.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const validateImports = require('./authoring-imports.cjs');
const root = path.resolve(__dirname, '../../..');
const decode = text => text.replace(/&#(x[0-9a-f]+|\d+);|&(amp|lt|gt|quot|apos);/gi, (_, n, name) =>
  n ? String.fromCodePoint(n[0].toLowerCase() === 'x' ? parseInt(n.slice(1), 16) : Number(n)) :
    ({amp: '&', lt: '<', gt: '>', quot: '"', apos: "'"})[name.toLowerCase()]);
let decks = 0;
for (let week = 5; week <= 13; week++) {
  const number = String(week).padStart(2, '0');
  const directory = path.join(root, 'lectures', number);
  const html = fs.readFileSync(path.join(directory, 'index.html'), 'utf8');
  const slides = [...html.matchAll(/<section\b([^>]*data-wd-slide="([^"]+)"[^>]*)>([\s\S]*?)<\/section>/g)];
  // A cover-only future deck has no authored lesson content yet.
  if (slides.length === 1) continue;
  assert.match(html, /data-wd-authoring="v1"/, `Lecture ${number}: missing authoring harness`);
  assert.match(html, /packages\/web-deck\/authoring\.css/, `Lecture ${number}: missing shared authoring CSS`);
  const sandbox = {window: {}};
  vm.runInNewContext(fs.readFileSync(path.join(directory, 'lecture-content.js'), 'utf8'), sandbox);
  const messages = sandbox.window.LECTURE_CONTENT;
  assert.deepEqual(Object.keys(messages.ko).sort(), Object.keys(messages.en).sort(), `${number}: KO/EN keys differ`);
  validateImports(html, messages, directory);
  const ids = new Set();
  for (const [, attributes, id, body] of slides) {
    const label = `${number}/${id}`;
    assert.ok(!ids.has(id), `${label}: duplicate slide ID`);
    ids.add(id);
    const prose = body.replace(/<aside\b[\s\S]*?<\/aside>|<pre\b[\s\S]*?<\/pre>/g, '');
    if (/data-wd-concept=/.test(attributes)) {
      assert.match(attributes, new RegExp(`data-wd-concept="${id}"`), `${label}: concept identity differs`);
      // A single primary definition is a structural guard; meaning still needs review.
      assert.equal((prose.match(/<dt>/g) || []).length, 1,
        `${label}: introduce one primary concept and keep conditions/examples subordinate`);
    }
    for (const [, , key, value] of prose.matchAll(/<(\w+)\b[^>]*data-wd-i18n="([^"]+)"[^>]*>([\s\S]*?)<\/\1>/g)) {
      assert.equal(decode(value), messages.ko[key], `${label}: stale HTML default for ${key}`);
      for (const locale of ['ko', 'en']) {
        const text = messages[locale][key];
        assert.ok(typeof text === 'string' && text.trim(), `${label}: missing ${locale}.${key}`);
        assert.doesNotMatch(text, /다음\s*(?:연결|슬라이드|섹션|장에서는)|이어서 살펴볼|제작 의도|검토 작업|\b(?:up next|connection to the next section)\b/i,
          `${label}: production/transition prose in ${locale}.${key}`);
        if (locale === 'ko') assert.doesNotMatch(text, /(?:한다|된다|이다|있다|없다|않는다|바뀐다|나타난다|해진다)\.$/,
          `${label}: use concise noun phrases in ${key}`);
      }
    }
    for (const [, list] of prose.matchAll(/<dl\b[^>]*class="[^"]*wd-lesson-concepts[^"]*"[^>]*>([\s\S]*?)<\/dl>/g)) {
      const terms = [...list.matchAll(/<dt>([\s\S]*?)<\/dt>/g)];
      assert.ok(terms.length, `${label}: empty concept list`);
      for (const [, term] of terms) {
        assert.match(term, /^<strong\b[^>]*data-wd-i18n="[^"]+"[^>]*>[^<]+<\/strong>$/, `${label}: bold concept-definition required`);
        const key = term.match(/data-wd-i18n="([^"]+)"/)[1];
        for (const locale of ['ko', 'en']) assert.match(messages[locale][key], /\S - \S/,
          `${label}: missing concept - definition in ${locale}.${key}`);
      }
    }
    if (/wd-slide--content/.test(attributes)) {
      assert.doesNotMatch(prose, /class="[^"]*wd-lesson-(?:eyebrow|references|page)\b/, `${label}: repeated chapter/footer chrome`);
    } else {
      assert.doesNotMatch(body, /<pre\b/, `${label}: no teaching code on covers/dividers`);
    }
    if (id === 'cover') {
      const variant = attributes.match(/data-wd-cover="(weekly|topic)"/)?.[1];
      assert.ok(variant, `${label}: choose weekly or topic cover format`);
      assert.equal((body.match(/<h1\b/g) || []).length, 1, `${label}: one cover title required`);
      const field = className => {
        const matches = [...body.matchAll(new RegExp(`<([a-z0-9]+)\\b[^>]*class="${className}"[^>]*>([\\s\\S]*?)<\\/\\1>`, 'g'))];
        assert.equal(matches.length, 1, `${label}: one ${className} required`);
        const key = matches[0][0].match(/data-wd-i18n="([^"]+)"/)?.[1];
        return {key, text: decode(matches[0][2])};
      };
      const title = field('wd-lesson-title');
      field('wd-lesson-cover__subtitle');
      assert.equal(field('wd-lesson-source').text, `LECTURE ${number}`, `${label}: wrong lecture identity`);
      assert.equal((body.match(/LECTURE \d+/g) || []).length, 1, `${label}: repeated lecture label`);
      assert.doesNotMatch(body, /class="wd-(?:slide-lead|lesson-eyebrow)"/, `${label}: use cover-specific text roles`);
      if (variant === 'weekly') {
        const eyebrow = field('wd-lesson-cover__eyebrow');
        const semester = messages.ko[eyebrow.key].match(/^(\d{4})학년도 ([12])학기 실전웹서비스개발$/);
        assert.ok(semester, `${label}: use the official semester and course name`);
        assert.equal(messages.en[eyebrow.key], `Practical Web Service Development · ${semester[2] === '2' ? 'Fall' : 'Spring'} ${semester[1]}`, `${label}: KO/EN semester mismatch`);
        assert.equal(messages.ko[title.key], `실전 웹서비스개발 – ${week}주차`, `${label}: wrong weekly title`);
        assert.equal(messages.en[title.key], `Practical Web Service Development – Week ${week}`, `${label}: wrong English weekly title`);
      } else {
        assert.doesNotMatch(body, /wd-lesson-cover__eyebrow/, `${label}: topic cover omits the course eyebrow`);
      }
    }
  }
  decks++;
}
console.log(`authoring: ${decks} authored deck(s) satisfy the 01–04-derived contract`);
