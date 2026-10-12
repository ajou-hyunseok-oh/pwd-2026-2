"""Lecture 05: reviewed React imports and 35 single-concept bodies and the original ecosystem appendix."""
from react_import import load_react_deck
from title_outline import load_title_slides
from slide_body import BODIES

WEEK = 5
cover = dict(
    id='cover', chapter=('', ''), kind='cover', topic_number=None, blocks=[], sources=[],
    title=(f'실전 웹서비스개발 – {WEEK}주차', f'Practical Web Service Development – Week {WEEK}'),
    lead=('React Framework의 이해', 'Understanding the React Framework'),
    cover=dict(variant='weekly',
               eyebrow=('2026학년도 2학기 실전웹서비스개발', 'Practical Web Service Development · Fall 2026'),
               lecture=f'LECTURE {WEEK:02}'))
SLIDES = load_title_slides([cover, *load_react_deck()])
concept_ids = [slide['id'] for slide in SLIDES if slide['id'].startswith('concept-')]
assert set(concept_ids) == BODIES.keys(), 'Each approved concept needs exactly one body'
for number, ident in enumerate(concept_ids, 1):
    slide = next(slide for slide in SLIDES if slide['id'] == ident)
    body = BODIES[ident]
    slide.update(blocks=body['blocks'], layout=body['layout'], topic_number=number)
    slide['sources'] = list(dict.fromkeys(tuple(source) for source in slide['sources'] + body['sources']))
    assert slide['blocks'], f'{ident}: missing body'
assert len(SLIDES) == 65 and len(concept_ids) == 35
assert sum('import_html' in slide for slide in SLIDES) == 24

# The user requested the original PDF slide verbatim, including its layout.
appendix = next(slide for slide in SLIDES if slide['id'] == 'appendix-react-ecosystem')
appendix.update(source_image='materials/images/react-ecosystem-original.png',
                sources=[('Original lecture PDF (page 18)',
                    'materials/%5BPWD%20Week%203%5D%20React%20프레임워크를%20이용한%20웹%20프론트엔드%20개발.pdf#page=18')])

# Only the right-hand package.json is updated; the PDF artwork stays intact.
from pathlib import Path
appendix['source_code_overlay'] = (Path(__file__).resolve().parents[1] /
    'materials/react-ecosystem-right-package.json').read_text()
appendix['sources'].append(('npm latest versions checked 2026-10-12',
    'materials/ecosystem-right-versions-2026.json'))

from practice_guide import PRACTICE
practice = next(slide for slide in SLIDES if slide['id'] == 'practice-week5')
practice.update(blocks=PRACTICE, layout='single', sources=[
    ('Lab README', 'https://github.com/ajou-hyunseok-oh/pwd-week5#readme'),
    ('Week 4 submission format', '../04/ai-design.html#/19')])
