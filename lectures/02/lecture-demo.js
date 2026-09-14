(function () {
  'use strict';

  var demo = document.querySelector('[data-week2-demo]');
  if (!demo) return;

  var intro = demo.querySelector('[aria-live]');
  var button = demo.querySelector('[data-week2-demo-toggle]');

  button.addEventListener('click', function () {
    var changed = intro.getAttribute('data-wd-i18n') === 's47_preview_before';
    var introKey = changed ? 's47_preview_after' : 's47_preview_before';
    var buttonKey = changed ? 's47_preview_reset' : 's47_preview_button';
    var locale = document.documentElement.lang;
    var messages = window.LECTURE_CONTENT[locale] || window.LECTURE_CONTENT.ko;

    intro.setAttribute('data-wd-i18n', introKey);
    intro.textContent = messages[introKey];
    button.setAttribute('data-wd-i18n', buttonKey);
    button.textContent = messages[buttonKey];
  });

  var root = document.querySelector('[data-web-deck]');
  function updateLesson() {
    var locale = document.documentElement.lang === 'en' ? 'en' : 'ko';
    document.querySelectorAll('[data-lesson-image]').forEach(function (img) {
      img.src = './materials/figures/' + locale + '-' + img.dataset.lessonImage + '.png';
    });
    document.querySelectorAll('[data-lesson-src-ko]').forEach(function (img) {
      img.src = img.getAttribute('data-lesson-src-' + locale);
    });
    document.querySelectorAll('[data-lesson-href-ko]').forEach(function (link) {
      link.href = link.getAttribute('data-lesson-href-' + locale);
    });
    document.querySelectorAll('[data-lesson-marks]').forEach(function (pre) {
      var container = pre.parentElement;
      var previous = container.querySelector('.lesson-code__markers');
      if (previous) previous.remove();
      var markers = document.createElement('div');
      markers.className = 'lesson-code__markers';
      markers.setAttribute('aria-hidden', 'true');
      var style = getComputedStyle(pre);
      var used = {};
      JSON.parse(pre.dataset.lessonMarks).forEach(function (mark) {
        var offset = pre.textContent.indexOf(mark[1]);
        if (offset < 0) return;
        var line = pre.textContent.slice(0, offset).split('\n').length - 1;
        var badge = document.createElement('b');
        badge.className = 'lesson-tag lesson-tag--' + mark[0];
        badge.textContent = mark[0];
        badge.style.top = (parseFloat(style.paddingTop) + line * parseFloat(style.lineHeight)) + 'px';
        if (used[line]) badge.style.left = (used[line] * 0.9) + 'rem';
        used[line] = (used[line] || 0) + 1;
        markers.appendChild(badge);
      });
      var count = Math.max(1, Math.max.apply(null, Object.values(used)));
      pre.style.paddingLeft = (1.65 + Math.max(0, count - 1) * 0.9) + 'rem';
      container.appendChild(markers);
    });
  }
  root.addEventListener('webdeck:localechange', function () { requestAnimationFrame(updateLesson); });
  window.addEventListener('resize', updateLesson);
  window.addEventListener('beforeprint', updateLesson);
  window.addEventListener('DOMContentLoaded', updateLesson);
})();
