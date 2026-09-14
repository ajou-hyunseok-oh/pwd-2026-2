const pages = {
  home: ['홈', '홈에서 소개와 프로젝트 페이지로 이동'],
  about: ['소개', '웹 개발 학습 중'],
  projects: ['프로젝트', 'Timetable · Memo']
};

function render() {
  const key = new URLSearchParams(location.search).get('page') || 'home';
  const [title, text] = pages[key] || pages.home;
  document.querySelector('#page-title').textContent = title;
  document.querySelector('#page').textContent = text;
}

document.querySelectorAll('nav a').forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    history.pushState({}, '', link.href);
    render();
  });
});

window.addEventListener('popstate', render);
render();
