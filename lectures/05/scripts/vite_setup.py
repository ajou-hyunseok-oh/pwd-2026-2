"""User-requested Week 5 replacement for imported React setup slide only."""
from html import escape
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / 'materials/vite-create-console.txt'


def apply_vite_setup(slide, messages):
    def text(key, ko, en, tag='p', cls=''):
        key = 'w5_vite_' + key
        for locale, value in [('ko', ko), ('en', en)]:
            messages[locale][key] = value
        return f'<{tag} class="{cls}" data-wd-i18n="{key}">{escape(ko)}</{tag}>'

    title = ('React 프로젝트 생성과 실행', 'Creating and Running a React Project')
    lead = ('Vite 대화형 메뉴의 선택 항목과 프로젝트 구성', 'Interactive Vite choices and the resulting project setup')
    rows = [
        ('Project name → pwd-week5-demo', '프로젝트 폴더 이름 - 생성할 소스와 설정 파일을 담는 디렉터리', 'Project directory name — contains the generated source and configuration files'),
        ('Select a framework → React', 'UI 라이브러리 선택 - React 개발에 필요한 기본 소스와 의존 패키지 구성', 'UI library — prepares the starter source and dependencies for React'),
        ('Select a variant → TypeScript', '소스 언어 선택 - 타입을 검사하는 TypeScript 기반 템플릿', 'Source language — a TypeScript template with type checking'),
        ('Which linter to use? → ESLint', '코드 검사 도구 선택 - 코드 규칙 위반과 잠재 오류를 찾는 ESLint 설정', 'Code checker — configures ESLint to detect rule violations and potential errors'),
        ('Install with npm and start now? → No', '자동 설치·실행 생략 - 생성 후 패키지 설치와 개발 서버 실행을 직접 수행', 'Skip automatic installation and startup — install packages and start the dev server manually'),
    ]
    markup = ['<section class="wd-slide wd-lesson-slide wd-slide--content" data-wd-slide="slide-23" data-wd-import="04/react" data-wd-source-slide="slide-23" data-wd-import-override="vite-interactive" role="region">',
              text('title', *title, 'h2', 'wd-slide-heading'), text('lead', *lead, 'p', 'wd-slide-lead'),
              '<div class="wd-lesson-body wd-lesson-body--vite-setup"><div class="wd-lesson-block">',
              text('log_label', '터미널 · 실제 선택 로그', 'Terminal · Recorded selections', 'p', 'wd-lesson-code-label')]
    # The visible excerpt preserves actual CLI wording and selected values.
    excerpt = LOG.read_text().split('[Selected console output]\n', 1)[1].split('\n[Generated project]', 1)[0].strip()
    for locale in messages:
        messages[locale]['w5_vite_log'] = excerpt
    markup.append('<pre class="wd-code" data-wd-code="text" data-wd-code-width="64" data-wd-i18n="w5_vite_log">' + escape(excerpt) + '</pre>')
    markup.append(text('manual', 'No 선택 후: cd로 폴더 이동 → npm install로 패키지 설치 → npm run dev로 개발 서버 실행. 접속 주소는 터미널의 Local 출력 확인.', 'After No: cd enters the directory → npm install installs dependencies → npm run dev starts the dev server. Open the Local URL printed in the terminal.', 'p', 'vite-setup-caption'))
    markup.append('</div><div class="wd-lesson-block"><dl class="wd-lesson-concepts">')
    for i, (choice, ko, en) in enumerate(rows):
        markup.append('<div><dt>' + text(f'choice_{i}', choice.replace(' → ', ' - '), choice.replace(' → ', ' - '), 'strong') + '</dt><dd><ul>' + text(f'meaning_{i}', ko, en, 'li') + '</ul></dd></div>')
    markup.append('</dl></div></div><aside hidden class="wd-lesson-notes">2026-10-12 실제 PTY 실행. create-vite 9.2.1, Node.js v26.11.0, npm 11.20.0. 전체 메뉴와 선택 로그: materials/vite-create-console.txt. 사용자 요청으로 05 화면 24만 재작성; 04 원본 보존. TypeScript + React Compiler 및 라우터 변형 대신 기본 TypeScript 선택. ESLint는 Oxlint 대신 선택한 코드 검사 도구. npm 설치 확인은 이번 실행에서 나타나지 않음.\n[Sources]\nhttps://vite.dev/guide/\n[/Sources]</aside></section>')
    slide.update(import_html='\n'.join(markup), title=title, lead=lead, import_override='vite-interactive')
