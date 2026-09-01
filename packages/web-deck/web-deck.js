/*
 * @pwd/web-deck v0.2.1
 * Framework-independent slide runtime for static websites.
 */
(function (global) {
  'use strict';

  var VERSION = '0.2.1';
  var SUPPORTED_LOCALES = ['ko', 'en'];
  var DEFAULT_MESSAGES = {
    ko: {
      ui_home: '전체 강의 보기',
      ui_language: '언어 선택',
      ui_previous: '이전',
      ui_next: '다음',
      ui_fullscreen: '전체화면',
      ui_fullscreen_exit: '전체화면 종료',
      ui_print: '인쇄 또는 PDF로 저장',
      ui_deck_label: '강의 슬라이드',
      ui_slide_role: '슬라이드',
      ui_slide_position: '{{current}} / {{total}} 슬라이드',
      ui_dot: '{{n}}번 슬라이드로 이동',
      ui_appendix: '부록',
      ui_appendix_position: '부록 {{current}} / {{total}}',
      ui_dot_appendix: '부록 {{n}}번 슬라이드로 이동'
    },
    en: {
      ui_home: 'View all lectures',
      ui_language: 'Select language',
      ui_previous: 'Previous',
      ui_next: 'Next',
      ui_fullscreen: 'Fullscreen',
      ui_fullscreen_exit: 'Exit fullscreen',
      ui_print: 'Print or save as PDF',
      ui_deck_label: 'Lecture slides',
      ui_slide_role: 'slide',
      ui_slide_position: 'Slide {{current}} of {{total}}',
      ui_dot: 'Go to slide {{n}}',
      ui_appendix: 'Appendix',
      ui_appendix_position: 'Appendix {{current}} of {{total}}',
      ui_dot_appendix: 'Go to appendix slide {{n}}'
    }
  };

  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function mergeMessages(custom) {
    var result = {};
    SUPPORTED_LOCALES.forEach(function (locale) {
      result[locale] = Object.assign({}, DEFAULT_MESSAGES[locale], custom && custom[locale]);
    });
    return result;
  }

  function format(message, variables) {
    var value = message === undefined || message === null ? '' : String(message);
    Object.keys(variables || {}).forEach(function (name) {
      value = value.split('{{' + name + '}}').join(String(variables[name]));
    });
    return value;
  }

  function readStorage(key) {
    try {
      return global.localStorage.getItem(key);
    } catch (error) {
      return null;
    }
  }

  function writeStorage(key, value) {
    try {
      global.localStorage.setItem(key, value);
    } catch (error) {
      // The deck remains usable when storage is unavailable.
    }
  }

  function resolveLocale(config, locales) {
    var params = new URLSearchParams(global.location.search);
    var query = params.get('lang');
    if (locales.indexOf(query) !== -1) return query;

    var saved = readStorage(config.storageKey);
    if (locales.indexOf(saved) !== -1) return saved;

    var browserLocale = (global.navigator.language || '').toLowerCase();
    if (browserLocale.indexOf('ko') === 0 && locales.indexOf('ko') !== -1) return 'ko';
    if (browserLocale.indexOf('en') === 0 && locales.indexOf('en') !== -1) return 'en';
    return locales.indexOf(config.defaultLocale) !== -1 ? config.defaultLocale : locales[0];
  }

  function buildChrome(root, config, locales) {
    var rail = make('div', 'wd-rail');
    rail.setAttribute('aria-hidden', 'true');
    var railFill = make('span', 'wd-rail__fill');
    rail.appendChild(railFill);

    var top = make('header', 'wd-bar wd-bar--top');
    var brand = config.homeHref ? make('a', 'wd-brand', config.brand) : make('span', 'wd-brand', config.brand);
    if (config.homeHref) brand.setAttribute('href', config.homeHref);
    top.appendChild(brand);

    var tools = make('div', 'wd-tools');
    var languageGroup = make('div', 'wd-languages');
    languageGroup.setAttribute('role', 'group');
    var languageButtons = locales.map(function (locale) {
      var button = make('button', 'wd-language', (config.localeLabels && config.localeLabels[locale]) || locale.toUpperCase());
      button.type = 'button';
      button.setAttribute('data-locale', locale);
      languageGroup.appendChild(button);
      return button;
    });
    tools.appendChild(languageGroup);

    var printButton = make('button', 'wd-tool wd-tool--print');
    printButton.type = 'button';
    printButton.appendChild(make('span', 'wd-tool__text', 'PDF'));
    tools.appendChild(printButton);

    var fullscreenButton = make('button', 'wd-tool wd-tool--fullscreen');
    fullscreenButton.type = 'button';
    fullscreenButton.setAttribute('aria-pressed', 'false');
    fullscreenButton.appendChild(make('span', 'wd-tool__icon wd-tool__icon--enter', '⛶'));
    fullscreenButton.appendChild(make('span', 'wd-tool__icon wd-tool__icon--exit', '×'));
    tools.appendChild(fullscreenButton);
    top.appendChild(tools);

    var bottom = make('footer', 'wd-bar wd-bar--bottom');
    var previousButton = make('button', 'wd-nav wd-nav--previous');
    previousButton.type = 'button';
    previousButton.appendChild(make('span', 'wd-nav__arrow', '←'));
    var previousLabel = make('span', 'wd-nav__label');
    previousButton.appendChild(previousLabel);

    var center = make('div', 'wd-center');
    var dots = make('div', 'wd-dots');
    var counter = make('p', 'wd-counter');
    var current = make('b', '', '01');
    var separator = make('span', '', ' / ');
    separator.setAttribute('aria-hidden', 'true');
    var total = make('span', '', '01');
    counter.appendChild(current);
    counter.appendChild(separator);
    counter.appendChild(total);
    center.appendChild(dots);
    center.appendChild(counter);

    var nextButton = make('button', 'wd-nav wd-nav--next');
    nextButton.type = 'button';
    var nextLabel = make('span', 'wd-nav__label');
    nextButton.appendChild(nextLabel);
    nextButton.appendChild(make('span', 'wd-nav__arrow', '→'));

    bottom.appendChild(previousButton);
    bottom.appendChild(center);
    bottom.appendChild(nextButton);

    var announcer = make('p', 'wd-sr');
    announcer.setAttribute('aria-live', 'polite');

    root.insertBefore(rail, root.firstChild);
    root.insertBefore(top, root.querySelector('[data-wd-viewport]'));
    root.appendChild(bottom);
    root.appendChild(announcer);

    return {
      rail: rail,
      railFill: railFill,
      bottom: bottom,
      brand: brand,
      languageGroup: languageGroup,
      languageButtons: languageButtons,
      printButton: printButton,
      fullscreenButton: fullscreenButton,
      previousButton: previousButton,
      previousLabel: previousLabel,
      nextButton: nextButton,
      nextLabel: nextLabel,
      dots: dots,
      current: current,
      separator: separator,
      total: total,
      announcer: announcer
    };
  }

  function create(rootOrSelector, options) {
    if (typeof document === 'undefined') throw new Error('WebDeck requires a browser document.');
    var root = typeof rootOrSelector === 'string' ? document.querySelector(rootOrSelector) : rootOrSelector;
    if (!root) throw new Error('WebDeck root element was not found.');
    if (root.__webDeck) return root.__webDeck;

    var config = Object.assign({
      brand: 'WEB DECK',
      brandKey: '',
      homeHref: '',
      defaultLocale: 'ko',
      storageKey: 'pwd.webDeck.language',
      idleMs: 2600,
      historyMode: 'replace',
      fullscreen: true,
      print: true,
      messages: {}
    }, options || {});

    var requestedLocales = Array.isArray(config.locales) ? config.locales : SUPPORTED_LOCALES;
    var locales = requestedLocales.filter(function (locale) {
      return SUPPORTED_LOCALES.indexOf(locale) !== -1;
    });
    if (!locales.length) locales = SUPPORTED_LOCALES.slice();

    var messages = mergeMessages(config.messages);
    var viewport = root.querySelector('[data-wd-viewport]');
    var stage = root.querySelector('[data-wd-stage]');
    if (!viewport || !stage) throw new Error('WebDeck requires [data-wd-viewport] and [data-wd-stage].');

    var params = new URLSearchParams(global.location.search);
    var previewAll = params.get('preview') === 'all';
    var slides = [];
    Array.prototype.forEach.call(stage.querySelectorAll('[data-wd-slide]'), function (element) {
      var enabled = element.getAttribute('data-wd-enabled') !== 'false' || previewAll;
      element.hidden = !enabled;
      if (enabled) slides.push({
        element: element,
        id: element.getAttribute('data-wd-slide') || String(slides.length + 1),
        appendix: element.hasAttribute('data-wd-appendix')
      });
    });
    if (!slides.length) throw new Error('WebDeck requires at least one enabled slide.');

    var mainTotal = 0;
    var appendixTotal = 0;
    slides.forEach(function (slide) {
      slide.number = slide.appendix ? ++appendixTotal : ++mainTotal;
      if (slide.appendix) slide.element.classList.add('wd-slide--appendix');
    });

    document.documentElement.classList.add('wd-page');
    root.classList.add('wd-deck');
    var chrome = buildChrome(root, config, locales);
    var singleSlide = slides.length === 1;
    root.classList.toggle('is-single-slide', singleSlide);
    document.documentElement.classList.toggle('wd-single-slide', singleSlide);
    chrome.rail.hidden = singleSlide;
    chrome.bottom.hidden = singleSlide;
    chrome.printButton.hidden = !config.print;
    chrome.fullscreenButton.hidden = !config.fullscreen;

    var dots = slides.map(function (slide, slideIndex) {
      var dot = make('button', 'wd-dot');
      dot.type = 'button';
      if (slide.appendix) dot.classList.add('wd-dot--appendix');
      dot.addEventListener('click', function () { goTo(slideIndex); });
      chrome.dots.appendChild(dot);
      return dot;
    });

    var locale = resolveLocale(config, locales);
    var index = 0;
    var fauxFullscreen = false;
    var idleTimer = null;
    var touchStartX = 0;
    var touchStartY = 0;
    var trackingTouch = false;

    function translate(key, variables) {
      var dictionary = messages[locale] || {};
      var fallback = messages[config.defaultLocale] || messages.ko || {};
      var value = dictionary[key];
      if (value === undefined) value = fallback[key];
      return format(value, variables);
    }

    function slidePosition(slide) {
      return translate(slide.appendix ? 'ui_appendix_position' : 'ui_slide_position', {
        current: slide.number,
        total: slide.appendix ? appendixTotal : mainTotal
      });
    }

    function applyAttribute(selector, attribute) {
      Array.prototype.forEach.call(root.querySelectorAll(selector), function (node) {
        node.setAttribute(attribute, translate(node.getAttribute(selector.slice(1, -1))));
      });
    }

    function applyLocale() {
      document.documentElement.lang = locale;
      Array.prototype.forEach.call(root.querySelectorAll('[data-wd-i18n]'), function (node) {
        node.textContent = translate(node.getAttribute('data-wd-i18n'));
      });
      Array.prototype.forEach.call(document.querySelectorAll('title[data-wd-i18n]'), function (node) {
        node.textContent = translate(node.getAttribute('data-wd-i18n'));
      });
      applyAttribute('[data-wd-i18n-alt]', 'alt');
      applyAttribute('[data-wd-i18n-aria-label]', 'aria-label');
      applyAttribute('[data-wd-i18n-title]', 'title');

      chrome.languageGroup.setAttribute('aria-label', translate('ui_language'));
      if (config.brandKey) chrome.brand.textContent = translate(config.brandKey);
      chrome.brand.setAttribute('aria-label', translate('ui_home'));
      chrome.previousLabel.textContent = translate('ui_previous');
      chrome.printButton.setAttribute('aria-label', translate('ui_print'));
      chrome.printButton.setAttribute('title', translate('ui_print'));
      root.setAttribute('aria-label', translate(config.deckLabelKey || 'ui_deck_label'));

      chrome.languageButtons.forEach(function (button) {
        var active = button.getAttribute('data-locale') === locale;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });

      slides.forEach(function (slide) {
        slide.element.setAttribute('aria-roledescription', translate('ui_slide_role'));
        slide.element.setAttribute('aria-label', slidePosition(slide));
      });
      dots.forEach(function (dot, dotIndex) {
        var slide = slides[dotIndex];
        dot.setAttribute('aria-label', translate(slide.appendix ? 'ui_dot_appendix' : 'ui_dot', { n: slide.number }));
      });
      updateNavigationLabel();
      updateFullscreenLabel();
    }

    function updateLanguageUrl(nextLocale) {
      var url = new URL(global.location.href);
      if (!url.searchParams.has('lang')) return;
      url.searchParams.set('lang', nextLocale);
      global.history.replaceState(null, '', url.pathname + url.search + url.hash);
    }

    function setLocale(nextLocale) {
      if (locales.indexOf(nextLocale) === -1 || nextLocale === locale) return;
      locale = nextLocale;
      writeStorage(config.storageKey, locale);
      updateLanguageUrl(locale);
      applyLocale();
      announce();
      root.dispatchEvent(new CustomEvent('webdeck:localechange', { detail: { locale: locale } }));
    }

    function pad(number) {
      return number < 10 ? '0' + number : String(number);
    }

    function updateNavigationLabel() {
      var nextSlide = slides[index + 1];
      var movingToAppendix = nextSlide && nextSlide.appendix && !slides[index].appendix;
      chrome.nextLabel.textContent = translate(movingToAppendix ? 'ui_appendix' : 'ui_next');
    }

    function updateHash() {
      var hash = '#/' + (index + 1);
      if (global.location.hash === hash || (index === 0 && !global.location.hash)) return;
      var url = global.location.pathname + global.location.search + hash;
      if (config.historyMode === 'push') {
        global.history.pushState(null, '', url);
      } else {
        global.history.replaceState(null, '', url);
      }
    }

    function announce() {
      var slide = slides[index];
      var heading = slide.element.querySelector('h1, h2, [data-wd-heading]');
      chrome.announcer.textContent = slidePosition(slide) + (heading ? ' — ' + heading.textContent : '');
    }

    function goTo(target, options) {
      var nextIndex = typeof target === 'string'
        ? slides.findIndex(function (slide) { return slide.id === target; })
        : Number(target);
      if (!Number.isFinite(nextIndex) || nextIndex < 0) nextIndex = 0;
      index = Math.max(0, Math.min(nextIndex, slides.length - 1));

      slides.forEach(function (slide, slideIndex) {
        var active = slideIndex === index;
        slide.element.classList.toggle('is-active', active);
        slide.element.setAttribute('aria-hidden', String(!active));
        if (active) {
          slide.element.removeAttribute('inert');
        } else {
          slide.element.setAttribute('inert', '');
          slide.element.scrollTop = 0;
        }
      });
      dots.forEach(function (dot, dotIndex) {
        var active = dotIndex === index;
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-current', active ? 'true' : 'false');
      });

      var slide = slides[index];
      chrome.previousButton.disabled = index === 0;
      chrome.nextButton.disabled = index === slides.length - 1;
      chrome.current.textContent = slide.appendix
        ? (appendixTotal > 1 ? slidePosition(slide) : translate('ui_appendix'))
        : pad(slide.number);
      chrome.separator.hidden = slide.appendix;
      chrome.total.hidden = slide.appendix;
      chrome.total.textContent = pad(mainTotal);
      chrome.railFill.style.width = (slide.appendix ? 100 : slide.number / Math.max(mainTotal, 1) * 100) + '%';
      updateNavigationLabel();

      var opts = options || {};
      if (!opts.silent) announce();
      if (!opts.skipHash) updateHash();
      root.dispatchEvent(new CustomEvent('webdeck:change', {
        detail: { index: index, id: slide.id, slide: slide.element }
      }));
    }

    function indexFromHash() {
      var match = /^#\/(\d+)$/.exec(global.location.hash || '');
      if (!match) return 0;
      return Math.max(0, Math.min(parseInt(match[1], 10) - 1, slides.length - 1));
    }

    function nativeFullscreenElement() {
      return document.fullscreenElement || document.webkitFullscreenElement || null;
    }

    function isFullscreen() {
      return nativeFullscreenElement() === root || fauxFullscreen;
    }

    function updateFullscreenLabel() {
      var label = translate(isFullscreen() ? 'ui_fullscreen_exit' : 'ui_fullscreen');
      chrome.fullscreenButton.setAttribute('aria-label', label);
      chrome.fullscreenButton.setAttribute('title', label);
      chrome.fullscreenButton.setAttribute('aria-pressed', String(isFullscreen()));
    }

    function wakeControls() {
      if (idleTimer) global.clearTimeout(idleTimer);
      idleTimer = null;
      root.classList.remove('is-idle');
      if (!isFullscreen()) return;
      idleTimer = global.setTimeout(function () {
        root.classList.add('is-idle');
        idleTimer = null;
      }, config.idleMs);
    }

    function syncFullscreen() {
      root.classList.toggle('is-fullscreen', isFullscreen());
      document.documentElement.classList.toggle('wd-is-fullscreen', isFullscreen());
      updateFullscreenLabel();
      wakeControls();
    }

    function enterFauxFullscreen() {
      fauxFullscreen = true;
      syncFullscreen();
    }

    function toggleFullscreen() {
      if (!config.fullscreen) return;
      if (isFullscreen()) {
        if (nativeFullscreenElement() === root) {
          var exit = document.exitFullscreen || document.webkitExitFullscreen;
          if (exit) exit.call(document);
        }
        if (fauxFullscreen) {
          fauxFullscreen = false;
          syncFullscreen();
        }
        return;
      }

      var request = root.requestFullscreen || root.webkitRequestFullscreen;
      if (!request) {
        enterFauxFullscreen();
        return;
      }
      try {
        var pending = request.call(root);
        if (pending && typeof pending.catch === 'function') pending.catch(enterFauxFullscreen);
      } catch (error) {
        enterFauxFullscreen();
      }
    }

    function onFullscreenChange() {
      if (nativeFullscreenElement() === root) fauxFullscreen = false;
      syncFullscreen();
    }

    chrome.previousButton.addEventListener('click', function () { goTo(index - 1); });
    chrome.nextButton.addEventListener('click', function () { goTo(index + 1); });
    chrome.printButton.addEventListener('click', function () { global.print(); });
    chrome.fullscreenButton.addEventListener('click', function () {
      toggleFullscreen();
      chrome.fullscreenButton.blur();
    });
    chrome.languageButtons.forEach(function (button) {
      button.addEventListener('click', function () { setLocale(button.getAttribute('data-locale')); });
    });

    document.addEventListener('fullscreenchange', onFullscreenChange);
    document.addEventListener('webkitfullscreenchange', onFullscreenChange);
    ['pointermove', 'pointerdown', 'keydown', 'touchstart', 'wheel'].forEach(function (eventName) {
      document.addEventListener(eventName, function () {
        if (isFullscreen()) wakeControls();
      }, { passive: true });
    });

    document.addEventListener('keydown', function (event) {
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      var target = event.target;
      if (target && (target.matches('input, textarea, select') || target.isContentEditable)) return;
      var onButton = document.activeElement && document.activeElement.tagName === 'BUTTON';
      if (onButton && (event.key === ' ' || event.key === 'Enter')) return;

      switch (event.key) {
        case 'ArrowRight':
        case 'PageDown':
        case ' ':
          event.preventDefault();
          goTo(index + 1);
          break;
        case 'ArrowLeft':
        case 'PageUp':
          event.preventDefault();
          goTo(index - 1);
          break;
        case 'Home':
          event.preventDefault();
          goTo(0);
          break;
        case 'End':
          event.preventDefault();
          goTo(slides.length - 1);
          break;
        case 'f':
        case 'F':
          event.preventDefault();
          toggleFullscreen();
          break;
        case 'Escape':
          if (fauxFullscreen) {
            event.preventDefault();
            fauxFullscreen = false;
            syncFullscreen();
          }
          break;
      }
    });

    viewport.addEventListener('touchstart', function (event) {
      if (event.touches.length !== 1) {
        trackingTouch = false;
        return;
      }
      trackingTouch = true;
      touchStartX = event.touches[0].clientX;
      touchStartY = event.touches[0].clientY;
    }, { passive: true });
    viewport.addEventListener('touchend', function (event) {
      if (!trackingTouch) return;
      trackingTouch = false;
      var touch = event.changedTouches[0];
      var distanceX = touch.clientX - touchStartX;
      var distanceY = touch.clientY - touchStartY;
      if (Math.abs(distanceX) < 60 || Math.abs(distanceX) <= Math.abs(distanceY)) return;
      goTo(distanceX < 0 ? index + 1 : index - 1);
    }, { passive: true });
    viewport.addEventListener('touchcancel', function () { trackingTouch = false; }, { passive: true });

    global.addEventListener('hashchange', function () {
      var nextIndex = indexFromHash();
      if (nextIndex !== index) goTo(nextIndex, { skipHash: true });
    });

    var instance = {
      version: VERSION,
      root: root,
      next: function () { goTo(index + 1); },
      previous: function () { goTo(index - 1); },
      goTo: goTo,
      getIndex: function () { return index; },
      getLocale: function () { return locale; },
      setLocale: setLocale,
      toggleFullscreen: toggleFullscreen,
      print: function () { global.print(); }
    };
    root.__webDeck = instance;

    applyLocale();
    goTo(indexFromHash(), { silent: true });
    root.classList.add('is-ready');
    return instance;
  }

  function autoInitialize() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-web-deck]'), function (root) {
      if (root.__webDeck) return;
      try {
        create(root, global.WEB_DECK_CONFIG || {});
      } catch (error) {
        console.error('[WebDeck]', error);
      }
    });
  }

  var api = { version: VERSION, create: create, supportedLocales: SUPPORTED_LOCALES.slice() };
  global.WebDeck = api;
  if (typeof module === 'object' && module.exports) module.exports = api;

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', autoInitialize, { once: true });
    } else {
      autoInitialize();
    }
  }
})(typeof window !== 'undefined' ? window : globalThis);
