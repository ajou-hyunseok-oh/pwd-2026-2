import { writeFile } from 'node:fs/promises';
import { renderPage } from './page.mjs';

await writeFile(new URL('./ssg.html', import.meta.url), renderPage('ko'));
await writeFile(new URL('./en/ssg.html', import.meta.url), renderPage('en'));
console.log('Generated: generation/ssg.html, generation/en/ssg.html');
