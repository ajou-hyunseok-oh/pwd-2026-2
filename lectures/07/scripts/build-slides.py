"""Generate the bilingual Week 7 lecture from its authored content."""
import html
import json
import re
from pathlib import Path
from lesson_content import SLIDES
from authoring_blocks import enrich
from design_examples import apply as apply_design_examples
from example_blocks import render_example

SLIDES = apply_design_examples(enrich(SLIDES))

ROOT = Path(__file__).resolve().parents[1]
messages = {'ko': {}, 'en': {}}
def tr(key, ko, en, tag='p', cls=''):
    messages['ko'][key], messages['en'][key] = ko, en
    return f'<{tag} class="{cls}" data-wd-i18n="{key}">{html.escape(ko)}</{tag}>'

def practice_guide(practice, key):
    """Reuse Week 5's goals, deadline, deliverables, and reference layout."""
    result = ['<div class="wd-lesson-body wd-lesson-body--single"><div class="wd-lesson-block"><div class="wd-practice-grid"><div class="wd-practice-main">']
    for group in ('goals', 'requirements'):
        result.append(tr(key+'_'+group+'_label', *practice[group+'_label'], 'h3'))
        result.append('<ul>' + ''.join(tr(f'{key}_{group}_{i}', *item, 'li') for i, item in enumerate(practice[group])) + '</ul>')
    result.append('</div><div class="wd-practice-side"><div class="wd-practice-submission"><div class="wd-practice-deadline">')
    result.append(tr(key+'_deadline_label', *practice['deadline_label'], 'span'))
    result.append(tr(key+'_deadline', *practice['deadline'], 'strong'))
    result.append('</div><div class="wd-practice-deliverables">' + tr(key+'_deliverables_label', *practice['deliverables_label'], 'h3'))
    result.append('<ul>' + ''.join(tr(f'{key}_deliverable_{i}', *item, 'li') for i, item in enumerate(practice['deliverables'])) + '</ul></div></div>')
    result.append('<div class="wd-practice-reference">' + tr(key+'_reference_label', *practice['reference_label'], 'h3'))
    link = tr(key+'_reference_title', *practice['reference_title'], 'a')
    result.append(link.replace('<a ', '<a href="' + html.escape(practice['reference_url'], quote=True) + '" target="_blank" rel="noopener noreferrer" '))
    result.append(tr(key+'_scope', *practice['scope']))
    result.append('</div></div></div></div></div>')
    return '\n'.join(result)

sections = ['''<section class="wd-slide wd-lesson-slide wd-lesson-cover is-active" data-wd-slide="cover" data-wd-cover="weekly" role="region"><div class="wd-lesson-cover__content">''' + tr('w7_cover_eyebrow', '2026학년도 2학기 실전웹서비스개발', 'Practical Web Service Development · Fall 2026', 'p', 'wd-lesson-cover__eyebrow') + tr('w7_cover_title', '실전 웹서비스개발 – 7주차', 'Practical Web Service Development – Week 7', 'h1', 'wd-lesson-title') + tr('w7_cover_subtitle', '데이터베이스 설계와 PostgreSQL · Supabase', 'Database Design with PostgreSQL and Supabase', 'p', 'wd-lesson-cover__subtitle') + '</div><p class="wd-lesson-source">LECTURE 07</p></section>']
slide_map = [{'number': 1, 'id': 'cover', 'kind': 'cover', 'title': '실전 웹서비스개발 – 7주차'}]
chapter = 0
for number, slide in enumerate(SLIDES, 2):
    ident = slide['id']; ko, en = slide['ko'], slide['en']; kind = slide['type']; key = 'w7_' + str(number).zfill(2)
    assert kind in ('chapter', 'content')
    css = 'wd-lesson-chapter' if kind == 'chapter' else 'wd-slide--content'
    if slide.get('example'):
        css += ' w7-supported-slide'
    concept = '' if kind == 'chapter' else f' data-wd-concept="{html.escape(ident, quote=True)}"'
    parts = [f'<section class="wd-slide wd-lesson-slide {css}" data-wd-slide="{html.escape(ident, quote=True)}"{concept} role="region">']
    if kind == 'chapter':
        chapter += 1
        parts.append(tr(key+'_chapter', f'{chapter:02}', f'{chapter:02}', 'p', 'wd-lesson-eyebrow'))
    parts.append(tr(key+'_title', ko['title'], en['title'], 'h2', 'wd-slide-heading'))
    if ko['lead'] or en['lead']:
        parts.append(tr(key+'_lead', ko['lead'], en['lead'], 'p', 'wd-slide-lead'))
    if slide.get('practice'):
        parts.append(practice_guide(slide['practice'], key))
    if slide.get('example'):
        assert len(ko['concepts']) == len(en['concepts'])
        parts.append('<div class="wd-lesson-body wd-lesson-body--single w7-supported-body"><div class="wd-lesson-block"><dl class="wd-lesson-concepts w7-case-concepts">')
        for i, (kc, ec) in enumerate(zip(ko['concepts'], en['concepts'])):
            kd = [kc[2]] if isinstance(kc[2], str) else kc[2]
            ed = [ec[2]] if isinstance(ec[2], str) else ec[2]
            assert len(kd) == len(ed), ident
            details = ''.join(tr(f'{key}_c{i}_detail{j}', k, e, 'li') for j, (k, e) in enumerate(zip(kd, ed)))
            parts.append('<div><dt>'+tr(f'{key}_c{i}_term', kc[0]+' - '+kc[1], ec[0]+' - '+ec[1], 'strong')+'</dt>'+('<dd><ul>'+details+'</ul></dd>' if details else '')+'</div>')
        parts.append('</dl></div><div class="wd-lesson-block w7-example" data-wd-example="'+ident+'">')
        parts.append(render_example(slide['example'], key+'_example', tr))
        parts.append('</div></div>')
    if ko.get('history'):
        assert len(ko['history']) == len(en['history'])
        figure = slide['source_figures'][0]
        alt_key = key + '_history_alt'
        messages['ko'][alt_key], messages['en'][alt_key] = figure['alt']
        link_key = key + '_history_link'
        messages['ko'][link_key] = figure['alt'][0] + ' 크게 보기 (새 창)'
        messages['en'][link_key] = 'Open full-size: ' + figure['alt'][1] + ' (new tab)'
        parts.append('<div class="wd-lesson-body wd-lesson-body--history"><div class="wd-lesson-block"><dl class="wd-lesson-concepts week7-history__timeline">')
        for i, (kh, eh) in enumerate(zip(ko['history'], en['history'])):
            assert len(kh[1]) == len(eh[1])
            def history_heading(value):
                match = re.fullmatch(r'(.*?) \((.*)\)', value)
                assert match, value
                return match.group(1) + ' - ' + match.group(2)
            title = tr(f'{key}_history{i}_title', history_heading(kh[0]), history_heading(eh[0]), 'strong')
            details = ''.join(tr(f'{key}_history{i}_detail{j}', kd, ed, 'li') for j, (kd, ed) in enumerate(zip(kh[1], eh[1])) )
            parts.append('<div><dt>' + title + '</dt><dd><ul>' + details + '</ul></dd></div>')
        src = html.escape(figure['src'], quote=True)
        parts.append('</dl></div><div class="wd-lesson-block"><figure class="week7-history__figure"><a href="' + src + '" target="_blank" rel="noopener noreferrer" aria-label="' + html.escape(messages['ko'][link_key], quote=True) + '" data-wd-i18n-aria-label="' + link_key + '"><img src="' + src + '" alt="' + html.escape(figure['alt'][0], quote=True) + '" data-wd-i18n-alt="' + alt_key + '"></a></figure></div></div>')
    if kind == 'content' and (ko['concepts'] or slide.get('source_figures')) and not ko.get('history') and not slide.get('example'):
        assert len(ko['concepts']) == len(en['concepts'])
        has_code = bool(ko.get('code'))
        has_table = bool(ko.get('table'))
        has_steps = bool(ko.get('steps'))
        figures = slide.get('source_figures', [])
        diagram = slide.get('diagram')
        assert bool(en.get('code')) == has_code and bool(en.get('table')) == has_table and bool(en.get('steps')) == has_steps
        assert sum((has_code, has_table, has_steps, ident == 'erd', bool(figures), bool(diagram))) <= 1, f'{ident}: choose one supporting block'
        layout = slide.get('layout', 'code' if has_code else ('split' if ko['concepts'] and (has_table or has_steps or figures or ident == 'erd') else 'single'))
        assert layout in ('single', 'split', 'code', 'visual')
        parts.append('<div class="wd-lesson-body wd-lesson-body--' + layout + (' week7-dbms-body' if diagram == 'dbms_architecture' else '') + '">')
        if ko['concepts']:
            parts.append('<div class="wd-lesson-block"><dl class="wd-lesson-concepts">')
        for i, (kc, ec) in enumerate(zip(ko['concepts'], en['concepts'])):
            assert len(kc) == len(ec) == 3
            kd = [kc[2]] if isinstance(kc[2], str) else kc[2]
            ed = [ec[2]] if isinstance(ec[2], str) else ec[2]
            assert len(kd) == len(ed), f'{ident}: KO/EN detail count differs'
            details = ''.join(tr(f'{key}_c{i}_detail{j}', k, e, 'li') for j, (k, e) in enumerate(zip(kd, ed)))
            parts.append('<div><dt>' + tr(f'{key}_c{i}_term', kc[0]+' - '+kc[1], ec[0]+' - '+ec[1], 'strong') + '</dt>' + ('<dd><ul>' + details + '</ul></dd>' if details else '') + '</div>')
        if ko['concepts']:
            parts.append('</dl></div>')
        if diagram == 'dbms_architecture':
            browser_icon = ('<svg class="week7-architecture__icon" viewBox="0 0 120 100" aria-hidden="true" focusable="false">'
                            '<rect x="8" y="9" width="104" height="76" rx="5"/><path d="M8 28h104"/>'
                            '<circle cx="19" cy="19" r="2"/><circle cx="27" cy="19" r="2"/><circle cx="35" cy="19" r="2"/>'
                            '<path d="M38 45h44M38 56h34M38 67h38"/></svg>')
            server_icon = ('<svg class="week7-architecture__icon" viewBox="0 0 120 100" aria-hidden="true" focusable="false">'
                           '<rect x="17" y="8" width="86" height="24" rx="4"/><rect x="17" y="38" width="86" height="24" rx="4"/>'
                           '<rect x="17" y="68" width="86" height="24" rx="4"/><path d="M34 20h3M34 50h3M34 80h3M51 20h36M51 50h36M51 80h36"/></svg>')
            database_icon = ('<svg class="week7-architecture__icon week7-architecture__icon--db" viewBox="0 0 120 100" aria-hidden="true" focusable="false">'
                             '<ellipse cx="60" cy="19" rx="40" ry="13"/><path d="M20 19v61c0 7 18 13 40 13s40-6 40-13V19"/>'
                             '<path d="M20 39c0 7 18 13 40 13s40-6 40-13M20 59c0 7 18 13 40 13s40-6 40-13"/></svg>')
            parts.append('<div class="wd-lesson-block week7-architecture" role="group">')
            parts.append('<div class="week7-architecture__node">' + browser_icon + tr(key+'_arch_client', '클라이언트', 'Client', 'strong') + tr(key+'_arch_browser', '웹 브라우저', 'Web browser', 'span') + '</div>')
            parts.append('<div class="week7-architecture__exchange">' + tr(key+'_arch_request', '요청', 'Request', 'span') + tr(key+'_arch_response', '응답', 'Response', 'span') + '</div>')
            parts.append('<div class="week7-architecture__node">' + server_icon + tr(key+'_arch_server', '웹 서버', 'Web server', 'strong') + tr(key+'_arch_logic', '요청 처리', 'Request handling', 'span') + '</div>')
            parts.append('<div class="week7-architecture__exchange">' + tr(key+'_arch_query', '질의 · 변경', 'Query · Write', 'span') + tr(key+'_arch_result', '결과', 'Result', 'span') + '</div>')
            parts.append('<div class="week7-architecture__node week7-architecture__dbms">' + database_icon + '<strong>DBMS</strong>' + tr(key+'_arch_database', '데이터베이스 관리', 'Manages the database', 'span') + '</div>')
            parts.append('</div>')
        if ident == 'erd':
            parts.append('<div class="wd-lesson-block week7-erd" role="group">' + tr(key+'_erd_submission', '제보', 'Submission', 'strong', 'week7-erd__entity') + '<span class="week7-erd__line"><span>1</span><span>0..1</span></span>' + tr(key+'_erd_restaurant', '맛집', 'Restaurant', 'strong', 'week7-erd__entity') + '</div>')
        if figures:
            parts.append('<div class="wd-lesson-block week7-source-figures">')
            for i, fig in enumerate(figures):
                alt_key = f'{key}_source_figure{i}_alt'
                messages['ko'][alt_key], messages['en'][alt_key] = fig['alt']
                caption = tr(f'{key}_source_figure{i}_caption', fig['caption'][0], fig['caption'][1], 'figcaption') if fig.get('caption') else ''
                href = html.escape(fig['src'], quote=True)
                link_key = f'{key}_source_figure{i}_link'
                messages['ko'][link_key] = fig['alt'][0] + ' 원본 크기로 보기 (새 창)'
                messages['en'][link_key] = 'Open full-size: ' + fig['alt'][1] + ' (new tab)'
                image_markup = '<img src="' + href + '" alt="' + html.escape(fig['alt'][0], quote=True) + '" data-wd-i18n-alt="' + alt_key + '">'
                if ident == 'database-trends-2025' and i == 0:
                    # Reflow the original chart legend below the plot so that both
                    # remain legible at presentation size. The complete image is linked.
                    image_markup += '<span class="week7-trend-legend" aria-hidden="true"><span></span><span></span><span></span></span>'
                parts.append('<figure class="wd-lesson-figure week7-source-figure"><a href="' + href + '" target="_blank" rel="noopener noreferrer" aria-label="' + html.escape(messages['ko'][link_key], quote=True) + '" data-wd-i18n-aria-label="' + link_key + '">' + image_markup + '</a>' + caption + '</figure>')
            parts.append('</div>')
        if has_code:
            parts.append('<div class="wd-lesson-block">' + tr(key+'_code_label', ko['code_label'], en['code_label'], 'p', 'wd-lesson-code-label'))
            parts.append(tr(key+'_code', ko['code'], en['code'], 'pre', 'wd-code').replace('<pre class="wd-code"', '<pre class="wd-code" data-wd-code="text" data-wd-code-width="64"'))
            parts.append('</div>')
        if has_table:
            kt, et = ko['table'], en['table']
            assert len(kt['head']) == len(et['head']) and len(kt['rows']) == len(et['rows']), f'{ident}: KO/EN table shape differs'
            head = ''.join(tr(f'{key}_table_h{j}', k, e, 'th') for j, (k, e) in enumerate(zip(kt['head'], et['head'])))
            rows = []
            for i, (kr, er) in enumerate(zip(kt['rows'], et['rows'])):
                assert len(kr) == len(er) == len(kt['head']), f'{ident}: table row shape differs'
                cells = ''.join(tr(f'{key}_table_r{i}_{j}', k, e, 'th' if j == 0 else 'td') for j, (k, e) in enumerate(zip(kr, er)))
                rows.append('<tr>' + cells + '</tr>')
            parts.append('<div class="wd-lesson-block"><table class="wd-lesson-table"><thead><tr>' + head + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
        if has_steps:
            assert len(ko['steps']) == len(en['steps']), f'{ident}: KO/EN step count differs'
            steps = []
            for i, (ks, es) in enumerate(zip(ko['steps'], en['steps'])):
                assert len(ks) == len(es) == 2
                steps.append('<li>' + tr(f'{key}_step{i}_title', ks[0], es[0], 'strong') + tr(f'{key}_step{i}_body', ks[1], es[1]) + '</li>')
            parts.append('<div class="wd-lesson-block"><ol class="wd-lesson-steps">' + ''.join(steps) + '</ol></div>')
        if slide.get('reference_link'):
            url = slide['reference_link']
            key_link = key + '_reference'
            parts.append('<div class="week7-trend-link">' + tr(key_link, url, url, 'a').replace('<a ', '<a href="' + html.escape(url, quote=True) + '" target="_blank" rel="noopener noreferrer" ') + '</div>')
        parts.append('</div>')
    if slide.get('sources') or slide.get('note'):
        sources = slide.get('sources', [])
        note = slide.get('note', '') + ('\n'+slide['example_note'] if slide.get('example_note') else '')
        parts.append('<aside hidden class="wd-lesson-notes">' + html.escape(note + '\n[Sources]\n' + '\n'.join(sources) + '\n[/Sources]') + '</aside>')
    parts.append('</section>')
    sections.append('\n'.join(parts))
    slide_map.append({'number': number, 'id': ident, 'kind': kind, 'title': ko['title'], 'subtitle': ko['lead'], 'sources': slide.get('sources', []), 'source_pages': slide.get('source_pages', []), 'source_figures': [f['src'] for f in slide.get('source_figures', [])]})
messages['ko']['page_title'] = '07 | 데이터베이스 설계와 PostgreSQL · Supabase'
messages['en']['page_title'] = '07 | Database Design with PostgreSQL and Supabase'
ROOT.joinpath('lecture-content.js').write_text('window.LECTURE_CONTENT = ' + json.dumps(messages, ensure_ascii=False, indent=2) + ';\n')
ROOT.joinpath('index.html').write_text('''<!doctype html>
<html class="wd-page" lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-wd-i18n="page_title">07 | 데이터베이스 설계와 PostgreSQL · Supabase</title>
<link rel="stylesheet" href="../../packages/web-deck/web-deck.css"><link rel="stylesheet" href="../../packages/web-deck/authoring.css"><link rel="stylesheet" href="lecture.css">
</head><body class="wd-page-body" data-lecture="07"><main class="wd-deck" data-web-deck data-wd-authoring="v1"><div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
''' + '\n\n'.join(sections) + '''
</div></div></main><script src="lecture-content.js"></script><script src="../shared/lecture-deck.js"></script><script src="../../packages/web-deck/vendor/prism/prism.js" data-manual></script><script src="../../packages/web-deck/web-deck.js"></script></body></html>\n''')
ROOT.joinpath('materials/slide-map.json').write_text(json.dumps(slide_map, ensure_ascii=False, indent=2)+'\n')
print(f'Built {len(sections)} bilingual slides')
