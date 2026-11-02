"""Build the bilingual Week 7 review from frozen Week 6 code and HTTP evidence."""
import argparse
import html
import json
from pathlib import Path
import subprocess
from lesson import SLIDES, JOURNEY_STEPS, JOURNEY_REQUESTS

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
MESSAGES = {'ko': {}, 'en': {}}
EXCERPTS = json.loads((ROOT / 'materials/code-excerpts.json').read_text())
EVIDENCE = json.loads((ROOT / 'materials/runtime-evidence.json').read_text())
HASHES = {record['file']: record['sha256'] for record in EVIDENCE['sourceFiles']}
for excerpt in EXCERPTS.values():
    assert HASHES.get(excerpt['file']) == excerpt['sha256'], f'Code / runtime source mismatch: {excerpt["file"]}'


def tr(key, values, tag='p', cls='', attrs=''):
    for locale, value in zip(MESSAGES, values):
        MESSAGES[locale][key] = value
    return f'<{tag}' + (f' class="{cls}"' if cls else '') + f' data-wd-i18n="{key}"{attrs}>' + html.escape(values[0]) + f'</{tag}>'


def formatted_code():
    # Match the Week 6 review's 58-column source formatting.
    script = """const fs=require('node:fs');
const prettier=require('./packages/web-deck/node_modules/prettier');
const options=require('./packages/web-deck/code-format.json');
(async()=>{const excerpts=JSON.parse(fs.readFileSync(0,'utf8'));const result={};
for(const [key,v] of Object.entries(excerpts)) result[key]=v.language==='bash'?v.code:(await prettier.format(v.code,{...options,parser:'typescript',printWidth:58})).trimEnd();
process.stdout.write(JSON.stringify(result));})();"""
    result = subprocess.run(['node', '-e', script], cwd=REPO, input=json.dumps(EXCERPTS), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


CODES = formatted_code()


def response_text(ident):
    requests = EVIDENCE['requests']
    if ident == 'create-input':
        return json.dumps(requests['created']['body'], ensure_ascii=False, indent=2)
    if ident == 'list-result':
        record = requests['list']
        selected = [{key: row[key] for key in ['id', 'name']} for row in record['response']['data']]
        lines = [f"HTTP {record['status']}", '{"data": [']
        lines.extend('  ' + json.dumps(row, ensure_ascii=False) + (',' if index < len(selected) - 1 else '')
                     for index, row in enumerate(selected))
        lines.append(']}')
        return '\n'.join(lines)
    if ident == 'restart':
        values = [
            ('생성 전 목록', 'Initial list', f"HTTP {requests['list']['status']} · {len(requests['list']['response']['data'])}"),
            ('생성 후 목록', 'List after creation', f"HTTP {requests['after-create']['status']} · {len(requests['after-create']['response']['data'])}"),
            ('다른 요청 GET /api/restaurants/4', 'Later GET /api/restaurants/4', f"HTTP {requests['shared']['status']}"),
            ('재시작 후 목록', 'List after restart', f"HTTP {requests['restarted']['status']} · {len(requests['restarted']['response']['data'])}"),
            ('재시작 후 GET /api/restaurants/4', 'GET /api/restaurants/4 after restart', f"HTTP {requests['lost']['status']}"),
        ]
        return tuple('\n'.join(f'{row[index]}: {row[2]}' +
                     (('건' if index == 0 else ' items') if ' · ' in row[2] else '')
                     for row in values) for index in [0, 1])
    record = requests[ident]
    data = record['response']
    if ident == 'created':
        data = {'data': {k: data['data'][k] for k in ['id', 'recommendedMenu']}}
    if ident in ['created', 'invalid', 'missing', 'not-found']:
        return 'HTTP ' + str(record['status']) + '\n' + json.dumps(data, ensure_ascii=False)
    return 'HTTP ' + str(record['status']) + '\n' + json.dumps(data, ensure_ascii=False, indent=2)


def block(b, key):
    if b['kind'] == 'concept':
        return '<dl class="wd-lesson-concepts"><div><dt>' + tr(key + '_term', b['term'], 'strong') + '</dt><dd><ul>' + ''.join(tr(f'{key}_{i}', detail, 'li') for i, detail in enumerate(b['details'])) + '</ul></dd></div></dl>'
    if b['kind'] == 'code':
        language = EXCERPTS[b['ident']]['language']
        return '<div class="review-code">' + tr(key + '_label', b['label'], 'p', 'wd-lesson-code-label') + tr(key + '_code', (CODES[b['ident']],) * 2, 'pre', 'wd-code', f' data-wd-code="{language}" data-wd-code-width="58"') + '</div>'
    if b['kind'] == 'result':
        value = response_text(b['ident'])
        values = value if isinstance(value, tuple) else (value, value)
        return '<div class="review-result">' + tr(key + '_label', b['label'], 'p', 'wd-lesson-code-label') + tr(key + '_output', values, 'samp', 'review-output') + '</div>'
    if b['kind'] == 'table':
        return '<table class="wd-lesson-table"><thead><tr>' + ''.join(tr(f'{key}_h{i}', c, 'th', attrs=' scope="col"') for i, c in enumerate(b['head'])) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(tr(f'{key}_{i}_{j}', c, 'th' if j == 0 else 'td', attrs=' scope="row"' if j == 0 else '') for j, c in enumerate(row)) + '</tr>' for i, row in enumerate(b['rows'])) + '</tbody></table>'
    raise ValueError(b['kind'])


def request_journey(value, key):
    steps = ''.join(tr(f'{key}_step_{index}', label, 'li',
                       'is-current' if index in value['current'] else '',
                       f' data-flow-step="{index}"')
                    for index, label in enumerate(JOURNEY_STEPS))
    return '<div class="review-journey" data-request-flow="' + value['kind'] + '">' + \
        tr(key + '_request', JOURNEY_REQUESTS[value['kind']], 'p', 'review-journey__request') + \
        '<ol>' + steps + '</ol></div>'


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
                      tr('review_cover_title', slide['title'], 'h1', 'wd-lesson-title'), tr('review_cover_subtitle', slide['lead'], 'p', 'wd-lesson-cover__subtitle'), '</div>', '<p class="wd-lesson-source">LECTURE 07</p>']
        else:
            parts += [tr(ident + '_title', slide['title'], 'h2', 'wd-slide-heading'), tr(ident + '_lead', slide['lead'], 'p', 'wd-slide-lead')]
            if slide.get('journey'):
                parts.append(request_journey(slide['journey'], ident + '_journey'))
            parts.append('<div class="wd-lesson-body review-body">')
            for side in ['left', 'right']:
                parts.append('<div class="wd-lesson-block review-stack">' + ''.join(block(b, f'{ident}_{side}_{i}') for i, b in enumerate(slide[side])) + '</div>')
            parts.append('</div>')
        if slide.get('sources'):
            source_text = '[Source]\n' + '\n'.join('pwd-week6/' + source if not source.startswith('https://') else source for source in slide['sources']) + '\n[/Source]'
            parts.append('<aside hidden class="wd-lesson-notes">' + html.escape(source_text) + '</aside>')
        parts.append('</section>')
        sections.append('\n'.join(parts))
        blocks = slide.get('left', []) + slide.get('right', [])
        rows.append(dict(number=index + 1, id=ident, title=slide['title'][0], subtitle=slide['lead'][0], sources=slide.get('sources', []),
                         code_excerpts=[b['ident'] for b in blocks if b['kind'] == 'code'],
                         runtime_results=[b['ident'] for b in blocks if b['kind'] == 'result'],
                         request_flow=slide.get('journey')))
    page_title = ('07 | 6주차 실습 리뷰 · Ajou Campus Foodmap API', '07 | Week 6 Practice Review · Ajou Campus Foodmap API')
    for locale, value in zip(MESSAGES, page_title):
        for key in ['page_title', 'ui_deck_label', 'lecture_title']:
            MESSAGES[locale][key] = value
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
<body class="wd-page-body" data-lecture="07">
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
print(f'Week 07 server review: {len(SLIDES)} slides ' + ('checked' if args.check else 'built'))
