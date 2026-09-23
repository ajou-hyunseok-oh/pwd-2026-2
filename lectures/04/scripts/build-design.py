"""Author the Week 4 planning lesson from the original Week 9 PDF."""
from pathlib import Path
from urllib.parse import quote as urlquote
import json, re

ROOT = Path(__file__).resolve().parents[1]
PDF = 'materials/' + urlquote('[PWD Week9] 웹 서비스 설계 기초.pdf')
SOURCES = {
    f'P{p}': [f'웹 서비스 설계 기초 · p.{p}', PDF + f'#page={p}', '2025 강의 자료', '원본 개념과 가상 서비스 기획 예시']
    for p in [2,4,5,6,7,9,10,11,12,13,14,15,16,17,18,20,21,22,23,24,26,27]
}
SOURCES.update({
    'PRD': ['Product Requirements · Atlassian', 'https://www.atlassian.com/agile/product-management/requirements', '2026-09-23 확인', '기획 문서의 목적과 구성'],
    'JOURNEY': ['Journey Mapping · NN/g', 'https://www.nngroup.com/articles/journey-mapping-101/', '2026-09-23 확인', '여정과 사용자 목표의 관계'],
    'MERMAID': ['Flowcharts · Mermaid', 'https://mermaid.js.org/syntax/flowchart.html', '2026-09-23 확인', '흐름도 작성 도구'],
})
CHAPTERS = [
    ['01 · 웹서비스 설계 핵심 개념', '01 · Core Concepts of Web Service Planning'],
    ['02 · 웹서비스 기획서 작성법', '02 · Writing a Service Plan'],
    ['03 · 웹서비스 기획 사례', '03 · A Worked Service Plan'],
    ['04 · 원페이저와 기획안 발표', '04 · The One-Pager and Project Pitch'],
]
CHAPTER_LEADS = [
    ['사용자 문제·경험·기능·데이터의 관계', 'The Relationship Between User Problems, Experience, Features, and Data'],
    ['프로젝트 개요부터 기능·기술·개발 계획까지의 문서 구성', 'A Document Connecting the Overview, Features, Technology, and Schedule'],
    ['NNN UGC Creator Hub · 문제 정의에서 기능과 화면으로 구체화', 'NNN UGC Creator Hub · Developing a Problem Statement into Features and Screens'],
    ['상세 기획의 핵심을 한 페이지로 요약하고 설명하는 방법', 'Selecting, Summarizing, and Presenting the Essentials of a Service Plan'],
]

def bi(s):
    if isinstance(s, list):
        assert len(s) == 2
        return s
    parts = s.split('||')
    if len(parts)==1:
        assert not re.search('[가-힣]',s), s
        return [s,s]
    assert len(parts) == 2, s
    return parts

def prose(s):
    # Reviewed explanation lists only; quoted examples, titles, URLs, and IDs use bi().
    return [re.sub(r'[ \t]*·[ \t]*', ' · ', value) for value in bi(s)]

def points(title, *items):
    return dict(type='points', title=prose(title), items=[prose(x) for x in items])

def concepts(title, *items):
    return dict(type='design_concepts', title=prose(title),
        sections=[dict(definition=prose(a), details=[prose(x) for x in details]) for a,*details in items])

def sequences(title, *items):
    return dict(type='design_sequences', title=prose(title),
        sections=[dict(role=prose(a), flow=prose(b)) for a,b in items])

def table(title, heads, *rows, widths=None):
    block=dict(type='table', title=prose(title), heads=[prose(x) for x in heads], rows=[[prose(x) for x in r] for r in rows])
    if widths: block['widths']=widths
    return block

def quotation(title, text):
    return dict(type='quote', title=bi(title), text=bi(text))

slides = []
def add(title, lead, *blocks, chapter=None, pages=(), note='', layout='stack', extra_refs=()):
    slides.append(dict(title=bi(title), lead=bi(lead), blocks=list(blocks),
        chapter=CHAPTERS[chapter-1] if chapter else None,
        refs=[],
        note_refs=[f'P{p}' for p in pages] + list(extra_refs),
        source_pages=list(pages), note=note, layout=layout))

add('웹 서비스 설계 기초||Web Service Planning Fundamentals',
    '사용자 문제·서비스 기획·원페이저 작성||User Problems, Service Planning, and the One-Pager')

add('학습 목표||Learning Objectives',
    '자신의 웹서비스를 기획하고 설명하기 위한 네 가지 수행 목표||Four Outcomes for Planning and Explaining a Web Service',
    concepts('기획안으로 표현할 내용||Planning Outcomes',
        ('문제 정의 - 해결할 사용자 불편의 구체화||Problem Definition - A specific user difficulty',
         '대상 사용자 · 사용 상황을 포함한 문제 문장 작성||A problem statement including the user and situation'),
        ('핵심 기능 선정 - 문제 해결에 필요한 기능 결정||Feature Selection - Functions needed to solve the problem',
         '기능별 개발 우선순위 결정||Development priorities for each feature'),
        ('사용 흐름 표현 - 목표 행동까지의 경로 구성||User Flow - A path to the target action',
         '행동 순서 · 주요 화면 정리||Action sequence · Key screens'),
        ('기획안 요약 · 설명 - 서비스 핵심의 전달||Summary and Presentation - Communication of the essentials',
         '목적 · 기능 · 사용 흐름을 원페이저로 정리하고 발표||Purpose · Features · User flow in a one-pager and presentation')),
    pages=(2,27), note='합의한 보완 1. 주제 목록을 학생의 수행 결과로 구체화. 네 가지 목표를 마지막 작성 기준과 연결. 새로운 제출 과제 추가 없음.')

add('웹 서비스 설계의 구성||Elements of Web Service Planning',
    '해결할 문제와 사용 경험을 화면·기능·데이터로 구체화||Translating User Problems and Experiences into Screens, Features, and Data',
    concepts('기획·UX·UI의 역할||Planning, UX, and UI',
        ('서비스 기획 - 사용자 문제와 해결 방향의 설정||Service Planning - Definition of the user problem and solution',
         '서비스의 목적 · 해결 방법 · 범위 결정||Service purpose · Solution approach · Scope'),
        ('UX - 목표 달성 과정에서 겪는 경험과 반응||UX - Experience and responses while pursuing a goal',
         '사용자 경험(User Experience)||User Experience'),
        ('UI - 사용자와 서비스의 상호작용 접점||UI - The point of interaction with a service',
         '사용자 인터페이스(User Interface)||User Interface',
         '화면의 정보 · 입력 요소 · 피드백||On-screen information · Input controls · Feedback')),
    quotation('설계 요소의 연결||Connected Design Elements', '사용자 행동 → 필요한 기능 → 화면에 표시하거나 저장할 데이터||User action → Required feature → Data to display or store'),
    chapter=1, pages=(4,6), note='기획자·디자이너·개발자가 공유하는 개념. 화면·기능·데이터를 독립된 목록으로 보지 않고 하나의 사용자 행동과 연결.')

add('서비스 기획 핵심 개념||Core Planning Concepts',
    '사용자·문제·가치를 중심으로 정리하는 서비스의 방향||The Direction of a Service Defined by Its Users, Problems, and Value',
    concepts('기획의 중심||Planning Essentials',
        ('타깃 사용자 - 서비스를 주로 이용할 집단||Target User - The main user group',
         '서비스를 이용하는 상황 포함||Context of service use'),
        ('문제 정의 - 사용자 불편과 필요의 구체화||Problem Definition - A specific user difficulty',
         '현재의 불편 · 충족되지 않은 필요||Current difficulties · Unmet needs'),
        ('가치 제안 - 사용자에게 제공할 핵심 이점||Value Proposition - The core user benefit',)),
    concepts('기획을 구체화하는 개념||Supporting Concepts',
        ('가설 - 검증 가능한 예상||Hypothesis - A testable expectation',
         '해결 방법과 기대 효과의 연결||A link between the solution and expected outcome'),
        ('경쟁 분석 - 기존 서비스와 대안의 비교||Competitive Analysis - A comparison of alternatives',
         '기능 · 경험 · 제공 가치 비교||Features · Experience · Offered value'),
        ('서비스 콘셉트 - 서비스 방향을 담은 핵심 문장||Service Concept - A statement of the service direction',
         '대상 사용자 · 문제 · 해결 방법||Target user · Problem · Solution')),
    chapter=1, pages=(5,), layout='split', note='합의한 보완 2. 사용자·문제·가치를 중심에 두고 가설·경쟁 분석·콘셉트를 보조 개념으로 구분. 용어 암기보다 항목의 역할을 설명.')

add('사용자 경험의 표현 방법||Representing the User Experience',
    '사용자 이해·경험의 흐름·화면 구성을 표현하는 산출물||Artifacts for Understanding Users, Mapping Experiences, and Arranging Screens',
    table('UX 설계 산출물||UX Design Artifacts', ['개념||Concept','표현할 내용||Content','설계에서의 역할||Purpose'],
        ['페르소나||Persona','대표 사용자의 행동 · 목표 · 불편||Representative user behavior · Goals · Difficulties','사용자 관점의 구체화||A concrete user perspective'],
        ['사용자 여정||User Journey','서비스 이용 전·중·후의 행동과 경험||Actions and experiences before, during, and after use','전체 경험과 개선 지점 파악||Understanding the whole experience'],
        ['사용자 흐름||User Flow','목표 행동까지의 절차와 선택 경로||Steps and choices leading to a goal','이동 순서와 조건 정리||The sequence and its conditions'],
        ['와이어프레임||Wireframe','화면의 정보 · 구성 요소 · 배치||Information · Elements · Layout','화면 구조의 구체화||A concrete screen structure'], widths='18% 44% 38%'),
    chapter=1, pages=(6,12,13), extra_refs=('JOURNEY',), note='용어별 한 문장 정의를 역할 비교로 구성. 서비스에 따라 달라지는 여정의 단계. 다음 주 UI/UX 수업에서 상세화할 수 있는 입문 수준.')

add('구조·기능·데이터 설계 용어||Structure, Feature, and Data Terms',
    '서비스 기획을 개발에 필요한 정보로 연결하는 공통 언어||Shared Terms Connecting a Service Plan to Development',
    concepts('정보와 기능||Information and Features',
        ('정보 구조 - 서비스 정보의 분류 · 연결 체계||Information Architecture - Organization of information',
         '사이트맵 - 화면 · 페이지 간 구조||Sitemap - The structure of screens and pages'),
        ('기능 요구사항 - 제공할 기능과 동작 조건||Feature Requirements - Functions and their conditions',
         '기능 목록 - 제공할 기능의 나열||Feature list - An inventory of functions'),
        ('기능 흐름도 - 처리 순서와 조건 분기||Function Flow - Processing steps and decisions',)),
    concepts('화면과 데이터||Screens and Data',
        ('화면 설계서 - 화면 구성과 동작을 기록한 문서||Screen Specification - A record of layout and behavior',
         '화면 요소 · 표시 데이터 · 사용자 동작||UI elements · Displayed data · User actions'),
        ('API - 소프트웨어 간 기능 · 데이터 이용 규칙||API - Rules for software interaction',
         '서버 요청 · 응답에 활용||Use in server requests and responses'),
        ('DB 스키마 - 저장할 데이터의 구조||Database Schema - The structure of stored data',
         '테이블 · 필드 · 관계||Tables · Fields · Relationships')),
    chapter=1, pages=(7,6), layout='split', note='합의한 보완 2. 구현 문법이나 상세 API·DB 설계 없이 역할을 이해하는 참고 용어로 소개. 학생에게 모든 문서의 완성을 요구하는 장이 아님.')

add('웹 서비스 기획서의 구성||Structure of a Service Plan',
    'PRD - 서비스의 목적·경험·기능·개발 계획을 공유하는 문서||PRD - A Shared Document of Purpose, Experience, Features, and Development Plans',
    table('기획서의 주요 항목||Main Sections', ['항목||Section','작성 내용||Content'],
        ['프로젝트 개요||Project Overview','목표 · 문제 정의 · 타깃 사용자||Goal · Problem statement · Target users'],
        ['서비스 콘셉트||Service Concept','서비스명 · 핵심 가치 · 메인 시나리오||Name · Core value · Main scenarios'],
        ['UX 설계||UX Design','사용자 여정 · 와이어프레임 · 플로차트||Journey · Wireframes · Flowcharts'],
        ['기능 정의||Feature Definition','핵심 기능 목록과 우선순위||Core features and priorities'],
        ['기술 구조 · 개발 계획||Technology and Development','기술 스택 · 배포 환경 · API 구상 · 일정||Stack · Deployment · API outline · Schedule']),
    chapter=2, pages=(9,), extra_refs=('PRD',), note='원본 PRD의 다섯 항목 유지. 유일한 표준 서식이 아닌 수업에서 사용할 구성 예시. 상세 기획서는 사고를 정리하는 기반이며 별도 신규 제출물로 추가하지 않음.')

add('프로젝트 개요 작성||Writing the Project Overview',
    '목표·문제·사용자를 구분하여 설명하는 서비스의 출발점||Distinguishing the Goal, Problem, and User at the Start of a Plan',
    concepts('개요의 세 요소||Three Elements of the Overview',
        ('목표 - 문제 해결을 통해 만들고 싶은 사용자 변화||Goal - The intended change for users',),
        ('문제 정의 - 특정 상황에서 사용자가 겪는 불편||Problem Statement - A difficulty in a specific situation',
         '설명 근거 - 사례 · 관찰 · 통계||Supporting evidence - Examples · Observations · Data'),
        ('타깃 페르소나 - 대표 사용자의 구체적인 모습||Target Persona - A concrete representation of the user',
         '배경 · 행동 · 목표 · 필요||Background · Behavior · Goals · Needs')),
    quotation('문제 문장의 구성||Structure of a Problem Statement', '사용자 + 사용 상황 + 달성하려는 목표 + 현재의 불편||User + Situation + Intended goal + Current difficulty'),
    chapter=2, pages=(10,), note='문제와 해결안의 구분을 말로 설명. 원본의 UGC 사례는 세 번째 챕터에서 작성 과정과 함께 사용. 가상 사례의 사업성이나 수치 검증을 수업 내용에 추가하지 않음.')

add('서비스 콘셉트 작성||Writing the Service Concept',
    '사용자에게 제공할 가치와 핵심 이용 장면의 정의||Defining the Value and Main Usage Scenarios',
    concepts('콘셉트의 구성||Elements of a Concept',
        ('서비스명 · 핵심 메시지 - 서비스의 특징을 전달하는 표현||Name and Core Message - An expression of the service’s purpose',
         '서비스명 · 한 줄 소개||Service name · One-line introduction'),
        ('핵심 가치 - 사용자가 서비스를 선택할 이유||Core Value - The reason to choose the service',
         '사용자에게 제공할 이점||Benefits offered to users'),
        ('메인 시나리오 - 핵심 가치를 얻는 대표적인 행동 순서||Main Scenario - The main sequence for receiving value',)),
    quotation('콘셉트 문장의 구성||Structure of a Concept Statement', '대상 사용자 → 해결할 문제 → 제공할 방법 → 기대하는 변화||Target user → Problem → Solution → Expected change'),
    chapter=2, pages=(11,5), note='서비스명과 슬로건만으로 콘셉트가 완성되는 것은 아니며 사용자와 가치의 연결이 핵심. 작성 과정은 UGC 사례에서 시연.')

add('사용자 여정 설계||Designing the User Journey',
    '사용자의 목표 달성 과정을 단계별 행동과 경험으로 정리||Organizing the Goal-Oriented Experience into Stages',
    table('인식·탐색·행동·피드백의 구성 예||An Example of Journey Stages', ['단계||Stage','사용자 경험||User Experience','설계할 요소||Design Focus'],
        ['인식||Awareness','서비스의 존재와 필요성 인지||Discovering the service and its relevance','가치 제시 · 홍보 · 랜딩 페이지||Value · Outreach · Landing page'],
        ['탐색||Exploration','정보를 찾고 비교·이해하는 과정||Finding, comparing, and understanding information','정보 구조 · 검색 · 필터||Information architecture · Search · Filters'],
        ['행동||Action','핵심 기능을 이용하여 목표 수행||Using a core feature to achieve the goal','절차 · 입력 · 실행 결과||Steps · Input · Results'],
        ['피드백||Feedback','결과 확인과 후속 행동||Reviewing the result and taking follow-up action','알림 · 상태 · 후기 · 통계||Notifications · Status · Reviews · Analytics'], widths='18% 44% 38%'),
    chapter=2, pages=(12,22), extra_refs=('JOURNEY',), note='원본 네 단계를 수업용 틀로 유지. 서비스와 목표에 따라 단계 명칭과 수가 달라질 수 있음을 설명. 표의 항목 전체를 모든 서비스에 의무적으로 넣는 기준이 아님.')

add('와이어프레임과 화면 구성||Wireframes and Screen Structure',
    '정보의 위치·입력 요소·주요 행동을 표현하는 화면 설계도||A Screen Blueprint for Information, Inputs, and Main Actions',
    {'type':'design_wire','mode':'application','title':bi('전시 신청 화면 예||Exhibition Application Wireframe')},
    concepts('화면에서 결정할 내용||Screen Design Decisions',
        ('정보 우선순위 - 먼저 필요한 정보의 표시 순서||Information Priority - The order of needed information',),
        ('입력과 행동 - 입력할 내용과 실행할 기능||Inputs and Actions - Data entry and available functions',),
        ('결과 표시 - 실행 후 상태와 후속 행동||Result Display - The resulting state and next action',),
        ('작성 도구 - 화면 구조의 표현 수단||Authoring Tools - Ways to represent a screen',
         '종이 스케치 · Figma · 간단한 화면 도식||Paper sketch · Figma · Simple screen outline')),
    chapter=2, pages=(13,22), layout='split', note='원본 와이어프레임의 목적을 유지하고 가상 UGC 전시 신청 화면으로 구체화. 화면의 미적 완성도보다 정보·행동·결과의 배치가 학습 대상. Figma 사용법 실습은 추가하지 않음.')

add('플로차트와 역할별 행동 흐름||Flowcharts and Role-Based Flows',
    '행동의 순서·조건 분기·역할 간 연결을 표현하는 도식||A Diagram of Sequences, Decisions, and Connections Between Roles',
    {'type':'design_flow','title':bi('UGC 서비스의 주요 흐름||Main Flows of the UGC Service'), 'lanes':[
        [bi('제작자||Creator'), *map(bi,['아이템 등록||Register Item','전시 신청||Apply for Exhibition','승인 결과 확인||Check Review Result','전시 · 수익 확인||View Exhibition · Earnings'])],
        [bi('운영자||Administrator'), *map(bi,['신청 접수||Receive Application','적합성 검토||Review Suitability','승인 · 반려||Approve / Reject','승인 건 전시 배치||Exhibit Approved Items'])],
        [bi('구매자||Consumer'), *map(bi,['피드 탐색||Browse Feed','상세 · 미리보기||Details · Preview','구매||Purchase','후기 · 좋아요||Review · Like'])],
    ]},
    points('조건과 역할의 연결||Conditions and Role Connections',
        '승인 → 전시 진행||Approval → Exhibition',
        '반려 → 사유 확인 → 수정 후 재신청||Rejection → Review reason → Revise and reapply',
        '제작자의 신청 → 운영자의 검토||Creator application → Admin review',
        '구매 발생 → 제작자의 수익 확인||Purchase → Creator earnings'),
    chapter=2, pages=(14,), extra_refs=('MERMAID',), note='원본 역할과 핵심 행동 유지. 노드 사이의 순서를 명시한 HTML 흐름도. Mermaid는 텍스트로 흐름도를 만드는 도구의 예로만 소개하며 문법 수업으로 확장하지 않음.')

add('기능 목록과 우선순위||Feature Lists and Priorities',
    '핵심 사용자 행동을 기준으로 결정하는 개발 범위||Development Scope Chosen Around the Core User Action',
    table('우선순위의 구분 예||Example Priority Levels', ['구분||Level','의미||Meaning','선정 기준||Selection Basis'],
        ['P1 (핵심)||P1 (Essential)','첫 버전에 반드시 포함할 기능||Required in the first version','주요 사용자 목표 달성에 필요한 기능||Needed for the main user goal'],
        ['P2 (중요)||P2 (Important)','사용 경험을 개선하는 확장 기능||Extensions improving the experience','핵심 흐름을 편리하게 만드는 기능||Improves the core experience'],
        ['P3 (보완)||P3 (Additional)','출시 이후 추가할 부가 기능||Features for a later release','추가적인 편의와 참여를 위한 기능||Additional convenience and engagement']),
    concepts('최소 기능 범위||Minimum Viable Scope',
        ('MVP - 핵심 가치를 제공하는 첫 제품||MVP - The first product delivering core value',
         'Minimum Viable Product',
         '사용자 반응 확인이 가능한 최소 기능 범위||The minimum scope enabling user feedback')),
    chapter=2, pages=(15,), note='원본 P1·P2·P3 분류 유지. 우선순위는 기능 이름에 고정된 정답이 아니라 프로젝트 목표와 개발 여건에 따른 선택. 가상 사례의 우선순위를 평가하거나 변경하지 않음.')

add('기술 구조와 배포 환경||Technology and Deployment',
    '화면·데이터 처리·저장·운영을 담당할 기술의 역할||The Roles of Technologies in UI, Processing, Storage, and Operation',
    table('기술 스택의 구성 예||Example Technology Stack', ['구분||Area','기술||Technology','역할||Role'],
        ['Frontend','React + Vite','화면 구성과 사용자 인터랙션||UI composition and user interaction'],
        ['Backend','Supabase','인증 · PostgreSQL 데이터 저장 · 서버 기능||Authentication · PostgreSQL storage · Server functions'],
        ['Deployment','Vercel · Supabase','프론트엔드와 백엔드의 배포·운영||Frontend and backend deployment'],
        ['Design · Collab','Figma · Notion · GitHub','화면 설계 · 문서 · 버전 관리||Screen design · Documents · Version control'], widths='20% 34% 46%'),
    quotation('화면·API·DB의 관계||Screens, APIs, and the Database','아이템 등록 화면 → 등록 요청(API) → 아이템 정보 저장(DB) → 등록 결과 표시||Registration screen → API request → Item saved in the database → Result displayed'),
    chapter=2, pages=(16,24), note='합의한 보완 2. 원본의 기술 스택과 API 구상을 역할 중심으로 유지. 요청 경로·응답 코드·테이블 설계는 이후 REST API와 DB 수업에서 구체화. 특정 기술 사용을 필수 과제 조건으로 추가하지 않음.')

add('개발 일정 수립||Planning the Development Schedule',
    '기능의 의존 관계와 산출물을 기준으로 나누는 작업 단계||Stages Defined by Dependencies and Deliverables',
    table('6주 프로젝트의 일정 예||Example Six-Week Schedule', ['단계||Stage','기간||Period','주요 작업||Main Tasks','산출물||Deliverables'],
        ['MVP 설계||MVP Planning','Week 1–2','기획서 · 와이어프레임 · 데이터·API 구상||Plan · Wireframes · Data and API outline','기획·설계 문서||Planning documents'],
        ['기능 구현||Implementation','Week 3–5','화면 구성 · 데이터 연동 · 주요 기능||UI · Data integration · Core features','동작하는 프로토타입||Working prototype'],
        ['테스트·배포||Test and Deploy','Week 6','기능 확인 · 오류 수정 · 서비스 배포||Checks · Fixes · Deployment','서비스 URL · 시연||Service URL and demo'], widths='18% 12% 46% 24%'),
    points('일정에 반영할 조건||Scheduling Considerations',
        '선행 작업과 후속 작업의 관계||Dependencies between tasks',
        '기능별 작업량||Workload by feature',
        '테스트 · 수정 · 배포 시간||Time for testing · Fixes · Deployment',
        '예상 지연에 대비한 여유||Allowance for unexpected delays'),
    chapter=2, pages=(17,), note='원본의 6주 일정은 가상 프로젝트 일정 예시로 유지. 올해 과제 제출일과 혼동하지 않도록 구체 날짜를 쓰지 않음. 버퍼 비율의 암기보다 여유 시간을 계획하는 목적을 설명.')

add('KPI와 성과 확인||KPIs and Success Measures',
    '서비스의 목표를 확인할 수 있는 지표와 측정 방법||Metrics and Methods for Checking Progress Toward Service Goals',
    table('성과 지표의 종류||Types of Metrics', ['구분||Type','확인할 내용||Focus','예시||Example'],
        ['서비스 지표||Service','사용량과 활동 규모||Usage and activity','활성 사용자 · 아이템 등록 수||Active users · Registered items'],
        ['참여 지표||Engagement','지속적인 이용과 참여||Continued use and participation','재방문 · 후기 · 좋아요||Return visits · Reviews · Likes'],
        ['전환 지표||Conversion','목표 행동의 달성 비율||Completion of a target action','상세 조회 → 구매 비율||Item view → Purchase rate'],
        ['수익 지표||Revenue','서비스의 경제적 성과||Economic outcomes','판매 수익 · 거래 수수료||Sales revenue · Transaction fees'],
        ['품질 지표||Quality','이용 품질과 만족도||Experience quality and satisfaction','로딩 시간 · 오류율 · 만족도||Loading time · Error rate · Satisfaction']),
    concepts('지표 선정||Metric Selection',
        ('핵심 지표 - 서비스 목표의 달성을 확인할 기준||Key Metric - A measure of progress toward the service goal',
         '지표와 측정 방법의 연결||A link between the metric and its measurement method')),
    chapter=2, pages=(18,), note='지표 분류는 원본을 유지. 학생의 초기 기획에는 목적에 맞는 지표 1~2개와 측정 방법의 연결을 기대하며 모든 KPI 운영이나 실적 제출을 요구하지 않음.')

add('가상 서비스의 프로젝트 개요||Overview of the Fictional Service',
    'NNN UGC Creator Hub · UGC 아이템의 전시·홍보를 지원하는 허브||NNN UGC Creator Hub · A Hub for Exhibiting and Promoting UGC Items',
    concepts('목표와 문제||Goal and Problem',
        ('목표 - 아이템 발견성과 판매 기회의 향상||Goal - Better item discovery and sales opportunities',
         '제작자의 전시 · 홍보 기회 확대||More exhibition and promotion opportunities for creators'),
        ('문제 - 제작자와 구매자의 연결 부족||Problem - Limited connections between creators and buyers',
         '제작자 - 제한된 전시 기회 · 홍보 부담||Creator - Limited exhibition opportunities · Promotion effort',
         '구매자 - 적합한 아이템 탐색 부담||Buyer - Effort to find suitable items')),
    table('타깃 사용자||Target Users', ['역할||Role','목표||Goal'],
        ['제작자(Creator)||Creator','아이템 전시 · 홍보 · 수익 확인||Item exhibition · Promotion · Earnings review'],
        ['구매자(Consumer)||Consumer','아이템 탐색 · 착용 미리보기 · 구매||Discovery · Preview · Purchase'],
        ['운영자(Admin)||Administrator','전시 큐레이션과 판매 · 정산 관리||Exhibition curation · Sales and settlement management']),
    chapter=3, pages=(20,10), note='원본의 NNN UGC Creator Hub와 제작자·구매자·운영자 역할 유지. 교육용 가상 서비스 기획안으로 취급하며 사업성·정책 타당성에 대한 비평을 추가하지 않음.')

add('문제 정의와 가치 제안 작성||From User Problem to Core Value',
    '사용자의 상황에서 불편을 도출하고 해결 방향으로 연결하는 과정||Connecting a User Situation to a Problem and a Direction for the Solution',
    {'type':'design_process','steps':[
        [bi('사용자 상황||User Situation'),bi('22세 대학생 Erik\nUGC 아이템 제작 · SNS 홍보||Erik, a 22-year-old student\nCreates UGC items and promotes them on social media')],
        [bi('문제 정의||Problem Statement'),bi('아이템을 만들어도\n사용자에게 노출될 기회 부족||Limited chances to reach users\neven after creating an item')],
        [bi('핵심 가치||Core Value'),bi('큐레이션 전시를 통한\n아이템의 발견성 향상||Better item discovery\nthrough curated exhibitions')],
    ]},
    quotation('서비스 콘셉트 문장||Service Concept Statement','UGC 제작자의 아이템을 큐레이션 전시로 소개하고, 판매와 수익 확인을 지원하는 허브 플랫폼||A hub showcasing creators’ UGC items through curated exhibitions and supporting sales and earnings tracking'),
    chapter=3, pages=(10,11,21), note='합의한 보완 3. 원본 페르소나·문제·콘셉트를 작성 순서대로 제시. 강사는 상황에서 핵심 불편을 골라 문제 문장으로 만들고 그 불편을 바꾸는 가치를 쓰는 과정을 시연. 모든 인물과 설정은 가상 사례.')

add('사용자 목표와 기능 도출||Deriving Features from User Goals',
    '필요한 행동을 기능으로 표현하고 개발 우선순위를 부여하는 과정||Turning Required Actions into Features and Assigning Priorities',
    table('목표 → 행동 → 기능||Goal → Action → Feature', ['사용자 목표||User Goal','필요한 행동||Required Action','기능||Feature','우선순위||Priority'],
        ['제작자의 아이템 소개||Present a creator’s item','아이템 정보 입력||Enter item information','아이템 등록||Item registration','P1'],
        ['제작자의 전시 참여||Join an exhibition','등록 아이템으로 전시 신청||Apply with a registered item','전시 신청||Exhibition application','P1'],
        ['구매자의 아이템 발견||Discover an item','태그 · 테마별 탐색||Browse by tag or theme','큐레이션 피드||Curated feed','P1'],
        ['운영자의 전시 관리||Manage exhibitions','신청 아이템 검토||Review submitted items','승인·반려||Approve or reject','P1'],
        ['제작자의 수익 확인||Review creator earnings','포인트 · 정산 내역 조회||View points and settlements','포인트 정산 조회||Settlement history','P2'], widths='26% 32% 30% 12%'),
    chapter=3, pages=(15,23), note='합의한 보완 3. 원본 기능과 우선순위를 그대로 활용해 목표에서 기능 이름을 도출하는 과정을 설명. 기능 목록 전체를 다시 나열하기보다 도출 논리에 집중. 후기·좋아요 P3는 원본과 같은 확장 예시로 구두 설명.')

add('사용자 행동과 화면 요소의 연결||Connecting Actions to Screen Elements',
    '사용자가 확인하거나 실행할 내용을 화면의 정보와 기능으로 배치||Mapping User Needs to Information and Actions on a Screen',
    table('제작자 마이페이지의 구성 근거||Creator Page Design Rationale', ['사용자 행동||User Action','필요한 정보·기능||Information or Feature'],
        ['신청 결과 확인||Check an application','아이템명 · 신청 상태||Item name and application status'],
        ['반려 내용 수정||Revise a rejected application','반려 사유 · 수정 후 재신청||Rejection reason and resubmission'],
        ['판매 수익 확인||Review earnings','판매 데이터 · 포인트 내역||Sales data and point history']),
    {'type':'design_wire','mode':'account','title':bi('제작자 마이페이지 구상||Creator Page Wireframe')},
    chapter=3, pages=(22,13), layout='split', note='합의한 보완 3. 앞에서 배운 사용자 행동이 구체적인 화면 요소로 바뀌는 과정을 표시. 신청 상태·반려 사유·포인트는 가상 서비스의 화면 예시이며 실제 운영 데이터가 아님.')

add('서비스 콘셉트와 메인 시나리오||Core Value and Main Scenarios',
    'Create. Exhibit. Earn. · 만들고, 전시하고, 수익을 얻는 서비스||Create. Exhibit. Earn. · The Service’s Core Promise',
    table('NNN UGC Creator Hub의 핵심 가치||Core Value of NNN UGC Creator Hub', ['가치||Value','기획 내용||Planned Experience'],
        ['Visibility(노출성)||Visibility','큐레이션 피드와 Outfit 월드를 통한 아이템 전시||Item exhibitions in a curated feed and the Outfit world'],
        ['Reward(보상성)||Reward','판매 수익금의 40%를 포인트로 자동 적립||Automatic point credits equal to 40% of sales proceeds'],
        ['Trust(신뢰성)||Trust','승인 상태와 판매·정산 내역의 투명한 제공||Clear approval status and sales and settlement records']),
    sequences('역할별 메인 시나리오||Main Scenarios by Role',
        ('제작자||Creator', '등록 → 전시 신청 → 승인·전시 → 수익 확인||Register → Apply → Approval and exhibition → Review earnings'),
        ('구매자||Consumer', '탐색 → 상세·미리보기 → 구매 → 후기||Browse → Details and preview → Purchase → Review'),
        ('운영자||Admin', '검토 → 승인·반려 → 전시 배치 → 리포트||Review → Approve or reject → Place exhibits → Reports')),
    chapter=3, pages=(21,11), note='원본 사례의 세 핵심 가치·40% 포인트 정책·역할별 시나리오 유지. 교육용 서비스의 가상 정책이며 실제 Roblox 수익 배분을 설명하는 자료가 아님. 학생 대상 정책 비평이나 사실 검증 설명은 추가하지 않음.')

add('서비스 기획 원페이저||The Service Planning One-Pager',
    '서비스의 핵심을 한 페이지로 설명하는 기획 요약 문서||A One-Page Summary of the Service’s Essentials',
    table('원페이저의 구성||One-Pager Sections', ['항목||Section','요약할 내용||Content to Summarize'],
        ['서비스명 · 슬로건||Name and Slogan','이름과 핵심 메시지||The name and main message'],
        ['문제 정의||Problem','대상 사용자와 해결할 불편||The target user and difficulty'],
        ['해결방안||Solution','문제를 해결하는 핵심 아이디어||The main idea for addressing the problem'],
        ['주요 기능||Key Features','서비스의 핵심 기능 3~5개||Three to five core features'],
        ['기술 구조||Technology','주요 기술과 구현 방식의 개요||The main technologies and implementation outline'],
        ['기대효과 · KPI||Impact and KPIs','사용자 가치와 성과 확인 지표||User value and success measures'],
        ['사용 흐름||User Flow','핵심 행동에 이르는 경로||The path to the core user action']),
    chapter=4, pages=(27,), note='원본의 일곱 구성 요소 유지. PRD는 상세 내용, 원페이저는 핵심을 선별한 요약이라는 문서 목적의 차이를 설명.')

add('상세 기획의 요약 과정||Summarizing a Detailed Plan',
    '사용자·문제·해결을 전달하는 핵심 정보를 골라 압축하는 과정||Selecting and Condensing the Information That Explains the User, Problem, and Solution',
    table('기획서 → 원페이저||Detailed Plan → One-Pager', ['항목||Section','상세 기획의 내용||Detailed Plan','한 페이지에 담을 요약||One-Page Summary'],
        ['문제||Problem','전시 기회 제한 · 홍보 역량 부족\n구매자의 탐색 부담||Limited exhibitions · Promotion resources\nBuyer discovery effort','제작자의 노출 기회와 구매자의 발견 경로 부족||Limited creator exposure and buyer discovery'],
        ['기능||Features','등록 정보 · 썸네일 · 전시 신청\n검토 · 승인 · 태그별 피드||Item information · Thumbnails · Applications\nReviews · Tagged feeds','아이템 등록 · 전시 신청·승인\n큐레이션 탐색||Item registration · Application and review\nCurated discovery'],
        ['기술||Technology','React 화면 · Supabase 인증·DB\nVercel 프론트엔드 배포||React UI · Supabase authentication and DB\nVercel hosting','React · Supabase · Vercel||React · Supabase · Vercel'], widths='14% 44% 42%'),
    concepts('요약의 기준||Selection Criteria',
        ('정보 선별 - 서비스 이해에 필요한 핵심 결정의 선택||Information Selection - The key decisions needed to understand the service',
         '원페이저 - 대상 · 문제 · 핵심 가치 · 주요 기능 · 사용 흐름||One-pager - Users · Problem · Value · Core features · User flow',
         '상세 문서 - 세부 입력 항목 · API 명세||Full plan - Field details · API specifications')),
    chapter=4, pages=(27,9,20,23,24), note='합의한 보완 4. 앞선 UGC 기획서의 같은 내용을 실제로 압축하는 과정을 시연. 무엇을 남기고 무엇을 상세 문서에 두는지 선택의 이유를 설명.')

add('NNN UGC Creator Hub 원페이저||NNN UGC Creator Hub One-Pager',
    '문제·해결·기능·실행 계획을 연결한 한 페이지 기획안||A One-Page Plan Connecting the Problem, Solution, Features, and Execution',
    {'type':'design_onepager'},
    chapter=4, pages=(27,20,21,22,23,24), note='합의한 보완 4. 원본 가상 서비스로 완성한 한 페이지 예시. 일곱 구성 요소를 실제 한 장에 배치. 상세 기획과 같은 서비스명·핵심 기능·기술·사용 흐름 사용.')

add('서비스 기획안 작성 기준||Service Plan Writing Criteria',
    '문제·기능·사용 흐름·요약의 연결을 확인하는 네 가지 기준||Four Criteria Connecting the Problem, Features, Flow, and Summary',
    table('학습 목표와 작성 결과||Learning Goals and Written Outcomes', ['학습 목표||Learning Goal','기획안에 표현할 내용||Content in the Plan','확인 기준||Review Criterion'],
        ['문제 정의||Problem Definition','대상 사용자·상황·불편을 담은 문장||A statement of the user, situation, and difficulty','사용자와 해결할 문제의 구체성||A specific user and problem'],
        ['핵심 기능 선정||Feature Selection','주요 기능과 우선순위||Core features and priorities','각 기능과 사용자 문제의 연결||Each feature linked to the problem'],
        ['사용 흐름 표현||User Flow','핵심 행동 순서와 주요 화면||The main action sequence and screens','시작부터 결과까지 이어지는 과정||A path from the start to the result'],
        ['기획안 요약||Plan Summary','서비스의 핵심을 담은 원페이저||A one-pager containing the essentials','목적·기능·흐름의 일관성||Consistent purpose, features, and flow']),
    chapter=4, pages=(2,27), note='합의한 보완 1·4. 첫 학습 목표와 마지막 작성 기준을 같은 네 항목으로 연결. 새로운 배점이나 추가 제출 항목을 정의하지 않음.')

add('기획안 발표와 결과물 준비||Preparing the Project Pitch',
    '원페이저를 바탕으로 서비스의 목적과 구현 방향을 설명하는 발표||A Presentation of the Service’s Purpose and Build Direction Using the One-Pager',
    table('발표의 설명 순서||Presentation Sequence', ['순서||Order','설명 내용||Content'],
        ['서비스 소개||Introduce the Service','서비스명 · 대상 사용자 · 해결할 문제||Name · Target users · Problem'],
        ['가치와 기능||Explain Value and Features','핵심 가치 · 주요 기능 · 우선순위||Core value · Main features · Priorities'],
        ['사용 과정||Show the User Experience','핵심 사용 흐름 · 주요 화면 구상||The main flow and key screen ideas'],
        ['개발과 기대효과||Explain Execution and Impact','기술 · 개발 계획 · 성과 확인 방법||Technology · Development plan · Success measures']),
    concepts('기획 결과물||Planning Deliverables',
        ('원페이저 - 서비스의 핵심을 담은 1페이지 기획안||One-Pager - A one-page summary of the service',),
        ('발표 영상 - 기획안을 설명하는 5분 이내 동영상||Pitch Video - A plan explanation of up to five minutes',
         '원페이저와 발표 내용의 일치||Content consistent with the one-pager',
         '화면 가독성 · 음성 · 재생 상태 확인||Readable visuals · Clear audio · Working playback')),
    chapter=4, pages=(26,27), note='원본의 5분 이내 기획 발표와 현재 로컬 계획의 원페이저·영상 결과물 유지. 2025 제출 날짜·배점을 복사하지 않음. 얼굴 노출·특정 도구·추가 발표 슬라이드를 필수화하지 않음.')

assert len(slides) == 26, len(slides)  # Cover + goals + 24 section topics; four chapter slides inserted by the page builder.
for path, data in [('design-sources.json', SOURCES), ('design-slides.json', slides), ('design-chapters.json', CHAPTER_LEADS)]:
    (ROOT/'materials'/path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

text = ['웹 서비스 설계 기초 · 2교시 재제작', '작성: 2026-09-23',
        '원본: [PWD Week9] 웹 서비스 설계 기초.pdf',
        '최종 HTML: ../ai-design.html · 표지·학습 목표·4개 챕터를 포함한 30장',
        '가상 서비스: NNN UGC Creator Hub. 사업성·수치·수익 배분·우선순위의 비평은 수업 범위에 포함하지 않음.',
        '보완: 수행 목표 · 핵심 용어의 비중 · 기획 작성 과정 · 원페이저 압축과 완성 예시', '']
number=0; last=None
for slide in slides:
    if slide['chapter'] and slide['chapter'] != last:
        number += 1; text += [f'{number:02}. {slide["chapter"][0]}', '챕터 구분', '']; last=slide['chapter']
    number += 1
    text += [f'{number:02}. {slide["title"][0]}',slide['lead'][0]]
    for b in slide['blocks']:
        if 'title' in b: text.append(b['title'][0])
        if b['type']=='points': text += ['- '+x[0] for x in b['items']]
        elif b['type']=='design_concepts':
            for section in b['sections']:
                text.append(section['definition'][0])
                text += ['  - '+x[0] for x in section['details']]
        elif b['type']=='design_sequences': text += [x['role'][0]+' - '+x['flow'][0] for x in b['sections']]
        elif b['type']=='quote': text.append(b['text'][0])
        elif b['type']=='table': text += [' | '.join(x[0] for x in row) for row in [b['heads'],*b['rows']]]
        elif b['type']=='design_process': text += [a[0]+' - '+v[0] for a,v in b['steps']]
        else: text.append('화면 구성: '+b['type']+' '+b.get('mode',''))
    text += ['원본 PDF: '+', '.join(map(str,slide['source_pages'])),'강의 메모: '+slide['note'],'']
assert number==30
(ROOT/'materials/week-04-service-planning.ko.txt').write_text('\n'.join(text)+'\n')
print(f'Built {len(slides)} content records for the 30-slide service-planning lesson.')
