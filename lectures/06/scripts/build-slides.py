"""Render original source elements with the Week 05 slide authoring format."""
import argparse
import html
import json
import re
from pathlib import Path
from lesson import SLIDES,SOURCE,PAGES
from translations import TEXT,TITLES,TABLES

ROOT=Path(__file__).resolve().parents[1]
UNITS={u['id']:u for p in SOURCE['pages'] for u in p['units']}
EN={}
for page in SOURCE['pages']:
    translated=TEXT.get(page['number'],[])
    assert len(translated)==len(page['units']),(page['number'],len(translated),len(page['units']))
    EN.update({u['id']:value for u,value in zip(page['units'],translated)})
ASSETS={a['id']:a for p in SOURCE['pages'] for a in p['assets']}
CODES={c['id']:c for p in SOURCE['pages'] for c in p['codes']}
SOURCE_TABLES={t['id']:t for p in SOURCE['pages'] for t in p['tables']}
ALT={
'webservice-diagram':('클라이언트·서버·요청·응답·네트워크·JSON 원본 구조도','Original client, server, request, response, network and JSON diagram'),
'backend-ranking-2025':('Jan-2025 백엔드 프레임워크 비교 그래프','Original Jan-2025 backend framework comparison chart'),
'node-homepage-2025':('Node.js 소개 홈페이지 원본 화면','Original Node.js home page screenshot'),
'nodejs-logo':('Node.js 로고','Node.js logo'),
'rocket-turtle-illustration':('원본의 로켓을 탄 거북이 삽화','Original rocket-riding turtle illustration'),
'http-exchange':('원본 Request·Response 구성 요소 비교','Original Request and Response component comparison'),
'rest-examples':('원본의 잘못된 REST 경로와 올바른 경로 예시','Original incorrect and correct REST path examples'),
'middleware-pipeline':('요청에서 로깅·인증·파싱 미들웨어를 거쳐 라우트 핸들러로 가는 원본 흐름','Original request flow through logging, authentication and parsing middleware to the route handler'),
'mvc-diagram':('사용자·Controller·Model·View·Database 관계를 보여주는 원본 MVC 도식','Original MVC diagram of the user, Controller, Model, View and Database'),
'mvcs-diagram':('Controller와 Model 사이에 Service를 추가하는 원본 MVCS 도식','Original MVCS diagram adding a Service between the Controller and Model'),
'mvcs-tree':('db 폴더를 포함한 원본 MVCS 프로젝트 폴더 구조','Original MVCS project folder structure including the db directory'),
'project-tree':('my-express-app의 src·node_modules·패키지 파일·server.js 구조','Original my-express-app structure with src, node_modules, package files and server.js'),
'express-tree':('pwd-week4 원본 Express MVCS 폴더 구조','Original pwd-week4 Express MVCS folder structure'),
'project-folder-icon':('폴더','Folder'), 'cross-icon':('잘못된 예 표시','Incorrect example marker'), 'check-icon':('올바른 예 표시','Correct example marker'),
'express-logo':('Express 로고','Express logo'), 'render-logo':('Render 로고','Render logo'),
' tdd-cycle':('Red·Green·Refactor를 순환하는 원본 TDD 도식','Original TDD cycle through Red, Green and Refactor'),
}
ALT['tdd-cycle']=ALT.pop(' tdd-cycle')

class Renderer:
    def __init__(self): self.messages={'ko':{},'en':{}}
    def tr(self,key,values,tag='p',cls='',attrs=''):
        for locale,value in zip(('ko','en'),values): self.messages[locale][key]=value
        escaped=html.escape(values[0])
        if tag=='pre':
            # Preserve meaningful source whitespace without trailing spaces in HTML.
            escaped=re.sub(r'(?m)[ \t]+$',lambda m:''.join('&#32;' if c==' ' else '&#9;' for c in m.group()),escaped)
        return f'<{tag}'+(f' class="{cls}"' if cls else '')+f' data-wd-i18n="{key}"{attrs}>'+escaped+f'</{tag}>'
    def unit(self,ident,tag='p',cls=''):
        u=UNITS[ident];key='w6_'+ident.replace('-','_');values=(u['text'],EN[ident])
        attrs=f' data-source-unit="{ident}"'
        if u.get('links'):
            url=u['links'][0]
            pairs=[]
            for value in values:
                match=re.search(r'https?://[^\s)]+',value)
                pairs.append((value[:match.start()],match.group(),value[match.end():]) if match else ('',value,''))
            start=f'<{tag}'+(f' class="{cls}"' if cls else '')+attrs+'>'
            prefix=self.tr(key+'_before',tuple(p[0] for p in pairs),'span') if any(p[0] for p in pairs) else ''
            link=self.tr(key+'_link',tuple(p[1] for p in pairs),'a','wd-source-anchor',f' href="{html.escape(url,quote=True)}" target="_blank" rel="noopener noreferrer" data-source-link="{html.escape(url,quote=True)}"')
            suffix=self.tr(key+'_after',tuple(p[2] for p in pairs),'span') if any(p[2] for p in pairs) else ''
            return start+prefix+link+suffix+f'</{tag}>'
        # Preserve original emphasis while translating each complete text part.
        if tag in ('li','p') and any(r['bold'] for r in u['runs']) and ':' in values[0] and ':' in values[1] and not values[0].startswith('http'):
            pairs=[value.split(':',1) for value in values]
            return f'<{tag}'+(f' class="{cls}"' if cls else '')+attrs+'>'+self.tr(key+'_term',tuple(p[0]+':' for p in pairs),'strong')+self.tr(key+'_detail',tuple(p[1] for p in pairs),'span')+f'</{tag}>'
        return self.tr(key,values,tag,cls,attrs)
    def image(self,ident,cls=''):
        a=ASSETS[ident];key='w6_asset_'+ident.replace('-','_')
        for locale,value in zip(('ko','en'),ALT[ident]):self.messages[locale][key]=value
        return f'<img class="{cls}" src="materials/elements/{a["file"]}" alt="{html.escape(ALT[ident][0],quote=True)}" data-wd-i18n-alt="{key}" data-source-asset="{ident}">'
    def block(self,b):
        kind=b['kind']
        if kind=='stack':return '<div class="wd-lesson-stack '+b['cls']+'">'+''.join(self.block(c) for c in b['children'])+'</div>'
        if kind=='paragraph':return self.unit(b['unit'],'p',b['cls'])
        if kind=='list':return '<ul class="wd-source-list">'+''.join(self.unit(i,'li') for i in b['items'])+'</ul>'
        if kind=='concepts':return '<dl class="wd-lesson-concepts"><div><dt>'+self.unit(b['head'],'strong')+'</dt><dd><ul>'+''.join(self.unit(i,'li','wd-source-subpoint' if UNITS[i]['bullet']=='○' else '') for i in b['items'])+'</ul></dd></div></dl>'
        if kind=='image':
            picture=self.image(b['asset'])
            if 'icon' not in b['asset'] and 'logo' not in b['asset']:
                picture='<a class="wd-source-zoom" href="materials/elements/'+ASSETS[b['asset']]['file']+'" target="_blank" rel="noopener noreferrer">'+picture+'</a>'
            return '<figure class="wd-lesson-figure '+b['cls']+'">'+picture+(self.unit(b['caption'],'figcaption') if b['caption'] else '')+'</figure>'
        if kind=='code':
            c=CODES[b['code']];key='w6_code_'+c['id'].replace('-','_')
            label=''
            if b['label']:
                label='<div class="wd-source-code-heading">'+(self.image(b['icon'],'wd-source-icon') if b.get('icon') else '')+self.unit(b['label'],'p','wd-lesson-code-label')+'</div>'
            return label+self.tr(key,(c['code'],c['code']),'pre','wd-code',f' data-wd-code="{c["language"]}" data-wd-preserve-code data-source-code="{c["id"]}"')
        if kind=='table':
            t=SOURCE_TABLES[b['table']];translated=TABLES[t['page']]
            assert len(t['rows'])==len(translated)
            result=f'<table class="wd-lesson-table" data-source-table="{t["id"]}"><thead>'
            for ri,row in enumerate(t['rows']):
                if ri==1:result+='</thead><tbody>'
                result+='<tr>'
                for ci,value in enumerate(row):result+=self.tr(f'w6_table_{t["page"]}_{ri}_{ci}',(value,translated[ri][ci]),'th' if ri==0 or ci==0 else 'td')
                result+='</tr>'
            return result+'</tbody></table>'
        if kind=='status':
            return self.unit(b['label'],'p','wd-source-heading')+'<table class="wd-lesson-table wd-status-table"><thead><tr>'+''.join(self.unit(i,'th') for i in b['heads'])+'</tr></thead><tbody><tr>'+''.join('<td>'+''.join(self.unit(i,'p') for i in column)+'</td>' for column in b['columns'])+'</tr></tbody></table>'
        if kind=='practice':
            from lesson import D, L, ids
            deadline_label='<div class="wd-practice-deadline__label">'+self.unit(ids(26,12)[0],'span')+self.tr('w6_practice_source_date',('원본 자료 표기','Original source date'),'small')+'</div>'
            return '<div class="wd-practice-grid"><div class="wd-practice-main">'+self.block(D(26,2,3,4,5,6))+self.block(D(26,7,8,9,10,11))+'</div><div class="wd-practice-side"><div class="wd-practice-submission"><div class="wd-practice-deadline">'+deadline_label+self.unit(ids(26,13)[0],'strong')+'</div><div class="wd-practice-deliverables">'+''.join(self.block(D(26,h,d)) for h,d in [(14,15),(16,17),(18,19)])+'</div></div></div></div>'
        raise ValueError(kind)

def outputs(titles_only=False):
    files={}
    for preview in ([True] if titles_only else [False,True]):
        r=Renderer();sections=[]
        for index,s in enumerate(SLIDES):
            n=s['source_page'];kind=s['kind'];classes='wd-lesson-cover' if kind=='cover' else 'wd-lesson-chapter' if kind=='chapter' else 'wd-slide--content'
            attrs=' data-wd-cover="weekly"' if kind=='cover' else ''
            parts=[f'<section class="wd-slide wd-lesson-slide {classes}'+(' is-active' if index==0 else '')+f'" data-wd-slide="{s["id"]}" data-source-page="{n}"{attrs} role="region">']
            if kind=='cover':
                parts+=['<div class="wd-lesson-cover__content">',r.tr('w6_cover_eyebrow',('2026학년도 2학기 실전웹서비스개발','Practical Web Service Development · Fall 2026'),'p','wd-lesson-cover__eyebrow'),r.tr('w6_cover_title',('실전 웹서비스개발 – 6주차',TITLES[1]),'h1','wd-lesson-title'),r.unit('p01-u01','p','wd-lesson-cover__subtitle'),'</div>','<p class="wd-lesson-source">LECTURE 06</p>']
            else:
                if kind=='chapter':parts.append(r.tr(f'w6_chapter_{n}',(str({3:1,9:2,21:3,27:4}[n]).zfill(2),)*2,'p','wd-lesson-eyebrow') if n!=27 else '')
                parts.append(r.tr(f'w6_title_{n}',(s['title'],TITLES[n]),'h2','wd-slide-heading'))
                if s['lead'] and not preview:parts.append(r.unit(s['lead'],'p','wd-slide-lead'))
                if not preview and s['blocks']:
                    parts.append('<div class="wd-lesson-body wd-lesson-body--'+s['layout']+'">'+''.join('<div class="wd-lesson-block">'+r.block(b)+'</div>' for b in s['blocks'])+'</div>')
            parts.append('<aside hidden class="wd-lesson-notes">'+html.escape(f'[Source]\n{SOURCE["source"]}#page={n}\n[/Source]')+'</aside></section>')
            sections.append('\n'.join(parts))
        name,content=('titles','titles-content.js') if preview else ('index','lecture-content.js')
        title='06 | Node.js Express 프레임워크를 이용한 웹 서버 개발'+(' · 제목 목록' if preview else '')
        r.messages['ko']['page_title']=title;r.messages['en']['page_title']='06 | Web Server Development Using the Node.js Express Framework'+(' · Title Outline' if preview else '')
        files[content]='window.LECTURE_CONTENT = '+json.dumps(r.messages,ensure_ascii=False,indent=2)+';\n'
        files[name+'.html']='''<!doctype html>
<html class="wd-page" lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="data:,">
<title data-wd-i18n="page_title">'''+html.escape(title)+'''</title>
<link rel="stylesheet" href="../../packages/web-deck/web-deck.css">
<link rel="stylesheet" href="../../packages/web-deck/authoring.css">
<link rel="stylesheet" href="lecture.css">
</head>
<body class="wd-page-body" data-lecture="06">
<main class="wd-deck" data-web-deck data-wd-authoring="v1" data-wd-format="week-05" data-wd-source-elements="materials/elements/manifest.json"><div class="wd-viewport" data-wd-viewport><div class="wd-stage" data-wd-stage>
'''+ '\n\n'.join(sections)+'''
</div></div></main>
<script src="'''+content+'''"></script>
<script src="../shared/lecture-deck.js"></script>
<script src="../../packages/web-deck/vendor/prism/prism.js" data-manual></script>
<script src="../../packages/web-deck/web-deck.js"></script>
</body></html>
'''
    rows=[dict(number=i+1,id=s['id'],title='실전 웹서비스개발 – 6주차' if s['kind']=='cover' else s['title'],kind=s['kind'],source_pages=[s['source_page']],layout=s['layout']) for i,s in enumerate(SLIDES)]
    if not titles_only:files['materials/slide-map.json']=json.dumps(rows,ensure_ascii=False,indent=2)+'\n'
    files['materials/title-outline.json']=json.dumps(dict(format='week-05',content_source=SOURCE['source'],total_slides=len(SLIDES),slides=rows),ensure_ascii=False,indent=2)+'\n'
    files['materials/week-06-titles.ko.txt']='\n'.join(f'{s["number"]:02}. {s["title"]}' for s in rows)+'\n'
    return files

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--titles-only',action='store_true');args=parser.parse_args();stale=[]
    for name,value in outputs(args.titles_only).items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=value:stale.append(name)
        else:path.write_text(value)
    if stale:raise SystemExit('Stale generated files: '+', '.join(stale))
    print(f'Week 06: {len(SLIDES)} slides; Week 05 format / original PDF content '+('checked' if args.check else 'built'))
if __name__=='__main__':main()
