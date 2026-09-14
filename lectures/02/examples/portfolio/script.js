const intro = document.querySelector('#intro');
const button = document.querySelector('#change');

if (button) {
  button.addEventListener('click', () => {
    intro.textContent = '나의 첫 웹사이트 제작 중';
  });
}

const add = document.querySelector('#add');
if (add) {
  add.addEventListener('click', () => {
    const paragraph = document.createElement('p');
    paragraph.textContent = '새 프로젝트를 준비 중';
    document.querySelector('#updates').appendChild(paragraph);
  });
}
