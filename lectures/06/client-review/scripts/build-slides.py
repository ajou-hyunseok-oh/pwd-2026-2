"""Build the Week 6 client review using the shared Week 05 HTML authoring format."""
import argparse
import html
import json
from pathlib import Path
import subprocess
from lesson import SLIDES

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
MESSAGES = {'ko': {}, 'en': {}}
EXCERPTS = json.loads((ROOT / 'materials/code-excerpts.json').read_text())
CAPTURE = json.loads((ROOT / 'materials/capture-manifest.json').read_text())
CAPTURE_HASHES = {record['file']: record['sha256'] for record in CAPTURE['sourceFiles']}
for excerpt in EXCERPTS.values():
    assert CAPTURE_HASHES.get(excerpt['file']) == excerpt['sha256'], \
        f'Code and screenshots are from different source versions: {excerpt["file"]}'


def tr(key, values, tag='p', cls='', attrs=''):
    for locale, value in zip(MESSAGES, values):
        MESSAGES[locale][key] = value
    return f'<{tag}' + (f' class="{cls}"' if cls else '') + f' data-wd-i18n="{key}"{attrs}>' + html.escape(values[0]) + f'</{tag}>'


def formatted_code():
    # Reuse the repository formatter and options at generation time.
    script = """const fs=require('node:fs');
const prettier=require('./packages/web-deck/node_modules/prettier');
const options=require('./packages/web-deck/code-format.json');
(async()=>{const codes=JSON.parse(fs.readFileSync(0,'utf8'));const result={};
for(const [key,value] of Object.entries(codes)) result[key]=(await prettier.format(value,{...options,parser:'typescript',printWidth:58})).trimEnd();
process.stdout.write(JSON.stringify(result));})();"""
    result = subprocess.run(['node', '-e', script], cwd=REPO, input=json.dumps({k: v['code'] for k, v in EXCERPTS.items()}), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


CODES = formatted_code()


def block(b, key):
    if b['kind'] == 'screen':
        caption = b['caption']
        for locale, value in zip(MESSAGES, caption):
            MESSAGES[locale][key + '_alt'] = value
        image = f'materials/screens/{b["name"]}.png'
        assert (ROOT / image).is_file(), f'Missing app capture: {image}'
        return f'<figure class="wd-lesson-figure review-screen review-screen--{b["name"]}"><a href="{image}" target="_blank" rel="noopener noreferrer"><img src="{image}" alt="{html.escape(caption[0], quote=True)}" data-wd-i18n-alt="{key}_alt"></a>' + tr(key + '_caption', caption, 'figcaption') + '</figure>'
    if b['kind'] == 'concept':
        return '<dl class="wd-lesson-concepts"><div><dt>' + tr(key + '_term', b['term'], 'strong') + '</dt><dd><ul>' + ''.join(tr(f'{key}_{i}', detail, 'li') for i, detail in enumerate(b['details'])) + '</ul></dd></div></dl>'
    if b['kind'] == 'code':
        return '<div class="review-code">' + tr(key + '_label', b['label'], 'p', 'wd-lesson-code-label') + tr(key + '_code', (CODES[b['ident']],) * 2, 'pre', 'wd-code', ' data-wd-code="tsx" data-wd-code-width="58"') + '</div>'
    if b['kind'] == 'table':
        return '<table class="wd-lesson-table"><thead><tr>' + ''.join(tr(f'{key}_h{i}', c, 'th', attrs=' scope="col"') for i, c in enumerate(b['head'])) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(tr(f'{key}_{i}_{j}', c, 'th' if j == 0 else 'td', attrs=' scope="row"' if j == 0 else '') for j, c in enumerate(row)) + '</tr>' for i, row in enumerate(b['rows'])) + '</tbody></table>'
    raise ValueError(b['kind'])


def outputs():
    sections, rows = [], []
    for index, slide in enumerate(SLIDES):
        ident = slide['id']
        cover = slide.get('kind') == 'cover'
        cls = 'wd-lesson-cover is-active' if cover else 'wd-slide--content'
        attrs = ' data-wd-cover="weekly"' if cover else f' data-wd-concept="{ident}"'
        parts = [f'<section class="wd-slide wd-lesson-slide review-{ident} {cls}" data-wd-slide="{ident}"{attrs} role="region">']
        if cover:
            parts += ['<div class="wd-lesson-cover__content">', tr('review_eyebrow', ('2026학년도 2학기 실전웹서비스개발', 'Practical Web Service Development · Fall 2026'), 'p', 'wd-lesson-cover__eyebrow'),
                      tr('review_cover_title', slide['title'], 'h1', 'wd-lesson-title'), tr('review_cover_subtitle', slide['lead'], 'p', 'wd-lesson-cover__subtitle'), '</div>', '<p class="wd-lesson-source">LECTURE 06</p>']
        else:
            parts += [tr(ident + '_title', slide['title'], 'h2', 'wd-slide-heading'), tr(ident + '_lead', slide['lead'], 'p', 'wd-slide-lead'), '<div class="wd-lesson-body review-body">']
            for side in ['left', 'right']:
                parts.append('<div class="wd-lesson-block review-stack">' + ''.join(block(b, f'{ident}_{side}_{i}') for i, b in enumerate(slide[side])) + '</div>')
            parts.append('</div>')
        if slide.get('sources'):
            source_text = '[Source]\n' + '\n'.join('pwd-week5/' + source if not source.startswith('https://') else source for source in slide['sources']) + '\n[/Source]'
            parts.append('<aside hidden class="wd-lesson-notes">' + html.escape(source_text) + '</aside>')
        parts.append('</section>')
        sections.append('\n'.join(parts))
        blocks = slide.get('left', []) + slide.get('right', [])
        rows.append(dict(number=index + 1, id=ident, title=slide['title'][0], sources=slide.get('sources', []),
                         screenshots=[dict(file=f'materials/screens/{b["name"]}.png', caption=b['caption'][0]) for b in blocks if b['kind'] == 'screen'],
                         code_excerpts=[b['ident'] for b in blocks if b['kind'] == 'code']))
    page_title = ('06 | Ajou Campus Foodmap 클라이언트 코드 리뷰', '06 | Ajou Campus Foodmap Client Code Review')
    for locale, text in zip(MESSAGES, page_title):
        MESSAGES[locale]['page_title'] = text
        MESSAGES[locale]['ui_deck_label'] = text
        MESSAGES[locale]['lecture_title'] = text
    markup = '''<!doctype html>
<html class="wd-page" lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="data:,">
<title data-wd-i18n="page_title">''' + html.escape(page_title[0]) + '''</title>
<link rel="stylesheet" href="../../../packages/web-deck/web-deck.css">
<link rel="stylesheet" href="../../../packages/web-deck/authoring.css">
<link rel="stylesheet" href="lecture.css">
</head>
<body class="wd-page-body" data-lecture="06">
<main class="wd-deck" data-web-deck data-wd-authoring="v1" data-wd-format="week-05"><div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
''' + '\n\n'.join(sections) + '''
</div></div></main>
<script src="lecture-content.js"></script>
<script src="../../shared/lecture-deck.js"></script>
<script>window.WEB_DECK_CONFIG.homeHref = '../../../';</script>
<script src="../../../packages/web-deck/vendor/prism/prism.js" data-manual></script>
<script src="../../../packages/web-deck/web-deck.js"></script>
</body></html>
'''
    return {'index.html': markup, 'lecture-content.js': 'window.LECTURE_CONTENT = ' + json.dumps(MESSAGES, ensure_ascii=False, indent=2) + ';\n',
            'materials/slide-map.json': json.dumps(rows, ensure_ascii=False, indent=2) + '\n'}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
for name, value in outputs().items():
    path = ROOT / name
    if args.check:
        assert path.read_text() == value, f'Stale generated file: {name}'
    else:
        path.write_text(value)
print('Week 06 client review: 8 slides ' + ('checked' if args.check else 'built'))
