const intro = document.querySelector('#intro');
const button = document.querySelector('#change');

if (button) {
  button.addEventListener('click', () => {
    intro.textContent = 'Building my first website.';
  });
}

const add = document.querySelector('#add');
if (add) {
  add.addEventListener('click', () => {
    const paragraph = document.createElement('p');
    paragraph.textContent = 'Preparing a new project.';
    document.querySelector('#updates').appendChild(paragraph);
  });
}
