"""Render bilingual lesson blocks into the repository's native web deck."""
from html import escape
from design_blocks import render_design_block

def render_body(slide, key, messages, sources):
    def tr(value, suffix, tag='span', attrs=''):
        ident=f'{key}_{suffix}'
        for i,locale in enumerate(('ko','en')): messages[locale][ident]=value[i]
        return f'<{tag} {attrs} data-wd-i18n="{ident}">{escape(value[0])}</{tag}>'
    def concepts(sections, ident, compact=False):
        content='<dl class="react-concepts'+(' react-concepts--caption' if compact else '')+'">'
        for i,section in enumerate(sections):
            content+='<div class="react-concept"><dt>'+tr(section['definition'],f'{ident}_definition{i}','strong')+'</dt>'
            if section['details']:
                content+='<dd><ul class="react-concept-details">'
                content+=''.join(tr(x,f'{ident}_detail{i}_{j}','li') for j,x in enumerate(section['details']))
                content+='</ul></dd>'
            content+='</div>'
        return content+'</dl>'
    blocks=[]
    for n,b in enumerate(slide.get('blocks',[])):
        ident=f'b{n}'
        heading=tr(b['title'],ident+'_heading','h3') if 'title' in b else ''
        kind=b['type']
        if kind.startswith('design_'):
            content=render_design_block(b,ident,tr)
        elif kind=='points':
            content='<ul class="week4-points">'+''.join(tr(x,f'{ident}_item{i}','li') for i,x in enumerate(b['items']))+'</ul>'
        elif kind=='table':
            widths='; --design-columns: '+escape(b['widths']) if 'widths' in b else ''
            content=f'<div role="table" class="week4-table" style="--table-columns: {len(b["heads"])}{widths}"><div role="row" class="week4-table__header">'+''.join(tr(x,f'{ident}_head{i}','div','role="columnheader"') for i,x in enumerate(b['heads']))+'</div>'
            for r,row in enumerate(b['rows']):
                content+='<div role="row">'+''.join(tr(x,f'{ident}_cell{r}_{c}','div','role="rowheader"' if c==0 else 'role="cell"') for c,x in enumerate(row))+'</div>'
            content+='</div>'
        elif kind=='quote':
            content=tr(b['text'],ident+'_text','blockquote','class="week4-quote"')
        elif kind=='code':
            content=tr(b['text'],ident+'_code','pre',f'class="wd-code" data-wd-code="{b["language"]}" data-wd-code-width="{b.get("width",80)}"')
            if 'caption' in b: content+=tr(b['caption'],ident+'_caption','p','class="react-code-caption"')
            if 'explanation' in b: content+=concepts(b['explanation'],ident+'_explanation',compact=True)
        elif kind=='concepts':
            content=concepts(b['sections'],ident)
        elif kind=='update_flow':
            content='<ol class="react-update-flow">'
            for j,(name,detail) in enumerate(b['steps']):
                content+='<li>'+tr(name,f'{ident}_name{j}','strong')+tr(detail,f'{ident}_detail{j}','span')+'</li>'
            content+='</ol>'
        elif kind=='role_diagram':
            content='<div class="react-role-diagram">'
            content+='<div class="react-role-diagram__server">'+tr(b['server'],ident+'_server','h4')+tr(b['server_role'],ident+'_server_role','p')+'</div>'
            content+='<div class="react-role-diagram__exchange"><span aria-hidden="true">↔</span>'+tr(b['exchange'],ident+'_exchange','span')+'</div>'
            content+='<div class="react-role-diagram__browser">'+tr(b['browser'],ident+'_browser','h4')+'<div class="react-role-diagram__browser-flow">'
            content+='<div class="react-role-diagram__react">'+tr(b['react'],ident+'_react','h5')+tr(b['react_role'],ident+'_react_role','p')+'</div>'
            content+='<span class="react-role-diagram__arrow" aria-hidden="true">→</span>'
            content+='<div class="react-role-diagram__display">'+tr(b['display'],ident+'_display','h5')+tr(b['display_role'],ident+'_display_role','p')+'</div>'
            content+='</div></div></div>'
        elif kind=='explain':
            content='<dl class="react-explanation">'
            for j,section in enumerate(b['sections']):
                content+=tr(section['title'],f'{ident}_term{j}','dt')
                content+=tr(section['text'],f'{ident}_description{j}','dd')
            content+='</dl>'
        elif kind=='figure':
            altkey=f'{key}_{ident}_alt'
            for i,locale in enumerate(('ko','en')): messages[locale][altkey]=b['alt'][i]
            content=f'<figure class="react-figure"><img src="{escape(b["src"])}" alt="{escape(b["alt"][0])}" data-react-alt="{altkey}" loading="eager">'
            content+=tr(b['caption'],ident+'_caption','figcaption')+'</figure>'
        elif kind=='demo':
            content=f'<div class="react-demo" data-react-demo="{escape(b["mode"])}"></div>'
        elif kind=='services':
            content='<ul class="react-service-grid">'
            for j,service in enumerate(b['items']):
                labelkey=f'{key}_{ident}_service{j}_label'
                for i,locale in enumerate(('ko','en')):
                    messages[locale][labelkey]=service['name'][i]+(' 사이트 열기 (새 탭)' if locale=='ko' else ' website (opens in a new tab)')
                content+=f'<li><a class="react-service-link" href="{escape(service["url"])}" target="_blank" rel="noopener noreferrer" aria-label="{escape(messages["ko"][labelkey])}" data-wd-i18n-aria-label="{labelkey}">'
                content+=f'<img class="react-service-icon" src="{escape(service["icon"])}" alt="" width="88" height="88" loading="eager">'
                content+=tr(service['name'],f'{ident}_service{j}_name','span','class="react-service-name"')
                content+=f'<span class="react-service-domain">{escape(service["domain"])} <span aria-hidden="true">↗</span></span></a></li>'
            content+='</ul>'
        elif kind=='wireframe':
            heading=tr(['모집 상세 · 화면 구상','Group Details · Wireframe'],ident+'_heading','h3')
            content='<div class="week4-wire">'
            for j,(ko,en) in enumerate([
                ('React 함께 공부하기','Study React Together'),
                ('수요일 18:00–19:00 · 도서관','Wednesday 18:00–19:00 · Library'),
                ('모집 중 · 잔여 2명 / 정원 6명','Open · 2 places left / 6 total'),
                ('주 1회 개념 정리와 짧은 예제 공유','Weekly concept review and short examples'),
                ('참여 신청','Apply'),
                ('성공 → 내 신청에서 확정 내역 확인','Success → Confirmation in My applications')]):
                content+=tr([ko,en],f'{ident}_wire{j}','p',f'class="week4-wire__row week4-wire__row--{j}"')
            content+='</div>'
        elif kind=='sources':
            content='<dl class="week4-sources">'
            for code,values in sources.items():
                title,url,date,*rest=values
                content+=f'<dt><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{escape(title)}</a></dt>'
                content+=tr([date+' · '+rest[0] if rest else date,date],f'{ident}_{code}','dd')
            content+='</dl>'
        else: raise ValueError(kind)
        blocks.append(f'<div class="week4-panel week4-panel--{kind}">{heading}{content}</div>')
    if not blocks: return ''
    layout='split' if any(b['type']=='wireframe' for b in slide['blocks']) else slide.get('layout','stack')
    body=f'<div class="week4-body week4-body--{layout}">'+''.join(blocks)+'</div>'
    refs=slide.get('refs',[])
    asset_sources=[item['icon_source'] for block in slide.get('blocks',[]) if block['type']=='services' for item in block['items']]
    note=slide.get('note','')+'\n[Sources]\n'+'\n'.join([sources[r][1] for r in refs+slide.get('note_refs',[])]+asset_sources)+'\n[/Sources]'
    body+='<aside hidden class="week4-notes">'+escape(note)+'</aside>'
    return body
