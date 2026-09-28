"""Native HTML illustrations of planning artifacts, with bilingual text bindings."""

def render_design_block(block, ident, tr):
    kind=block['type']
    def t(ko, en, suffix, tag='span', cls=''):
        return tr([ko,en],ident+'_'+suffix,tag,f'class="{cls}"' if cls else '')
    if kind=='design_concepts':
        html='<dl class="design-concepts">'
        for i,section in enumerate(block['sections']):
            html+='<div class="design-concept"><dt>'+tr(section['definition'],f'{ident}_definition{i}','strong')+'</dt>'
            if section['details']:
                html+='<dd><ul class="design-details">'
                for j,detail in enumerate(section['details']):
                    html+=tr(detail,f'{ident}_detail{i}_{j}','li')
                html+='</ul></dd>'
            html+='</div>'
        return html+'</dl>'
    if kind=='design_sequences':
        html='<dl class="design-sequences">'
        for i,section in enumerate(block['sections']):
            html+='<div>'+tr(section['role'],f'{ident}_role{i}','dt')+tr(section['flow'],f'{ident}_flow{i}','dd')+'</div>'
        return html+'</dl>'
    if kind=='design_flow':
        html='<div class="design-flow">'
        for i,lane in enumerate(block['lanes']):
            html+='<div class="design-flow-lane">'+tr(lane[0],f'{ident}_role{i}','strong','class="design-flow-role"')+'<ol class="design-flow-steps">'
            for j,step in enumerate(lane[1:]):
                html+=tr(step,f'{ident}_step{i}_{j}','li')
            html+='</ol></div>'
        return html+'</div>'
    if kind=='design_process':
        html='<ol class="design-process">'
        for i,(label,text) in enumerate(block['steps']):
            html+='<li>'+tr(label,f'{ident}_label{i}','h3')+tr(text,f'{ident}_text{i}','p')+'</li>'
        return html+'</ol>'
    if kind=='design_submission':
        html='<section class="design-submission">'
        html+='<div class="design-submission-deadline">'+tr(block['deadline_label'],f'{ident}_deadline_label','span')+tr(block['deadline'],f'{ident}_deadline','strong')+'</div>'
        html+='<div class="design-submission-grid"><div class="design-submission-items">'+tr(block['items_label'],f'{ident}_items_label','h4')+'<ul>'
        for i,item in enumerate(block['items']):
            html+=tr(item,f'{ident}_item{i}','li')
        html+='</ul></div><div class="design-submission-places">'+tr(block['places_label'],f'{ident}_places_label','h4')+'<dl>'
        for i,(place,detail) in enumerate(block['places']):
            html+='<div>'+tr(place,f'{ident}_place{i}','dt')+tr(detail,f'{ident}_place_detail{i}','dd')+'</div>'
        return html+'</dl></div></div></section>'
    if kind=='design_wire':
        html='<div class="design-wire">'
        if block['mode']=='application':
            html+=t('UGC Creator Hub · 전시 신청','UGC Creator Hub · Exhibition Application','top','div','design-wire-top')
            for i,(ko,en,value,ev) in enumerate([
                ('아이템 링크','Item Link','Roblox 아이템 URL','Roblox item URL'),
                ('아이템명','Item Name','제작한 아이템의 이름','Name of the created item'),
                ('태그 · 테마','Tags and Theme','의상 · 액세서리 · 테마','Clothing · Accessories · Theme')]):
                html+='<div class="design-wire-field">'+t(ko,en,f'label{i}','strong')+t(value,ev,f'value{i}','div','design-wire-input')+'</div>'
            html+=t('전시 신청','Apply for Exhibition','action','div','design-wire-action')
            html+=t('신청 완료 → 승인 대기 상태 확인','Application sent → Pending review','result','div','design-wire-status')
        else:
            html+=t('마이페이지 · 내 아이템','My Page · My Items','top','div','design-wire-top')
            html+='<div class="design-wire-item">'+t('아이템 A','Item A','itema','strong')+t('전시 승인 · 전시 중','Approved · On Display','statea','span')+'</div>'
            html+='<div class="design-wire-item">'+t('아이템 B','Item B','itemb','strong')+t('반려 · 테마 정보 보완','Rejected · Add Theme Information','stateb','span')+'</div>'
            html+=t('수정 후 재신청','Revise and Reapply','action','div','design-wire-action')
            html+='<div class="design-wire-balance">'+t('포인트 내역','Point History','balance_label','strong')+t('1,200 P','1,200 P','balance_value','span')+'</div>'
            html+=t('판매 · 정산 내역 확인','View Sales and Settlements','result','div','design-wire-status')
        return html+'</div>'
    if kind=='design_onepager':
        html='<article class="design-onepager">'
        html+='<header>'+t('NNN UGC Creator Hub','NNN UGC Creator Hub','name','h3')+t('Create. Exhibit. Earn.','Create. Exhibit. Earn.','slogan','p')+'</header>'
        html+='<div class="design-onepager-grid">'
        rows=[
            ('문제 · 대상 사용자','Problem · Target Users','UGC 제작자의 전시 · 홍보 기회 부족\n구매자의 적합한 아이템 탐색 부담','Limited creator exposure and promotion\nEffort for buyers to find suitable items','problem'),
            ('해결방안','Solution','큐레이션 피드와 Outfit 월드 전시를 통한\n제작자와 구매자의 연결','Connect creators and buyers through\na curated feed and Outfit exhibitions','solution'),
            ('주요 기능','Key Features','아이템 등록 · 전시 신청 · 승인 · 큐레이션 탐색','Item registration · Exhibition applications and review · Curated discovery','features'),
            ('기술 구조','Technology','React + Vite - 화면 구성\nSupabase - 인증 · DB\nVercel - 배포','React + Vite - UI\nSupabase - Authentication · DB\nVercel - Deployment','technology'),
            ('기대효과 · KPI','Impact · KPIs','아이템 발견성과 판매 기회 향상\n전시 아이템 조회 · 구매 전환','Better item discovery and sales opportunities\nExhibited item views · Purchase conversion','impact'),
            ('핵심 사용 흐름','Core User Flow','제작자 - 등록 → 전시 신청 → 승인 · 전시 → 수익 확인','Creator - Register → Apply → Approval and exhibition → Review earnings','flow'),
        ]
        for i,(ko,en,value,ev,cls) in enumerate(rows):
            html+=f'<section class="design-onepager-{cls}">'+t(ko,en,f'label{i}','h4')+t(value,ev,f'text{i}','p')+'</section>'
        return html+'</div></article>'
    raise ValueError(kind)
