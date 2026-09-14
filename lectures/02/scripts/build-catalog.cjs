const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../examples');
const escape = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const css = `body{max-width:1050px;margin:40px auto;padding:0 24px;color:#263a2c;font:16px/1.7 Arial,sans-serif}h1{line-height:1.3}a{color:#1f6b4a}table{width:100%;border-collapse:collapse}td,th{padding:16px;text-align:left;border-bottom:1px solid #d5dfd7}code,pre{font-family:Consolas,monospace}pre{padding:20px;background:#f0f3ef;overflow:auto;font-size:15px;line-height:1.6}select{padding:8px;max-width:100%;font-size:16px}.note{padding:16px;background:#f0f3ef}.links{display:flex;gap:16px;flex-wrap:wrap}@media(max-width:600px){td,th{padding:8px}body{margin:24px auto;padding:0 12px}}`;
const doc=(lang,title,body,script='')=>`<!doctype html><html lang="${lang}"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>${title}</title><style>${css}</style></head><body>${body}${script}</body></html>`;
const entries=[
  ['portfolio/index.html','세 페이지 개인 사이트','Three-page portfolio','portfolio/about.html'],
  ['rendering/index.html','렌더링 실험','Rendering experiments','rendering/rendering.js'],
  ['rendering/cascade.html','스타일 규칙과 계산 결과','CSS rules and computed styles','rendering/cascade.css'],
  ['rendering/image-unreserved.html','이미지 공간 미지정','Unreserved image space','rendering/image-unreserved.html'],
  ['rendering/image-reserved.html','이미지 공간 예약','Reserved image space','rendering/image-reserved.html'],
  ['generation/csr.html','CSR','CSR','generation/csr.js'],
  ['generation/ssr.html','SSR · 로컬 서버 필요','SSR · local server required','generation/page.mjs'],
  ['generation/ssg.html','SSG','SSG','generation/build.mjs'],
  ['routing/index.html','SPA 페이지 이동','SPA navigation','routing/router.js'],
  ['components/dist/index.html','React 카드 두 개','Two React cards','components/src/ProjectCard.jsx']
];
const rows=entries.map(([file,ko,en,src])=>`<tr><td>${ko}<br>${en}</td><td><a href="./${file}">KO / 실행</a> · <a href="./${file.startsWith('components/')?file:file.replace('/', '/en/')}">EN</a></td><td><a href="./source.html?file=${src}">Source</a></td></tr>`).join('');
fs.writeFileSync(path.join(root,'index.html'),doc('ko','Week 2 · 실행 예제',`<h1>02회차 · 실행 예제<br>Week 2 · Runnable Examples</h1><p>슬라이드에 사용한 코드와 실행 화면 / Source code and results used in the slides</p><p class="links"><a href="./README.md">실행 안내 / Run Guide</a><a href="../materials/week2-examples.zip" download>ZIP 다운로드 / Download</a><a href="./source.html">전체 소스 / All Sources</a></p><p class="note">SSR은 <code>npm run dev</code> 실행 후 <a href="http://localhost:4183">localhost:4183</a>에서 확인합니다.<br>SSR requires the local server started with <code>npm run dev</code>.</p><table><thead><tr><th>예제 / Example</th><th>실행 / Run</th><th>코드 / Code</th></tr></thead><tbody>${rows}</tbody></table>`));
for(const lang of ['ko','en']){
  const sub=lang==='en'?'en/':'';
  const body=lang==='ko'?'<h1>SSR 예제 실행</h1><p>요청마다 HTML을 생성하는 Node 서버가 필요합니다.</p>':'<h1>Run the SSR Example</h1><p>This example needs the Node server that generates HTML for each request.</p>';
  fs.writeFileSync(path.join(root,'generation',sub,'ssr.html'),doc(lang,'SSR · Local Server',body+'<pre>cd lectures/02/examples\nnpm run dev</pre><p><a href="http://localhost:4183/generation/'+sub+'ssr.html">Open SSR on localhost:4183</a></p>'));
}
const files={};
function collect(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){if(['node_modules','dist'].includes(entry.name))continue;const absolute=path.join(dir,entry.name);if(entry.isDirectory()){collect(absolute);continue;}const relative=path.relative(root,absolute).replace(/\\/g,'/');if(!/\.(html|css|js|mjs|jsx|json)$/.test(relative)||['source.html','source-data.js','catalog.js','package-lock.json','components/package-lock.json'].includes(relative))continue;files[relative]=fs.readFileSync(absolute,'utf8');}}
fs.writeFileSync(path.join(root,'source.html'),doc('ko','Week 2 · Source Code','<h1>예제 소스 / Example Source</h1><p><a href="./index.html">예제 목록 / Catalog</a></p><label for="file">파일 / File </label><select id="file"></select><pre><code id="source"></code></pre>','<script src="./source-data.js"></script><script src="./catalog.js"></script>'));
fs.writeFileSync(path.join(root,'catalog.js'),`const select = document.querySelector('#file');
const output = document.querySelector('#source');
for (const file of Object.keys(window.EXAMPLE_SOURCES).sort()) {
  const option = document.createElement('option');
  option.value = file;
  option.textContent = file;
  select.appendChild(option);
}
const requested = new URLSearchParams(location.search).get('file');
if (requested && requested in window.EXAMPLE_SOURCES) select.value = requested;
function show() { output.textContent = window.EXAMPLE_SOURCES[select.value]; }
select.addEventListener('change', () => {
  history.replaceState({}, '', '?file=' + encodeURIComponent(select.value));
  show();
});
show();
`);
require('node:child_process').execFileSync(process.execPath,[path.join(__dirname,'format-examples.cjs')]);
collect(root);
fs.writeFileSync(path.join(root,'source-data.js'),'window.EXAMPLE_SOURCES = '+JSON.stringify(files,null,2)+';\n');
console.log('Built formatted example catalog, static SSR instructions and source viewer.');
