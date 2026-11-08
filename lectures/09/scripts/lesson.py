"""Week 9: complete bilingual explanations and resources for 76 concepts."""
from chapters import WEEK, SUBTITLE, CHAPTER_SLIDES
from title_outline import proposal
from reused_resources import RESOURCES
from new_resources import RESOURCES as NEW_RESOURCES
from slide_body import BODY, compose

assert not RESOURCES.keys() & NEW_RESOURCES.keys()

SLIDES = []
for chapter in proposal()['chapters']:
    SLIDES.append(CHAPTER_SLIDES[chapter['number']-1])
    for item in chapter['concepts']:
        media = RESOURCES.get(item['id']) or NEW_RESOURCES.get(item['id'])
        assert media, item['id']
        slide = dict(id=item['id'],kind='content',title=item['title'],lead=item['lead'],
                     **compose(item['id'],media))
        # Sources belong only in materials/slide-references.*; no hidden notes.
        SLIDES.append(slide)
assert len(SLIDES)==84
assert {s['id'] for s in SLIDES if s['kind']=='content'}==BODY.keys()
