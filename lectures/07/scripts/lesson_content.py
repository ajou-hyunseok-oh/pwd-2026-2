"""Week 7 source content: database foundations and PostgreSQL on Supabase."""
SLIDES = []

def chapter(id, ko, en):
    SLIDES.append({'type': 'chapter', 'id': id,
        'ko': {'title': ko, 'lead': '', 'concepts': []},
        'en': {'title': en, 'lead': '', 'concepts': []}})

def slide(id, kt, kl, kc, et, el, ec, code=None, label=None):
    ko = {'title': kt, 'lead': kl, 'concepts': kc}
    en = {'title': et, 'lead': el, 'concepts': ec}
    if code is not None:
        ko.update(code=code, code_label=label or 'SQL Editor')
        en.update(code=code, code_label=label or 'SQL Editor')
    SLIDES.append({'type': 'content', 'id': id, 'ko': ko, 'en': en})

slide('objectives', '학습 목표', '데이터베이스 설계에서 클라우드 구축까지', [
 ['데이터베이스','관계형 데이터와 설계 절차 이해','엔티티·관계·키·무결성의 역할'],
 ['PostgreSQL','관계형 데이터베이스와 SQL 이해','테이블 정의와 데이터 조작의 기본 구조'],
 ['Supabase','관리형 PostgreSQL 구축 흐름 이해','테이블 생성·조회와 데이터 접근 제어']
], 'Learning Objectives', 'From database design to cloud deployment', [
 ['Database','Understand relational data and the design process','Roles of entities, relationships, keys, and integrity'],
 ['PostgreSQL','Understand relational databases and SQL','Basic structures for defining tables and manipulating data'],
 ['Supabase','Understand managed PostgreSQL setup','Table creation, querying, and data access control']])
chapter('foundation', '데이터베이스 기초', 'Database Foundations')
slide('database', '데이터베이스', '공유 데이터를 통합 관리하는 데이터의 집합', [
 ['데이터베이스','공유되어 사용될 목적으로 통합 관리되는 데이터의 집합',['여러 사용자가 공유하고 접근 가능','무결성 및 보안이 중요']],
 ['데이터 관리','서비스 운영에 필요한 데이터의 지속적인 관리','정확성·보안·접근성을 함께 고려']
], 'Database', 'An integrated collection of shared data', [
 ['Database','An integrated collection of data managed for shared use',['Accessible to multiple users','Integrity and security are important']],
 ['Data management','Ongoing management of service data','Consider accuracy, security, and accessibility']])
slide('dbms', 'DBMS', '데이터베이스 생성과 관리를 지원하는 시스템', [
 ['DBMS','데이터베이스를 만들고, 저장 및 관리할 수 있는 기능들을 제공하는 응용 프로그램','여러 사용자의 데이터 접근과 변경을 관리'],
 ['역할','응용 프로그램과 저장된 데이터 사이의 관리 계층','권한·제약·복구 기능으로 데이터 관리 지원']
], 'Database Management System', 'Software for creating and managing databases', [
 ['DBMS','An application providing functions to create, store, and manage databases','Coordinates data access and changes by multiple users'],
 ['Role','A management layer between applications and stored data','Supports permissions, constraints, and recovery']])
# 2025 source PDF p.5: preserve all headings and bullet text in order.
SLIDES.append({
    'type': 'content', 'id': 'database-history',
    'ko': {
        'title': '데이터베이스 역사', 'lead': '', 'concepts': [],
        'history': [
            ('1960s (시작: 네트워크/계층형, Charles Bachman)', [
                '기업 전산에서 데이터 독립성 요구가 커지며 DBMS 개념이 등장.'
            ]),
            ('1970 (관계형 이론: E. F. Codd)', [
                '데이터를 엔티티와 관계로 표현',
                '관계대수/관계해석 기반의 정형 질의(Query) 개념 정립.',
                '정규화로 중복 최소화, 논리·물리적 데이터 독립성 강화.'
            ]),
            ('1970s (System R & 핵심 기술 완성)', [
                'IBM System R에서 SQL 최초 구현',
                'RDBMS 필수 아키텍처가 표준화.'
            ]),
            ('1970s~1990s (오픈·상용 생태 확장)', [
                'ANSI SQL 표준화',
                '클라이언트/서버 아키텍처 보급'
            ]),
            ('1990s (Oracle 상용 선도: Larry Ellison/Bob Miner)', [
                '대규모 상용 워크로드에서 확장성·고가용성으로 RDBMS가 기업 표준으로 자리잡음.'
            ]),
            ('1995~ (오픈소스 부상: MySQL + InnoDB, PostgreSQL)', [
                'LAMP(Linux + Apache + MySQL + PHP) 스택과 함께 대중화'
            ]),
            ('2000s (웹·빅데이터: NoSQL 등장)', [
                '웹 규모 확장성 요구로 NoSQL 확산',
                'RDBMS는 여전히 코어 시스템으로 사용'
            ]),
        ],
    },
    'en': {
        'title': 'History of Databases', 'lead': '', 'concepts': [],
        'history': [
            ('1960s (Origins: network/hierarchical, Charles Bachman)', [
                'Growing demand for data independence in enterprise computing led to the DBMS concept.'
            ]),
            ('1970 (Relational theory: E. F. Codd)', [
                'Data represented as entities and relationships',
                'Formal queries established using relational algebra and relational calculus.',
                'Normalization minimized redundancy and strengthened logical and physical data independence.'
            ]),
            ('1970s (System R & core technologies)', [
                'SQL first implemented in IBM System R',
                'Essential RDBMS architecture standardized.'
            ]),
            ('1970s–1990s (Growth of open and commercial ecosystems)', [
                'ANSI SQL standardization',
                'Adoption of client/server architecture'
            ]),
            ('1990s (Oracle commercial leadership: Larry Ellison/Bob Miner)', [
                'Scalability and high availability made RDBMSs an enterprise standard for large commercial workloads.'
            ]),
            ('1995 onward (Open source: MySQL + InnoDB, PostgreSQL)', [
                'Popularized alongside the LAMP (Linux + Apache + MySQL + PHP) stack'
            ]),
            ('2000s (Web and big data: NoSQL emerges)', [
                'NoSQL spread with the need for web-scale scalability',
                'RDBMSs remained in use for core systems'
            ]),
        ],
    },
})
# 2025 PDF pp.6–8: restore the original comparison, trend and professions.
slide('db-types', '데이터베이스 유형', '', [
 ['관계형 데이터베이스(RDBMS)', '데이터를 테이블 형태로 구조화하여 저장하고, 각 테이블 간에 관계를 맺어 데이터를 관리', [
  '데이터의 정합성을 유지하고, SQL이라는 표준 쿼리 언어를 사용하여 복잡한 데이터 조작 및 검색이 가능',
  '데이터의 구조 변경이 어렵고, 대규모의 비정형 데이터 처리에는 비효율적',
  '주요 RDBMS : Oracle, MySQL, PostgreSQL, MariaDB']],
 ['비관계형 데이터베이스(NoSQL DBMS)', '유연한 형태로 비정형 데이터를 저장', [
  '대규모의 분산 환경에서 뛰어난 확장성을 가지며, 유연한 데이터 모델링이 가능',
  '복잡한 쿼리나 트랜잭션 처리가 어려울 수 있음',
  '유형별',
  '문서형(Document) DBMS: JSON과 같은 문서 형태로 데이터를 저장, MongoDB',
  '키-값형(Key-Value) DBMS: 키와 값의 형태로 데이터를 저장하여 빠른 검색이 가능, Redis',
  '그래프형(Graph) DBMS: 노드와 엣지 형태로 복잡한 관계를 표현하고 저장']]
], 'Database Types', '', [
 ['Relational Database (RDBMS)', 'Stores structured data in tables and manages it through relationships between tables', [
  'Maintains data consistency and supports complex data manipulation and retrieval with SQL',
  'Structure changes are difficult and large-scale unstructured data processing is inefficient',
  'Major RDBMSs: Oracle, MySQL, PostgreSQL, MariaDB']],
 ['Non-relational Database (NoSQL DBMS)', 'Stores unstructured data in flexible forms', [
  'Offers scalability in large distributed environments and flexible data modeling',
  'Complex queries or transaction processing may be difficult',
  'By type',
  'Document DBMS: Stores JSON-like documents, e.g. MongoDB',
  'Key-value DBMS: Stores key-value pairs for fast lookup, e.g. Redis',
  'Graph DBMS: Represents and stores complex relationships using nodes and edges']]
])
slide('database-trends-2025', '2026년 10월 데이터베이스 트렌드', '', [],
      'Database Trends: October 2026', '', [])
SLIDES[-1]['reference_link'] = 'https://db-engines.com/en/ranking'
slide('database-careers', '데이터베이스 관련 직군', '', [
 ['데이터 모델러', '데이터 구조, 관계, 제약 조건을 설계', []],
 ['데이터 아키텍트', 'DBMS 선택 및 전체 데이터 아키텍처를 책임', []],
 ['데이터 엔지니어', '데이터 파이프라인과 데이터 웨어하우스를 설계하고 구축', []],
 ['DBA(Database Administrator)', '데이터베이스 운영, 모니터링, 백업, 보안 및 튜닝을 담당', []]
], 'Database Careers', '', [
 ['Data Modeler', 'Designs data structures, relationships, and constraints', []],
 ['Data Architect', 'Selects the DBMS and owns the overall data architecture', []],
 ['Data Engineer', 'Designs and builds data pipelines and data warehouses', []],
 ['Database Administrator (DBA)', 'Manages database operations, monitoring, backup, security, and tuning', []]
])
chapter('design', '데이터베이스 설계', 'Database Design')
slide('design-purpose', '데이터베이스 설계', '서비스 요구사항을 데이터 구조로 변환', [
 ['설계','서비스 요구 사항을 데이터 모델로 변환하여, 정확하고 빠르며 잘 확장되는 시스템을 만드는 작업','필요한 데이터와 데이터 사이의 관계를 식별'],
 ['목표','정확성·성능·확장성·개발 속도',['정확성: 잘못된·중복 데이터 방지','성능: 적절한 인덱스·스키마로 응답 속도와 동시성 확보, 비용 절감','확장성: 트래픽·데이터 증가에 맞춰 확장','개발 속도: 변경에 강한 스키마와 마이그레이션 전략 수립']]
], 'Database Design', 'Turning service requirements into data structures', [
 ['Design','Transform service requirements into a data model for an accurate, fast, and scalable system','Identify required data and relationships'],
 ['Goals','Correctness, performance, scalability, and development speed',['Correctness: prevent invalid and duplicate data','Performance: support response time and concurrency with appropriate indexes and schemas','Scalability: grow with traffic and data','Development speed: plan schemas and migrations that accommodate change']]])
slide('design-stages', '데이터베이스 설계 절차', '개념적 설계에서 물리적 설계까지', [
 ['설계 흐름','개념적 설계 → 논리적 설계 → 물리적 설계','요구사항을 개념으로 표현하고 구현 가능한 구조로 구체화'],
 ['반복','요구사항과 사용 방식에 따른 설계 검토','각 단계의 결정이 다른 단계에 영향을 줄 수 있음']
], 'Database Design Stages', 'From conceptual to physical design', [
 ['Design flow','Conceptual design → logical design → physical design','Express requirements as concepts and refine them into an implementable structure'],
 ['Iteration','Review the design against requirements and usage','Decisions in one stage can affect other stages']])
slide('conceptual', '개념적 설계', '서비스의 대상을 데이터 개념으로 표현', [
 ['개념적 설계','서비스의 요구를 데이터 세계의 개념(사물·행위)으로 표현','구현 방법보다 서비스의 의미와 업무 규칙에 집중'],
 ['FoodMap 사례','사용자·제보·맛집과 그 관계 식별','제보 승인에 따른 맛집 등록이라는 업무 규칙 표현']
], 'Conceptual Design', 'Represent service requirements as data concepts', [
 ['Conceptual design','Express service requirements as data concepts such as objects and actions','Focus on service meaning and business rules rather than implementation'],
 ['FoodMap example','Identify users, submissions, restaurants, and relationships','Express the rule that approval can register a restaurant']])
slide('entity', '엔티티', '저장할 대상의 종류', [
 ['엔티티','저장할 대상의 종류',['사용자·식당·주문 등이 엔티티의 예','각 인스턴스는 해당 대상의 개별 사례']],
 ['FoodMap 사례','사용자·식당·제보','하나의 식당은 식당 엔티티의 한 인스턴스']
], 'Entity', 'A kind of object to store', [
 ['Entity','A kind of object to store',['Users, restaurants, and orders are examples of entities','Each instance is an individual example of that entity']],
 ['FoodMap example','User, restaurant, and submission','One restaurant is an instance of the restaurant entity']])
slide('attributes', '속성', '엔티티를 설명하는 값의 항목', [
 ['속성','엔티티를 설명하는 값의 항목',['이름·전화번호 등이 속성의 예','각 인스턴스는 속성에 해당하는 값을 가짐']],
 ['도메인','속성이 가질 수 있는 합법적 값의 집합과 단위·형식','예: 평점 1~5 정수']
], 'Attribute', 'A data item describing an entity', [
 ['Attribute','A value item describing an entity',['Name and phone number are examples of attributes','Each instance has a value for the attribute']],
 ['Domain','The set of valid values, units, and formats an attribute can have','Example: integer ratings from 1 through 5']])
slide('relationship', '관계', '엔티티 사이의 연관성', [
 ['관계','엔티티 간의 연관성·연결','관계의 이름은 서비스에서 두 대상이 맺는 역할 표현'],
 ['FoodMap 사례','사용자가 제보를 작성','하나의 사용자가 여러 제보와 연결될 수 있음']
], 'Relationship', 'An association between entities', [
 ['Relationship','An association or connection between entities','Its name expresses the role of the association in the service'],
 ['FoodMap example','A user creates submissions','One user can be connected to multiple submissions']])
slide('cardinality', '카디널리티', '관계에 참여할 수 있는 인스턴스의 개수', [
 ['카디널리티','한쪽 엔티티가 다른 쪽과 맺을 수 있는 개수 규칙','1:1·1:N·N:M 관계로 표현'],
 ['참여 제약','관계에 반드시 참여해야 하는지 또는 해도 되고 안 해도 되는지 결정하는 규칙','필수 참여와 선택 참여를 구분']
], 'Cardinality', 'The number of instances participating in a relationship', [
 ['Cardinality','A rule for the number of connections between entities','Expressed as 1:1, 1:N, or N:M relationships'],
 ['Participation','A rule specifying whether participation is mandatory or optional','Distinguishes required from optional participation']])
slide('logical', '논리적 설계', '개념 모델을 데이터 구조와 규칙으로 변환', [
 ['논리적 설계','DBMS가 곧바로 이해·변환할 수 있는 논리 데이터 스키마를 만드는 작업','엔티티와 속성을 테이블과 열로 표현'],
 ['스키마','데이터 구조와 규칙의 설계서','테이블·열·자료형·키·제약조건으로 구성']
], 'Logical Design', 'Transform a conceptual model into structures and rules', [
 ['Logical design','Create a logical data schema that a DBMS can understand and transform','Represent entities and attributes as tables and columns'],
 ['Schema','A blueprint for data structure and rules','Includes tables, columns, types, keys, and constraints']])
slide('primary-key', '기본 키', '각 행을 유일하게 구별하는 식별자', [
 ['기본 키','테이블의 각 행을 식별하는 열 또는 열의 조합','값은 중복될 수 없으며 NULL을 허용하지 않음'],
 ['식별','식당 이름처럼 바뀌거나 중복될 수 있는 값과 구분','여러 테이블이 동일한 대상을 참조하는 기준']
], 'Primary Key', 'An identifier that uniquely distinguishes each row', [
 ['Primary key','A column or combination of columns identifying each row','Values must be unique and cannot be NULL'],
 ['Identification','Distinct from values that may change or repeat, such as a name','Provides a stable reference to an entity across tables']])
slide('foreign-key', '외래 키', '같은 테이블 또는 다른 테이블의 행을 참조하는 관계', [
 ['외래 키','같은 테이블 또는 다른 테이블의 지정된 키를 참조하는 열 또는 열의 조합','참조 값이 대상 테이블에 존재하도록 관계를 검증'],
 ['참조 대상','기본 키 또는 참조 가능한 고유한 키','NULL 허용 여부는 별도의 제약조건으로 결정']
], 'Foreign Key', 'A relationship referencing a row in the same or another table', [
 ['Foreign key','A column or columns referencing a key in the same or another table','Checks that a referenced value exists in the target table'],
 ['Referenced key','A primary key or an eligible unique key','A separate constraint determines whether NULL is allowed']])
slide('physical', '물리적 설계', '데이터 저장과 접근을 위한 구현 결정', [
 ['물리적 설계','논리적 구조를 선택한 DBMS가 실제로 저장·조회할 수 있는 물리 구조로 구체화','데이터의 크기와 조회·변경 패턴을 고려'],
 ['접근 경로','필요한 데이터를 찾기 위한 구조','인덱스와 저장 설정은 성능과 저장 비용에 영향']
], 'Physical Design', 'Implementation decisions for storage and access', [
 ['Physical design','Refine logical structures into physical structures the selected DBMS can store and query','Consider data size and read/write patterns'],
 ['Access path','A structure used to locate required data','Indexes and storage settings affect performance and cost']])
slide('erd', 'ERD', '엔티티와 관계를 시각화한 데이터 설계도', [
 ['ERD','엔티티·속성·관계·카디널리티를 그림으로 표현한 데이터 설계도','관계의 양쪽 끝에 참여 개수와 선택 여부 표시'],
 ['제보와 맛집','제보 한 건당 맛집 0개 또는 1개','각 맛집은 정확히 하나의 출처 제보와 연결']
], 'Entity–Relationship Diagram', 'A visual model of entities and relationships', [
 ['ERD','A visual data design representing entities, attributes, relationships, and cardinality','Each end indicates participation and the number of related instances'],
 ['Submission and restaurant','Each submission links to zero or one restaurant','Each restaurant links to exactly one source submission']])
slide('constraints', '제약조건', '허용할 수 있는 데이터에 적용하는 규칙', [
 ['제약조건','데이터가 만족해야 하는 조건을 데이터베이스에 정의','정의된 규칙에 맞지 않는 잘못된·중복·모순 데이터의 저장을 거부'],
 ['적용','필수 값·고유성·참조 관계·값의 범위를 제한','응용 프로그램 외의 접근에도 동일한 규칙 적용']
], 'Constraints', 'Rules applied to allowed data', [
 ['Constraint','A condition defined in the database that data must satisfy','Rejects invalid, duplicate, or inconsistent data that violates the defined rule'],
 ['Application','Restricts required values, uniqueness, references, and ranges','Applies the same rules to access outside the application']])
slide('integrity', '데이터 무결성', '데이터가 항상 올바른 상태를 유지하는 성질', [
 ['개체 무결성','각 행을 식별하는 기본 키의 고유성과 NULL 금지','같은 테이블의 행을 명확히 구분'],
 ['참조·도메인 무결성','참조 관계와 속성의 허용 범위 유지','외래 키·자료형·값의 범위 등으로 규칙 표현']
], 'Data Integrity', 'The property of data remaining in a correct state', [
 ['Entity integrity','Uniqueness and non-NULL values for a primary key','Distinguishes rows within a table'],
 ['Referential and domain integrity','Valid references and allowed attribute values','Expressed through foreign keys, types, and value restrictions']])
slide('normalization', '정규화', '중복과 변경 이상을 줄이는 테이블 설계', [
 ['정규화','데이터의 종속 관계에 따라 테이블을 구성하는 과정','불필요한 중복과 삽입·수정·삭제 이상 감소'],
 ['변경 이상','같은 사실의 중복으로 발생하는 데이터 불일치','동일한 식당 이름이 여러 행에 있으면 일부만 수정될 수 있음']
], 'Normalization', 'Table design that reduces redundancy and anomalies', [
 ['Normalization','Organizing tables according to dependencies between data','Reduces unnecessary duplication and insertion, update, and deletion anomalies'],
 ['Update anomaly','Inconsistency caused by repeated facts','If a restaurant name appears in several rows, only some may be updated']])
slide('functional-dependency', '함수 종속', '결정자에 따라 정해지는 속성의 값', [
 ['함수 종속','한 속성 집합의 값이 다른 속성의 값을 결정하는 관계','결정자 값이 같으면 종속 속성의 값도 같아야 함'],
 ['FoodMap 사례','식당 ID → 식당 이름','하나의 식당 ID는 하나의 식당 이름을 결정']
], 'Functional Dependency', 'Attribute values determined by another set of attributes', [
 ['Functional dependency','A relationship where one set of attributes determines another','Equal determinant values require equal dependent values'],
 ['FoodMap example','Restaurant ID → restaurant name','One restaurant ID determines one restaurant name']])
slide('superkey', '슈퍼키', '테이블의 각 행을 구별하는 속성 집합', [
 ['슈퍼키','행을 유일하게 식별하는 하나 이상의 속성 집합','식별에 불필요한 속성을 추가해도 유일성이 유지되면 슈퍼키'],
 ['FoodMap 사례','식당 ID와 식당 이름의 조합도 슈퍼키','식당 ID만으로 행이 유일하게 구별되는 경우']
], 'Superkey', 'A set of attributes that identifies each row', [
 ['Superkey','One or more attributes that uniquely identify a row','Adding unnecessary attributes preserves a superkey if uniqueness remains'],
 ['FoodMap example','Restaurant ID and restaurant name together are a superkey','When restaurant ID alone uniquely identifies a row']])
slide('candidate-key', '후보 키', '불필요한 속성이 없는 최소 슈퍼키', [
 ['후보 키','행을 유일하게 식별하는 최소 속성 집합','속성 하나라도 제거하면 유일한 식별이 불가능'],
 ['기본 키와의 관계','후보 키 중 하나를 기본 키로 선택','식당 ID만으로 유일한 경우 식당 ID는 후보 키']
], 'Candidate Key', 'A minimal superkey without unnecessary attributes', [
 ['Candidate key','A minimal attribute set that uniquely identifies a row','Removing any attribute makes unique identification impossible'],
 ['Primary key','A primary key is chosen from the candidate keys','Restaurant ID is a candidate key when it uniquely identifies a row']])
slide('prime-attribute', '주요 속성', '후보 키에 속하는 속성', [
 ['주요 속성','하나 이상의 후보 키에 속하는 속성','어느 후보 키에도 속하지 않는 속성은 비주요 속성'],
 ['복합 후보 키','두 개 이상의 속성으로 구성된 후보 키','식당 ID와 메뉴 ID 조합이 후보 키라면 두 속성은 주요 속성']
], 'Prime Attribute', 'An attribute belonging to a candidate key', [
 ['Prime attribute','An attribute belonging to at least one candidate key','An attribute in no candidate key is non-prime'],
 ['Composite candidate key','A candidate key composed of two or more attributes','If restaurant ID and menu ID form a candidate key, both are prime']])
slide('partial-dependency', '부분 종속', '복합 후보 키의 일부에 대한 함수 종속', [
 ['부분 종속','비주요 속성이 복합 후보 키의 일부에만 종속되는 관계','키 전체가 아닌 더 작은 키 부분으로 값 결정'],
 ['FoodMap 사례','식당 ID → 식당 이름','식당 ID·메뉴 ID가 복합 키일 때 식당 이름은 키의 일부에 종속']
], 'Partial Dependency', 'A dependency on part of a composite candidate key', [
 ['Partial dependency','A non-prime attribute depends on only part of a composite candidate key','A smaller part of the key determines the value'],
 ['FoodMap example','Restaurant ID → restaurant name','With a restaurant ID and menu ID key, restaurant name depends on part of the key']])
slide('transitive-dependency', '이행 종속', '중간 속성을 거쳐 결정되는 함수 종속', [
 ['이행 종속','한 속성이 중간 속성을 통해 다른 속성을 결정하는 관계','A → B와 B → C가 성립하면 A → C가 성립'],
 ['FoodMap 사례','식당 ID → 지역 코드 → 지역 이름','지역 이름은 식당 ID에서 지역 코드를 거쳐 결정']
], 'Transitive Dependency', 'A functional dependency through an intermediate attribute', [
 ['Transitive dependency','A dependency in which one attribute determines another through an intermediate','If A → B and B → C, then A → C'],
 ['FoodMap example','Restaurant ID → region code → region name','Restaurant ID determines region name through region code']])
slide('first-normal-form', '제1정규형', '각 열에 도메인 기준의 단일 값 저장', [
 ['1NF','다중값 분해 · 각 열에 해당 도메인의 원자값을 두는 정규형','여러 전화번호를 하나의 목록 문자열로 저장하지 않음'],
 ['적용','반복되는 전화번호를 별도 행으로 표현','식당 ID로 전화번호 행을 해당 식당에 연결']
], 'First Normal Form', 'Store a single value for each column domain', [
 ['1NF','Separate multiple values · use an atomic value from the domain in each column','Avoid storing multiple phone numbers as one list string'],
 ['Application','Represent repeated phone numbers as separate rows','Connect phone-number rows to the restaurant by restaurant ID']])
slide('second-normal-form', '제2정규형', '복합 키의 일부에만 의존하는 속성 분리', [
 ['2NF','부분 종속 제거 · 1NF를 만족하고 비주요 속성의 부분 종속이 없는 정규형','비주요 속성은 후보 키의 일부가 아닌 전체에 종속'],
 ['분리 사례','식당 ID·메뉴 ID → 가격, 식당 ID → 식당 이름','식당 이름을 식당 테이블로 옮겨 같은 이름의 중복 감소']
], 'Second Normal Form', 'Remove attributes dependent on part of a composite key', [
 ['2NF','Remove partial dependencies · 1NF without partial dependencies of non-prime attributes','A non-prime attribute depends on the whole candidate key rather than part'],
 ['Decomposition','Restaurant ID·menu ID → price; restaurant ID → restaurant name','Move restaurant name to a restaurant table to reduce repetition']])
slide('third-normal-form', '제3정규형', '비주요 속성 사이의 이행 종속 분리', [
 ['3NF','이행 종속 제거 · 비자명한 X → A에서 X가 슈퍼키이거나 A가 주요 속성인 정규형','A는 X에 포함되지 않는 단일 속성 · 2NF를 만족'],
 ['분리 사례','식당 ID → 지역 코드 → 지역 이름','지역 코드와 지역 이름을 지역 테이블에 분리']
], 'Third Normal Form', 'Separate transitive dependencies between non-prime attributes', [
 ['3NF','Remove transitive dependencies · for each nontrivial X → A, X is a superkey or A is prime','A is a single attribute outside X · 2NF is satisfied'],
 ['Decomposition','Restaurant ID → region code → region name','Move region code and region name into a separate region table']])
slide('bcnf', 'BCNF', '모든 결정자가 슈퍼키인 정규형', [
 ['BCNF','모든 비자명한 함수 종속의 결정자가 슈퍼키인 정규형','결정자가 후보 키를 포함해 행을 유일하게 식별'],
 ['3NF와의 관계','주요 속성이 종속 속성인 경우에도 슈퍼키 조건 적용','3NF보다 강한 함수 종속 조건']
], 'Boyce–Codd Normal Form', 'A normal form in which every determinant is a superkey', [
 ['BCNF','A normal form where every determinant of a nontrivial dependency is a superkey','The determinant includes a candidate key and uniquely identifies each row'],
 ['Relationship to 3NF','The superkey condition also applies when the dependent attribute is prime','A stronger dependency condition than 3NF']])
chapter('postgres', 'PostgreSQL과 SQL', 'PostgreSQL and SQL')
slide('postgresql', 'PostgreSQL', 'SQL을 사용하는 오픈소스 관계형 DBMS', [
 ['PostgreSQL','관계형 데이터베이스를 관리하는 오픈소스 DBMS','테이블과 관계를 정의하고 SQL로 데이터를 처리'],
 ['기능','자료형·제약조건·트랜잭션 등 제공','서비스 요구에 맞춰 구조와 접근 규칙을 구성']
], 'PostgreSQL', 'An open-source relational DBMS using SQL', [
 ['PostgreSQL','An open-source DBMS for relational databases','Defines tables and relationships and processes data with SQL'],
 ['Capabilities','Provides data types, constraints, and transactions','Structures and access rules can be configured for service needs']])
slide('sql', 'SQL', '관계형 데이터베이스를 다루는 언어', [
 ['SQL','관계형 데이터베이스(RDBMS)를 다루는 표준 언어','DBMS에 명령을 전달하고 결과를 반환'],
 ['명령의 범주','데이터 정의(DDL)·조작(DML)·권한 제어(DCL)·트랜잭션 제어(TCL)','구체적인 문법과 지원 기능은 DBMS에 따라 차이']
], 'Structured Query Language', 'A language for relational databases', [
 ['SQL','A standard language for working with relational databases','Sends commands to the DBMS and returns results'],
 ['Command categories','Data definition (DDL), manipulation (DML), authorization (DCL), and transaction control (TCL)','Specific syntax and features vary across DBMSs']])
slide('data-types', 'PostgreSQL 자료형', '열에 저장할 값의 종류와 범위', [
 ['자료형','열에 저장할 수 있는 값의 종류와 연산을 정의','잘못된 형태의 값이 저장되는 것을 방지'],
 ['주요 자료형','text · integer · boolean · timestamp with time zone','문자열·정수·참거짓·시각 데이터 표현']
], 'PostgreSQL Data Types', 'The kinds and ranges of values stored in a column', [
 ['Data type','Defines the values and operations available for a column','Prevents incompatible values from being stored'],
 ['Common types','text · integer · boolean · timestamp with time zone','Represent text, integers, truth values, and timestamps']])
slide('create-table', '테이블 생성', '이름·열·자료형과 제약조건 정의', [
 ['CREATE TABLE','테이블의 구조를 정의하는 SQL 명령','각 열에 이름과 자료형을 지정'],
 ['제약조건','열에 허용되는 값을 제한하는 규칙','기본 키와 필수 값을 구조에 함께 정의']
], 'Creating a Table', 'Define names, columns, types, and constraints', [
 ['CREATE TABLE','An SQL command that defines a table structure','Specify a name and data type for each column'],
 ['Constraints','Rules limiting allowed values in columns','Define a primary key and required values in the structure']
], code='CREATE TABLE restaurants (\n  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n  name text NOT NULL,\n  address text NOT NULL\n);')
slide('submission-table', '제보 테이블 생성', '제보의 식별자와 내용을 저장', [
 ['제보 테이블','각 제보를 하나의 행으로 저장하는 구조','기본 키는 개별 제보를 식별'],
 ['관계의 기준','맛집은 이 식별자를 참조해 출처 제보와 연결','제보와 맛집은 독립된 테이블로 관리']
], 'Creating a Submission Table', 'Store submission identifiers and details', [
 ['Submission table','A structure storing each submission as one row','The primary key identifies each submission'],
 ['Relationship target','A restaurant can refer to this identifier as its source submission','Submissions and restaurants are managed in separate tables']
], code='CREATE TABLE submissions (\n  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n  name text NOT NULL\n);')
slide('one-to-one', '제보와 맛집의 관계', '외래 키와 고유 제약으로 관계 구현', [
 ['외래 키','맛집의 제보 식별자가 존재하는 제보를 참조','각 맛집에는 출처 제보가 반드시 하나 필요'],
 ['고유 제약','하나의 제보 식별자가 여러 맛집 행에 반복되지 않도록 제한','제보당 연결된 맛집은 최대 한 개 · 승인 처리는 별도 로직']
], 'Submission–Restaurant Relationship', 'Implement the relationship with a foreign key and uniqueness', [
 ['Foreign key','A restaurant submission identifier references an existing submission','Each restaurant requires exactly one source submission'],
 ['Unique constraint','Prevents a submission identifier from repeating across restaurant rows','At most one restaurant per submission · approval requires separate logic']
], code='ALTER TABLE restaurants\nADD COLUMN submission_id bigint NOT NULL UNIQUE\n  REFERENCES submissions(id);', label='SQL Editor · restaurants + submissions')
slide('insert-submission', '제보 데이터 추가', '새 제보를 저장하고 식별자 확인', [
 ['INSERT','열과 값을 지정해 새 행을 생성','생성된 식별자는 RETURNING으로 확인'],
 ['연결 준비','식당 행에 저장할 출처 제보의 식별자 확인','다른 식당은 이 제보를 중복 참조할 수 없음']
], 'Inserting a Submission', 'Store a submission and retrieve its identifier', [
 ['INSERT','Creates a row with specified columns and values','RETURNING retrieves the generated identifier'],
 ['Preparing the relationship','Retrieve the source submission identifier for the restaurant row','Another restaurant cannot reference the same submission']
], code="INSERT INTO submissions (name)\nVALUES ('Campus Kitchen')\nRETURNING id;", label='SQL Editor · submissions')
slide('insert', '데이터 추가', '테이블에 새로운 행 저장', [
 ['INSERT','지정한 열에 값을 넣어 새로운 행을 생성','생략한 열은 기본값 또는 허용된 NULL 사용'],
 ['무결성','추가되는 행에 테이블의 제약조건 적용','허용되지 않는 값은 저장되지 않음']
], 'Inserting Data', 'Store a new row in a table', [
 ['INSERT','Creates a new row using values for specified columns','Omitted columns use a default or an allowed NULL'],
 ['Integrity','Table constraints apply to the new row','Values violating constraints are rejected']
], code="INSERT INTO restaurants (name, address, submission_id)\nVALUES ('Campus Kitchen', 'Suwon', 1);")
slide('select', '데이터 조회', '조건에 맞는 행과 필요한 열 선택', [
 ['SELECT','테이블에서 지정한 열의 값을 조회','WHERE 조건으로 반환할 행의 범위 제한'],
 ['결과','조회 결과는 조건을 만족하는 행의 집합','정렬을 지정하지 않으면 반환 순서는 보장되지 않음']
], 'Querying Data', 'Choose required columns and matching rows', [
 ['SELECT','Retrieves values from specified table columns','WHERE restricts which rows are returned'],
 ['Result','A set of rows satisfying the query condition','Row order is not guaranteed without an explicit sort']
], code="SELECT id, name, address\nFROM restaurants\nWHERE address = 'Suwon';")
slide('join', 'JOIN', '관계로 연결된 테이블의 데이터 결합', [
 ['JOIN','공통 값의 비교를 이용해 여러 테이블의 행을 결합','결합 조건은 어떤 행을 연결할지 결정'],
 ['관계 활용','제보와 맛집의 식별값을 이용해 연결','내부 결합은 양쪽에 일치하는 행만 반환']
], 'JOIN', 'Combine data from related tables', [
 ['JOIN','Combines rows from tables by comparing common values','The join condition determines which rows are connected'],
 ['Using relationships','Connect submissions and restaurants through identifiers','An inner join returns only rows matched in both tables']
], code='SELECT s.name, r.name\nFROM submissions AS s\nJOIN restaurants AS r\n  ON r.submission_id = s.id;', label='SQL Editor · submissions + restaurants')
slide('update', '데이터 수정', '기존 행의 열 값 변경', [
 ['UPDATE','조건에 맞는 기존 행의 값을 변경','SET으로 변경할 열과 값을 지정'],
 ['변경 범위','WHERE 조건이 적용 대상 행을 결정','조건이 없으면 테이블의 모든 행이 대상']
], 'Updating Data', 'Change column values in existing rows', [
 ['UPDATE','Changes values in existing rows that match a condition','SET specifies the columns and new values'],
 ['Scope','WHERE determines which rows are affected','Without a condition, every row is affected']
], code="UPDATE restaurants\nSET address = 'Ajou University'\nWHERE id = 1;")
slide('delete', '데이터 삭제', '조건에 맞는 기존 행 제거', [
 ['DELETE','테이블에서 조건에 맞는 행을 제거','열의 구조가 아니라 행의 데이터가 삭제 대상'],
 ['삭제 범위','WHERE 조건으로 제거할 행을 제한','조건이 없으면 테이블의 모든 행이 대상']
], 'Deleting Data', 'Remove existing rows matching a condition', [
 ['DELETE','Removes matching rows from a table','Deletes row data rather than column structure'],
 ['Scope','WHERE restricts the rows removed','Without a condition, every row is affected']
], code='DELETE FROM restaurants\nWHERE id = 1;')
# Supabase practice is authored separately from the preceding design examples.
from supabase_chapter import SLIDES as SUPABASE_SLIDES
SLIDES.extend(SUPABASE_SLIDES)
slide('questions', 'Q&A', '데이터베이스 설계와 구축', [], 'Q&A', 'Database design and setup', [])

# The UPDATE and DELETE examples assume the inserted row has id 1.
for _example in SLIDES:
    if _example['id'] == 'one-to-one':
        _example['ko']['code_label'] = 'SQL Editor · 빈 restaurants 테이블 기준'
        _example['en']['code_label'] = 'SQL Editor · Empty restaurants table'
    if _example['id'] == 'insert':
        _example['ko']['code_label'] = 'SQL Editor · 반환된 제보 id가 1인 경우'
        _example['en']['code_label'] = 'SQL Editor · Returned submission id is 1'
    if _example['id'] == 'join':
        _example['ko']['code_label'] = 'SQL Editor · 연결된 제보와 맛집이 있는 경우'
        _example['en']['code_label'] = 'SQL Editor · Requires linked rows'
    if _example['id'] in ('update', 'delete'):
        _example['ko']['code_label'] = 'SQL Editor · 예시 행의 id가 1인 경우'
        _example['en']['code_label'] = 'SQL Editor · Example row with id 1'
