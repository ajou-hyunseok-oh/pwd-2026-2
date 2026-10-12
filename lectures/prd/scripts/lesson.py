"""One-slide PRD overview: expansion, writing checklist, official references."""

SLIDES = [{
    'id': 'prd-overview',
    'kind': 'content',
    'title': ('PRD · 제품 요구사항 문서', 'PRD · Product Requirements Document'),
    'lead': ('Product Requirements Document', 'A concise guide to writing product requirements'),
    'definition': (
        'PRD - 제품의 목적·범위·요구사항·완료 기준을 합의하는 문서',
        'PRD - A shared agreement on product purpose, scope, requirements, and completion criteria'),
    'table_title': ('작성 항목 요약', 'What to include'),
    'head': [('항목', 'Section'), ('작성할 내용', 'What to write')],
    'rows': [
        [('문제·배경', 'Problem & context'), ('해결할 불편, 발생 상황과 근거', 'User pain, context, and supporting evidence')],
        [('대상 사용자', 'Target users'), ('누가 어떤 상황에서 무엇을 하려는지', 'Who the users are and what they need to do')],
        [('목표·성공 지표', 'Goals & metrics'), ('기대 결과, 측정 방법과 목표값', 'Desired outcomes, measures, and targets')],
        [('범위·비목표', 'Scope & non-goals'), ('이번 버전의 포함·제외 항목과 우선순위', 'What is in or out, with priorities')],
        [('기능·사용자 흐름', 'Features & flows'), ('주요 행동, 입력·처리·결과와 예외', 'User actions, inputs, outcomes, and exceptions')],
        [('인수 기준·품질 조건', 'Acceptance & quality'), ('완료 판정 조건, 성능·보안·접근성 기준', 'Observable completion and quality criteria')],
        [('가정·미결정 사항', 'Assumptions & TBD'), ('확인할 질문, 외부 의존성과 담당자', 'Open questions, dependencies, and owners')],
    ],
    'references_title': ('공식 작성 레퍼런스', 'Official writing references'),
    'references': [
        {'source': 'openai-prd', 'label': ('OpenAI · PRD 작성 사례', 'OpenAI · Draft PRDs'),
         'purpose': ('근거 자료로 PRD 초안 작성', 'Draft a PRD from source materials')},
        {'source': 'claude-prd', 'label': ('Claude Academy · PRD 작성', 'Claude Academy · Draft a PRD'),
         'purpose': ('인터뷰와 기존 양식으로 초안 작성', 'Use interviews and an existing template')},
        {'source': 'claude-write-spec', 'label': ('Anthropic · Write Spec', 'Anthropic · Write Spec'),
         'purpose': ('문서 구성·우선순위·인수 기준', 'Structure, priorities, and acceptance criteria')},
    ],
}]
