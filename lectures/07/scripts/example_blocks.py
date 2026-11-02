"""Render bilingual, editable teaching examples within the Week 7 deck."""
import html


def render_example(block, key, tr):
    def label(suffix, value, tag='p', cls=''):
        assert isinstance(value, (list, tuple)) and len(value) == 2, (key, value)
        return tr(key+'_'+suffix, *value, tag, cls)

    kind = block['kind']
    cls = 'w7-case-'+kind + (' '+block['class'] if block.get('class') else '')
    if kind in ('grid', 'stack', 'flow'):
        children = []
        for i, child in enumerate(block['items']):
            if kind == 'flow' and i:
                children.append('<span class="w7-case-arrow" aria-hidden="true">→</span>')
            children.append(render_example(child, f'{key}_{i}', tr))
        return '<div class="'+cls+'">'+''.join(children)+'</div>'
    if kind == 'note':
        return label('text', block['text'], 'p', cls)
    if kind == 'code':
        language = html.escape(block['language'], quote=True)
        caption = label('caption', block['caption'], 'p', 'wd-lesson-code-label')
        code = label('code', block['code'], 'pre', 'wd-code')
        return '<div class="'+cls+'">'+caption+code.replace('<pre ', '<pre data-wd-code="'+language+'" data-wd-code-width="64" ')+'</div>'
    if kind == 'spatial':
        labels = label('title', block['title'], 'figcaption')
        center = label('center', ('현재 위치','Current location'), 'text', 'w7-spatial-label').replace('<text ', '<text x="240" y="165" text-anchor="middle" ')
        points = []
        for i, point in enumerate(block['points']):
            x, y = 240+point['x']*.19, 140-point['y']*.19
            color = '#2e7250' if point['inside'] else '#a4493b'
            points.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>')
            points.append(label(f'point{i}', point['label'], 'text', 'w7-spatial-label').replace('<text ', f'<text x="{x+9}" y="{y-7}" '))
        return '<figure class="w7-spatial">'+labels+'<svg viewBox="0 0 480 280" role="img" aria-label="'+html.escape(block['title'][0],quote=True)+'" data-wd-i18n-aria-label="'+key+'_title"><circle cx="240" cy="140" r="95" fill="#edf5ef" stroke="#557e60" stroke-width="2"/><path d="M240 140h95" stroke="#557e60" stroke-dasharray="5 5"/><text x="273" y="130" class="w7-spatial-label">500 m</text><circle cx="240" cy="140" r="5" fill="#274c38"/>'+center+''.join(points)+'</svg></figure>'
    if kind == 'node':
        lines = ''.join(label(f'line{i}', value) for i, value in enumerate(block.get('lines', [])))
        return '<div class="'+cls+'">'+label('title', block['title'], 'strong')+lines+'</div>'
    if kind == 'table':
        head = block['head']
        keys = block.get('keys', [])
        marks = {(r, c): tone for r, c, tone in block.get('marks', [])}
        headings = ''.join(label(f'h{j}', value, 'th', 'w7-key-column' if j in keys else '').replace('<th ', '<th scope="col" ') for j, value in enumerate(head))
        rows = []
        for i, row in enumerate(block['rows']):
            assert len(row) == len(head), (key, row)
            cells = []
            for j, value in enumerate(row):
                tone = marks.get((i, j), '')
                cell_cls = ('w7-key-column ' if j in keys else '') + ('w7-cell-'+tone if tone else '')
                cells.append(label(f'r{i}_{j}', value, 'td', cell_cls.strip()))
            rows.append('<tr>'+''.join(cells)+'</tr>')
        cols = ''
        if block.get('widths'):
            assert len(block['widths']) == len(head)
            cols = '<colgroup>'+''.join(f'<col style="width:{n}%">' for n in block['widths'])+'</colgroup>'
        return '<table class="wd-lesson-table '+cls+'">'+label('title', block['title'], 'caption')+cols+'<thead><tr>'+headings+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
    if kind == 'figure':
        src = html.escape(block['src'], quote=True)
        # Register the same image description for both visible and accessible text.
        label('alt', block['alt'], 'span')
        label('link', (block['alt'][0]+' 크게 보기 (새 창)', 'Open full-size: '+block['alt'][1]+' (new tab)'), 'span')
        caption = label('caption', block['caption'], 'figcaption') if block.get('caption') else ''
        return '<figure class="'+cls+'"><a href="'+src+'" target="_blank" rel="noopener noreferrer" aria-label="'+html.escape(block['alt'][0]+' 크게 보기 (새 창)', quote=True)+'" data-wd-i18n-aria-label="'+key+'_link"><img src="'+src+'" alt="'+html.escape(block['alt'][0], quote=True)+'" data-wd-i18n-alt="'+key+'_alt"></a>'+caption+'</figure>'
    if kind == 'relation':
        left = render_example(block['left'], key+'_left', tr)
        right = render_example(block['right'], key+'_right', tr)
        line = '<div class="w7-relation-line">'+label('name', block['label'], 'strong')+'<div><span>'+html.escape(block['counts'][0])+'</span><span>'+html.escape(block['counts'][1])+'</span></div></div>'
        return '<div class="'+cls+'">'+left+line+right+'</div>'
    raise ValueError(kind)
