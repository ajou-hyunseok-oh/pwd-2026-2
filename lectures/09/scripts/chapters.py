"""Week 9's cover and chapter headings.

Periods describe major developments, not the invention dates of every technique.
Block formats: lectures/authoring/scaffolds.md.
"""

WEEK = 9
SUBTITLE = ('인공지능의 발전과 에이전트를 활용한 소프트웨어 개발',
            'The Evolution of AI and Software Development with Agents')
CHAPTER_SLIDES = [
    dict(id='chapter-01', kind='chapter',
         title=('인공지능 연구의 출발', 'The Beginnings of AI Research'),
         lead=('1950~1970년대 · 기계 지능의 평가와 규칙·신경망을 이용한 초기 구현',
               '1950s–1970s · Evaluating machine intelligence and early approaches using rules and neural networks')),
    dict(id='chapter-02', kind='chapter',
         title=('데이터 학습과 신경망', 'Data-Driven Learning and Neural Networks'),
         lead=('1980년대~2016년 · 모델을 학습시키는 방법과 이미지 분류·바둑 적용 사례',
               '1980s–2016 · How models learn, with examples from image classification and Go')),
    dict(id='chapter-03', kind='chapter',
         title=('대규모 언어 모델의 학습과 생성', 'Training and Generation in Large Language Models'),
         lead=('2017~2020년 · 텍스트의 표현부터 Transformer의 사전 학습과 생성까지',
               '2017–2020 · From representing text to pretraining Transformers and generating output')),
    dict(id='chapter-04', kind='chapter',
         title=('코드 생성과 대화형 개발 지원', 'Code Generation and Conversational Assistance'),
         lead=('2021~2023년 · 코드 자동 완성에서 자연어 요청과 실행 결과를 통한 수정으로',
               '2021–2023 · From code completion to requesting and revising code in conversation')),
    dict(id='chapter-05', kind='chapter',
         title=('AI 에이전트의 도구 사용', 'Tool Use in AI Agents'),
         lead=('2022~2024년 · 도구를 호출하고 실행 결과를 바탕으로 다음 행동을 결정하는 구조',
               '2022–2024 · Calling tools and using their results to decide what to do next')),
    dict(id='chapter-06', kind='chapter',
         title=('에이전트의 프로젝트 맥락 관리', 'Managing Project Context for Agents'),
         lead=('2025년 · 저장소 정보와 작업 지침을 선별하고 진행 상태를 이어가는 방법',
               '2025 · Selecting repository context and instructions and carrying work state forward')),
    dict(id='chapter-07', kind='chapter',
         title=('명세에 따른 구현과 검증', 'Specification-Driven Implementation and Verification'),
         lead=('2025년 후반~2026년 · 명세를 작업으로 나누고 실행 결과로 완료 여부를 판단하는 과정',
               'Late 2025–2026 · Breaking specifications into tasks and using evidence to judge completion')),
    dict(id='chapter-08', kind='chapter',
         title=('병렬 개발과 장기 작업 관리', 'Parallel Development and Long-Running Work'),
         lead=('2026년 · 분리한 변경을 통합하고 여러 실행에 걸쳐 목표와 진행 상태를 관리',
               '2026 · Integrating separate changes and managing goals and progress across runs')),
]
