const select = document.querySelector('#file');
const output = document.querySelector('#source');
for (const file of Object.keys(window.EXAMPLE_SOURCES).sort()) {
  const option = document.createElement('option');
  option.value = file;
  option.textContent = file;
  select.appendChild(option);
}
const requested = new URLSearchParams(location.search).get('file');
if (requested && requested in window.EXAMPLE_SOURCES) select.value = requested;
function show() {
  output.textContent = window.EXAMPLE_SOURCES[select.value];
}
select.addEventListener('change', () => {
  history.replaceState({}, '', '?file=' + encodeURIComponent(select.value));
  show();
});
show();
