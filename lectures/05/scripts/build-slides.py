"""Build the Week 5 body deck or its separate titles-first preview."""
import argparse
import html
import hashlib
import json
from pathlib import Path
from lesson import SLIDES
from react_import import copy_runtime_assets

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--titles-only', action='store_true', help='Build titles.html from title_outline.py without changing the body deck')
args = parser.parse_args()
if args.titles_only:
    from title_outline import load_title_slides, write_title_materials
    SLIDES = load_title_slides(SLIDES)
    write_title_materials(ROOT, SLIDES)
html_name = 'titles.html' if args.titles_only else 'index.html'
content_name = 'titles-content.js' if args.titles_only else 'lecture-content.js'
MESSAGES = {'ko': {}, 'en': {}}

def tr(key, value, tag='p', cls=''):
    if isinstance(value, str):
        value = (value, value)
    for i, lang in enumerate(('ko', 'en')):
        MESSAGES[lang][key] = value[i]
    return f'<{tag} class="{cls}" data-wd-i18n="{key}">{html.escape(value[0])}</{tag}>'

def block(b, key):
    kind = b['kind']
    if kind == 'practice':
        result = '<div class="wd-practice-grid"><div class="wd-practice-main">'
        for group in ('goals', 'requirements'):
            result += tr(f'{key}_{group}_label', b[group + '_label'], 'h3')
            result += '<ul>' + ''.join(tr(f'{key}_{group}_{i}', item, 'li') for i, item in enumerate(b[group])) + '</ul>'
        result += '</div><div class="wd-practice-side"><div class="wd-practice-submission">'
        result += '<div class="wd-practice-deadline">' + tr(key + '_deadline_label', b['deadline_label'], 'span') + tr(key + '_deadline', b['deadline'], 'strong') + '</div>'
        result += '<div class="wd-practice-deliverables">' + tr(key + '_deliverables_label', b['deliverables_label'], 'h3')
        result += '<ul>' + ''.join(tr(f'{key}_deliverable_{i}', item, 'li') for i, item in enumerate(b['deliverables'])) + '</ul></div></div>'
        result += '<div class="wd-practice-reference">' + tr(key + '_reference_label', b['reference_label'], 'h3')
        for i, locale in enumerate(('ko', 'en')):
            MESSAGES[locale][key + '_reference_title'] = b['reference_title'][i]
        result += '<a href="' + html.escape(b['reference_url'], quote=True) + '" target="_blank" rel="noopener" data-wd-i18n="' + key + '_reference_title">' + html.escape(b['reference_title'][0]) + '</a>'
        result += tr(key + '_scope', b['scope']) + '</div></div></div>'
        return result
    if kind == 'concepts':
        rows = []
        for i, (title, details) in enumerate(b['items']):
            rows.append('<div><dt>' + tr(f'{key}_{i}_term', title, 'strong') + '</dt><dd><ul>' + ''.join(tr(f'{key}_{i}_{j}', d, 'li') for j, d in enumerate(details)) + '</ul></dd></div>')
        result = ''
        if b.get('result'):
            result = '<div class="wd-lesson-result">' + tr(key + '_result_label', b.get('result_label', ('실행 결과', 'Result')), 'p', 'wd-lesson-code-label') + ''.join(tr(f'{key}_result_{i}', value) for i, value in enumerate(b['result'])) + '</div>'
        return '<dl class="wd-lesson-concepts">' + ''.join(rows) + '</dl>' + result
    if kind == 'code':
        code = b['code'].strip('\n')
        label = '' if b.get('hide_label') else tr(key + '_label', b['label'], 'p', 'wd-lesson-code-label')
        # Identical executable identifiers and sample data in both languages.
        for lang in MESSAGES:
            MESSAGES[lang][key + '_code'] = code
        rendered = label + f'<pre class="wd-code" data-wd-code="{b.get("lang", "jsx")}" data-wd-code-width="{b.get("width", 64)}" data-wd-i18n="{key}_code">{html.escape(code)}</pre>'
        if b.get('caption'):
            rendered += tr(key + '_caption', b['caption'], 'p', 'wd-lesson-code-caption')
        if b.get('result'):
            rendered += '<div class="wd-lesson-result">' + tr(key + '_result_label', b.get('result_label', ('실행 결과', 'Rendered output')), 'p', 'wd-lesson-code-label') + ''.join(tr(f'{key}_result_{i}', value) for i, value in enumerate(b['result'])) + '</div>'
        if b.get('result_figure'):
            rendered += '<div class="wd-lesson-result">' + block(b['result_figure'], key + '_result_figure') + '</div>'
        return rendered
    if kind == 'table':
        head = '<thead><tr>' + ''.join(tr(f'{key}_h{i}', c, 'th') for i, c in enumerate(b['head'])) + '</tr></thead>'
        rows = '<tbody>' + ''.join('<tr>' + ''.join(tr(f'{key}_r{i}_{j}', c, 'th' if j == 0 else 'td') for j, c in enumerate(row)) + '</tr>' for i, row in enumerate(b['rows'])) + '</tbody>'
        return '<table class="wd-lesson-table">' + head + rows + '</table>'
    if kind == 'steps':
        return '<ol class="wd-lesson-steps">' + ''.join('<li>' + tr(f'{key}_{i}_title', title, 'strong') + tr(f'{key}_{i}_body', body) + '</li>' for i, (title, body) in enumerate(b['items'])) + '</ol>'
    if kind == 'image':
        for i, lang in enumerate(('ko', 'en')):
            MESSAGES[lang][key + '_alt'] = b['alt'][i]
        caption = tr(key + '_caption', b['caption'], 'figcaption') if b.get('caption') else ''
        return '<figure class="wd-lesson-figure"><img src="' + b['src'] + '" alt="' + html.escape(b['alt'][0]) + '" data-wd-i18n-alt="' + key + '_alt">' + caption + '</figure>'
    raise ValueError(kind)

sections = []
for i, s in enumerate(SLIDES):
    if 'import_html' in s:
        sections.append(s['import_html'])
        for locale, values in s.get('import_messages', {}).items():
            assert not MESSAGES[locale].keys() & values.keys(), 'Imported translation keys collide'
            MESSAGES[locale].update(values)
        continue
    if s.get('source_image'):
        # Native SVG text replaces only the source page's right-hand code panel.
        overlay = ''
        if s.get('source_code_overlay'):
            code = json.dumps(json.loads(s['source_code_overlay']), indent=2)
            lines = ''.join(f'<tspan x="1004" y="{320 + line * 21}">{html.escape(text)}</tspan>'
                            for line, text in enumerate(code.splitlines()))
            overlay = ('<svg class="wd-source-code-overlay" viewBox="0 0 1600 900" role="img" aria-label="package.json · pwd-week5 · npm latest 2026-10-12">'
                       '<rect x="968" y="239" width="588" height="623" fill="black" />'
                       '<text x="984" y="277" fill="white" font-family="Arial, sans-serif" font-size="28" font-weight="700">package.json</text>'
                       '<text fill="#00ff00" font-family="Consolas, monospace" font-size="16" xml:space="preserve">' + lines + '</text></svg>')
        sections.append(
            f'<section class="wd-slide wd-source-slide" data-wd-slide="{html.escape(s["id"], quote=True)}" role="region" aria-label="React 생태계 · 원본 PDF 18쪽">'
            f'<div class="wd-source-page" role="img" aria-label="React 생태계 원본 슬라이드, 우측 패키지 버전 최신화" style="background-image: url({html.escape(s["source_image"], quote=True)})">{overlay}</div>'
            '<aside hidden class="wd-lesson-notes">' + html.escape('Original PDF page 18; only right-hand package.json updated.\n' + '\n'.join(url for _, url in s['sources'])) + '</aside></section>')
        continue
    key = f'w5_{i + 1:02}'
    ident = 'cover' if i == 0 else s['id']
    cover = s.get('cover') if s['kind'] == 'cover' else None
    cls = 'wd-lesson-cover' if cover else ('wd-lesson-chapter' if s['kind'] == 'chapter' else 'wd-slide--content')
    cover_attribute = f' data-wd-cover="{html.escape(cover["variant"], quote=True)}"' if cover else ''
    concept_attribute = f' data-wd-concept="{html.escape(ident, quote=True)}"' if ident.startswith('concept-') else ''
    parts = [f'<section class="wd-slide wd-lesson-slide {cls}{" is-active" if i == 0 else ""}" data-wd-slide="{ident}"{cover_attribute}{concept_attribute} role="region">']
    if cover:
        parts.append('<div class="wd-lesson-cover__content">')
        if cover.get('eyebrow'):
            parts.append(tr(key + '_eyebrow', cover['eyebrow'], 'p', 'wd-lesson-cover__eyebrow'))
        parts.append(tr(key + '_title', s['title'], 'h1', 'wd-lesson-title'))
        parts.append(tr(key + '_subtitle', s['lead'], 'p', 'wd-lesson-cover__subtitle'))
        parts.append('</div>')
    else:
        if s['kind'] == 'chapter':
            parts.append(tr(key + '_chapter', (s['id'][-2:], s['id'][-2:]), 'p', 'wd-lesson-eyebrow'))
        parts.append(tr(key + '_title', s['title'], 'h2', 'wd-slide-heading'))
        parts.append(tr(key + '_lead', s['lead'], 'p', 'wd-slide-lead'))
    if s.get('blocks'):
        parts.append('<div class="wd-lesson-body wd-lesson-body--' + s.get('layout', 'split') + '">')
        for j, b in enumerate(s['blocks']):
            parts.append('<div class="wd-lesson-block">' + block(b, f'{key}_b{j}') + '</div>')
        parts.append('</div>')
    sources = s.get('sources', [])
    if sources:
        parts.append('<aside hidden class="wd-lesson-notes">' + html.escape(s.get('note', '') + '\n[Sources]\n' + '\n'.join(url for _, url in sources) + '\n[/Sources]') + '</aside>')
    if cover:
        parts.append('<p class="wd-lesson-source">' + html.escape(cover['lecture']) + '</p>')
    parts.append('</section>')
    sections.append('\n'.join(parts))

MESSAGES['ko']['page_title'] = '05 | React Framework의 이해'
MESSAGES['en']['page_title'] = '05 | Understanding the React Framework'
if args.titles_only:
    MESSAGES['ko']['page_title'] += ' · 제목 목록'
    MESSAGES['en']['page_title'] += ' · Title Outline'
ROOT.joinpath(content_name).write_text('window.LECTURE_CONTENT = ' + json.dumps(MESSAGES, ensure_ascii=False, indent=2) + ';\n')
ROOT.joinpath(html_name).write_text('''<!doctype html>
<html class="wd-page" lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title data-wd-i18n="page_title">''' + html.escape(MESSAGES['ko']['page_title']) + '''</title>
  <link rel="stylesheet" href="../../packages/web-deck/web-deck.css">
  <link rel="stylesheet" href="../04/lecture.css">
  <link rel="stylesheet" href="../04/react-cleanup.css">
  <link rel="stylesheet" href="../../packages/web-deck/authoring.css">
  <link rel="stylesheet" href="lecture.css?v=''' + hashlib.sha256(ROOT.joinpath('lecture.css').read_bytes()).hexdigest()[:12] + '''">
</head>
<body class="wd-page-body" data-lecture="05">
<main class="wd-deck" data-web-deck data-wd-authoring="v1"><div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
''' + '\n\n'.join(sections) + '''
</div></div></main>
<script src="''' + content_name + '''"></script>
<script src="../shared/lecture-deck.js"></script>
<script src="../../packages/web-deck/vendor/prism/prism.js" data-manual></script>
<script src="../../packages/web-deck/web-deck.js"></script>
<script src="../04/assets/react-demos.js"></script>
</body></html>
''')
if not args.titles_only:
    ROOT.joinpath('materials/slide-map.json').write_text(json.dumps([{'number': i + 1, 'id': s.get('id', 'cover'), 'title': s['title'][0], 'subtitle': s['lead'][0], 'kind': s['kind'], 'topic_number': s['topic_number'], 'chapter': s['chapter'][0], 'sources': s.get('sources', []), **({'import_source': s['import_source']} if 'import_source' in s else {}), **({'import_override': s['import_override']} if 'import_override' in s else {}), **({'import_text_corrections': s['import_text_corrections']} if 'import_text_corrections' in s else {}), **({'source_slide_ids': s['source_slide_ids'], 'source_pages': s['source_pages']} if 'source_slide_ids' in s else {})} for i, s in enumerate(SLIDES)], ensure_ascii=False, indent=2) + '\n')
copy_runtime_assets(ROOT)
print(f'Built {len(SLIDES)} bilingual slides in {html_name}')
