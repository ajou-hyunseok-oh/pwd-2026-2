"""Build the one-slide bilingual PRD overview using the shared authoring format."""
import html
import json
from pathlib import Path

from lesson import SLIDES

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {source['id']: source for source in json.loads((ROOT / 'materials/references.json').read_text())}
MESSAGES = {'ko': {}, 'en': {}}
assert len(SLIDES) == 1, 'This overview must remain one slide'
slide = SLIDES[0]


def tr(key, values, tag='p', cls=''):
    assert len(values) == 2 and all(isinstance(value, str) and value.strip() for value in values), key
    for lang, value in zip(MESSAGES, values):
        MESSAGES[lang][key] = value
    attr = f' class="{cls}"' if cls else ''
    return f'<{tag}{attr} data-wd-i18n="{key}">{html.escape(values[0])}</{tag}>'


parts = ['<section class="wd-slide wd-lesson-slide wd-slide--content is-active" data-wd-slide="prd-overview" data-wd-concept="prd-overview" role="region">',
         tr('prd_title', slide['title'], 'h2', 'wd-slide-heading'),
         tr('prd_lead', slide['lead'], 'p', 'wd-slide-lead'),
         '<dl class="wd-lesson-concepts prd-overview"><div><dt>' +
         tr('prd_definition', slide['definition'], 'strong') +
         '</dt><dd><div class="wd-lesson-body prd-overview-body"><div class="wd-lesson-block">',
         tr('prd_table_title', slide['table_title'], 'h3', 'prd-block-title'),
         '<table class="wd-lesson-table"><thead><tr>']
parts += [tr(f'prd_head_{i}', cell, 'th').replace('<th ', '<th scope="col" ') for i, cell in enumerate(slide['head'])]
parts.append('</tr></thead><tbody>')
for i, row in enumerate(slide['rows']):
    parts.append('<tr>')
    for j, cell in enumerate(row):
        node = tr(f'prd_row_{i}_{j}', cell, 'th' if j == 0 else 'td')
        parts.append(node.replace('<th ', '<th scope="row" ') if j == 0 else node)
    parts.append('</tr>')
parts += ['</tbody></table></div><div class="wd-lesson-block">',
          tr('prd_references_title', slide['references_title'], 'h3', 'prd-block-title'),
          '<ul class="prd-reading-list">']
for i, item in enumerate(slide['references']):
    source = SOURCES[item['source']]
    link = tr(f'prd_reference_{i}', item['label'], 'a').replace('<a ',
        '<a href="' + html.escape(source['url'], quote=True) + '" target="_blank" rel="noopener" ')
    parts += ['<li>', link, tr(f'prd_reference_{i}_purpose', item['purpose']), '</li>']
parts.append('</ul></div></div></dd></div></dl>')
notes = []
for lang_index in range(2):
    lines = [('표의 7개 항목은 공식 자료를 참고한 수업용 요약이며 고정된 공식 양식이 아님.',
              'The seven table rows are a teaching summary informed by the official sources, not a mandatory official template.')[lang_index]]
    for item in slide['references']:
        source = SOURCES[item['source']]
        lines.append(f"{source['title']}\n{source['url']}\nAccessed: {source['accessed']}")
    notes.append('\n\n'.join(lines))
parts += [tr('prd_notes', notes, 'aside', 'wd-lesson-notes').replace('<aside ', '<aside hidden '), '</section>']

for lang, title, brand in [('ko', 'PRD 작성 개요', '실전웹서비스개발 · PRD'),
                           ('en', 'PRD Writing Overview', 'Practical Web Service Development · PRD')]:
    MESSAGES[lang].update(page_title=title, course_title=brand, ui_deck_label=title)

(ROOT / 'lecture-content.js').write_text('window.LECTURE_CONTENT = ' + json.dumps(MESSAGES, ensure_ascii=False, indent=2) + ';\n')
(ROOT / 'index.html').write_text('''<!doctype html>
<html class="wd-page" lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title data-wd-i18n="page_title">PRD 작성 개요</title>
  <link rel="stylesheet" href="../../packages/web-deck/web-deck.css">
  <link rel="stylesheet" href="../../packages/web-deck/authoring.css">
  <link rel="stylesheet" href="lecture.css">
</head>
<body class="wd-page-body" data-wd-supplement="PRD">
<main class="wd-deck" data-web-deck data-wd-authoring="v1"><div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
''' + '\n'.join(parts) + '''
</div></div></main>
<script src="lecture-content.js"></script>
<script>
window.WEB_DECK_CONFIG = {
  brand: '실전웹서비스개발 · PRD',
  brandKey: 'course_title', homeHref: '../../', locales: ['ko', 'en'],
  defaultLocale: 'ko', storageKey: 'pwd.webDeck.language',
  messages: window.LECTURE_CONTENT
};
</script>
<script src="../../packages/web-deck/web-deck.js"></script>
</body>
</html>
''')
mapping = [{'number': 1, 'id': slide['id'], 'kind': slide['kind'], 'title': slide['title'],
            'lead': slide['lead'], 'sources': [item['source'] for item in slide['references']],
            'application': 'one-slide-overview'}]
(ROOT / 'materials/slide-map.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'materials/title-outline.json').write_text(json.dumps([
    {key: value for key, value in mapping[0].items() if key in ('number', 'id', 'title', 'lead')}
], ensure_ascii=False, indent=2) + '\n')
for lang_index, lang in enumerate(MESSAGES):
    lines = [('PRD 작성 개요 · 공식 레퍼런스', 'PRD Writing Overview · Official References')[lang_index],
             'Accessed: 2026-10-12', '']
    for item in slide['references']:
        source = SOURCES[item['source']]
        lines += [source['title'], source['url'], item['purpose'][lang_index], '']
    (ROOT / f'materials/references.{lang}.txt').write_text('\n'.join(lines))
print('Built 1 bilingual PRD overview slide')
