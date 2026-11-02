"""Concrete examples for the existing Week 7 design slides (11–35).

All row values are teaching data, not live Supabase query results.
Titles, leads, slide IDs, and order are preserved by apply().
"""
from copy import deepcopy


def P(ko, en=None):
    return (str(ko), str(ko) if en is None else str(en))


def N(ko, en=None, tone=''):
    return dict(kind='note', text=P(ko, en), **({'class':'w7-tone-'+tone} if tone else {}))


def E(title, *lines):
    return dict(kind='node', title=title, lines=list(lines))


def G(*items, cls=''):
    return dict(kind='grid', items=list(items), **({'class':cls} if cls else {}))


def S(*items):
    return dict(kind='stack', items=list(items))


def F(*items, vertical=False):
    return dict(kind='flow', items=list(items), **({'class':'w7-flow-vertical'} if vertical else {}))


def T(title, head, rows, keys=(), marks=(), widths=()):
    def pair(v):
        return v if isinstance(v, tuple) else P(v)
    return dict(kind='table', title=title, head=[pair(v) for v in head],
                rows=[[pair(v) for v in row] for row in rows], keys=list(keys),
                marks=list(marks), widths=list(widths))


def I(src, ko, en, caption=None):
    return dict(kind='figure', src='materials/source-figures/'+src,
                alt=P(ko,en), caption=caption)


R = P('식당ID', 'Rest. ID')
M = P('메뉴ID', 'Menu ID')
NAME = P('식당이름', 'Name')
PRICE = P('가격', 'Price')
REGION = P('지역코드', 'Region code')
REGION_NAME = P('지역이름', 'Region name')
AJOU = P('아주식당', 'Ajou Diner')
CAMPUS = P('캠퍼스분식', 'Campus Snacks')
MENU_ROWS = [[11,1,AJOU,7000], [11,2,AJOU,8000], [12,1,CAMPUS,6500], [13,1,AJOU,7500]]
RESTAURANTS = [[11,AJOU], [12,CAMPUS], [13,AJOU]]
REGION_ROWS = [[11,'A01',P('원천동','Woncheon')], [12,'A01',P('원천동','Woncheon')], [13,'A02',P('광교동','Gwanggyo')]]


def menu(title, rows=None, marks=(), keys=()):
    return T(title,[R,M,NAME,PRICE], MENU_ROWS if rows is None else rows,
             keys=keys,marks=marks,widths=(17,17,42,24))


def relation(left, right, label, counts):
    return dict(kind='relation', left=left, right=right, label=label, counts=counts)


EXAMPLES = {}

# 11: a concrete requirement is read alongside the original design diagram.
EXAMPLES['design-purpose'] = G(
    S(E(P('서비스 요구사항','Service requirement'),
        P('사용자가 식당 정보를 제보하고, 승인된 제보로 맛집 등록',
          'Users submit restaurant information; approved submissions can become restaurants')),
      T(P('요구사항과 설계 대상','Requirements and design decisions'),
        [P('요구','Requirement'),P('데이터로 표현할 내용','Data to represent')],
        [[P('제보 작성자','Submission author'),P('사용자와 제보의 연결','User–submission relationship')],
         [P('맛집 등록 내용','Restaurant registration'),P('식당 정보와 출처 제보','Restaurant details and source submission')]])),
    I('design-objective.png','현실 세계에서 개념·논리 모델과 데이터베이스로의 변환','From the real world to conceptual and logical models and a database'),
    cls='w7-grid-example-figure')

EXAMPLES['design-stages'] = G(
    T(P('같은 맛집 서비스의 단계별 산출물','Outputs for the same restaurant service'),
      [P('설계 단계','Stage'),P('산출물의 예','Example output')],
      [[P('개념적 설계','Conceptual'),P('사용자 — 작성 — 제보','User — creates — Submission')],
       [P('논리적 설계','Logical'),P('사용자·제보 테이블과 각 열','User and submission tables with columns')],
       [P('물리적 설계','Physical'),P('데이터 저장 위치와 조회 접근 경로','Storage organization and access paths')]],widths=(29,71)),
    I('design-process-lifecycle.png','설계의 세 단계와 데이터베이스 개발 생명주기','Three design stages and the database development lifecycle'),
    cls='w7-grid-example-figure')

EXAMPLES['conceptual'] = S(
    N('사용자가 식당을 제보하고, 승인된 제보로 맛집을 등록하는 서비스',
      'A service where users submit restaurants and approved submissions can be registered'),
    relation(E(P('사용자','User')),E(P('제보','Submission')),P('작성','creates'),('','')),
    relation(E(P('제보','Submission')),E(P('맛집','Restaurant')),P('승인 시 등록','registered upon approval'),('','')))

EXAMPLES['entity'] = F(E(P('엔티티: 식당','Entity: Restaurant')),
    S(E(P('인스턴스 1','Instance 1'),AJOU), E(P('인스턴스 2','Instance 2'),CAMPUS)))

EXAMPLES['attributes'] = G(
    T(P('아주식당 한 곳의 속성과 값','Attributes and values of one Ajou Diner'),
      [P('속성','Attribute'),P('값','Value')],
      [[P('이름','Name'),AJOU],[P('전화번호','Phone'),'031-000-0000'],[P('평점','Rating'),4]],widths=(38,62)),
    S(E(P('도메인 예제: 평점 1~5 정수','Example domain: integer ratings 1–5')),
      T(P('도메인에 따른 값의 판정','Checking values against the domain'),
        [P('값','Value'),P('판정','Decision')],[[4,P('허용: 범위 안의 정수','Allowed: integer in range')],[6,P('거부: 범위 초과','Rejected: out of range')]],marks=((0,1,'good'),(1,1,'bad'))),
      N('개념 예제의 범위 · 실제 실습 평점은 소수 허용','Teaching domain; practice ratings also allow decimals')))

EXAMPLES['relationship'] = S(
    relation(E(P('사용자','User')), E(P('제보','Submission')),P('작성','creates'),('','')),
    F(E(P('사용자 민수','User Minsu')),
      S(E(P('제보 101','Submission 101')),E(P('제보 102','Submission 102')))),
    N('관계 이름 “작성”은 사용자와 제보가 맺는 업무 의미','“Creates” names the business association between a user and a submission'))

EXAMPLES['cardinality'] = G(
    S(relation(E(P('사용자','User')),E(P('제보','Submission')),P('작성','creates'),('1','0..N')),
      T(P('인스턴스에 적용한 참여 규칙','Participation rules applied to instances'),
        [P('대상','Instance'),P('연결된 대상','Connected instances')],
        [[P('사용자 민수','User Minsu'),P('제보 101·102 → 2건','Submissions 101 and 102 → 2')],
         [P('사용자 지수','User Jisu'),P('제보 없음 → 0건 허용','No submissions → zero allowed')],
         [P('제보 101','Submission 101'),P('작성자 민수 → 정확히 1명','Author Minsu → exactly one')]]),
      N('1:1 제보–맛집 · 1:N 사용자–제보 · N:M 사용자–관심 맛집',
        '1:1 submission–restaurant · 1:N user–submission · N:M user–saved restaurant')),
    G(I('erd-cardinality-legend.png','관계의 최소·최대 개수와 필수·선택 기호','Symbols for minimum and maximum counts and optional or required participation'),
      I('erd-company-example.png','회사·직원·프로젝트의 관계 도식','Company, employee, and project relationships'),cls='w7-grid-legend'),
    cls='w7-grid-cardinality')

EXAMPLES['logical'] = G(
    S(F(E(P('식당','Restaurant'),P('이름 · 전화번호','Name · Phone')),
        E(P('restaurants','restaurants'),P('name · phone','name · phone'))),
      T(P('restaurants · 논리적 구조와 예시 행','restaurants · Logical structure and example rows'),
        ['name','phone'],[[AJOU,'031-000-0000'],[CAMPUS,'031-000-0001']]),
      N('엔티티는 테이블로, 속성은 열로 표현','Entities become tables; attributes become columns')),
    I('logical-model-mapping.png','엔티티·속성·관계와 테이블·열·키의 대응','Mapping entities, attributes, and relationships to tables, columns, and keys'),
    cls='w7-grid-example-figure')

EXAMPLES['primary-key'] = G(
    T(P('식당 · id로 구별한 정상 데이터','Restaurants · Valid rows identified by id'),['id','name'],RESTAURANTS,keys=(0,)),
    S(T(P('새 행의 기본 키 입력 판정','Primary-key checks for new rows'),
        [P('입력','Input'),P('결과','Result')],
        [['id = 11',P('거부: 기존 id와 중복','Rejected: id already exists')],['id = NULL',P('거부: 식별자 없음','Rejected: identifier missing')]],marks=((0,1,'bad'),(1,1,'bad'))),
      N('이름이 같은 두 식당도 서로 다른 id로 식별','Different ids identify restaurants even when names repeat','good')))

EXAMPLES['foreign-key'] = S(
    G(T(P('참조 대상: submissions','Referenced rows: submissions'),['id',P('제보 내용','Submission')],
        [[101,P('아주식당 제보','Ajou Diner report')],[102,P('캠퍼스분식 제보','Campus Snacks report')]],keys=(0,)),
      T(P('restaurants 등록 시도','Attempted restaurant inserts'),['id','submission_id',P('판정','Decision')],
        [[11,101,P('허용','Allowed')],[12,999,P('거부: 대상 없음','Rejected: no target')]],keys=(1,),marks=((0,2,'good'),(1,1,'bad'),(1,2,'bad')),widths=(15,38,47))),
    F(E(P('restaurants.submission_id')),E(P('submissions.id'))),
    N('참조 값의 존재 검사 · NULL 허용 여부와 참조 값의 중복 제한은 별도 규칙',
      'Checks reference existence; allowing NULL and restricting repeated references are separate rules'))

EXAMPLES['physical'] = S(
    T(P('조회 대상: category가 한식인 행','Target: rows whose category is Korean'),
      ['id','name','category'],[[11,AJOU,P('한식','Korean')],[12,CAMPUS,P('분식','Snacks')],[13,AJOU,P('한식','Korean')],[14,P('대학카페','Campus Cafe'),P('카페','Cafe')]],marks=((0,2,'good'),(2,2,'good'))),
    G(F(E(P('순차 탐색','Sequential scan')),E(P('모든 행 확인','Inspect all rows'),P('11 → 12 → 13 → 14'))),
      F(E(P('인덱스 경로','Index path')),E(P('한식 → 행 11·13','Korean → rows 11 and 13')))),
    N('같은 결과 · 다른 접근 경로 · 인덱스의 추가 저장·변경 비용과 조회 조건을 함께 고려',
      'Same results, different access paths; consider index storage, update cost, and query conditions'))

EXAMPLES['erd'] = S(
    relation(E(P('제보 · submissions','Submission · submissions'),P('id (PK)')),
             E(P('맛집 · restaurants','Restaurant · restaurants'),P('id (PK)'),P('submission_id (FK)')),
             P('출처 제보','source submission'),('1','0..1')),
    T(P('관계에 맞는 연결과 위반 사례','Valid connections and a relationship violation'),
      [P('제보','Submission'),P('연결된 맛집','Related restaurants'),P('판정','Decision')],
      [[101,P('맛집 11','Restaurant 11'),P('허용: 1개','Allowed: one')],
       [102,P('없음','None'),P('허용: 0개','Allowed: zero')],
       [103,P('맛집 12·13','Restaurants 12 and 13'),P('거부: 최대 1개 초과','Rejected: more than one')]],marks=((0,2,'good'),(1,2,'good'),(2,2,'bad'))),
    N('각 맛집은 출처 제보 1건 필수 · 제보당 연결된 맛집은 최대 1개',
      'Each restaurant requires one source submission; a submission can link to at most one restaurant'))

EXAMPLES['constraints'] = S(
    T(P('선언한 규칙에 따른 입력 판정','Input checks against declared rules'),
      [P('규칙','Rule'),P('허용 입력','Allowed input'),P('위반 입력','Invalid input'),P('위반 결과','Result')],
      [['NOT NULL · name',AJOU,'NULL',P('거부','Rejected')],
       ['UNIQUE · submission_id',P('미사용 102','Unused 102'),P('이미 사용한 101','Already-used 101'),P('거부','Rejected')],
       ['FK · submission_id',P('존재하는 101','Existing 101'),'999',P('거부','Rejected')],
       [P('CHECK · 평점 1~5','CHECK · rating 1–5'),4,6,P('거부','Rejected')]],marks=tuple((i,2,'bad') for i in range(4)),widths=(31,25,28,16)),
    N('NOT NULL은 빈 문자열을 허용 · CHECK로 NULL까지 거부하려면 NOT NULL도 필요',
      'NOT NULL permits empty strings; rejecting NULL with a range check also requires NOT NULL'),
    N('개념용 제약 예제 · 실습 스키마에 같은 규칙이 모두 정의된 것은 아님',
      'Illustrative constraints; the practice schema does not define all of these rules'))

EXAMPLES['integrity'] = S(
    T(P('위반 입력과 지켜야 할 데이터 상태','Invalid input and the data property to preserve'),
      [P('입력','Input'),P('깨지는 상태','Broken property'),P('무결성(Integrity)','Integrity')],
      [[P('id = 11 중복','id = 11 again'),P('서로 다른 행의 식별','Distinct row identity'),P('개체 무결성','Entity integrity')],
       ['submission_id = 999',P('실제로 존재하는 행과의 연결','Reference to an existing row'),P('참조 무결성(Referential Integrity)','Referential integrity')],
       ['rating = 6',P('평점 1~5라는 허용 범위','Allowed rating range of 1–5'),P('도메인 무결성(Domain Integrity)','Domain integrity')]],marks=((0,0,'bad'),(1,0,'bad'),(2,0,'bad')),widths=(29,40,31)),
    F(E(P('정상 데이터','Valid data')),E(P('위반 입력 거부','Reject invalid input')),E(P('기존 정상 상태 유지','Keep the valid state'))))

updated = deepcopy(MENU_ROWS)
updated[0][2] = P('아주밥집','Ajou Kitchen')
EXAMPLES['normalization'] = S(
    G(menu(P('변경 전: 식당 이름의 반복','Before: repeated restaurant name'),marks=((0,2,'repeat'),(1,2,'repeat'))),
      menu(P('한 행만 이름 수정: 같은 식당의 이름 불일치','After changing one row: inconsistent names'),updated,marks=((0,2,'bad'),(1,2,'repeat')))),
    G(N('삽입 이상(Insertion Anomaly): 메뉴 없이 식당 정보만 기록하기 어려운 구조',
        'Insertion anomaly: restaurant facts are tied to having a menu'),
      N('삭제 이상(Deletion Anomaly): 마지막 메뉴를 지우면 식당 정보도 함께 소멸',
        'Deletion anomaly: deleting the last menu also removes restaurant facts')))

EXAMPLES['functional-dependency'] = G(
    T(P('식당별 메뉴의 이름 결정 규칙','Name dependency in restaurant menus'),[R,M,NAME],
      [row[:3] for row in MENU_ROWS],marks=((0,0,'repeat'),(1,0,'repeat'),(0,2,'repeat'),(1,2,'repeat')),widths=(22,22,56)),
    S(F(E(P('식당ID = 11','Rest. ID = 11')),E(AJOU)),
      T(P('같은 결정자에 서로 다른 값','Conflicting values for one determinant'),[R,NAME],
        [[11,AJOU],[11,P('아주밥집','Ajou Kitchen')]],marks=((1,1,'bad'),)),
      N('이름이 같아도 식당ID는 다를 수 있음 · 역방향 종속은 보장하지 않음',
        'The same name can have different restaurant IDs; the reverse dependency is not guaranteed')))

EXAMPLES['superkey'] = G(
    T(P('식당 한 행 = 식당 한 곳','One restaurant row = one restaurant'),[R,NAME],RESTAURANTS),
    T(P('속성 집합별 식별 가능 여부','Can the attribute set identify a row?'),
      [P('속성 집합','Attribute set'),P('슈퍼키 판정','Superkey decision')],
      [[P('{식당ID}','{Rest. ID}'),P('가능','Yes')],
       [P('{식당ID, 식당이름}','{Rest. ID, Name}'),P('가능','Yes')],
       [P('{식당이름}','{Name}'),P('불가능: 같은 이름 존재','No: names repeat')]],marks=((0,1,'good'),(1,1,'good'),(2,1,'bad')),widths=(57,43)))

EXAMPLES['candidate-key'] = S(
    F(E(P('{식당ID, 식당이름}','{Rest. ID, Name}'),P('슈퍼키 · 이름 제거 가능','Superkey; name can be removed')),
      E(P('{식당ID}','{Rest. ID}'),P('후보 키 · 더 제거 불가','Candidate key; nothing removable')),
      E(P('{} · 속성 없음','{} · No attributes'),P('서로 다른 행의 식별 불가','Cannot distinguish rows'))),
    G(T(P('식당 데이터','Restaurant data'),[R,NAME],RESTAURANTS),
      T(P('유일성과 최소성','Uniqueness and minimality'),
        [P('집합','Set'),P('유일성(Uniqueness)','Unique'),P('최소성(Minimality)','Minimal')],
        [[P('{식당ID, 이름}','{ID, Name}'),P('충족','Yes'),P('미충족','No')],
         [P('{식당ID}','{ID}'),P('충족','Yes'),P('충족','Yes')]],marks=((0,2,'bad'),(1,2,'good')))))

EXAMPLES['prime-attribute'] = S(
    menu(P('식당별 메뉴 · 후보 키 {식당ID, 메뉴ID}','Restaurant menus · Candidate key {Rest. ID, Menu ID}'),keys=(0,1)),
    G(E(P('주요 속성','Prime attributes'),P('식당ID · 메뉴ID','Rest. ID · Menu ID')),
      E(P('비주요 속성','Non-prime attributes'),P('식당이름 · 가격','Name · Price'))),
    N('메뉴ID는 식당 안에서 유일 · 다른 식당에서는 같은 메뉴ID 사용 가능',
      'Menu IDs are unique within a restaurant and may repeat across restaurants'))

EXAMPLES['partial-dependency'] = G(
    menu(P('복합 후보 키 {식당ID, 메뉴ID}','Composite candidate key {Rest. ID, Menu ID}'),keys=(0,1),marks=((0,2,'repeat'),(1,2,'repeat'))),
    S(F(E(P('키의 일부: 식당ID','Part of key: Rest. ID')),E(NAME)),
      N('부분 종속: 메뉴가 달라도 같은 식당의 이름은 동일','Partial dependency: changing the menu does not change the restaurant name','bad'),
      F(E(P('키 전체: 식당ID + 메뉴ID','Whole key: Rest. ID + Menu ID')),E(PRICE)),
      N('전체 종속(Full Functional Dependency): 식당 11의 메뉴 1은 7000, 메뉴 2는 8000','Full dependency: restaurant 11 has prices 7000 for menu 1 and 8000 for menu 2')))

EXAMPLES['transitive-dependency'] = G(
    T(P('식당마다 반복된 지역 정보','Region facts repeated across restaurants'),[R,REGION,REGION_NAME],REGION_ROWS,keys=(0,),marks=((0,1,'repeat'),(1,1,'repeat'),(0,2,'repeat'),(1,2,'repeat')),widths=(25,30,45)),
    S(F(E(P('식당ID 11','Rest. ID 11')),E(P('지역코드 A01','Region code A01')),E(P('지역이름 원천동','Region name Woncheon')),vertical=True),
      N('지역코드가 지역이름을 결정 · 같은 지역의 식당에서 동일한 사실 반복',
        'Region code determines region name; restaurants in that region repeat the same fact')))

EXAMPLES['first-normal-form'] = S(
    G(T(P('분리 전: 전화번호 목록이 한 셀에 존재','Before: a phone list in one cell'),[R,P('전화번호','Phone')],
        [[11,'031-111-1111, 031-222-2222'],[12,'031-333-3333']],marks=((0,1,'repeat'),),widths=(23,77)),
      T(P('분리 후: 한 행에 전화번호 한 개','After: one phone number per row'),[R,P('전화번호','Phone')],
        [[11,'031-111-1111'],[11,'031-222-2222'],[12,'031-333-3333']],keys=(0,1),widths=(23,77))),
    N('이 모델의 값 단위: 전화번호 한 개 · 전화번호 표의 행 식별: {식당ID, 전화번호}',
      'Value unit: one phone number; a phone row is identified by {Rest. ID, Phone}'))

EXAMPLES['second-normal-form'] = G(
    menu(P('분리 전: 이름의 부분 종속','Before: name depends on part of the key'),keys=(0,1),marks=((0,2,'repeat'),(1,2,'repeat'))),
    S(T(P('식당 · 이름 저장','Restaurants · Names'),[R,NAME],RESTAURANTS,keys=(0,)),
      T(P('식당메뉴 · 가격 저장','Menus · Prices'),[R,M,PRICE],
        [[r[0],r[1],r[3]] for r in MENU_ROWS],keys=(0,1))),
    I('normalization-2nf.png','수강 등록 데이터의 부분 종속을 분리하는 원본 도식','Original diagram separating partial dependencies in course registrations',
      P('수강 등록의 2NF 분해 사례','2NF decomposition of course registrations')),
    cls='w7-grid-decomposition')

EXAMPLES['third-normal-form'] = G(
    T(P('분리 전: 지역코드를 거친 종속','Before: dependency through region code'),[R,REGION,REGION_NAME],REGION_ROWS,keys=(0,),marks=((0,2,'repeat'),(1,2,'repeat'))),
    S(T(P('식당 · 지역코드만 참조','Restaurants · Refer to a region code'),[R,REGION],[[r[0],r[1]] for r in REGION_ROWS],keys=(0,)),
      T(P('지역 · 코드별 이름 한 번 저장','Regions · Store each region name once'),[REGION,REGION_NAME],
        [['A01',P('원천동','Woncheon')],['A02',P('광교동','Gwanggyo')]],keys=(0,))),
    I('normalization-3nf.png','수강 등록 데이터의 이행 종속을 분리하는 원본 도식','Original diagram separating transitive dependencies in course registrations',
      P('수강 등록의 3NF 분해 사례','3NF decomposition of course registrations')),
    cls='w7-grid-decomposition')

EXAMPLES['bcnf'] = G(
    S(T(P('수강 · 학생·과목별 담당 교수 한 명','Enrollment · One professor per student and course'),
        [P('학생','Student'),P('과목','Course'),P('교수','Professor')],
        [['S1','DB','P1'],['S2','DB','P1'],['S1','WEB','P2'],['S3','DB','P3']],marks=((0,2,'repeat'),(1,2,'repeat'))),
      N('업무 규칙: 교수 한 명은 한 과목 담당 · 한 과목의 교수는 여러 명 가능',
        'Rule: each professor teaches one course; a course may have multiple professors')),
    S(E(P('함수 종속','Functional dependencies'),
        P('{학생, 과목} → 교수','{Student, Course} → Professor'),P('교수 → 과목','Professor → Course')),
      E(P('후보 키 2개 · 세 속성 모두 주요 속성','Two candidate keys; all three attributes are prime'),
        P('{학생, 과목} · {학생, 교수}','{Student, Course} · {Student, Professor}')),
      N('3NF 충족: 교수→과목의 오른쪽 과목이 주요 속성',
        '3NF satisfied: Course on the right of Professor → Course is prime','good'),
      N('BCNF 위반: 교수만으로 학생을 식별할 수 없어 슈퍼키가 아님',
        'BCNF violated: Professor does not identify the student, so it is not a superkey','bad')))


def apply(slides):
    """Attach examples and preserve every existing title, lead, ID, and position."""
    for slide in slides:
        if slide['id'] not in EXAMPLES:
            continue
        slide['example'] = deepcopy(EXAMPLES[slide['id']])
        slide['example_note'] = '설계 개념용 예제 데이터. pwd-week7 실습의 실행 스키마·실제 조회 결과와 구별.'
        if slide['id'] == 'design-purpose':
            slide['ko']['concepts'] = [
                ['설계(Database Design)','서비스 요구사항을 저장할 데이터와 관계로 바꾸는 작업','필요한 데이터와 데이터 사이의 관계를 식별'],
                ['목표','정확성·성능·확장성·개발 속도',[
                    '정확성: 잘못된 데이터·불필요한 중복 방지',
                    '성능: 조회·동시 처리 효율과 비용',
                    '확장성: 데이터·트래픽 증가에 대응',
                    '개발 속도: 스키마(Schema)·마이그레이션(Migration)으로 변경 대응']]]
            slide['en']['concepts'] = [
                ['Design','Translate requirements into stored data and relationships','Identify required data and relationships'],
                ['Goals','Correctness, performance, scalability, and development speed',[
                    'Correctness: valid data with controlled duplication',
                    'Performance: reads, concurrency, and cost',
                    'Scalability: growing data and traffic',
                    'Development speed: schema changes and migrations']]]
        if slide['id'] == 'normalization':
            slide.pop('source_figures', None)
        if slide['id'] in ('second-normal-form','third-normal-form'):
            for locale in ('ko','en'):
                slide[locale].pop('table', None)
            source = slide['example']['items'][2]
            slide['source_figures'] = [{field:source[field] for field in ('src','alt','caption')}]
        if slide['id'] == 'second-normal-form':
            slide['ko']['concepts'][0][2] = '비주요 속성은 모든 후보 키 전체에 종속'
            slide['en']['concepts'][0][2] = 'A non-prime attribute depends on the whole candidate key'
        if slide['id'] in ('functional-dependency','superkey','candidate-key','prime-attribute','partial-dependency','transitive-dependency','first-normal-form','second-normal-form','third-normal-form','bcnf'):
            slide['sources'].append('https://www.cs.cmu.edu/~natassa/courses/15-415/S03/notes/18Norm6up.pdf')
        if slide['id'] == 'physical':
            slide['sources'].append('https://www.postgresql.org/docs/current/indexes-intro.html')
    return slides
