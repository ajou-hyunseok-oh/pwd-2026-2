export function renderPage(locale = 'ko') {
  const en = locale === 'en';
  const title = en ? 'About Me' : '자기소개';
  const intro = en ? 'Learning web development.' : '웹 개발 학습 중';
  const paragraph = `<p id="intro">${intro}</p>`;
  return `<!doctype html>
<html lang="${locale}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${title}</title>
  <link rel="stylesheet" href="./style.css" />
</head>
<body>
  <main><section class="profile">
    <h1>${title}</h1>
    ${paragraph}
  </section></main>
</body>
</html>`;
}
