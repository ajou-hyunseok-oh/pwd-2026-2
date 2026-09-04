import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';

const repoRoot = process.cwd();
const outputRoot = path.join(repoRoot, '.pages-site');
const manifestPath = path.join(repoRoot, 'released-lectures.txt');

if (path.dirname(outputRoot) !== repoRoot || path.basename(outputRoot) !== '.pages-site') {
  throw new Error(`Unsafe output directory: ${outputRoot}`);
}

const manifest = await readFile(manifestPath, 'utf8');
const releasedLectures = manifest
  .split(/\r?\n/)
  .map((line) => line.trim())
  .filter((line) => line && !line.startsWith('#'));

if (releasedLectures.length === 0) {
  throw new Error('released-lectures.txt must contain at least one lecture number.');
}

const releasedSet = new Set(releasedLectures);
if (releasedSet.size !== releasedLectures.length) {
  throw new Error('released-lectures.txt contains duplicate lecture numbers.');
}

for (const lecture of releasedLectures) {
  if (!/^(0[1-9]|1[0-3])$/.test(lecture)) {
    throw new Error(`Invalid lecture number: ${lecture}`);
  }
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(path.join(outputRoot, 'lectures'), { recursive: true });
await mkdir(path.join(outputRoot, 'packages', 'web-deck'), { recursive: true });

await cp(path.join(repoRoot, 'assets'), path.join(outputRoot, 'assets'), { recursive: true });
await cp(path.join(repoRoot, 'lectures', 'shared'), path.join(outputRoot, 'lectures', 'shared'), { recursive: true });
await cp(path.join(repoRoot, 'packages', 'web-deck', 'fonts'), path.join(outputRoot, 'packages', 'web-deck', 'fonts'), { recursive: true });
await cp(path.join(repoRoot, 'packages', 'web-deck', 'web-deck.css'), path.join(outputRoot, 'packages', 'web-deck', 'web-deck.css'));
await cp(path.join(repoRoot, 'packages', 'web-deck', 'web-deck.js'), path.join(outputRoot, 'packages', 'web-deck', 'web-deck.js'));

for (const lecture of releasedLectures) {
  await cp(
    path.join(repoRoot, 'lectures', lecture),
    path.join(outputRoot, 'lectures', lecture),
    { recursive: true }
  );
}

const sourceIndex = await readFile(path.join(repoRoot, 'index.html'), 'utf8');
let cardCount = 0;
const publishedIndex = sourceIndex.replace(
  /<li data-lecture="(\d{2})">(?:<a\b[^>]*>|<div class="lecture-grid__item is-disabled" aria-disabled="true">)([\s\S]*?)(?:<\/a>|<\/div>)<\/li>/g,
  (_, lecture, content) => {
    cardCount += 1;
    if (releasedSet.has(lecture)) {
      return `<li data-lecture="${lecture}"><a href="lectures/${lecture}/index.html">${content}</a></li>`;
    }
    return `<li data-lecture="${lecture}"><div class="lecture-grid__item is-disabled" aria-disabled="true">${content}</div></li>`;
  }
);

if (cardCount !== 13) {
  throw new Error(`Expected 13 lecture cards in index.html, found ${cardCount}.`);
}

await writeFile(path.join(outputRoot, 'index.html'), publishedIndex, 'utf8');
console.log(`Built GitHub Pages site with lectures: ${releasedLectures.join(', ')}`);
