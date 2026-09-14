const image = document.querySelector('#hero');
document.querySelector('#load').addEventListener('click', () => {
  setTimeout(() => {
    image.src = './banner.svg';
  }, 800);
});
