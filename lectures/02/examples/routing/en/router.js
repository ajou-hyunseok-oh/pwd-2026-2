const pages = {
  home: ['Home', 'Navigate to the About and Projects pages'],
  about: ['About', 'Learning web development.'],
  projects: ['Projects', 'Timetable · Memo']
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
