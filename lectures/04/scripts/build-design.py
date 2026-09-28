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
    ['01 · 설계의 공통언어', '01 · A Shared Language for Service Design'],
    ['02 · 기획시 결정 사항', '02 · Planning Decisions'],
    ['03 · 기획 사례', '03 · Planning Case Study'],
    ['04 · 프로젝트 기획 발표', '04 · Presenting the Project Plan'],
]
CHAPTER_LEADS = [
    ['기획·UX·UI의 관계와 사용자 경험을 표현하는 도구', 'Planning, UX, UI, and Ways to Represent User Experience'],
    ['사용자 문제 → 가치 → 핵심 기능 → 구현 방식', 'User Problem → Value → Core Features → Implementation'],
    ['사용자 맥락 → 문제·가치 → 기능 → 흐름·화면', 'User Context → Problem and Value → Features → Flow and Screens'],
    ['상세 내용을 선별해 한 페이지로 만들고 5분 이내로 설명', 'Select the Essentials for a One-Pager and a Five-Minute Pitch'],
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

add('사용자 경험의 표현 방법||Representing the User Experience',
    '사용자 이해·경험의 흐름·화면 구성을 표현하는 산출물||Artifacts for Understanding Users, Mapping Experiences, and Arranging Screens',
    table('UX 설계 산출물||UX Design Artifacts', ['개념||Concept','표현할 내용||Content','설계에서의 역할||Purpose'],
        ['페르소나||Persona','대표 사용자의 행동 · 목표 · 불편||Representative user behavior · Goals · Difficulties','사용자 관점의 구체화||A concrete user perspective'],
        ['사용자 여정||User Journey','서비스 이용 전·중·후의 행동과 경험||Actions and experiences before, during, and after use','전체 경험과 개선 지점 파악||Understanding the whole experience'],
        ['사용자 흐름||User Flow','목표 행동까지의 절차와 선택 경로||Steps and choices leading to a goal','이동 순서와 조건 정리||The sequence and its conditions'],
        ['와이어프레임||Wireframe','화면의 정보 · 구성 요소 · 배치||Information · Elements · Layout','화면 구조의 구체화||A concrete screen structure'], widths='18% 44% 38%'),
    chapter=1, pages=(6,12,13), extra_refs=('JOURNEY',), note='용어별 한 문장 정의를 역할 비교로 구성. 서비스에 따라 달라지는 여정의 단계. 다음 주 UI/UX 수업에서 상세화할 수 있는 입문 수준.')

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

add('가상 서비스의 사용자와 이용 맥락||Users and Context of the Fictional Service',
    'NNN UGC Creator Hub · 제작자·구매자·운영자가 만나는 전시 서비스||NNN UGC Creator Hub · An Exhibition Service for Creators, Buyers, and Administrators',
    table('역할별 목표와 현재 상황||Roles, Goals, and Current Situations', ['역할||Role','목표||Goal','현재 상황||Current Situation'],
        ['제작자(Creator)||Creator','아이템을 알리고 판매||Promote and sell items','SNS 홍보에 의존하고 전시 기회가 제한됨||Relies on social media and has limited exhibition opportunities'],
        ['구매자(Consumer)||Consumer','취향에 맞는 아이템 발견||Find suitable items','아이템을 비교·탐색하는 데 시간 소요||Spends time searching and comparing items'],
        ['운영자(Admin)||Administrator','전시 품질과 판매 과정 관리||Manage exhibition quality and sales','신청 아이템 검토와 전시 배치가 필요||Needs to review applications and place exhibits'], widths='21% 28% 51%'),
    chapter=3, pages=(20,10), note='가상 서비스의 등장인물과 이용 맥락만 제시. 문제 문장과 가치 제안은 다음 장에서 도출한다.')

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


add('플로차트와 역할별 행동 흐름||Flowcharts and Role-Based Flows',
    '행동의 순서·조건 분기·역할 간 연결을 표현하는 도식||A Diagram of Sequences, Decisions, and Connections Between Roles',
    {'type':'design_flow','title':bi('UGC 서비스의 주요 흐름||Main Flows of the UGC Service'), 'lanes':[
        [bi('제작자||Creator'), *map(bi,['아이템 등록||Register Item','전시 신청||Apply for Exhibition','승인 결과 확인||Check Review Result','전시 · 수익 확인||View Exhibition · Earnings'])],
        [bi('운영자||Administrator'), *map(bi,['신청 접수||Receive Application','적합성 검토||Review Suitability','승인 · 반려||Approve / Reject','승인 건 전시 배치||Exhibit Approved Items'])],
        [bi('구매자||Consumer'), *map(bi,['피드 탐색||Browse Feed','상세 · 미리보기||Details · Preview','구매||Purchase','후기 · 좋아요||Review · Like'])],
    ]},
    points('전시 신청의 조건 분기||Application Decision Branch',
        '승인 → 전시 진행||Approval → Exhibition',
        '반려 → 사유 확인 → 수정 후 재신청||Rejection → Review reason → Revise and reapply'),
    chapter=3, pages=(14,), extra_refs=('MERMAID',), note='원본 역할과 핵심 행동 유지. 노드 사이의 순서를 명시한 HTML 흐름도. Mermaid는 텍스트로 흐름도를 만드는 도구의 예로만 소개하며 문법 수업으로 확장하지 않음.')


add('와이어프레임과 화면 구성||Wireframes and Screen Structure',
    '정보의 위치·입력 요소·주요 행동을 표현하는 화면 설계도||A Screen Blueprint for Information, Inputs, and Main Actions',
    {'type':'design_wire','mode':'application','title':bi('전시 신청 화면 예||Exhibition Application Wireframe')},
    concepts('화면에서 결정할 내용||Screen Design Decisions',
        ('정보 우선순위 - 먼저 필요한 정보의 표시 순서||Information Priority - The order of needed information',),
        ('입력과 행동 - 입력할 내용과 실행할 기능||Inputs and Actions - Data entry and available functions',),
        ('결과 표시 - 실행 후 상태와 후속 행동||Result Display - The resulting state and next action',),
        ('작성 도구 - 화면 구조의 표현 수단||Authoring Tools - Ways to represent a screen',
         '종이 스케치 · Figma · 간단한 화면 도식||Paper sketch · Figma · Simple screen outline')),
    chapter=3, pages=(13,22), layout='split', note='원본 와이어프레임의 목적을 유지하고 가상 UGC 전시 신청 화면으로 구체화. 화면의 미적 완성도보다 정보·행동·결과의 배치가 학습 대상. Figma 사용법 실습은 추가하지 않음.')

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

add('기획안 발표와 결과물 준비||Preparing the Project Pitch',
    '원페이저를 바탕으로 서비스의 목적과 구현 방향을 설명하는 발표||A Presentation of the Service’s Purpose and Build Direction Using the One-Pager',
    table('발표의 설명 순서||Presentation Sequence', ['순서||Order','설명 내용||Content'],
        ['서비스 소개||Introduce the Service','서비스명 · 대상 사용자 · 해결할 문제||Name · Target users · Problem'],
        ['가치와 기능||Explain Value and Features','핵심 가치 · 주요 기능 · 우선순위||Core value · Main features · Priorities'],
        ['사용 과정||Show the User Experience','핵심 사용 흐름 · 주요 화면 구상||The main flow and key screen ideas'],
        ['개발과 기대효과||Explain Execution and Impact','기술 · 개발 계획 · 성과 확인 방법||Technology · Development plan · Success measures']),
    {'type':'design_submission',
     'deadline_label':bi('제출 마감||Deadline'),
     'deadline':bi('10월 11일 23:59||October 11 · 23:59'),
     'items_label':bi('제출물||Deliverables'),
     'items':[bi('원페이저 PDF||One-Pager PDF'), bi('5분 이내 발표 영상의 유튜브 링크||YouTube link to a pitch video of up to five minutes')],
     'places_label':bi('제출처||Where to Submit'),
     'places':[
         [bi('아주BB||AjouBB'), bi('원페이저 PDF · 영상 링크||One-Pager PDF · Video link')],
         [bi('디스코드||Discord'), bi('영상 링크 업데이트||Post the video link')]]},
    chapter=4, pages=(26,27), note='2026년 10월 11일 23:59 제출 안내 반영. 아주BB에 원페이저 PDF와 유튜브 영상 링크를 제출하고, 디스코드에 영상 링크를 업데이트. 원본의 2025 날짜·배점은 사용하지 않음.')

assert len(slides) == 15, len(slides)  # Cover + 14 section topics; four chapter slides inserted by the page builder.
for path, data in [('design-sources.json', SOURCES), ('design-slides.json', slides), ('design-chapters.json', CHAPTER_LEADS)]:
    (ROOT/'materials'/path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

text = ['웹 서비스 설계 기초 · 2교시 재제작', '작성: 2026-09-23',
        '원본: [PWD Week9] 웹 서비스 설계 기초.pdf',
        '최종 HTML: ../ai-design.html · 표지·4개 챕터를 포함한 19장',
        '가상 서비스: NNN UGC Creator Hub. 사업성·수치·수익 배분·우선순위의 비평은 수업 범위에 포함하지 않음.',
        '보완: 핵심 용어의 비중 · 기획 작성 과정 · 원페이저 압축과 완성 예시', '']
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
        elif b['type']=='design_submission':
            text += [b['deadline_label'][0]+' - '+b['deadline'][0], b['items_label'][0]]
            text += ['- '+item[0] for item in b['items']]
            text += [b['places_label'][0]]
            text += ['- '+place[0][0]+': '+place[1][0] for place in b['places']]
        else: text.append(('화면 구성: '+b['type']+' '+b.get('mode','')).rstrip())
    text += [('원본 PDF: '+', '.join(map(str,slide['source_pages']))).rstrip(),('강의 메모: '+slide['note']).rstrip(),'']
assert number==19
(ROOT/'materials/week-04-service-planning.ko.txt').write_text('\n'.join(text).rstrip()+'\n')
print(f'Built {len(slides)} content records for the 19-slide service-planning lesson.')
