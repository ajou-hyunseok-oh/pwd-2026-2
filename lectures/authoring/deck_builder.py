"""Shared source-to-HTML builder for the Week 8/9 authoring scaffolds.

The block markup follows Week 6/7 and opts into web-deck/authoring.css.
Run a deck's scripts/build-slides.py; edit scripts/lesson.py, not its outputs.
"""
import argparse
import html
import json
import os
import re
from pathlib import Path


def build(root, week, subtitle, slides, *, render_extra=None, stylesheets=()):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[2]
    messages = {'ko': {}, 'en': {}}

    def relative(target):
        return Path(os.path.relpath(target, root)).as_posix()

    def tr(key, values, tag='p', cls='', attrs=''):
        assert len(values) == 2 and all(isinstance(v, str) and v.strip() for v in values), key
        messages['ko'][key], messages['en'][key] = values
        classes = f' class="{cls}"' if cls else ''
        return f'<{tag}{classes}{attrs} data-wd-i18n="{key}">{html.escape(values[0])}</{tag}>'

    def block(item, key):
        kind = item['kind']
        if kind == 'concepts':
            parts = ['<dl class="wd-lesson-concepts wd-lesson-concepts--bulleted">']
            for i, concept in enumerate(item['items']):
                assert all(' - ' in value for value in concept['term']), key
                parts.append('<div><dt>' + tr(f'{key}_{i}_term', concept['term'], 'strong') + '</dt>')
                if concept.get('details'):
                    parts.append('<dd><ul>' + ''.join(tr(f'{key}_{i}_detail{j}', detail, 'li') for j, detail in enumerate(concept['details'])) + '</ul></dd>')
                parts.append('</div>')
            return '\n'.join(parts + ['</dl>'])
        if kind == 'placeholder':
            return tr(key, item['label'], 'div', 'wd-lesson-placeholder')
        if kind == 'code':
            language = item['language']
            assert language in ('html', 'css', 'javascript', 'jsx', 'typescript', 'tsx', 'json', 'bash', 'text')
            width = item.get('width', 64)
            assert 32 <= width <= 80
            return (tr(key + '_label', item['label'], cls='wd-lesson-code-label') +
                    tr(key + '_code', item['text'], 'pre', 'wd-code', f' data-wd-code="{language}" data-wd-code-width="{width}"'))
        if kind == 'table':
            head = ''.join(tr(f'{key}_h{i}', cell, 'th', attrs=' scope="col"') for i, cell in enumerate(item['head']))
            rows = []
            for i, row in enumerate(item['rows']):
                assert len(row) == len(item['head']), key
                rows.append('<tr>' + ''.join(tr(f'{key}_r{i}_{j}', cell, 'th' if j == 0 else 'td', attrs=' scope="row"' if j == 0 else '') for j, cell in enumerate(row)) + '</tr>')
            return '<table class="wd-lesson-table"><thead><tr>' + head + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
        if kind == 'steps':
            return '<ol class="wd-lesson-steps">' + ''.join('<li>' + tr(f'{key}_{i}_title', step['title'], 'strong') + tr(f'{key}_{i}_body', step['body']) + '</li>' for i, step in enumerate(item['items'])) + '</ol>'
        if kind == 'figure':
            src = html.escape(item['src'], quote=True)
            assert (root / item['src']).is_file(), item['src']
            alt_key = key + '_alt'
            messages['ko'][alt_key], messages['en'][alt_key] = item['alt']
            return ('<figure class="wd-lesson-figure"><img src="' + src + '" alt="' + html.escape(item['alt'][0], quote=True) + '" data-wd-i18n-alt="' + alt_key + '">' +
                    tr(key + '_caption', item['caption'], 'figcaption') + '</figure>')
        if render_extra is not None:
            rendered = render_extra(item, key, tr)
            if rendered is not None:
                return rendered
        raise ValueError(f'Unknown block kind: {kind}')

    title = (f'실전 웹서비스개발 – {week}주차', f'Practical Web Service Development – Week {week}')
    sections = ['<section class="wd-slide wd-lesson-slide wd-lesson-cover is-active" data-wd-slide="cover" data-wd-cover="weekly" role="region">\n<div class="wd-lesson-cover__content">' +
                tr('cover_eyebrow', ('2026학년도 2학기 실전웹서비스개발', 'Practical Web Service Development · Fall 2026'), cls='wd-lesson-cover__eyebrow') +
                tr('cover_title', title, 'h1', 'wd-lesson-title') +
                tr('cover_subtitle', subtitle, cls='wd-lesson-cover__subtitle') +
                f'</div><p class="wd-lesson-source">LECTURE {week:02}</p></section>']
    slide_map = [dict(number=1, id='cover', kind='cover', title=title[0], subtitle=subtitle[0])]
    ids = {'cover'}
    chapter = 0
    for number, slide in enumerate(slides, 2):
        ident = slide['id']
        assert re.fullmatch(r'[a-z][a-z0-9-]*', ident) and ident not in ids, ident
        ids.add(ident)
        key = ident.replace('-', '_')
        kind = slide.get('kind', 'content')
        assert kind in ('chapter', 'content')
        cls = 'wd-lesson-chapter' if kind == 'chapter' else 'wd-slide--content'
        concept = f' data-wd-concept="{ident}"' if kind == 'content' else ''
        parts = [f'<section class="wd-slide wd-lesson-slide {cls}" data-wd-slide="{ident}"{concept} role="region">']
        if kind == 'chapter':
            chapter += 1
            assert not slide.get('columns'), f'{ident}: no body on chapter covers'
            parts.append(tr(key + '_number', (f'{chapter:02}',) * 2, cls='wd-lesson-eyebrow'))
        parts.append(tr(key + '_title', slide['title'], 'h2', 'wd-slide-heading'))
        if slide.get('lead'):
            parts.append(tr(key + '_lead', slide['lead'], cls='wd-slide-lead'))
        if kind == 'content':
            layout = slide.get('layout', 'single')
            assert layout in ('single', 'split', 'code', 'visual')
            columns = slide['columns']
            assert len(columns) == (1 if layout == 'single' else 2), ident
            parts.append(f'<div class="wd-lesson-body wd-lesson-body--{layout}">')
            for i, column in enumerate(columns):
                parts.append('<div class="wd-lesson-block">' + '\n'.join(block(item, f'{key}_b{i}_{j}') for j, item in enumerate(column)) + '</div>')
            parts.append('</div>')
        if slide.get('sources') or slide.get('note'):
            parts.append('<aside hidden class="wd-lesson-notes">' + html.escape(slide.get('note', '') + '\n[Sources]\n' + '\n'.join(slide.get('sources', [])) + '\n[/Sources]') + '</aside>')
        sections.append('\n'.join(parts + ['</section>']))
        slide_map.append(dict(number=number, id=ident, kind=kind, title=slide['title'][0], subtitle=slide.get('lead', ('', ''))[0], sources=slide.get('sources', [])))

    page_title = (f'{week:02} | {subtitle[0]}', f'{week:02} | {subtitle[1]}')
    for key in ('page_title', 'ui_deck_label', 'lecture_title'):
        messages['ko'][key], messages['en'][key] = page_title
    package = relative(repository / 'packages/web-deck')
    shared = relative(repository / 'lectures/shared/lecture-deck.js')
    extra_styles = ''
    for stylesheet in stylesheets:
        assert (root / stylesheet).is_file(), stylesheet
        extra_styles += '\n<link rel="stylesheet" href="' + html.escape(stylesheet, quote=True) + '">'
    markup = f'''<!doctype html>
<html class="wd-page" lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="data:,">
<title data-wd-i18n="page_title">{html.escape(page_title[0])}</title>
<link rel="stylesheet" href="{package}/web-deck.css">
<link rel="stylesheet" href="{package}/authoring.css">{extra_styles}
</head>
<body class="wd-page-body" data-lecture="{week:02}">
<main class="wd-deck" data-web-deck data-wd-authoring="v1" data-wd-format="week-05">
<div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
''' + '\n\n'.join(sections) + f'''
</div></div></main>
<script src="lecture-content.js"></script>
<script src="{shared}"></script>
<script>window.WEB_DECK_CONFIG.homeHref = '{relative(repository)}/';</script>
<script src="{package}/vendor/prism/prism.js" data-manual></script>
<script src="{package}/web-deck.js"></script>
</body>
</html>
'''
    outputs = {'index.html': markup, 'lecture-content.js': 'window.LECTURE_CONTENT = ' + json.dumps(messages, ensure_ascii=False, indent=2) + ';\n',
               'materials/slide-map.json': json.dumps(slide_map, ensure_ascii=False, indent=2) + '\n'}
    for name, value in outputs.items():
        target = root / name
        if args.check:
            assert target.read_text() == value, f'Stale generated file: {target}'
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value)
    print(f'{root.relative_to(repository)}: {len(sections)} slides ' + ('checked' if args.check else 'built'))
