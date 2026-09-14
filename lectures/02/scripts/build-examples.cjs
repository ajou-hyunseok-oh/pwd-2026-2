const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../examples');
const write = (name, value) => {
  const file = path.join(root, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, value.trim() + '\n');
};
const style = `* { box-sizing: border-box; }
body { margin: 0; color: #333; font: 16px/1.6 Arial, sans-serif; background: #fff; }
header, main, footer { max-width: 760px; margin: auto; padding: 24px; }
header { border-bottom: 1px solid #d5dfd7; }
header strong { color: #1f6b4a; letter-spacing: .08em; font-size: 13px; }
nav { display: flex; gap: 24px; margin-top: 12px; }
a { color: #1f6b4a; text-underline-offset: 4px; }
h1 { margin: 0 0 16px; font-size: 28px; line-height: 1.3; }
h2 { margin: 0 0 8px; font-size: 21px; }
p { margin: 0 0 16px; }
section, article { margin-bottom: 20px; }
.profile { width: 360px; max-width: 100%; padding: 24px; background: #f0f3ef; border-radius: 8px; }
.profile p { margin-bottom: 16px; }
button { padding: 10px 16px; border: 0; border-radius: 4px; background: #1f6b4a; color: white; font: inherit; cursor: pointer; }
button:focus-visible, a:focus-visible { outline: 3px solid #9a351f; outline-offset: 3px; }
button:hover { background: #174f37; }
button:disabled { opacity: .6; cursor: default; }
.cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.cards article { padding: 20px; border: 1px solid #d5dfd7; border-radius: 8px; }
footer { color: #596a60; border-top: 1px solid #d5dfd7; font-size: 13px; }
.tools { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0; }
.tools button { font-size: 13px; }
.note { color: #596a60; font-size: 14px; }
.measure { width: 360px; max-width: 100%; }
.measure img { display: block; width: 100%; height: auto; }
.measure p { padding: 16px; background: #f0f3ef; }
.tree { font-family: monospace; white-space: pre; }
@media (max-width: 480px) { .cards { grid-template-columns: 1fr; } header, main, footer { padding: 20px; } }
`;
const words = {
  ko: {title:'자기소개',before:'웹 개발 학습 중',after:'나의 첫 웹사이트 제작 중',change:'소개 바꾸기',home:'홈',about:'소개',projects:'프로젝트',welcome:'나의 포트폴리오',desc:'HTML · CSS · JavaScript로 만든 개인 사이트',add:'문단 추가',added:'새 프로젝트를 준비 중',interest:'관심 분야',interests:'웹 개발과 디자인',hero:'프로젝트 이미지',featured:'대표 프로젝트',projectDesc:'직접 만든 웹 프로젝트',foot:'2026 · 웹서비스개발',reset:'초기화',result:'실행 결과',lab:'렌더링 실험',width:'너비 변경',color:'배경색 변경',text:'소개 문구 변경',hidden:'문단 숨김',layout:'이미지 공간 예약',later:'이미지 뒤의 설명 문단',run:'이미지 불러오기',homeBody:'홈에서 소개와 프로젝트 페이지로 이동',aboutBody:'웹 개발 학습 중',projectBody:'Timetable · Memo',nodeMessage:'프로젝트 2개',view:'실행 예제',code:'소스 코드'},
  en: {title:'About Me',before:'Learning web development.',after:'Building my first website.',change:'Change Introduction',home:'Home',about:'About',projects:'Projects',welcome:'My Portfolio',desc:'A personal site built with HTML, CSS and JavaScript',add:'Add Paragraph',added:'Preparing a new project.',interest:'Interests',interests:'Web development and design',hero:'Project illustration',featured:'Featured Projects',projectDesc:'A web project I built',foot:'2026 · Web Service Development',reset:'Reset',result:'Result',lab:'Rendering Experiments',width:'Change Width',color:'Change Background',text:'Change Introduction',hidden:'Hide Paragraph',layout:'Reserved Image Space',later:'The paragraph after the image',run:'Load Image',homeBody:'Navigate to the About and Projects pages',aboutBody:'Learning web development.',projectBody:'Timetable · Memo',nodeMessage:'2 projects',view:'Live Example',code:'Source Code'}
};
function document(lang, title, body, script = '', css = './style.css') {
  return `<!doctype html>\n<html lang="${lang}">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n  <title>${title}</title>\n  <meta name="description" content="${words[lang].desc}" />\n  <link rel="stylesheet" href="${css}" />\n${script ? `  <script src="${script}" defer></script>\n` : ''}</head>\n<body>\n${body}\n</body>\n</html>`;
}
function nav(w) {
  return `<nav aria-label="${w.projects}">\n  <a href="./index.html">${w.home}</a>\n  <a href="./about.html">${w.about}</a>\n  <a href="./projects.html">${w.projects}</a>\n</nav>`;
}
for (const [lang,w] of Object.entries(words)) {
  const sub = lang === 'en' ? 'en/' : '';
  const chrome = body => `<header>\n<strong>MY PORTFOLIO</strong>\n${nav(w)}\n</header>\n<main>\n${body}\n</main>\n<footer>${w.foot}</footer>`;
  const profile = `<section class="profile">\n  <h1>${w.title}</h1>\n  <p id="intro" aria-live="polite">${w.before}</p>\n  <button id="change" type="button">${w.change}</button>\n</section>`;
  write(`portfolio/${sub}style.css`,style);
  write(`portfolio/${sub}index.html`,document(lang,w.welcome,chrome(`<h1>${w.welcome}</h1>\n<p>${w.desc}</p>\n<section><h2>${w.projects}</h2><p>Timetable · Memo</p>\n<a href="./projects.html?sort=date#featured">${w.featured}</a></section>`)));
  write(`portfolio/${sub}about.html`,document(lang,w.title,chrome(profile+`\n<section id="interests"><h2>${w.interest}</h2><p>${w.interests}</p></section>`),'./script.js'));
  write(`portfolio/${sub}projects.html`,document(lang,w.projects,chrome(`<h1>${w.projects}</h1>\n<section id="featured"><h2>${w.featured}</h2>\n<div class="cards"><article><h3>Timetable</h3><p>${w.projectDesc}</p></article><article><h3>Memo</h3><p>${w.projectDesc}</p></article></div>\n</section>\n<section id="updates"><button id="add" type="button">${w.add}</button></section>`),'./script.js'));
  write(`portfolio/${sub}script.js`,`const intro = document.querySelector('#intro');\nconst button = document.querySelector('#change');\n\nif (button) {\n  button.addEventListener('click', () => {\n    intro.textContent = '${w.after}';\n  });\n}\n\nconst add = document.querySelector('#add');\nif (add) {\n  add.addEventListener('click', () => {\n    const paragraph = document.createElement('p');\n    paragraph.textContent = '${w.added}';\n    document.querySelector('#updates').appendChild(paragraph);\n  });\n}`);
  write(`portfolio/${sub}demo.js`,`const projects = ['Timetable', 'Memo'];\nconsole.log(projects.length);`);
  write(`rendering/${sub}style.css`,style);
  write(`rendering/${sub}index.html`,document(lang,w.lab,`<main>\n<h1>${w.lab}</h1>\n${profile.replace(w.before,w.after)}\n<div class="tools"><button id="width" type="button">${w.width}</button><button id="color" type="button">${w.color}</button><button id="hide" type="button">${w.hidden}</button><button id="reset" type="button">${w.reset}</button></div>\n<p class="note">width: 360px → 220px · background-color: #f0f3ef → #dceaf5</p>\n</main>`,'./rendering.js'));
  write(`rendering/${sub}rendering.js`,`const profile = document.querySelector('.profile');\nconst intro = document.querySelector('#intro');\n\ndocument.querySelector('#width').addEventListener('click', () => {\n  performance.mark('change-width');\n  profile.style.width = '220px';\n});\n\ndocument.querySelector('#color').addEventListener('click', () => {\n  performance.mark('change-background');\n  profile.style.backgroundColor = '#dceaf5';\n});\n\ndocument.querySelector('#change').addEventListener('click', () => {\n  intro.textContent = '${w.before}';\n});\n\ndocument.querySelector('#hide').addEventListener('click', () => {\n  intro.style.display = 'none';\n});\n\ndocument.querySelector('#reset').addEventListener('click', () => {\n  location.reload();\n});`);
  write(`rendering/${sub}cascade.css`,`body { color: #333; }\n#intro { color: #9a351f; }`);
  write(`rendering/${sub}cascade.html`,document(lang,'CSS · '+w.title,`<main>${profile}</main>`).replace('</head>','  <link rel="stylesheet" href="./cascade.css" />\n</head>'));
  for (const reserved of [false,true]) {
    write(`rendering/${sub}image-${reserved?'reserved':'unreserved'}.html`,document(lang,w.layout,`<main><h1>${w.layout}</h1>\n<div class="measure">\n  <img id="hero" ${reserved?'width="360" height="180" ':''}alt="${w.hero}" />\n  <p>${w.later}</p>\n</div>\n<button id="load" type="button">${w.run}</button>\n<p class="note">${reserved?'width="360" height="180"':'width / height: —'}</p>\n</main>`,'./image.js'));
  }
  write(`rendering/${sub}image.js`,`const image = document.querySelector('#hero');\ndocument.querySelector('#load').addEventListener('click', () => {\n  setTimeout(() => {\n    image.src = './banner.svg';\n  }, 800);\n});`);
  write(`rendering/${sub}banner.svg`,`<svg xmlns="http://www.w3.org/2000/svg" width="360" height="180" viewBox="0 0 360 180"><rect width="360" height="180" fill="#dce6de"/><rect x="32" y="28" width="132" height="124" rx="8" fill="#fff"/><rect x="50" y="48" width="96" height="12" rx="3" fill="#1f6b4a"/><path d="M50 78h96M50 94h72M50 110h88" stroke="#81958a" stroke-width="6"/><circle cx="246" cy="90" r="46" fill="#1f6b4a"/><path d="m224 90 15 16 30-33" fill="none" stroke="white" stroke-width="8"/></svg>`);
  write(`routing/${sub}style.css`,style);
  const spaNav = `<nav>\n  <a href="?page=home">${w.home}</a>\n  <a href="?page=about">${w.about}</a>\n  <a href="?page=projects">${w.projects}</a>\n</nav>`;
  write(`routing/${sub}index.html`,document(lang,'SPA · '+w.welcome,`<header><strong>MY PORTFOLIO · SPA</strong>\n${spaNav}</header>\n<main><h1 id="page-title"></h1><section class="profile"><p id="page"></p></section></main>\n<footer>${w.foot}</footer>`,'./router.js'));
  write(`routing/${sub}router.js`,`const pages = {\n  home: ['${w.home}', '${w.homeBody}'],\n  about: ['${w.about}', '${w.aboutBody}'],\n  projects: ['${w.projects}', '${w.projectBody}']\n};\n\nfunction render() {\n  const key = new URLSearchParams(location.search).get('page') || 'home';\n  const [title, text] = pages[key] || pages.home;\n  document.querySelector('#page-title').textContent = title;\n  document.querySelector('#page').textContent = text;\n}\n\ndocument.querySelectorAll('nav a').forEach((link) => {\n  link.addEventListener('click', (event) => {\n    event.preventDefault();\n    history.pushState({}, '', link.href);\n    render();\n  });\n});\n\nwindow.addEventListener('popstate', render);\nrender();`);
  write(`generation/${sub}style.css`,style);
  write(`generation/${sub}csr.html`,document(lang,'CSR · '+w.title,`<main><section class="profile">\n  <h1>${w.title}</h1>\n  <p id="intro"></p>\n</section></main>`,'./csr.js'));
  write(`generation/${sub}csr.js`,`const intro = document.querySelector('#intro');\nintro.textContent = '${w.before}';`);
}
write('generation/page.mjs',"export function renderPage(locale = 'ko') {\n  const en = locale === 'en';\n  const title = en ? 'About Me' : '자기소개';\n  const intro = en ? 'Learning web development.' : '웹 개발 학습 중';\n  const paragraph = `<p id=\"intro\">${intro}</p>`;\n  return `<!doctype html>\n<html lang=\"${locale}\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n  <title>${title}</title>\n  <link rel=\"stylesheet\" href=\"./style.css\" />\n</head>\n<body>\n  <main><section class=\"profile\">\n    <h1>${title}</h1>\n    ${paragraph}\n  </section></main>\n</body>\n</html>`;\n}\n");
write('generation/build.mjs',`import { writeFile } from 'node:fs/promises';\nimport { renderPage } from './page.mjs';\n\nawait writeFile(new URL('./ssg.html', import.meta.url), renderPage('ko'));\nawait writeFile(new URL('./en/ssg.html', import.meta.url), renderPage('en'));\nconsole.log('Generated: generation/ssg.html, generation/en/ssg.html');`);
write('server.mjs',`import http from 'node:http';\nimport { readFile, stat } from 'node:fs/promises';\nimport path from 'node:path';\nimport { fileURLToPath } from 'node:url';\nimport { renderPage } from './generation/page.mjs';\n\nconst root = path.dirname(fileURLToPath(import.meta.url));\nconst port = Number(process.env.PORT || 4183);\nconst types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.md': 'text/plain; charset=utf-8' };\nconst server = http.createServer(async (request, response) => {\n  try {\n    const url = new URL(request.url, 'http://localhost');\n    if (url.pathname === '/favicon.ico') { response.writeHead(204).end(); return; }\n    if (url.pathname === '/materials/week2-examples.zip') {\n      response.setHeader('Content-Type', 'application/zip');\n      response.end(await readFile(path.join(root, '../materials/week2-examples.zip')));\n      return;\n    }\n    if (url.pathname === '/generation/ssr.html' || url.pathname === '/generation/en/ssr.html') {\n      response.setHeader('Content-Type', 'text/html; charset=utf-8');\n      response.end(renderPage(url.pathname.includes('/en/') ? 'en' : 'ko'));\n      return;\n    }\n    const file = path.resolve(root, '.' + decodeURIComponent(url.pathname));\n    const relative = path.relative(root, file);\n    if (relative.startsWith('..') || path.isAbsolute(relative) || relative.split(path.sep).includes('node_modules')) {\n      response.writeHead(403).end('Forbidden');\n      return;\n    }\n    const target = (await stat(file)).isDirectory() ? path.join(file, 'index.html') : file;\n    response.setHeader('Content-Type', types[path.extname(target)] || 'text/plain; charset=utf-8');\n    response.setHeader('Cache-Control', 'no-store');\n    response.end(await readFile(target));\n  } catch {\n    response.writeHead(404).end('Not found');\n  }\n});\nserver.listen(port, '127.0.0.1', () => console.log('Examples: http://localhost:' + port));`);
write('package.json',JSON.stringify({name:'pwd-week2-examples',private:true,type:'module',scripts:{dev:'node server.mjs',build:'node generation/build.mjs',demo:'node portfolio/demo.js',static:'serve . --listen 4174'},devDependencies:{serve:'14.2.6'}},null,2));
write('components/package.json',JSON.stringify({name:'pwd-project-cards',private:true,type:'module',scripts:{dev:'vite --host 127.0.0.1 --port 4175',build:'vite build'},dependencies:{react:'19.3.0','react-dom':'19.3.0'},devDependencies:{vite:'8.3.0'}},null,2));
write('components/index.html',`<!doctype html>\n<html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Project Cards</title></head><body><div id="root"></div><script type="module" src="./src/main.jsx"></script></body></html>`);
write('components/vite.config.js',`import { defineConfig } from 'vite';\nexport default defineConfig({ base: './' });`);
write('components/src/main.jsx',`import React from 'react';\nimport { createRoot } from 'react-dom/client';\nimport App from './App.jsx';\nimport './style.css';\n\ncreateRoot(document.querySelector('#root')).render(<App />);`);
write('components/src/ProjectCard.jsx',`import React from 'react';\n\nexport default function ProjectCard({ title }) {\n  return (\n    <article className="card">\n      <h2>{title}</h2>\n    </article>\n  );\n}`);
write('components/src/App.jsx',`import React from 'react';\nimport ProjectCard from './ProjectCard.jsx';\n\nexport default function App() {\n  return (\n    <main>\n      <h1>Projects</h1>\n      <ProjectCard title="Timetable" />\n      <ProjectCard title="Memo" />\n    </main>\n  );\n}`);
write('components/src/style.css',`body { margin: 0; color: #333; font: 16px/1.6 Arial, sans-serif; }\nmain { max-width: 640px; margin: 40px auto; padding: 24px; }\nh1 { font-size: 28px; }\n.card { padding: 24px; margin: 16px 0; border-left: 4px solid #1f6b4a; border-radius: 8px; background: #f0f3ef; }\n.card h2 { margin: 0; font-size: 22px; }`);
console.log('Created bilingual portfolio, rendering, generation, routing and component examples.');
