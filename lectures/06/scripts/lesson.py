"""Explicit per-source-slide compositions using the established Week 05 format."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=json.loads((ROOT/'materials/elements/manifest.json').read_text())
PAGES={p['number']:p for p in SOURCE['pages']}

def ids(page, *numbers):
    return [f'p{page:02}-u{n:02}' for n in numbers]

def D(page, head, *items):
    return dict(kind='concepts',head=ids(page,head)[0],items=ids(page,*items))

def L(page,*items):
    return dict(kind='list',items=ids(page,*items))

def P(page,number,cls=''):
    return dict(kind='paragraph',unit=ids(page,number)[0],cls=cls)

def F(ident,caption=None,cls=''):
    return dict(kind='image',asset=ident,caption=caption,cls=cls)

def K(ident,label=None,icon=None):
    return dict(kind='code',code=ident,label=label,icon=icon)

def G(*children,cls=''):
    return dict(kind='stack',children=list(children),cls=cls)

def T(page):
    return dict(kind='table',table=f'table-{page:02}')

def slide(page,*blocks,layout='split',lead=None,kind='content'):
    return dict(id='cover' if page==1 else f'pdf-{page:02}',source_page=page,title=PAGES[page]['title'],
                kind=kind,blocks=list(blocks),layout=layout,lead=lead)

SLIDES=[
 slide(1,kind='cover'),
 slide(2,L(2,1,2,3,4,5),layout='single'),
 slide(3,kind='chapter'),
 slide(4,G(D(4,1,2,3),L(4,4),D(4,5,6,7),D(4,8,9)),F('webservice-diagram'),layout='webservice'),
 slide(5,G(D(5,1,2),D(5,3,4),D(5,5,6),D(5,7,8),D(5,9,10)),layout='roles'),
 slide(6,T(6),G(D(6,1,2,3,4,5,6,7)),F('backend-ranking-2025',ids(6,8)[0]),layout='comparison'),
 slide(7,G(D(7,1,2,3),P(7,4,'wd-source-heading'),G(D(7,5,6,7),D(7,8,9,10,11),D(7,12,13,14),D(7,15,16,17),cls='node-features')),F('node-homepage-2025'),layout='node-intro'),
 slide(8,G(L(8,1,2,3),D(8,4,5,6,7,8,9,10),D(8,11,12,13)),G(F('rocket-turtle-illustration'),F('nodejs-logo')),layout='engine'),
 slide(9,kind='chapter'),
 slide(10,G(D(10,1,2,3,4,5),D(10,6,7,8,9),D(10,10,11,12)),F('http-exchange'),layout='http'),
 slide(11,K('http-request'),T(11),layout='request'),
 slide(12,K('http-response'),dict(kind='status',label=ids(12,1)[0],heads=ids(12,2,5,8),columns=[ids(12,3,4),ids(12,6,7),ids(12,9,10)]),layout='response'),
 slide(13,G(D(13,1,2,3,4),D(13,5,6,7,8,9)),G(K('json-object'),K('json-transform',ids(13,11)[0])),P(13,10,'wd-source-link'),layout='json'),
 slide(14,G(D(14,1,2,3),D(14,4,5,6,7)),G(D(14,8,9,10),D(14,11,12,13,14,15),F('rest-examples')),layout='rest'),
 slide(15,G(L(15,1,2,3),D(15,4,5,6,7,8,9)),T(15),layout='routing'),
 slide(16,D(16,2,3,4,5,6,7,8),K('middleware-code'),F('middleware-pipeline'),layout='middleware',lead=ids(16,1)[0]),
 slide(17,G(D(17,1,2),D(17,3,4),D(17,5,6),D(17,7,8,9,10),D(17,11,12,13)),F('mvc-diagram'),layout='mvc'),
 slide(18,G(D(18,1,2),D(18,3,4,5,6,7)),F('mvcs-diagram',ids(18,8)[0]),layout='mvcs'),
 slide(19,F('mvcs-tree',ids(19,1)[0]),layout='tree'),
 slide(20,G(D(20,1,2),D(20,3,4,5,6,7,8),D(20,9,10,11,12)),F('tdd-cycle'),layout='tdd'),
 slide(21,kind='chapter'),
 slide(22,L(22,1,2,3,4,5),F('express-logo'),K('node-http',ids(22,6)[0],icon='cross-icon'),K('express-http',ids(22,7)[0],icon='check-icon'),layout='express'),
 slide(23,K('install-express'),F('project-tree'),K('hello-world',ids(23,1)[0]),layout='project'),
 slide(24,G(G(F('project-folder-icon',cls='inline-folder'),P(24,1,'wd-source-heading'),cls='folder-heading'),L(24,2,3,4,5,6,7,8,9,10)),F('express-tree'),layout='project-roles'),
 slide(25,G(L(25,2),D(25,3,4,5,6,7,8),D(25,9,10,11)),F('render-logo'),layout='render',lead=ids(25,1)[0]),
 slide(26,dict(kind='practice'),layout='single',lead=ids(26,1)[0]),
 slide(27,kind='chapter'),
]
assert [s['source_page'] for s in SLIDES]==list(range(1,SOURCE['page_count']+1))
