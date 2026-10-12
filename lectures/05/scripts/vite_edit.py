"""Screen 25: replace the entire starter App.tsx with Hello, World!."""
from html import escape
from pathlib import Path


def apply_vite_edit(slide, messages):
    def tr(key, ko, en, tag='p', cls=''):
        key = 'w5_edit_' + key
        messages['ko'][key], messages['en'][key] = ko, en
        return f'<{tag} class="{cls}" data-wd-i18n="{key}">{escape(ko)}</{tag}>'
    title = ('Hello, World! 출력', 'Displaying Hello, World!')
    lead = ('App.tsx로 정의하는 첫 React 화면', 'Your first React screen defined in App.tsx')
    code = (Path(__file__).resolve().parents[1] / 'materials/vite-hello-App.tsx').read_text().strip()
    messages['ko']['w5_edit_code'] = messages['en']['w5_edit_code'] = code
    parts = ['<section class="wd-slide wd-lesson-slide wd-slide--content" data-wd-slide="slide-24" data-wd-import="04/react" data-wd-source-slide="slide-24" data-wd-import-override="vite-template-edit" role="region">', tr('title', *title, 'h2', 'wd-slide-heading'), tr('lead', *lead, 'p', 'wd-slide-lead'), '<div class="wd-lesson-body wd-lesson-body--vite-edit"><div class="wd-lesson-block">', tr('label', 'src/App.tsx · 파일 전체를 아래 코드로 교체', 'src/App.tsx · Replace the entire file with this code', 'p', 'wd-lesson-code-label'), f'<pre class="wd-code" data-wd-code="tsx" data-wd-code-width="64" data-wd-i18n="w5_edit_code">{escape(code)}</pre>', '</div><div class="wd-lesson-block">', '<figure class="wd-lesson-figure"><img src="materials/images/vite-hello-world.png" alt="Hello, World!만 표시된 브라우저 화면" data-wd-i18n-alt="w5_edit_alt">', '</figure></div></div>', '<aside hidden class="wd-lesson-notes">2026-10-12 사용자 요청으로 05 화면 25 전체 재작성. create-vite 9.2.1 React/TypeScript/ESLint 프로젝트의 src/App.tsx 전체를 materials/vite-hello-App.tsx로 교체. App.css import를 포함한 기존 App.tsx 내용 제거. main.tsx 및 index.css는 기본값 유지. 실제 개발 서버 화면 캡처. 04 원본 보존.\n[Sources]\nhttps://vite.dev/guide/\n[/Sources]</aside></section>']
    messages['ko']['w5_edit_alt'] = 'Hello, World!만 표시된 브라우저 화면'
    messages['en']['w5_edit_alt'] = 'Browser displaying only Hello, World!'
    slide.update(import_html=''.join(parts), title=title, lead=lead, import_override='vite-template-edit')
