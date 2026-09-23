"""Build the bilingual Week 5 HTML deck. Content source: lesson.py."""
import html
import json
from pathlib import Path
from lesson import SLIDES

ROOT = Path(__file__).resolve().parents[1]
MESSAGES = {'ko': {}, 'en': {}}

def tr(key, value, tag='p', cls=''):
    if isinstance(value, str):
        value = (value, value)
    for i, lang in enumerate(('ko', 'en')):
        MESSAGES[lang][key] = value[i]
    return f'<{tag} class="{cls}" data-wd-i18n="{key}">{html.escape(value[0])}</{tag}>'

def block(b, key):
    kind = b['kind']
    if kind == 'concepts':
        rows = []
        for i, (title, details) in enumerate(b['items']):
            rows.append('<div>' + tr(f'{key}_{i}_term', title, 'dt') + '<dd><ul>' + ''.join(tr(f'{key}_{i}_{j}', d, 'li') for j, d in enumerate(details)) + '</ul></dd></div>')
        return '<dl class="w5-concepts">' + ''.join(rows) + '</dl>'
    if kind == 'code':
        code = b['code'].strip('\n')
        label = tr(key + '_label', b['label'], 'p', 'w5-code-label')
        # Identical executable identifiers and sample data in both languages.
        for lang in MESSAGES:
            MESSAGES[lang][key + '_code'] = code
        return label + f'<pre class="wd-code" data-wd-code="{b.get("lang", "jsx")}" data-wd-code-width="{b.get("width", 64)}" data-wd-i18n="{key}_code">{html.escape(code)}</pre>'
    if kind == 'table':
        head = '<thead><tr>' + ''.join(tr(f'{key}_h{i}', c, 'th') for i, c in enumerate(b['head'])) + '</tr></thead>'
        rows = '<tbody>' + ''.join('<tr>' + ''.join(tr(f'{key}_r{i}_{j}', c, 'th' if j == 0 else 'td') for j, c in enumerate(row)) + '</tr>' for i, row in enumerate(b['rows'])) + '</tbody>'
        return '<table class="w5-table">' + head + rows + '</table>'
    if kind == 'steps':
        return '<ol class="w5-steps">' + ''.join('<li>' + tr(f'{key}_{i}_title', title, 'strong') + tr(f'{key}_{i}_body', body) + '</li>' for i, (title, body) in enumerate(b['items'])) + '</ol>'
    if kind == 'image':
        for i, lang in enumerate(('ko', 'en')):
            MESSAGES[lang][key + '_alt'] = b['alt'][i]
        return '<figure class="w5-figure"><img src="' + b['src'] + '" alt="' + html.escape(b['alt'][0]) + '" data-wd-i18n-alt="' + key + '_alt">' + tr(key + '_caption', b['caption'], 'figcaption') + '</figure>'
    raise ValueError(kind)

sections = []
for i, s in enumerate(SLIDES):
    key = f'w5_{i + 1:02}'
    ident = 'cover' if i == 0 else s['id']
    cls = 'w5-cover' if i == 0 else 'wd-slide--content'
    parts = [f'<section class="wd-slide w5-slide {cls}{" is-active" if i == 0 else ""}" data-wd-slide="{ident}" role="region">']
    parts.append(tr(key + '_chapter', s['chapter'], 'p', 'w5-eyebrow'))
    parts.append(tr(key + '_title', s['title'], 'h1' if i == 0 else 'h2', 'w5-title' if i == 0 else 'wd-slide-heading'))
    parts.append(tr(key + '_lead', s['lead'], 'p', 'wd-slide-lead'))
    if s.get('blocks'):
        parts.append('<div class="w5-body w5-body--' + s.get('layout', 'split') + '">')
        for j, b in enumerate(s['blocks']):
            parts.append('<div class="w5-block">' + block(b, f'{key}_b{j}') + '</div>')
        parts.append('</div>')
    sources = s.get('sources', [])
    if sources:
        parts.append('<div class="w5-references">' + ' · '.join(f'<a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>' for label, url in sources) + '</div>')
        parts.append('<aside hidden class="w5-notes">' + html.escape(s.get('note', '') + '\n[Sources]\n' + '\n'.join(url for _, url in sources) + '\n[/Sources]') + '</aside>')
    if i == 0:
        parts.append('<footer class="wd-slide-footer"><span data-wd-i18n="lecture_date">2026. 10. 12. 월요일</span><span>16:30–19:30</span><span>05 / 13</span></footer>')
    else:
        parts.append(f'<span class="w5-page">{i + 1:02} / {len(SLIDES):02}</span>')
    parts.append('</section>')
    sections.append('\n'.join(parts))

MESSAGES['ko']['page_title'] = '05 | React 심화 · 캠퍼스 푸드맵'
MESSAGES['en']['page_title'] = '05 | React Development · Campus Foodmap'
ROOT.joinpath('lecture-content.js').write_text('window.LECTURE_CONTENT = ' + json.dumps(MESSAGES, ensure_ascii=False, indent=2) + ';\n')
ROOT.joinpath('index.html').write_text('''<!doctype html>
<html class="wd-page" lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title data-wd-i18n="page_title">05 | React 심화 · 캠퍼스 푸드맵</title>
  <link rel="stylesheet" href="../../packages/web-deck/web-deck.css">
  <link rel="stylesheet" href="lecture.css">
</head>
<body class="wd-page-body" data-lecture="05">
<main class="wd-deck" data-web-deck><div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
''' + '\n\n'.join(sections) + '''
</div></div></main>
<script src="lecture-content.js"></script>
<script src="../shared/lecture-deck.js"></script>
<script src="../../packages/web-deck/vendor/prism/prism.js" data-manual></script>
<script src="../../packages/web-deck/web-deck.js"></script>
</body></html>
''')
ROOT.joinpath('materials/slide-map.json').write_text(json.dumps([{'number': i + 1, 'id': s.get('id', 'cover'), 'title': s['title'][0], 'sources': s.get('sources', [])} for i, s in enumerate(SLIDES)], ensure_ascii=False, indent=2) + '\n')
print(f'Built {len(SLIDES)} bilingual slides')
