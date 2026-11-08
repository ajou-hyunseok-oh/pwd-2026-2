"""Editable source-derived diagrams for the Week 9 HTML deck.

SVG expresses the source's node/edge relationships; all labels are live KO/EN
text. Mobile uses the same relationships as a readable ordered list.
"""
from html import escape


def render_resource(item, key, tr):
    kind = item['kind']
    def caption():
        return tr(key+'_caption',item['caption'],'figcaption','w9-caption') if item.get('show_caption',True) else ''
    if kind == 'resource-row':
        parts=['<div class="w9-resource-row">']
        for i,column in enumerate(item['columns']):
            parts.append('<div class="w9-resource-column">')
            for j,child in enumerate(column):
                rendered=render_resource(child,f'{key}_{i}_{j}',tr)
                assert rendered is not None,child['kind']
                parts.append(rendered)
            parts.append('</div>')
        return '\n'.join(parts+['</div>'])
    # Nested resources reuse the same native markup as the common builder.
    if kind == 'figure':
        alt_key=key+'_alt'
        tr(alt_key,item['alt'])
        return ('<figure class="wd-lesson-figure"><img src="'+escape(item['src'],quote=True)+'" alt="'+
                escape(item['alt'][0],quote=True)+'" data-wd-i18n-alt="'+alt_key+'">'+
                tr(key+'_caption',item['caption'],'figcaption')+'</figure>')
    if kind == 'code':
        language=item['language']; width=item.get('width',64)
        return (tr(key+'_label',item['label'],cls='wd-lesson-code-label')+
                tr(key+'_code',item['text'],'pre','wd-code',
                   f' data-wd-code="{language}" data-wd-code-width="{width}"'))
    if kind == 'table':
        head=''.join(tr(f'{key}_h{i}',c,'th',attrs=' scope="col"') for i,c in enumerate(item['head']))
        rows=[]
        for i,row in enumerate(item['rows']):
            assert len(row)==len(item['head'])
            rows.append('<tr>'+''.join(tr(f'{key}_r{i}_{j}',c,'th' if j==0 else 'td',
                                        attrs=' scope="row"' if j==0 else '') for j,c in enumerate(row))+'</tr>')
        return '<table class="wd-lesson-table"><thead><tr>'+head+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
    if kind == 'resource-groups':
        parts = [f'<figure class="w9-groups" data-groups="{len(item["items"])}"><div class="w9-group-list">']
        for i, group in enumerate(item['items']):
            parts += ['<div>', tr(f'{key}_{i}_title',group['title'],'strong'),
                      tr(f'{key}_{i}_body',group['body']), '</div>']
        return '\n'.join(parts+['</div>',caption(),'</figure>'])
    if kind == 'resource-tokens':
        parts = ['<figure class="w9-tokens">',tr(key+'_input',item['text'],'p','w9-token-input'),'<ol>']
        for i,(piece,ident) in enumerate(item['items']):
            parts += ['<li>',tr(f'{key}_{i}_text',(piece,piece),'strong'),tr(f'{key}_{i}_id',(f'ID {ident}',)*2),'</li>']
        return '\n'.join(parts+['</ol>',caption(),'</figure>'])
    if kind == 'resource-context':
        parts = ['<figure class="w9-context"><ol>']
        parts += [tr(f'{key}_{i}',part,'li') for i,part in enumerate(item['items'])]
        return '\n'.join(parts+['</ol>',caption(),'</figure>'])
    if kind == 'resource-editor':
        parts = ['<figure class="w9-editor"><div class="w9-editor-code">']
        for part in ['prefix','suggestion','suffix']:
            parts.append(tr(key+'_'+part,item[part],'div','w9-editor-'+part))
        return '\n'.join(parts+['</div>',caption(),'</figure>'])
    if kind == 'resource-screen':
        parts = ['<figure class="w9-screen"><div class="w9-screen-surface">',
                 tr(key+'_title',('게시글 등록','Create a post'),'strong'),
                 tr(key+'_label',('제목','Title'),'p','w9-screen-label'),
                 tr(key+'_value',item['value'],'p','w9-screen-input'),
                 tr(key+'_button',('등록','Submit'),'p','w9-screen-button')]
        result = ('제목 입력 필요 …','A title is required …') if item['state']=='clipped' else item['result']
        parts += [tr(key+'_result',result,'p','w9-screen-result'),'</div>',
                  caption(),'</figure>']
        return '\n'.join(parts)
    if kind == 'resource-wide-table':
        head = ''.join(tr(f'{key}_h{i}',cell,'th',attrs=' scope="col"') for i,cell in enumerate(item['head']))
        parts = ['<div class="w9-responsive-table"><table class="wd-lesson-table"><thead><tr>'+head+'</tr></thead><tbody>']
        for i,row in enumerate(item['rows']):
            assert len(row)==len(item['head'])
            parts.append('<tr>')
            for j,cell in enumerate(row):
                tag = 'th' if j==0 else 'td'
                scope = ' scope="row"' if j==0 else ''
                parts += [f'<{tag}{scope}>',
                          tr(f'{key}_r{i}_{j}_label',item['head'][j],'span','w9-cell-label',' aria-hidden="true"'),
                          tr(f'{key}_r{i}_{j}',cell,'span'),f'</{tag}>']
            parts.append('</tr>')
        return '\n'.join(parts+['</tbody></table></div>'])
    if kind == 'resource-note':
        return tr(key, item['text'], 'p', 'w9-resource-note')
    if kind == 'resource-flow':
        parts = [f'<figure class="w9-flow" data-steps="{len(item["items"])}"><ol>']
        for i, step in enumerate(item['items']):
            parts += ['<li>', tr(f'{key}_{i}_title', step['title'], 'strong'),
                      tr(f'{key}_{i}_body', step['body']), '</li>']
        parts.append('</ol>')
        if item.get('repeat'):
            parts.append(tr(key+'_repeat', item['repeat'], 'p', 'w9-return'))
        parts += [caption(), '</figure>']
        return '\n'.join(parts)
    if kind == 'resource-sets':
        parts = ['<figure class="w9-sets">']
        for i, level in enumerate(item['levels']):
            parts += ['<div class="w9-set">', tr(f'{key}_{i}_title', level['title'], 'strong'),
                      tr(f'{key}_{i}_body', level['body'])]
        parts += ['</div>'] * len(item['levels'])
        return '\n'.join(parts + [caption(), '</figure>'])
    if kind != 'resource-diagram':
        return None
    width, height = item['size']
    parts = ['<figure class="w9-diagram"><div class="w9-diagram-canvas">',
             f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="{key}_description">',
             tr(key+'_description', item['description'], 'title', attrs=f' id="{key}_description"'),
             f'<defs><marker id="{key}_arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 Z" fill="#47725b"/></marker></defs>']
    for i, frame in enumerate(item.get('frames', [])):
        x,y,w,h = frame['rect']
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="w9-frame"/>')
        parts.append(tr(f'{key}_frame{i}',frame['text'],'text','w9-svg-body',
                        f' x="{x+20}" y="{y+25}"'))
    for edge in item.get('edges', []):
        path = escape(edge['d'], quote=True)
        arrows = f' marker-end="url(#{key}_arrow)"' if edge.get('arrow',True) else ''
        if edge.get('both'):
            arrows += f' marker-start="url(#{key}_arrow)"'
        parts.append(f'<path d="{path}" class="w9-edge"{arrows}/>')
    for i, box in enumerate(item.get('boxes', [])):
        x,y,w,h = box['rect']
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="w9-box"/>')
        title_y = y+h/2+7 if not box.get('body') else y+h/2-6
        parts.append(tr(f'{key}_box{i}', box['title'], 'text', 'w9-svg-title',
                        f' x="{x+w/2}" y="{title_y}" text-anchor="middle"'))
        if box.get('body'):
            parts.append(tr(f'{key}_box{i}_body', box['body'], 'text', 'w9-svg-body',
                            f' x="{x+w/2}" y="{title_y+28}" text-anchor="middle"'))
    for dot in item.get('dots', []):
        parts.append(f'<circle cx="{dot[0]}" cy="{dot[1]}" r="{dot[2]}" class="w9-unit"/>')
    for i,label in enumerate(item.get('labels', [])):
        cls = 'w9-svg-body' if label.get('small') else 'w9-svg-title'
        parts.append(tr(f'{key}_label{i}', label['text'], 'text', cls,
                        f' x="{label["x"]}" y="{label["y"]}" text-anchor="middle"'))
    parts += ['</svg></div>', '<ol class="w9-diagram-mobile">']
    for i, route in enumerate(item['routes']):
        parts.append(tr(f'{key}_route{i}', route, 'li'))
    parts += ['</ol>', caption(), '</figure>']
    return '\n'.join(parts)
