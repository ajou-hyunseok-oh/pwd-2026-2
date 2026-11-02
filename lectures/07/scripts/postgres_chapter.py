"""Week 7 pages 36–44: PostgreSQL introduction with student-level examples.

Based on the supplied November 2026 research text and checked primary sources.
Examples are illustrative, not new requirements for the FoodMap practice.
"""
import json
from design_examples import P, N, E, G, S, F, T

PG = 'https://www.postgresql.org/'
DOC = PG+'docs/current/'
SURVEY = 'https://survey.stackoverflow.co/2025/technology/'
VECTOR = 'https://github.com/pgvector/pgvector'
POSTGIS = 'https://postgis.net/'
RESEARCH = 'materials/postgresql-research.ko.txt'
SLIDES = [dict(id='postgres', type='chapter',
    ko=dict(title='PostgreSQL', lead='기술적 특징과 대중화 배경', concepts=[]),
    en=dict(title='PostgreSQL', lead='Technology and the reasons behind its adoption', concepts=[]),
    source_urls=[RESEARCH, PG+'about/'])]


def page(ident, ko, en, example, refs=(), note=''):
    title, lead, concepts = ko
    etitle, elead, econcepts = en
    item = dict(id='pg-'+ident, type='content',
        ko=dict(title=title,lead=lead,concepts=concepts),
        en=dict(title=etitle,lead=elead,concepts=econcepts),
        example=example, source_urls=[RESEARCH,*refs],
        note='공식 자료 확인: 2026-11-02.'+(' '+note if note else ''))
    def figures(block):
        if block['kind'] == 'figure':
            return [{k:block[k] for k in ('src','alt','caption')}]
        return [fig for child in block.get('items',[]) for fig in figures(child)]
    item['source_figures'] = figures(example)
    SLIDES.append(item)


logo = dict(kind='figure',src='materials/postgresql/elephant.png',
    alt=P('PostgreSQL 공식 코끼리 로고 Slonik','Official PostgreSQL elephant logo, Slonik'),
    caption=P('PostgreSQL® · Slonik','PostgreSQL® · Slonik'))

page('overview',
 ('PostgreSQL 개요','관계형 모델에 다양한 자료형과 확장 기능을 결합한 DBMS',[
  ['PostgreSQL','오픈소스 객체 관계형 데이터베이스 관리 시스템(ORDBMS)','SQL 기반 테이블 처리와 사용자 정의 자료형·함수 지원'],
  ['활용 범위','일반 서비스 데이터에서 공간·AI 데이터까지 처리','JOIN·집계·윈도 함수·CTE 등 복합 질의 기능 제공']]),
 ('PostgreSQL Overview','A DBMS combining relational data with rich types and extensions',[
  ['PostgreSQL','An open-source object-relational DBMS (ORDBMS)','SQL tables combined with custom types and functions'],
  ['Scope','Service data, geospatial data, and AI applications','Joins, aggregates, window functions, and CTEs for complex queries']]),
 G(S(logo,F(E(P('응용 프로그램','Application')),E(P('PostgreSQL')))),
   T(P('활용 분야와 저장 대상','Applications and the data they manage'),
     [P('분야','Domain'),P('데이터·기능의 예','Example data or capability')],
     [[P('웹서비스·SaaS','Web services / SaaS'),P('계정·콘텐츠·주문·구독','Accounts, content, orders, subscriptions')],
      [P('기업 업무','Business systems'),P('재고·회계·업무 기록','Inventory, accounting, business records')],
      [P('게임 백엔드','Game backends'),P('계정·아이템·결제 기록','Accounts, items, purchase records')],
      [P('위치 기반 서비스','Location-based services'),P('좌표·거리·영역 연산','Coordinates, distances, spatial regions')],
      [P('AI 애플리케이션','AI applications'),P('임베딩 저장·문서 유사도 검색','Embeddings and document similarity')]]),cls='w7-pg-overview'),
 [PG+'about/',PG+'about/featurematrix/',PG+'about/press/presskit18/',PG+'about/policies/trademarks/'],
 '공식 로고 원본을 수정 없이 사용. PostgreSQL 및 Slonik은 PostgreSQL Community Association of Canada의 상표. 프로젝트의 후원·공인을 뜻하지 않음.')

page('history',
 ('PostgreSQL의 발전','Berkeley 연구 프로젝트에서 커뮤니티와 확장 생태계로',[
  ['기원','1986년 UC Berkeley의 POSTGRES 연구 프로젝트','Michael Stonebraker 주도로 구현 시작'],
  ['발전 방식','공개 소스와 커뮤니티를 통한 지속적인 기능 개선','연구 기반의 기술이 범용 서비스와 새로운 데이터 처리로 확대']]),
 ('PostgreSQL Evolution','From Berkeley research to a community and extension ecosystem',[
  ['Origins','The POSTGRES research project at UC Berkeley in 1986','Implementation began under Michael Stonebraker'],
  ['Development','Continuing improvements through open code and community work','Research technology expanded into services and new data workloads']]),
 G(F(E(P('1986 · POSTGRES'),P('Berkeley 연구 프로젝트','Berkeley research project')),
     E(P('1994~1995 · Postgres95','1994–1995 · Postgres95'),P('SQL 도입과 공개 배포','SQL support and public release')),
     E(P('1996 · PostgreSQL'),P('SQL을 반영한 명칭 채택','Name reflecting SQL support')),vertical=True),
   T(P('후속 발전의 사례','Examples of later development'),[P('시기','Period'),P('발전 내용','Development')],
     [[2014,P('9.4 · JSONB 도입','9.4 · JSONB introduced')],
      [2016,P('9.6 · 병렬 질의 실행','9.6 · Parallel query execution')],
      [2017,P('10 · 논리적 복제','10 · Logical replication')],
      [P('2020년대','2020s'),P('관리형 클라우드·벡터 검색 생태계 확대','Managed cloud and vector-search ecosystems')]],widths=(23,77))),
 [DOC+'history.html',PG+'docs/9.4/release-9-4.html',PG+'docs/9.6/release-9-6.html',PG+'docs/10/release-10.html',VECTOR])

page('adoption',
 ('PostgreSQL의 사용 현황','개발자 설문과 생태계의 확산을 함께 읽는 관점',[
  ['개발자 선호','2025 Stack Overflow 설문의 DB 부문에서 높은 채택 의향','PostgreSQL은 사용 희망·지속 사용 선호 지표에서 최상위'],
  ['지표의 의미','설문 응답자의 경험과 의향을 측정한 결과','전체 데이터베이스 시장점유율과 구별']]),
 ('PostgreSQL Adoption','Read developer surveys alongside ecosystem growth',[
  ['Developer preference','Strong adoption interest in the 2025 Stack Overflow database survey','PostgreSQL leads the desired and admired database measures'],
  ['Meaning','Survey measures of respondents’ experience and intentions','Distinct from overall database market share']]),
 G(S(T(P('설문이 관찰하는 항목','What the survey observes'),
       [P('항목','Measure'),P('관찰 대상','What it describes')],
       [[P('사용 경험','Have used'),P('지난 1년의 개발 경험','Development experience in the past year')],
        [P('사용 희망','Want to use'),P('다음 1년의 사용 의향','Intention to use in the next year')],
        [P('지속 사용 선호','Admired'),P('기존 사용자의 계속 사용 의향','Existing users’ intention to continue')]],widths=(32,68)),
      N('조사 연도: 2025 · 비율은 조사 표본과 질문에 따라 달라지는 값',
        'Survey year: 2025; percentages depend on the sample and question')),
   S(F(E(P('낮은 도입 장벽·기술 신뢰성','Access and technical reliability')),
       E(P('개발자·기업의 채택','Developer and business adoption')),
       E(P('도구·클라우드·확장 증가','More tools, cloud services, extensions')),
       E(P('새 프로젝트의 도입 경로 확대','More paths for new projects')),vertical=True),
     N('확산 요인을 연결한 설명 모형','An explanatory model of adoption factors'))),
 [SURVEY],
 '공식 페이지의 2025 DB 부문 desired/admired 서술을 근거로 사용. 수치 비율이나 2026 결과를 임의로 제시하지 않음. 선순환은 제공 문서의 설명 모형이며 인과 효과를 실증한 결과가 아님.')

page('license',
 ('PostgreSQL 라이선스','소프트웨어 도입 비용과 서비스 운영 비용의 구분',[
  ['PostgreSQL License','사용·수정·재배포를 허용하는 허용적 오픈소스 라이선스','상업적 서비스에도 PostgreSQL 자체 라이선스 요금 없음'],
  ['도입 효과','교육·개인 프로젝트·기업 서비스의 소프트웨어 접근성 확대','운영 규모가 커질 때의 인프라·관리 비용은 별도 발생']]),
 ('The PostgreSQL License','Separate software licensing from service operating costs',[
  ['PostgreSQL License','A permissive open-source license allowing use, changes, and redistribution','No PostgreSQL software license fee for commercial services'],
  ['Adoption','Accessible software for education, personal projects, and businesses','Infrastructure and management still incur costs as services grow']]),
 G(T(P('비용을 구성하는 항목','Components of cost'),[P('항목','Component'),P('비용의 성격','Cost characteristic')],
     [[P('PostgreSQL 소프트웨어','PostgreSQL software'),P('라이선스 요금 없음','No software license fee')],
      [P('서버·스토리지·네트워크','Compute, storage, network'),P('용량과 사용량에 따른 운영 비용','Operating costs depend on capacity and usage')],
      [P('백업·고가용성 구성','Backups and high availability'),P('보관·복제·추가 자원 비용','Retention, replication, extra resources')],
      [P('유지보수·관리형 서비스','Maintenance / managed services'),P('인력·지원·운영 서비스 비용','People, support, service costs')]],widths=(43,57)),
   S(E(P('도입 선택지','Deployment options'),P('로컬 설치 · 자체 서버 · 관리형 클라우드','Local installation · Self-managed server · Managed cloud')),
     F(E(P('자유로운 학습·시제품 제작','Learning and prototyping')),E(P('서비스 적용·운영','Service deployment and operation'))),
     N('소프트웨어의 개방성은 운영 비용 전체가 0원이라는 의미가 아님',
       'Open software does not make the total cost of operation zero'))),
 [PG+'about/licence/',PG+'about/press/presskit18/'],
 '라이선스 요금과 운영 자원 비용의 일반적 구분. 확장 모듈과 클라우드 서비스의 라이선스·요금 조건은 별도.')

page('transactions',
 ('함께 처리하는 데이터 변경','주문 기록과 재고 변경을 하나로 묶는 트랜잭션',[
  ['트랜잭션(Transaction)','여러 데이터 변경을 하나로 묶는 처리 단위','묶인 변경을 모두 반영하거나 모두 취소'],
  ['사용 목적','일부 변경만 남는 문제 방지','주문 기록과 재고 차감처럼 함께 맞아야 하는 데이터에 적용']]),
 ('Related Data Changes','A transaction groups an order record with a stock change',[
  ['Transaction','A unit of work that groups several data changes','Apply all grouped changes or cancel them all'],
  ['Purpose','Prevent an operation from being only partly applied','Use for related changes, such as recording an order and reducing stock']]),
 S(F(E(P('처리 전','Before'),P('재고 5개 · 주문 0건','Stock: 5 · Orders: 0')),
     E(P('한 트랜잭션으로 처리','One transaction'),P('주문 1건 기록 + 재고 1개 차감','Record one order + reduce stock by one'))),
   T(P('주문 1건의 처리 결과','Results of processing one order'),
     [P('상황','Outcome'),P('남은 재고','Stock'),P('주문 기록','Order records')],
     [[P('두 변경 모두 성공 → 함께 반영','Both changes succeed → apply both'),4,P('1건','1 order')],
      [P('처리 중 오류 → 둘 다 취소','An error occurs → cancel both'),5,P('0건','0 orders')]],
     marks=((0,1,'good'),(0,2,'good'),(1,1,'repeat'),(1,2,'repeat')),widths=(56,22,22))),
 [DOC+'tutorial-transactions.html'],
 '트랜잭션의 전부 반영/전부 취소만 다루는 입문 예제. 애플리케이션에서 두 변경을 같은 트랜잭션으로 묶는 조건. ACID 네 성질·격리 수준·MVCC·잠금은 학습 범위에서 제외. 실제 주문 기능이나 스키마 변경 없음.')

DETAILS = {'seats':24,'parking':True,'tags':['vegetarian']}
page('jsonb',
 ('JSON 부가 정보 저장','테이블의 기본 정보에 다양한 속성을 추가하는 방식',[
  ['JSON','이름과 값의 쌍으로 정보를 묶는 데이터 형식','문자·숫자·참/거짓·목록 등을 하나의 값으로 표현'],
  ['JSONB','PostgreSQL에서 JSON 데이터를 저장·검색하는 자료형','식별자·이름은 일반 열로, 추가 속성은 JSONB 열로 구성 가능']]),
 ('Storing Extra Details as JSON','Add varied attributes alongside the basic data in a table',[
  ['JSON','A data format that groups information as name–value pairs','A value can contain text, numbers, true/false values, and lists'],
  ['JSONB','A PostgreSQL type for storing and searching JSON data','Use regular columns for IDs and names, and a JSONB column for extra details']]),
 G(S(T(P('식당 한 행의 기본 정보','Basic data for one restaurant row'),['id','name'],[[11,P('아주식당','Ajou Diner')]]),
     T(P('details에 담긴 속성의 의미','Meaning of the attributes in details'),[P('이름','Name'),P('의미와 값','Meaning and value')],
       [['seats',P('좌석 수: 24석','Seat count: 24')],
        ['parking',P('주차 가능: 참','Parking available: true')],
        ['tags',P('태그 목록: vegetarian','Tag list: vegetarian')]],widths=(25,75))),
   dict(kind='code',language='json',caption=P('아주식당의 details 열 값 · JSONB','Ajou Diner’s details column value · JSONB'),
        code=P(json.dumps(DETAILS,indent=2)))),
 [DOC+'datatype-json.html'],
 '한 식당 행에 id·name 일반 열과 details JSONB 열이 있다고 가정한 개념 예제. 필수 관계·키를 모두 JSON으로 대체하는 설계 지침이 아님. JSONB 이진 저장·인덱싱·JSON과의 성능 비교는 제외. 실제 restaurants 스키마는 수정하지 않음.')

SPATIAL_POINTS = [dict(x=0,y=-300,inside=True,label=P('A · 300 m')),
                  dict(x=600,y=0,inside=False,label=P('B · 600 m')),
                  dict(x=0,y=400,inside=True,label=P('C · 400 m'))]
page('extensions',
 ('필요한 기능의 확장','주변 맛집 검색으로 이해하는 PostgreSQL 확장',[
  ['확장(Extension)','데이터베이스에 필요한 기능을 더하는 추가 모듈','기본 PostgreSQL에 설치해 특정 분야의 기능을 추가'],
  ['PostGIS','위치·거리·영역을 다루는 공간정보 확장','식당 위치와 사용자 위치를 바탕으로 가까운 식당 검색']]),
 ('Adding Features with Extensions','Understand PostgreSQL extensions through nearby restaurant search',[
  ['Extension','An extra module that adds capabilities to a database','Install it in PostgreSQL to add features for a specific domain'],
  ['PostGIS','An extension for locations, distances, and regions','Find nearby restaurants using restaurant and user locations']]),
 G(dict(kind='spatial',title=P('현재 위치를 중심으로 한 거리 예시','Example distances from the current location'),points=SPATIAL_POINTS),
   T(P('500 m 이내의 식당 검색','Searching for restaurants within 500 m'),
     [P('식당','Restaurant'),P('거리','Distance'),P('결과','Result')],
     [['A','300 m',P('포함','Include')],['B','600 m',P('제외','Exclude')],['C','400 m',P('포함','Include')]],
     marks=((0,2,'good'),(1,2,'bad'),(2,2,'good')),widths=(26,28,46))),
 [POSTGIS,POSTGIS+'docs/ST_DWithin.html'],
 'PostGIS의 거리 조건 검색을 바탕으로 자체 구성한 평면 좌표(m) 모식도. A(0,-300)·C(0,400)는 반경 500m 안, B(600,0)는 밖. 실제 지도·위경도 측정 결과가 아님. 확장 설치·SQL 함수·좌표계·인덱스는 설명하지 않음. 다른 확장 나열과 pgvector·RAG 내용 제외.')

page('cloud',
 ('관리형 PostgreSQL','직접 설치하는 대신 클라우드에서 데이터베이스를 이용하는 방식',[
  ['관리형 서비스','데이터베이스 설치와 운영 도구를 제공하는 서비스','웹 관리 화면에서 데이터베이스 생성과 상태 확인'],
  ['개발자 역할','저장할 데이터의 구조와 접근 범위 결정','테이블 설계·데이터 관리·사용자 권한 설정은 개발자의 작업']]),
 ('Managed PostgreSQL','Use a database in the cloud instead of installing it yourself',[
  ['Managed service','A service that provides database setup and operating tools','Create a database and check its status through a web dashboard'],
  ['Developer’s role','Decide the data structure and who can access it','Developers still design tables, manage data, and configure permissions']]),
 G(T(P('직접 설치와 관리형 서비스','Self-managed installation and managed services'),
     [P('항목','Task'),P('직접 설치','Self-managed'),P('관리형 서비스','Managed service')],
     [[P('준비','Setup'),P('서버 준비·DB 설치','Prepare a server and install the DB'),P('서비스 화면에서 DB 생성','Create the DB in a dashboard')],
      [P('운영','Upkeep'),P('업데이트·백업 직접 구성','Configure updates and backups'),P('제공되는 운영 도구 활용','Use the provided operating tools')],
      [P('데이터 설계','Data design'),P('개발자가 결정','Developer decides'),P('개발자가 결정','Developer decides')]],widths=(20,40,40)),
   S(F(E(P('브라우저의 관리 화면','Web dashboard')),E(P('클라우드의 PostgreSQL','PostgreSQL in the cloud')),vertical=True),
     E(P('서비스의 예','Examples'),P('Supabase · Amazon RDS for PostgreSQL')),
     N('백업·관리 기능과 요금은 서비스·설정에 따라 차이',
       'Backup tools, management features, and costs depend on the service and configuration'))),
 ['https://supabase.com/docs/guides/database/overview',
  'https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html'],
 '관리형 서비스의 목적과 개발자 역할만 소개. 공급자별 엔진 분류·복제·패치 정책·이전 호환성은 제외. Supabase 플랫폼의 자세한 구성은 뒤의 기존 소개 장에서 다룸. 백업 이용 조건은 요금제와 설정에 따라 달라짐.')

assert len(SLIDES) == 9
