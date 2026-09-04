const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const packageRoot = path.resolve(__dirname, '..');
const repositoryRoot = path.resolve(packageRoot, '..', '..');
const WebDeck = require(path.join(packageRoot, 'web-deck.js'));
const politeKoreanEnding = /(?:니다|세요|십시오)(?:[.!?…]|$)/u;

assert.match('웹 주소를 확인합니다.', politeKoreanEnding);
assert.doesNotMatch('웹 주소 확인', politeKoreanEnding);

assert.equal(WebDeck.version, '0.2.1');
assert.equal(typeof WebDeck.create, 'function');
assert.deepEqual(WebDeck.supportedLocales, ['ko', 'en']);

const template = fs.readFileSync(path.join(packageRoot, 'template', 'index.html'), 'utf8');
const runtime = fs.readFileSync(path.join(packageRoot, 'web-deck.js'), 'utf8');
const styles = fs.readFileSync(path.join(packageRoot, 'web-deck.css'), 'utf8');
assert.match(template, /data-web-deck/);
assert.match(template, /data-wd-viewport/);
assert.match(template, /data-wd-stage/);
assert.match(template, /data-wd-slide="cover"/);
assert.match(template, /ko:\s*{/);
assert.match(template, /en:\s*{/);
assert.match(runtime, /is-single-slide/);
assert.match(runtime, /config\.brandKey/);
assert.match(styles, /fonts\/noto-sans-kr\.css/);
assert.match(styles, /\.wd-slide--content/);
assert.match(styles, /\.wd-code/);
assert.match(styles, /\.wd-table/);
assert.ok(fs.existsSync(path.join(packageRoot, 'fonts', 'OFL-1.1.txt')));
assert.ok(fs.existsSync(path.join(packageRoot, 'fonts', 'files', 'noto-sans-kr-latin-wght-normal.woff2')));

const lectureBootstrap = fs.readFileSync(path.join(repositoryRoot, 'lectures', 'shared', 'lecture-deck.js'), 'utf8');
assert.equal((lectureBootstrap.match(/^\s*'\d{2}':/gm) || []).length, 13);
assert.match(lectureBootstrap, /brandKey:\s*'course_title'/);
assert.match(lectureBootstrap, /course_title:\s*'실전 웹 서비스 개발 · 2026년 2학기'/);
assert.match(lectureBootstrap, /course_title:\s*'Practical Web Service Development · Fall 2026'/);

for (let week = 1; week <= 13; week += 1) {
  const number = String(week).padStart(2, '0');
  const lecturePath = path.join(repositoryRoot, 'lectures', number, 'index.html');
  const html = fs.readFileSync(lecturePath, 'utf8');
  const sandbox = {
    document: { body: { getAttribute: () => number } },
    window: {}
  };
  const lectureContentPath = path.join(repositoryRoot, 'lectures', number, 'lecture-content.js');
  if (fs.existsSync(lectureContentPath)) {
    const lectureContent = fs.readFileSync(lectureContentPath, 'utf8');
    vm.runInNewContext(lectureContent, sandbox);
    for (const [key, value] of Object.entries(sandbox.window.LECTURE_CONTENT.ko)) {
      if (typeof value !== 'string') continue;
      assert.doesNotMatch(
        value,
        politeKoreanEnding,
        `Lecture ${number} ko.${key} uses a polite sentence ending; use the deck's concise declarative or noun-ending style`
      );
    }
  }
  vm.runInNewContext(lectureBootstrap, sandbox);
  const messages = sandbox.window.WEB_DECK_CONFIG.messages;
  const contentKeys = [
    ...html.matchAll(/data-wd-i18n(?:-alt|-aria-label|-title)?="([^"]+)"/g)
  ].map((match) => match[1]);
  const localAssets = [...html.matchAll(/(?:src|href)="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((reference) => !/^(?:[a-z]+:|#)/i.test(reference));

  assert.match(html, /data-web-deck/, `Lecture ${number} is missing the deck root`);
  assert.match(html, /data-wd-slide="cover"/, `Lecture ${number} is missing its cover slide`);
  const expectedSlideCount = week === 1 ? 28 : 1;
  assert.equal((html.match(/data-wd-slide=/g) || []).length, expectedSlideCount, `Lecture ${number} has the wrong slide count`);
  assert.match(html, /packages\/web-deck\/web-deck\.css/, `Lecture ${number} is missing package CSS`);
  assert.match(html, /packages\/web-deck\/web-deck\.js/, `Lecture ${number} is missing package JS`);
  assert.match(html, /\.\.\/shared\/lecture-deck\.js/, `Lecture ${number} is missing shared lecture config`);
  assert.match(html, new RegExp(`data-lecture="${number}"`), `Lecture ${number} has the wrong lecture number`);
  assert.ok(contentKeys.length > 0, `Lecture ${number} has no translated content`);
  for (const reference of localAssets) {
    const assetPath = path.resolve(path.dirname(lecturePath), reference.split(/[?#]/, 1)[0]);
    assert.ok(fs.existsSync(assetPath), `Lecture ${number} has a missing asset: ${reference}`);
  }
  for (const locale of ['ko', 'en']) {
    for (const key of contentKeys) {
      assert.ok(key in messages[locale], `Lecture ${number} is missing ${locale}.${key}`);
      assert.notEqual(messages[locale][key], '', `Lecture ${number} has an empty ${locale}.${key}`);
    }
  }
}

console.log('web-deck: package and 13 lecture decks are valid');
