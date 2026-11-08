"""Editable bilingual scaffold. No lecture or practice content authored yet.

Replace bracketed fields; duplicate slides with unique IDs when content is ready.
Block formats: lectures/authoring/scaffolds.md.
"""

WEEK = 9
SUBTITLE = ('8주차 실습 리뷰 · 초안', 'Week 8 Practice Review Draft')
SLIDES = [
    dict(id='chapter-01', kind='chapter',
         title=('[단원 제목]', '[Chapter Title]'),
         lead=('[단원 범위]', '[Chapter Scope]')),
    dict(id='topic-01', kind='content',
         title=('[슬라이드 제목]', '[Slide Title]'),
         lead=('[설명 범위]', '[Explanation Scope]'),
         layout='split',
         columns=[
             [dict(kind='concepts', items=[
                 dict(term=('[개념] - [짧은 정의]', '[Concept] - [Short Definition]'),
                      details=[('[세부 설명]', '[Supporting Detail]'),
                               ('[조건 · 예시]', '[Condition · Example]')]),
             ])],
             [dict(kind='placeholder',
                   label=('[코드 · 표 · 도식 · 실행 화면]', '[Code · Table · Diagram · Screen]'))],
         ],
         sources=[],
         note=''),
]
