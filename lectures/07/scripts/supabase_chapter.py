"""Week 7 pages 45–55: student-level Supabase introduction.

The supplied research is reference material. Its proposed assignment does not
replace the existing FoodMap lab, and its estimated growth figures are omitted.
"""
import json
from design_examples import P, N, E, G, S, F, T

SB = 'https://supabase.com/docs/'
RESEARCH = 'materials/supabase/research.ko.md'
ARCH = SB+'guides/getting-started/architecture'
PRICING = 'https://supabase.com/pricing'
SLIDES = [dict(id='supabase', type='chapter',
    ko=dict(title='Supabase',lead='PostgreSQL을 활용한 쉬운 백엔드 개발',concepts=[]),
    en=dict(title='Supabase',lead='Accessible backend development with PostgreSQL',concepts=[]),
    source_urls=[RESEARCH,ARCH])]


def page(ident, ko, en, example, refs=(), note=''):
    title, lead, concepts = ko
    etitle, elead, econcepts = en
    item = dict(id='sb-'+ident,type='content',
        ko=dict(title=title,lead=lead,concepts=concepts),
        en=dict(title=etitle,lead=elead,concepts=econcepts),
        example=example,source_urls=[RESEARCH,*refs],
        note='공식 자료 확인: 2026-11-02. '+note)
    def figures(block):
        if block['kind']=='figure':
            return [{k:block[k] for k in ('src','alt','caption') if k in block}]
        return [fig for child in block.get('items',[]) for fig in figures(child)]
    item['source_figures']=figures(example)
    SLIDES.append(item)


logo = dict(kind='figure',src='materials/supabase/supabase-logo.svg',
    alt=P('Supabase 공식 로고','Official Supabase logo'),
    caption=P('Supabase 공식 워드마크','Official Supabase wordmark'))
page('overview',
 ('Supabase 개요','PostgreSQL에 백엔드 개발 기능을 더한 플랫폼',[
  ['Supabase','PostgreSQL 기반의 오픈소스 백엔드 개발 플랫폼','데이터베이스에 API·로그인·파일 저장 등의 기능을 결합'],
  ['BaaS(Backend as a Service)','공통 백엔드 기능을 서비스로 제공하는 방식','개발자가 필요한 기능을 선택해 앱과 연결']]),
 ('Supabase Overview','A platform that adds backend development features to PostgreSQL',[
  ['Supabase','An open-source backend platform built on PostgreSQL','Combines the database with APIs, login, and file storage'],
  ['BaaS (Backend as a Service)','Shared backend capabilities provided as a service','Developers select the capabilities their app needs']]),
 G(S(logo,E(P('Supabase의 데이터 기반','The data foundation of Supabase'),P('PostgreSQL의 테이블·키·관계를 그대로 활용','Use PostgreSQL tables, keys, and relationships'))),
   T(P('데이터베이스와 백엔드 플랫폼의 관계','Database and backend platform'),
     [P('대상','Product'),P('역할','Role')],
     [['PostgreSQL',P('데이터를 저장·처리하는 DBMS','The DBMS that stores and processes data')],
      ['Supabase',P('PostgreSQL과 백엔드 서비스를 함께 제공하는 플랫폼','A platform providing PostgreSQL and backend services')]],widths=(28,72)),cls='w7-sb-overview'),
 [ARCH,SB+'guides/database/overview','https://supabase.com/brand'],
 '공식 워드마크 SVG를 수정 없이 사용. PostgreSQL과 Supabase의 포함 관계를 설명하며 동급 DBMS 경쟁 제품으로 비교하지 않음.')

page('backend',
 ('백엔드의 반복 작업','공통 기능을 직접 구축하는 부담을 줄이는 BaaS',[
  ['공통 기반','여러 웹서비스에서 반복해서 필요한 백엔드 기능','데이터 저장·회원 로그인·파일 보관처럼 자주 등장하는 작업'],
  ['역할 분담','공통 기능은 서비스로 활용하고 앱 고유 기능은 직접 구현','데이터 구조·화면·업무 규칙은 개발자의 설계 영역']]),
 ('Repeated Backend Work','BaaS reduces the work of building common backend capabilities',[
  ['Shared needs','Backend capabilities required by many web services','Recurring needs such as data storage, login, and file handling'],
  ['Responsibilities','Use shared services and implement the app’s own features','Developers still design data structures, screens, and business rules']]),
 T(P('맛집 서비스에서 필요한 작업의 예','Example tasks for a restaurant app'),
   [P('필요한 작업','Task'),P('직접 구축할 때','When building it yourself'),P('Supabase를 활용할 때','With Supabase')],
   [[P('식당 정보 저장','Store data'),P('DB 서버 설치·관리','Install and manage a database'),P('관리형 PostgreSQL 이용','Use managed PostgreSQL')],
    [P('회원 로그인','User login'),P('인증 기능 구현·연동','Build or integrate authentication'),P('Auth 연결','Connect Auth')],
    [P('사진 업로드','Photo upload'),P('파일 보관 서비스 구성','Set up a file storage service'),P('Storage 연결','Connect Storage')],
    [P('맛집 추천 규칙','App rules'),P('앱에 맞게 직접 구현','Implement rules for the app'),P('앱에 맞게 직접 구현','Implement rules for the app')]],widths=(24,38,38)),
 [ARCH,SB+'guides/auth',SB+'guides/storage'],
 '각 기능은 역할을 미리 살펴보는 예이며 설치·SDK 사용법을 앞당겨 설명하지 않음. Supabase가 모든 서버 코드나 업무 로직을 자동으로 작성한다는 의미가 아님. 현재 FoodMap에 Auth·Storage를 추가하지 않음.')

page('history',
 ('Supabase의 출발과 성장','PostgreSQL을 쉽게 쓰려는 목표에서 출발한 오픈소스 플랫폼',[
  ['출발','2020년 Paul Copplestone·Ant Wilson이 시작한 프로젝트','Firebase 대안이라는 메시지로 관계형 DB 기반의 개발 편의성 제시'],
  ['발전','공개 개발과 사용자 피드백을 통한 플랫폼 개선','기능 공개와 문서·사례 공유를 통해 커뮤니티 확대']]),
 ('Supabase History','An open-source platform created to make PostgreSQL easier to use',[
  ['Origin','A project started in 2020 by Paul Copplestone and Ant Wilson','Positioned as a Firebase alternative with a relational database foundation'],
  ['Development','Improve the platform through open development and user feedback','Public releases, documentation, and examples help the community grow']]),
 S(F(E(P('2020 · 개발 시작','2020 · Development begins'),P('PostgreSQL 기반 백엔드 플랫폼','A PostgreSQL-based backend platform')),
     E(P('2024.04 · 정식 서비스','2024.04 · General Availability'),P('GA 발표','GA announced')),
     E(P('2026.04 · 커뮤니티','2026.04 · Community'),P('GitHub 별 10만 개 달성 발표','100,000 GitHub stars announced'))),
   T(P('초기 목표의 두 요소','Two parts of the initial goal'),[P('요소','Part'),P('의미','Meaning')],
     [[P('간편한 개발 경험','Convenient development'),P('앱 개발에 필요한 공통 백엔드 기능 제공','Provide the common backend capabilities apps need')],
      [P('관계형 데이터 기반','Relational data'),P('PostgreSQL의 테이블·SQL·관계 활용','Use PostgreSQL tables, SQL, and relationships')]],widths=(30,70))),
 ['https://supabase.com/blog/supabase-how-we-launch','https://www.ycombinator.com/companies/supabase',
  'https://supabase.com/ga','https://supabase.com/blog/100000-github-stars',ARCH],
 '개발 시작은 2020년 1월, GA는 2024-04-15, GitHub 별 10만 발표는 2026-04-02. 별 개수는 발표 당시 커뮤니티 관심 지표이며 현재 사용자 수·시장점유율·매출이 아님. Firebase는 배경 맥락으로만 소개하고 다른 제품군 전체를 Firestore 하나로 단정하지 않음.')

page('services',
 ('Supabase의 주요 기능','한 프로젝트에서 필요한 백엔드 기능을 선택하는 구성',[
  ['프로젝트','데이터베이스와 관련 서비스를 관리하는 기본 단위','Dashboard에서 테이블·사용자·파일·설정 확인'],
  ['기능 선택','앱의 요구에 맞게 백엔드 서비스를 조합하는 방식','기본 데이터 저장에서 로그인·실시간 기능까지 필요한 범위만 활용']]),
 ('Supabase Services','Select backend capabilities within a project',[
  ['Project','A unit for managing a database and related services','Use the Dashboard to inspect tables, users, files, and settings'],
  ['Selection','Combine backend services to match the app’s needs','Choose the needed scope, from data storage to login and live updates']]),
 T(P('서비스의 역할과 활용 사례','Service roles and examples'),
   [P('기능','Service'),P('역할','Role'),P('활용 예','Example')],
   [['Database · Data API',P('테이블 저장·HTTP 데이터 접근','Table storage and HTTP data access'),P('식당 목록 조회','Read a restaurant list')],
    ['Auth',P('회원가입·로그인','Sign-up and sign-in'),P('사용자 계정','User accounts')],
    ['Storage',P('파일 보관·전달','Store and serve files'),P('프로필 사진·첨부파일','Profile photos and attachments')],
    ['Realtime',P('연결된 앱에 변경·메시지 전달','Deliver changes and messages to connected apps'),P('채팅·공동 작업','Chat and collaboration')],
    ['Edge Functions',P('서버 측 함수 실행','Run server-side functions'),P('외부 API 호출','Call an external API')]],widths=(27,40,33)),
 [ARCH,SB+'guides/api',SB+'guides/auth',SB+'guides/storage',SB+'guides/realtime',SB+'guides/functions'],
 '기능 지도이며 내부 서비스의 물리적 배치도가 아님. Realtime은 구독·연결·권한 및 앱의 화면 갱신 처리가 필요. Storage 파일 본문과 DB의 파일 메타데이터를 구별. 상세 설치·함수 작성법은 실습 범위에 추가하지 않음.')

RESTAURANTS_KO = [dict(id=11,name='아주식당'),dict(id=12,name='캠퍼스분식')]
RESTAURANTS_EN = [dict(id=11,name='Ajou Diner'),dict(id=12,name='Campus Bunsik')]
page('api',
 ('테이블과 자동 API','데이터베이스 구조를 바탕으로 만들어지는 데이터 접근 창구',[
  ['Data API','테이블 데이터를 HTTP로 조회·변경하는 인터페이스','테이블 구조를 바탕으로 기본 데이터 API 제공'],
  ['앱과의 연결','앱의 요청을 API가 받아 PostgreSQL 데이터에 접근','접근 권한을 확인한 뒤 결과를 JSON으로 반환']]),
 ('Tables and Automatic APIs','Data access generated from the database structure',[
  ['Data API','An interface to read and change table data over HTTP','Basic data APIs are provided from the table structure'],
  ['App connection','The API receives an app request and accesses PostgreSQL','Checks access permissions and returns the result as JSON']]),
 S(F(E(P('앱의 조회 요청','App read request')),E(P('Supabase Data API')),E(P('PostgreSQL 테이블','PostgreSQL table'))),
   G(T(P('조회 대상 · restaurants 예시','Example table · restaurants'),['id','name'],[[11,P('아주식당','Ajou Diner')],[12,P('캠퍼스분식','Campus Bunsik')]]),
     dict(kind='code',language='json',caption=P('id·name을 선택한 JSON 응답 예','Example JSON response selecting id and name'),
          code=P(json.dumps(RESTAURANTS_KO,ensure_ascii=False,indent=2),json.dumps(RESTAURANTS_EN,indent=2))))),
 [SB+'guides/api',SB+'guides/api/securing-your-api'],
 '테이블 권한과 행 정책이 조회를 허용한 경우의 설명용 데이터. 필드는 id·name만 선택한 투영이며 정렬 순서는 이 예시에서 id 오름차순을 가정. 원고의 posts SDK 코드는 전제 개념을 늘리지 않도록 표·요청 흐름·JSON으로 대체. 실제 실습은 브라우저→기존 Express API→Data API→DB이며 위 직접 접근 경로도 가능한 일반 구성임. 네트워크 요청을 실제 실행한 결과가 아님.')

page('auth',
 ('사용자 로그인','Supabase Auth로 앱의 사용자를 확인하는 과정',[
  ['Auth','회원가입과 로그인 기능을 제공하는 인증 서비스','이메일·비밀번호 또는 외부 계정 등으로 사용자 확인'],
  ['로그인 상태','앱이 인증된 사용자를 식별할 수 있는 상태','로그인 결과의 사용자 ID로 개인화된 화면 구성']]),
 ('User Login','Identify app users with Supabase Auth',[
  ['Auth','An authentication service for sign-up and sign-in','Identify users through email and password or an external account'],
  ['Signed-in state','A state in which the app can identify an authenticated user','Use the resulting user ID to personalize the screen']]),
 S(F(E(P('로그인 정보 입력','Enter login details'),P('이메일·비밀번호','Email and password')),
     E(P('Supabase Auth'),P('사용자 확인','Verify the user')),
     E(P('앱에 로그인 상태 전달','Return signed-in state'),P('사용자 ID: U1','User ID: U1'))),
   T(P('같은 앱의 화면 표시 예','Example screen content in the same app'),[P('상태','State'),P('확인된 사용자','Identified user'),P('화면 표시','Screen content')],
     [[P('로그인 전','Signed out'),P('없음','None'),P('로그인 버튼','Sign-in button')],
      [P('로그인 후','Signed in'),'U1',P('민지님 · 로그아웃','Minji · Sign out')]],widths=(25,27,48))),
 [SB+'guides/auth'],
 'U1은 사용자 UUID를 단순화한 표기. 인증된 사용자 정보로 UI를 바꾸는 예이며 로그인만으로 모든 데이터 접근이 허용되거나 차단된다는 뜻이 아님. JWT·세션 갱신·OAuth 프로토콜 내부 설명은 제외. 현재 FoodMap에 Auth를 추가하지 않음.')

NOTES = [dict(id=1,owner_id='U1',content=P('점심 맛집 기록','Lunch restaurant notes')),
         dict(id=2,owner_id='U2',content=P('친구와 갈 식당','Restaurants to visit with friends'))]
page('rls',
 ('행별 데이터 접근','로그인한 사용자에게 허용된 행만 보여주는 규칙',[
  ['RLS(Row Level Security)','테이블의 각 행에 접근 규칙을 적용하는 기능','로그인 정보와 행의 소유자 값을 비교해 접근 범위 결정'],
  ['접근 설정','테이블 권한과 행 정책을 함께 설정하는 구조','조회·등록·수정 등 작업별로 허용할 범위 설계']]),
 ('Row-Level Data Access','Rules that expose only the rows a signed-in user may access',[
  ['RLS (Row Level Security)','A feature that applies access rules to individual table rows','Compare signed-in user information with row ownership to decide access'],
  ['Access settings','Table privileges and row policies work together','Design the allowed scope for reads, inserts, updates, and other operations']]),
 S(F(E(P('현재 로그인한 사용자','Signed-in user'),P('U1 · 민지','U1 · Minji')),
     E(P('개인 메모의 조회 정책 예','Example policy for private notes'),P('소유자 ID = 로그인 사용자 ID','Owner ID = signed-in user ID'))),
   T(P('U1의 행별 조회 판정 · 테이블 조회 권한 보유','Row access decisions · U1 has table read permission'),
     ['id',P('소유자','Owner'),P('내용','Content'),P('U1의 조회','U1 reads')],
     [[n['id'],n['owner_id'],n['content'],P('허용','Allow') if n['owner_id']=='U1' else P('제외','Exclude')] for n in NOTES],
     marks=((0,3,'good'),(1,3,'bad')),widths=(10,18,49,23)),
   N('관리자용 비밀 키는 서버에서 보관','Keep administrative secret keys on the server')),
 [SB+'guides/database/postgres/row-level-security',SB+'guides/api/api-keys'],
 'RLS 활성화·해당 역할의 SELECT 권한·자기 행 조회 정책을 설정한 비우회 사용자 요청의 예. RLS만 설정하면 테이블 권한이나 서버 측 검사 전체를 대체한다는 의미가 아님. U1/U2는 UUID의 설명용 약식 표기. service_role·secret key는 RLS를 우회할 수 있으므로 클라이언트에 노출하지 않음. 실제 실습의 서버 전용 키·권한 구성을 변경하지 않음.')

page('adoption',
 ('Supabase의 대중화 배경','익숙한 기술과 쉬운 시작이 맞물린 도입 배경',[
  ['도입 장벽','새 서비스를 시작할 때 필요한 학습·구축 부담','PostgreSQL 지식과 통합 서비스를 활용해 초기 작업량 감소'],
  ['확산 환경','오픈소스·문서·커뮤니티를 통한 사용 경험 공유','무료 시작과 공개 예제가 학습·시제품 제작의 기회 확대']]),
 ('Why Supabase Spread','Familiar technology and an accessible starting point',[
  ['Adoption barrier','The learning and setup work needed to start a service','Use PostgreSQL knowledge and integrated services to reduce initial work'],
  ['Community','Open source, documentation, and shared experience','A free starting point and public examples support learning and prototyping']]),
 T(P('도입을 돕는 요인과 구체적 의미','Adoption factors and what they offer'),
   [P('요인','Factor'),P('개발자가 얻는 점','Developer benefit'),P('사례','Example')],
   [['PostgreSQL',P('기존 관계형 데이터 지식 활용','Reuse relational data knowledge'),P('배운 테이블·키·관계 적용','Apply tables, keys, and relationships')],
    [P('통합 기능','Integrated services'),P('공통 기능의 구축 작업 감소','Less setup for common capabilities'),P('자동 API·로그인 활용','Use automatic APIs and login')],
    [P('오픈소스·커뮤니티','Open source and community'),P('자료·코드·문제 해결 경험 공유','Share code, documentation, and solutions'),P('공식 예제로 작은 앱 제작','Build a small app from official examples')],
    [P('무료 시작','Free starting point'),P('작은 규모로 시험할 기회','Try a project at a small scale'),P('수업 프로젝트·시제품','Course projects and prototypes')]],widths=(26,39,35)),
 [ARCH,'https://supabase.com/ga','https://supabase.com/blog/100000-github-stars',PRICING],
 '제공 조사 문서의 보급 요인을 공식 제품 기능·커뮤니티 발표와 연결한 설명. 각 요인의 인과 효과를 통계적으로 검증한 결과가 아님. 외부 추정 ARR·초기 DB 수·AI 생성 비중은 제외. 오픈소스가 Cloud의 모든 운영 작업을 없애거나 한 번에 자체 호스팅으로 이전한다는 주장을 하지 않음.')

page('ai-tools',
 ('AI 개발 도구와의 연결','생성한 화면·코드를 실제 백엔드와 연결하는 개발 과정',[
  ['개발 도구 연결','AI 코딩 도구가 Supabase 프로젝트와 연동하는 환경','화면·데이터 구조·연결 코드 작성을 돕는 기능 제공'],
  ['개발자 검증','생성된 결과가 요구사항에 맞는지 확인하는 작업','데이터 구조·권한·동작·사용량을 개발자가 검토']]),
 ('Connecting AI Development Tools','Connect generated screens and code to a real backend',[
  ['Tool connection','An environment linking an AI coding tool to a Supabase project','Tools assist with screens, data structures, and connection code'],
  ['Developer review','Check whether generated results meet the requirements','Developers review structures, access, behavior, and usage']]),
 G(F(E(P('요구사항 설명','Describe the requirement'),P('맛집 목록을 보여주는 앱','An app showing a restaurant list')),
     E(P('AI 도구의 코드 작성','AI-assisted code writing')),
     E(P('Supabase 연결','Connect Supabase')),
     E(P('개발자 확인 후 배포','Review, then deploy')),vertical=True),
   T(P('생성 결과를 확인하는 사례','Example checks for generated results'),[P('대상','Area'),P('확인할 내용','What to check')],
     [[P('데이터','Data'),P('식당 이름·주소가 요구한 열에 저장되는지','Names and addresses are stored in the intended columns')],
      [P('접근 권한','Access'),P('다른 사용자의 개인 메모가 보이지 않는지','Another user’s private notes remain inaccessible')],
      [P('화면 동작','App behavior'),P('조회 결과·오류·빈 목록이 올바르게 표시되는지','Results, errors, and empty lists display correctly')]],widths=(26,74))),
 [SB+'guides/ai-tools',SB+'guides/database/postgres/row-level-security'],
 'AI 개발 워크플로의 설명용 구성. MCP 프로토콜·자동 마이그레이션·임베딩·RAG 내부는 제외. 특정 도구의 자동 처리나 시장 표준 지위를 보장하지 않음. 연결이 가능한 기능과 실제 개발자 검증 책임을 구별하며 실제 프로젝트에 도구를 연결하지 않음.')

page('cost',
 ('무료 시작과 사용량 관리','작은 프로젝트의 시작 조건과 서비스 사용량의 구분',[
  ['무료 플랜','학습·시제품을 시작할 수 있는 요금제','저장 공간과 사용량에 정해진 한도 적용'],
  ['운영 비용','프로젝트 자원과 서비스 사용량에 따라 달라지는 비용','규모가 커질 때 요금제·사용량·백업 조건 확인']]),
 ('Starting Free and Managing Usage','Distinguish a small project’s starting conditions from ongoing usage',[
  ['Free plan','A plan for starting learning projects and prototypes','Storage and usage remain subject to limits'],
  ['Operating cost','Costs depend on project resources and service usage','Review the plan, usage, and backup terms as the service grows']]),
 G(T(P('무료 플랜의 주요 조건 · 2026-11-02 확인','Selected Free plan terms · checked 2026-11-02'),
     [P('항목','Item'),P('공식 안내','Published term')],
     [[P('기본 요금','Base price'),P('월 US$0','US$0 / month')],[P('DB 크기','DB size'),'500 MB'],
      [P('파일 저장','File storage'),'1 GB'],[P('비활성 프로젝트','Inactive project'),P('1주 비활성 후 일시 정지','Paused after 1 week of inactivity')]],widths=(40,60)),
   T(P('맛집 서비스에서 사용량이 늘어나는 예','Example usage growth in a restaurant app'),
     [P('변화','Change'),P('관련 사용량','Related usage')],
     [[P('식당·메모 행 증가','More restaurant and note rows'),P('DB 저장 공간','Database storage')],
      [P('업로드 사진 증가','More uploaded photos'),P('파일 저장 공간','File storage')],
      [P('사진 조회 증가','More photo views'),P('데이터 전송량','Data transfer')]],widths=(56,44))),
 [PRICING],
 '공식 가격표를 2026-11-02 확인한 일부 조건. 모든 무료 한도·지원 기능을 나열한 표가 아니며 요금·정책은 변경 가능. 무료 한도 초과가 자동 유료 전환이나 모든 항목의 자동 과금이라는 의미가 아님. 현재 과제의 Storage 도입이나 유료 플랜 가입을 요구하지 않음.')

assert len(SLIDES)==11
