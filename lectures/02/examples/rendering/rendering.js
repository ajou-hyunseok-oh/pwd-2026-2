const profile = document.querySelector('.profile');
const intro = document.querySelector('#intro');

document.querySelector('#width').addEventListener('click', () => {
  performance.mark('change-width');
  profile.style.width = '220px';
});

document.querySelector('#color').addEventListener('click', () => {
  performance.mark('change-background');
  profile.style.backgroundColor = '#dceaf5';
});

document.querySelector('#change').addEventListener('click', () => {
  intro.textContent = '웹 개발 학습 중';
});

document.querySelector('#hide').addEventListener('click', () => {
  intro.style.display = 'none';
});

document.querySelector('#reset').addEventListener('click', () => {
  location.reload();
});
