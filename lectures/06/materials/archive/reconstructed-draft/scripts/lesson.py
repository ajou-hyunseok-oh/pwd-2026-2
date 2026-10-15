"""Join reviewed titles and bodies, retaining PDF provenance and prerequisites."""
from urllib.parse import quote
from title_outline import CHAPTERS
from slide_body import BODIES, PRACTICE

WEEK = 6
PAGE_TITLE = ('Node.js와 Express를 이용한 웹 서버 개발', 'Web Server Development with Node.js and Express')
PDF = 'materials/' + quote('[PWD Week4] Node.js Express 프레임워크를 이용한 웹 서버 개발.pdf')
SLIDES = [dict(id='cover', kind='cover', chapter=('', ''), blocks=[], sources=[], source_pages=[1],
               title=('실전 웹서비스개발 – 6주차', 'Practical Web Service Development – Week 6'),
               lead=PAGE_TITLE, cover=dict(variant='weekly', lecture='LECTURE 06',
               eyebrow=('2026학년도 2학기 실전웹서비스개발', 'Practical Web Service Development · Fall 2026')))]
concepts = []
for chapter in CHAPTERS:
    name = tuple(f'CHAPTER {chapter["number"]:02} · {title}' for title in chapter['title'])
    SLIDES.append(dict(id=f'chapter-{chapter["number"]:02}', kind='chapter', chapter=name,
                       title=chapter['title'], lead=chapter['lead'], blocks=[], sources=[], source_pages=[]))
    for outline in chapter['concepts']:
        ident = outline['id']
        concepts.append(ident)
        content = BODIES[ident]
        sources = [('Supplied lecture PDF', PDF + f'#page={page}') for page in outline['source_pages']]
        SLIDES.append(dict(outline, **content, kind='topic', chapter=name, topic_number=len(concepts)))
        SLIDES[-1]['sources'] = sources + content['sources']
assert set(concepts) == set(BODIES), 'Each concept title needs one explicit body'
SLIDES.append(dict(id='practice-week6', kind='topic', chapter=('실습', 'Practice'),
                   title=('실습 · Ajou Campus Foodmap API', 'Lab · Ajou Campus Foodmap API'),
                   lead=('Express·MVCS·테스트·React 연동', 'Express, MVCS, tests, and React integration'),
                   blocks=PRACTICE, layout='practice', source_pages=[26], requires=['concept-frontend-api'],
                   sources=[('Supplied lecture PDF · adapted as an in-class lab', PDF + '#page=26'),
                            ('Executable source and setup', 'examples/README.md')]))
assert len(SLIDES) == 50 and len(concepts) == 43
