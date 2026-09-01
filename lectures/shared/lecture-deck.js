(function () {
  'use strict';

  var lectures = {
    '01': { ko: '2026 웹서비스 개발 개요', en: 'Web Service Development in 2026', dateKo: '2026. 09. 07. 월요일', dateEn: 'Monday, September 7, 2026' },
    '02': { ko: 'HTML / CSS / JS / Web 기본', en: 'HTML, CSS, JavaScript & Web Fundamentals', dateKo: '2026. 09. 14. 월요일', dateEn: 'Monday, September 14, 2026' },
    '03': { ko: 'JavaScript → TypeScript', en: 'JavaScript → TypeScript', dateKo: '2026. 09. 21. 월요일', dateEn: 'Monday, September 21, 2026' },
    '04': { ko: 'React + Vite', en: 'React + Vite', dateKo: '2026. 09. 28. 월요일', dateEn: 'Monday, September 28, 2026' },
    '05': { ko: 'UI/UX + Responsive', en: 'UI/UX & Responsive Design', dateKo: '2026. 10. 12. 월요일', dateEn: 'Monday, October 12, 2026' },
    '06': { ko: 'Backend + REST API', en: 'Backend & REST APIs', dateKo: '2026. 10. 19. 월요일', dateEn: 'Monday, October 19, 2026' },
    '07': { ko: 'Database + Authentication', en: 'Database & Authentication', dateKo: '2026. 11. 02. 월요일', dateEn: 'Monday, November 2, 2026' },
    '08': { ko: 'Full Stack Integration', en: 'Full Stack Integration', dateKo: '2026. 11. 09. 월요일', dateEn: 'Monday, November 9, 2026' },
    '09': { ko: 'Deployment', en: 'Deployment', dateKo: '2026. 11. 16. 월요일', dateEn: 'Monday, November 16, 2026' },
    '10': { ko: 'AI Web Service', en: 'AI Web Service', dateKo: '2026. 11. 23. 월요일', dateEn: 'Monday, November 23, 2026' },
    '11': { ko: 'AI Coding Agent', en: 'AI Coding Agent', dateKo: '2026. 11. 30. 월요일', dateEn: 'Monday, November 30, 2026' },
    '12': { ko: 'Test / Security / Quality', en: 'Testing, Security & Quality', dateKo: '2026. 12. 07. 월요일', dateEn: 'Monday, December 7, 2026' },
    '13': { ko: '운영 / Final Review', en: 'Operations & Final Review', dateKo: '2026. 12. 14. 월요일', dateEn: 'Monday, December 14, 2026' }
  };

  var number = document.body.getAttribute('data-lecture');
  var lecture = lectures[number];
  var content = window.LECTURE_CONTENT || {};
  if (!lecture) throw new Error('Unknown lecture number: ' + number);

  window.LECTURE_CATALOG = lectures;
  window.WEB_DECK_CONFIG = {
    brand: '실전 웹 서비스 개발 · 2026년 2학기',
    brandKey: 'course_title',
    homeHref: '../../',
    locales: ['ko', 'en'],
    defaultLocale: 'ko',
    storageKey: 'pwd.webDeck.language',
    messages: {
      ko: Object.assign({
        page_title: number + ' | ' + lecture.ko,
        ui_deck_label: number + '회차 ' + lecture.ko + ' 강의 슬라이드',
        lecture_title: lecture.ko,
        course_title: '실전 웹 서비스 개발 · 2026년 2학기',
        course: '실전 웹 서비스 개발 · 2026년 2학기',
        status: '강의 자료 준비 중',
        status_detail: '자료 수집이 완료되면 이 골격에 슬라이드를 추가합니다.',
        lecture_date: lecture.dateKo
      }, content.ko),
      en: Object.assign({
        page_title: 'Lecture ' + number + ' | ' + lecture.en,
        ui_deck_label: 'Lecture ' + number + ': ' + lecture.en,
        lecture_title: lecture.en,
        course_title: 'Practical Web Service Development · Fall 2026',
        course: 'Practical Web Service Development · Fall 2026',
        status: 'Lecture materials in preparation',
        status_detail: 'Slides will be added to this deck as the materials are collected.',
        lecture_date: lecture.dateEn
      }, content.en)
    }
  };
})();
