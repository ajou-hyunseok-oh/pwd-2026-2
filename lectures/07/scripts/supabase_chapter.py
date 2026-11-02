"""Week 7 Supabase chapter: the verified restaurants-only practice.

SQL excerpts preserve pwd-week7/supabase/{schema,seed}.sql semantics.
Dashboard credentials and live mutations are deliberately absent.
"""

PG = 'https://www.postgresql.org/docs/current/'
SB = 'https://supabase.com/docs/'
SLIDES = []


def page(ident, ko, en, refs=(), code=None, label=None, table=None, steps=None, note=''):
    ktitle, klead, kconcepts = ko
    etitle, elead, econcepts = en
    item = {'id': ident, 'type': 'content',
            'ko': {'title': ktitle, 'lead': klead, 'concepts': kconcepts},
            'en': {'title': etitle, 'lead': elead, 'concepts': econcepts},
            'source_urls': list(refs), 'note': note}
    if code:
        for locale, caption in zip(('ko', 'en'), label):
            item[locale].update(code=code, code_label=caption)
    for key, value in (('table', table), ('steps', steps)):
        if value:
            item['ko'][key], item['en'][key] = value
    SLIDES.append(item)


SLIDES.append({'id': 'supabase-chapter', 'type': 'chapter',
               'ko': {'title': 'Supabase 데이터베이스 구축', 'lead': '', 'concepts': []},
               'en': {'title': 'Building a Database with Supabase', 'lead': '', 'concepts': []}})

page('supabase',
     ('Supabase', 'PostgreSQL을 중심으로 구성한 백엔드 개발 플랫폼', [
         ['기반', '프로젝트별 PostgreSQL 데이터베이스 제공', '테이블·SQL·제약조건을 실제 PostgreSQL에서 처리'],
         ['서비스', '데이터베이스에 API와 관리 도구를 결합', '인증·스토리지·실시간 기능도 제공하는 오픈 소스 생태계']]),
     ('Supabase', 'A backend development platform centered on PostgreSQL', [
         ['Foundation', 'A PostgreSQL database for each project', 'Tables, SQL, and constraints run in PostgreSQL'],
         ['Services', 'APIs and management tools around the database', 'An open-source ecosystem also offering Auth, Storage, and Realtime']]),
     [SB+'guides/database/overview', 'https://supabase.com/'])

page('supabase-history',
     ('Supabase의 출발과 성장', '오픈 소스 개발 도구에서 관리형 플랫폼으로', [
         ['출발점', 'Firebase의 개발 편의성을 PostgreSQL과 연결', 'Paul Copplestone·Ant Wilson이 시작한 오픈 소스 프로젝트'],
         ['발전 방향', '개발자 경험과 기존 오픈 소스 도구의 결합', '데이터베이스 구축과 연결에 필요한 반복 작업을 서비스로 제공']]),
     ('Supabase History', 'From open-source developer tools to a managed platform', [
         ['Origin', 'Connect Firebase-style convenience with PostgreSQL', 'An open-source project started by Paul Copplestone and Ant Wilson'],
         ['Direction', 'Developer experience built on existing open-source tools', 'Services reduce repetitive work when creating and connecting databases']]),
     ['https://supabase.com/blog/supabase-how-we-launch', 'https://www.ycombinator.com/companies/supabase',
      'https://supabase.com/ga', 'https://supabase.com/blog/100000-github-stars'],
     steps=([['2020년 1월', '개발 시작 · 2020년 YC 여름 배치 참여'],
             ['2024년 4월 15일', '정식 서비스 GA 발표'],
             ['2026년 4월 2일', 'GitHub 별 10만 개 달성 발표']],
            [['January 2020', 'Development begins · YC Summer 2020 batch'],
             ['April 15, 2024', 'General Availability announcement'],
             ['April 2, 2026', '100,000 GitHub stars announced']]),
     note='연혁은 공식 발표일 기준. GitHub 별은 커뮤니티 관심 지표이며 DB 시장 점유율이 아니다.')

page('supabase-current',
     ('Supabase의 현재 구성', '2026년 11월 2일 공식 문서 확인 기준', [
         ['중심 구조', '관리형 PostgreSQL에 여러 백엔드 기능 연결', '한 프로젝트에서 데이터와 관련 서비스를 관리'],
         ['실습에서의 선택', 'Database와 Data API만 사용', '제공되는 모든 서비스를 애플리케이션에 도입할 필요는 없음']]),
     ('Supabase Today', 'Official documentation checked on November 2, 2026', [
         ['Core', 'Managed PostgreSQL connected to backend services', 'Manage data and related services within a project'],
         ['Practice selection', 'Use Database and the Data API', 'An application can select the services it needs']]),
     [SB+'guides/database/overview', SB+'guides/api', SB+'guides/storage', SB+'guides/auth', SB+'guides/realtime'],
     table=({'head': ['구성', '제공 역할'], 'rows': [
         ['Database · Data API', 'SQL 저장·제약 적용 · HTTP 데이터 접근'],
         ['Auth', '사용자 인증'], ['Storage', '이미지 등 파일 보관'], ['Realtime', '변경 사항 전달·실시간 통신']]},
            {'head': ['Component', 'Role'], 'rows': [
         ['Database · Data API', 'SQL persistence and constraints · HTTP access'],
         ['Auth', 'User authentication'], ['Storage', 'File storage, including images'], ['Realtime', 'Change delivery and real-time communication']]}))

page('supabase-meaning',
     ('관리형 데이터베이스의 의의', '서버 프로세스와 데이터의 수명 분리', [
         ['지속성', '프로세스 메모리 밖에 데이터를 보관', 'Express 종료·재시작 후에도 같은 DB 행 조회'],
         ['역할 분담', '플랫폼은 DB 운영, 개발자는 구조와 요청 처리 담당', 'SQL로 데이터 규칙 정의 · Express로 기존 API와 검증 유지'],
         ['학습의 연결', '관계형 모델과 SQL을 웹서비스 요청에 적용', '클라이언트 → 서버 → DB의 전체 흐름을 실제 배포 환경에서 확인']]),
     ('Why a Managed Database Matters', 'Separate data lifetime from the server process', [
         ['Persistence', 'Keep data outside process memory', 'The same database rows remain after Express restarts'],
         ['Responsibilities', 'The platform operates the DB; developers define data and requests', 'SQL defines data rules; Express preserves API behavior and validation'],
         ['Learning connection', 'Apply relational models and SQL to web requests', 'Observe client → server → database in the deployed application']]),
     [SB+'guides/database/overview'])

page('foodmap-architecture',
     ('이번 실습의 요청 흐름', '기존 클라이언트 API 뒤에 Supabase 연결', [
         ['클라이언트 요청', 'React는 기존 Express API 호출', '브라우저에 Supabase Secret key를 전달하지 않는 구조'],
         ['서버 요청', 'Express가 SDK로 Data API에 접근', 'HTTP 데이터 요청이 PostgreSQL 조회·입력으로 이어지고 결과가 기존 응답으로 반환']]),
     ('Request Flow in This Practice', 'Connect Supabase behind the existing client API', [
         ['Client request', 'React calls the existing Express API', 'The Supabase secret key stays on the server'],
         ['Server request', 'Express uses the SDK to call the Data API', 'HTTP data requests reach PostgreSQL and results return through the existing response shape']]),
     [SB+'guides/api', SB+'guides/getting-started/api-keys'],
     steps=([['Vercel · React', '목록·상세·등록 요청'], ['Render · Express', '입력 검증 · SDK 호출 · 응답 변환'], ['Supabase · PostgreSQL', 'Data API를 통한 행 조회·저장']],
            [['Vercel · React', 'List, detail, and create requests'], ['Render · Express', 'Validation, SDK calls, and response mapping'], ['Supabase · PostgreSQL', 'Read and persist rows through the Data API']]))

page('foodmap-design',
     ('pwd-week7의 저장 범위', '완료된 구현의 실제 저장 위치', [
         ['실습 테이블', '기존 Restaurant의 10개 필드 저장', '앞 장의 제보–맛집 관계 SQL은 별도 설계 예제 · 이번 실행 스키마는 restaurants 하나'],
         ['동작 유지', '저장소 변경 후에도 기존 API와 화면 사용', '평점순 인기 목록 · 기존 생성 요청 · 비활성 수정·삭제 버튼 유지']]),
     ('Persistence Scope of pwd-week7', 'Actual storage locations in the completed implementation', [
         ['Practice table', 'Store the ten existing Restaurant fields', 'The earlier submission relationship is a separate design example; this schema has one restaurants table'],
         ['Compatibility', 'Keep the existing API and screens', 'Rating-based popularity, create requests, and disabled edit/delete buttons remain']]),
     table=({'head': ['정보', '현재 저장 위치'], 'rows': [
         ['맛집 기본 정보', 'Supabase restaurants'], ['제보·승인 상태', '기존 브라우저 LocalStorage'],
         ['화면의 좋아요 상태', '기존 브라우저 LocalStorage'], ['이미지', 'DB에는 URL 문자열 · 파일은 기존 외부 서버']]},
            {'head': ['Information', 'Current location'], 'rows': [
         ['Restaurant fields', 'Supabase restaurants'], ['Submissions and approval state', 'Existing browser LocalStorage'],
         ['UI like state', 'Existing browser LocalStorage'], ['Images', 'URL text in DB; files on existing external servers']]}),
     note='DB의 likes 열은 기존 Restaurant 필드로 보존. 클라이언트 좋아요 상태의 DB 연동을 의미하지 않는다. 이미지 파일 이전은 보류.')

page('project',
     ('Supabase 프로젝트 준비', 'SQL을 실행할 데이터베이스와 연결 정보 확보', [
         ['프로젝트', '이름·지역·DB 암호를 정해 생성하는 관리 단위', '대시보드의 SQL Editor와 Table Editor가 같은 프로젝트 DB 사용'],
         ['연결 정보', 'Project URL과 서버용 Secret key 준비', 'Express의 환경변수에만 설정 · Data API 활성화 확인']]),
     ('Prepare a Supabase Project', 'Obtain the database and connection settings', [
         ['Project', 'A management unit created with a name, region, and DB password', 'SQL Editor and Table Editor use the same project database'],
         ['Connection settings', 'Obtain the Project URL and a server secret key', 'Set them in Express environment variables and enable the Data API']]),
     [SB+'guides/getting-started/quickstarts/reactjs', SB+'guides/getting-started/api-keys'])

page('build-flow',
     ('실행한 SQL 파일의 역할', '구조와 권한을 준비한 뒤 초기 데이터 입력', [
         ['schema.sql', '테이블·접근 권한·초기화 함수 정의', '함수 정의만으로 기존 행이 초기화되지는 않음'],
         ['seed.sql', '테이블이 비어 있을 때만 원본 3건 입력', '행이 있으면 초기화 함수를 호출하지 않는 조건부 실행']]),
     ('Roles of the SQL Files', 'Prepare structure and permissions before seeding', [
         ['schema.sql', 'Define the table, privileges, and reset function', 'Defining the function does not reset existing rows'],
         ['seed.sql', 'Insert the three original rows only into an empty table', 'Skip the reset function when rows already exist']]),
     note='원본: pwd-week7/supabase/schema.sql 및 seed.sql. 서버 시작·배포 시 두 파일을 자동 실행하지 않는다.')

page('sql-editor',
     ('SQL 실행과 결과 확인', '같은 데이터베이스를 다루는 두 관리 도구', [
         ['SQL Editor', 'SQL 문장을 DB에 실행하는 도구', 'schema.sql → seed.sql 순서로 실행한 뒤 SELECT로 결과 확인'],
         ['Table Editor', '테이블의 열과 행을 시각적으로 확인하는 도구', '원본 맛집 3건과 등록 후 추가 행 확인 · 관리자 조회와 API 권한은 별개']]),
     ('Run SQL and Inspect Results', 'Two management tools for the same database', [
         ['SQL Editor', 'Runs SQL statements against the database', 'Run schema.sql, then seed.sql, and inspect results with SELECT'],
         ['Table Editor', 'Displays table columns and rows', 'Check seed rows and created rows; administrator access differs from API privileges']]),
     [SB+'guides/database/tables', SB+'guides/database/postgres/row-level-security'])

page('table-schema',
     ('restaurants 테이블 생성', '스키마 이름·테이블 이름·열 정의의 구성', [
         ['CREATE TABLE', '이름과 열 정의로 저장 구조 생성', 'public.restaurants는 public 스키마 안의 restaurants 테이블'],
         ['IF NOT EXISTS', '같은 이름의 테이블이 있으면 생성 생략', '기존 테이블의 잘못된 열이나 제약을 수정하는 명령은 아님']]),
     ('Create the restaurants Table', 'Schema name, table name, and column definitions', [
         ['CREATE TABLE', 'Create a storage structure from column definitions', 'public.restaurants identifies the table within the public schema'],
         ['IF NOT EXISTS', 'Skip creation if that table name already exists', 'It does not repair an existing table with different columns or constraints']]),
     [PG+'sql-createtable.html', PG+'ddl-schemas.html'],
     code="create table if not exists public.restaurants (\n  id bigint generated by default\n    as identity primary key,\n  name text not null,\n  category text not null,\n  location text not null,\n  price_range text not null default '정보 없음',\n  rating numeric not null default 0,\n  description text not null default '',\n  recommended_menu text[] not null default '{}',\n  likes integer not null default 0,\n  image text not null default ''\n);",
     label=('schema.sql · 테이블 정의 전체 · 줄바꿈 조정', 'schema.sql · Complete table definition · Reflowed'))

page('column-types',
     ('실습 열의 자료형', '저장할 값의 형태에 맞춘 PostgreSQL 타입', [
         ['자료형', '각 열에 저장 가능한 값의 종류 지정', '평점은 numeric · 좋아요 수는 integer · 식별자는 bigint'],
         ['문자열', '이름·위치·가격대·설명·이미지 주소를 text로 저장', 'image의 값은 파일 내용이 아닌 URL 또는 빈 문자열']]),
     ('Column Types in the Practice', 'PostgreSQL types matched to stored values', [
         ['Data type', 'Specifies the kind of value stored in a column', 'numeric for ratings, integer for likes, bigint for identifiers'],
         ['Text', 'Names, locations, price ranges, descriptions, and image addresses', 'image contains a URL or an empty string, rather than file bytes']]),
     [PG+'datatype.html'],
     table=({'head': ['자료형', '이번 테이블의 열'], 'rows': [['bigint', 'id'], ['text', 'name · category · location · price_range'], ['text', 'description · image'], ['numeric · integer', 'rating · likes'], ['text[]', 'recommended_menu']]},
            {'head': ['Type', 'Columns in this table'], 'rows': [['bigint', 'id'], ['text', 'name · category · location · price_range'], ['text', 'description · image'], ['numeric · integer', 'rating · likes'], ['text[]', 'recommended_menu']]}))

page('table-identity',
     ('맛집 ID의 자동 생성', '값 생성은 IDENTITY · 중복 방지는 PRIMARY KEY', [
         ['IDENTITY', '연결된 시퀀스로 생략된 ID 값 생성', 'BY DEFAULT는 명시적인 ID 입력도 허용 · 원본 3건의 ID 복원에 사용'],
         ['PRIMARY KEY', '행 식별 값의 중복과 NULL 금지', '자동 생성만으로 고유성이나 빈 번호 없는 연속성을 보장하지 않음']]),
     ('Generate Restaurant IDs', 'IDENTITY generates values; PRIMARY KEY enforces uniqueness', [
         ['IDENTITY', 'Uses an associated sequence when an ID is omitted', 'BY DEFAULT also permits explicit IDs, used to restore the three original IDs'],
         ['PRIMARY KEY', 'Disallows duplicate or NULL identifiers', 'Generation alone does not guarantee uniqueness or gapless numbering']]),
     [PG+'ddl-identity-columns.html', PG+'ddl-constraints.html'],
     code='id bigint generated by default\n  as identity primary key',
     label=('schema.sql · id 열 정의 발췌', 'schema.sql · ID column excerpt'))

page('table-not-null',
     ('NOT NULL 제약조건', '값이 없음을 나타내는 NULL의 저장 제한', [
         ['필수 값', 'NOT NULL 열에는 NULL을 저장할 수 없음', '기본값 없는 name·category·location은 입력 값 필요'],
         ['빈 문자열', 'NULL과 다른 문자열 값', 'NOT NULL만으로 공백·빈 문자열을 막지 않으므로 기존 서버 검증도 유지']]),
     ('The NOT NULL Constraint', 'Prevent SQL NULL values in a column', [
         ['Required values', 'A NOT NULL column cannot store NULL', 'name, category, and location have no default and require values'],
         ['Empty strings', 'String values distinct from NULL', 'NOT NULL alone does not reject blanks; existing server validation remains']]),
     [PG+'ddl-constraints.html'], code='name text not null,\ncategory text not null,\nlocation text not null,',
     label=('schema.sql · 필수 열 발췌', 'schema.sql · Required column excerpts'))

page('table-default',
     ('DEFAULT 기본값', '입력에서 생략한 열에 사용할 값', [
         ['적용 시점', '열을 생략하거나 DEFAULT를 지정할 때 적용', '명시한 NULL을 기본값으로 바꾸는 규칙은 아님'],
         ['실습 값', '미입력 정보의 초기 표현 정의', '가격대는 정보 없음 · 평점·좋아요 수는 0 · 설명·이미지는 빈 문자열']]),
     ('DEFAULT Values', 'Values used for omitted columns', [
         ['When applied', 'Used when a column is omitted or DEFAULT is requested', 'An explicit NULL is not replaced with the default'],
         ['Practice values', 'Define initial representations of missing information', 'Unknown price range, zero rating and likes, empty description and image']]),
     [PG+'ddl-default.html'],
     code="price_range text not null default '정보 없음',\nrating numeric not null default 0,\ndescription text not null default '',\nlikes integer not null default 0,\nimage text not null default ''",
     label=('schema.sql · 기본값이 있는 열 발췌', 'schema.sql · Columns with defaults'))

page('table-array',
     ('추천 메뉴의 배열 저장', '여러 문자열을 하나의 text[] 열에 보관', [
         ['text[]', '문자열 원소를 담는 PostgreSQL 배열 타입', '클라이언트의 recommendedMenu 배열과 대응'],
         ['배열 값', '빈 배열은 원소가 없는 값 · NULL과 구별', '초기 데이터의 ARRAY[...]는 메뉴 원소 구성 · ::text[]는 타입 지정']]),
     ('Store Recommended Menus as an Array', 'Multiple strings in one text[] column', [
         ['text[]', 'A PostgreSQL array of text elements', 'Maps to the client recommendedMenu array'],
         ['Array values', 'An empty array has no elements and differs from NULL', 'ARRAY[...] constructs seed menu elements; ::text[] specifies the type']]),
     [PG+'arrays.html'],
     code="recommended_menu text[] not null default '{}'\n\narray['떡볶이', '튀김', '순대', '어묵']::text[]",
     label=('schema.sql · 열 정의와 초기 데이터 배열 표현 발췌', 'schema.sql · Column definition and seed array excerpts'))

page('access',
     ('API 키와 DB 역할', '요청이 실행될 권한의 기준', [
         ['공개 키', '브라우저 등에 배포할 수 있는 Publishable key', '로그인 없는 요청은 anon 역할 · 이번 테이블의 직접 접근 권한 없음'],
         ['서버 키', 'Express에서 사용하는 Secret key', 'service_role로 요청 · RLS 우회 권한이 있어 서버 환경변수에서 보호']]),
     ('API Keys and Database Roles', 'The privileges under which a request runs', [
         ['Publishable key', 'A key that may be shipped to a browser', 'Requests without a signed-in user use anon; this table grants it no direct access'],
         ['Secret key', 'The key used by Express', 'Requests use service_role, which bypasses RLS; keep it in server environment variables']]),
     [SB+'guides/getting-started/api-keys'],
     note='서버 SUPABASE_SECRET_KEY에는 sb_secret_ 키. authenticated는 로그인한 사용자 요청의 역할이며 이번 실습에 사용자 인증을 추가하지 않는다.')

page('rls',
     ('RLS와 테이블 접근', '행 정책과 객체 권한의 구분', [
         ['RLS', '일반 역할의 접근 가능 행을 정책으로 제한', 'SQL로 만든 테이블은 명시적으로 활성화 · 정책이 없으면 일반 역할의 행 접근 기본 차단'],
         ['이번 실습', 'anon·authenticated의 테이블 권한 회수', 'Express의 service_role은 RLS 우회 · 테이블 자체의 SQL 권한은 별도로 필요']]),
     ('RLS and Table Access', 'Distinguish row policies from object privileges', [
         ['RLS', 'Policies restrict rows available to ordinary roles', 'Enable it explicitly for SQL-created tables; no policy means default denial for ordinary roles'],
         ['This practice', 'Revoke table privileges from anon and authenticated', 'Express uses service_role to bypass RLS; SQL object privileges are still required']]),
     [SB+'guides/database/postgres/row-level-security', PG+'ddl-rowsecurity.html'],
     code='alter table public.restaurants\n  enable row level security;\nrevoke all on table public.restaurants\n  from anon, authenticated;',
     label=('schema.sql · 행 정책 활성화와 권한 회수', 'schema.sql · Enable RLS and revoke privileges'))

page('table-privileges',
     ('서버의 테이블 권한', '대상 객체와 허용할 작업을 지정하는 GRANT', [
         ['스키마 USAGE', '해당 스키마 안 객체에 접근할 기반 권한', '스키마 사용 권한만으로 테이블 조회·등록이 허용되지는 않음'],
         ['테이블 권한', 'SELECT 조회 · INSERT 입력 · DELETE 삭제 허용', 'DELETE는 기존 초기화 함수에 필요 · GRANT와 REVOKE는 행 데이터를 변경하지 않음']]),
     ('Server Table Privileges', 'GRANT specifies the object and allowed operations', [
         ['Schema USAGE', 'Allows access to objects within the schema', 'Schema access alone does not grant table reads or inserts'],
         ['Table privileges', 'Allow SELECT, INSERT, and DELETE', 'DELETE supports the existing reset function; GRANT and REVOKE do not change rows']]),
     [PG+'ddl-priv.html', PG+'sql-grant.html'],
     code='grant usage on schema public\n  to service_role;\ngrant select, insert, delete\n  on table public.restaurants\n  to service_role;',
     label=('schema.sql · 스키마와 테이블 권한', 'schema.sql · Schema and table grants'))

page('sequence-privileges',
     ('ID 시퀀스의 권한', '번호 생성 객체는 테이블과 별도로 관리', [
         ['시퀀스', 'IDENTITY의 번호 상태를 관리하는 DB 객체', 'restaurants_id_seq는 restaurants 테이블과 다른 권한 대상'],
         ['허용 작업', 'USAGE·SELECT·UPDATE를 서버 역할에 부여', '번호 생성·조회·재설정에 사용하는 권한 · setval에는 UPDATE 필요']]),
     ('ID Sequence Privileges', 'The number generator is a separate database object', [
         ['Sequence', 'A database object holding IDENTITY number state', 'restaurants_id_seq is a different privilege target from the table'],
         ['Allowed operations', 'Grant USAGE, SELECT, and UPDATE to the server role', 'Privileges support generating, reading, and resetting sequence values; setval needs UPDATE']]),
     [PG+'sql-grant.html', PG+'functions-sequence.html'],
     code='grant usage, select, update\n  on sequence public.restaurants_id_seq\n  to service_role;',
     label=('schema.sql · 시퀀스 권한', 'schema.sql · Sequence grant'))

page('function-definition',
     ('초기화 함수의 정의', '여러 SQL 작업을 이름 있는 DB 함수로 묶기', [
         ['CREATE OR REPLACE FUNCTION', 'DB에 호출 가능한 함수 정의를 저장', '빈 괄호는 입력 인자 없음 · RETURNS void는 반환할 데이터 없음'],
         ['함수 본문', 'PL/pgSQL로 작성한 실행 영역', '$$는 본문 문자열의 경계 · BEGIN과 END는 문장 블록의 경계']]),
     ('Define the Reset Function', 'Group SQL operations in a named database function', [
         ['CREATE OR REPLACE FUNCTION', 'Store a callable function definition', 'Empty parentheses mean no arguments; RETURNS void means no result data'],
         ['Function body', 'An execution block written in PL/pgSQL', '$$ delimits the body string; BEGIN and END delimit the statement block']]),
     [PG+'sql-createfunction.html', PG+'plpgsql-structure.html'],
     code="create or replace function\n  public.reset_restaurant_demo_data()\nreturns void\nlanguage plpgsql\nsecurity invoker\nset search_path = ''\nas $$",
     label=('schema.sql · 함수 선언부 발췌 · 본문은 다음 화면', 'schema.sql · Function header excerpt · Body follows'),
     note='함수 정의와 실행은 다르다. schema.sql을 실행해 정의해도 본문이 즉시 실행되지 않는다. BEGIN/END는 SQL의 BEGIN/COMMIT 트랜잭션 명령이 아니다.')

page('function-context',
     ('함수의 실행 환경', '호출자 권한과 객체 이름의 해석', [
         ['SECURITY INVOKER', '함수를 호출한 역할의 권한으로 실행', 'Express의 service_role에 부여한 테이블·시퀀스 권한을 사용'],
         ['search_path', '접두어 없는 객체 이름을 찾는 경로', '빈 경로를 설정하고 public·pg_catalog를 명시해 사용할 객체를 식별']]),
     ('Function Execution Context', 'Caller privileges and object-name resolution', [
         ['SECURITY INVOKER', 'Run with the privileges of the calling role', 'Use the table and sequence privileges granted to Express service_role'],
         ['search_path', 'The lookup path for unqualified object names', 'Use an empty path and explicit public or pg_catalog qualification to identify objects']]),
     [PG+'sql-createfunction.html', PG+'ddl-schemas.html'],
     code="security invoker\nset search_path = ''\n\npublic.restaurants\npg_catalog.setval",
     label=('schema.sql · 실행 설정과 이름 표현 발췌', 'schema.sql · Execution settings and name excerpts'))

page('reset-rows',
     ('초기화 함수의 데이터 처리', '현재 행을 제거하고 원본 3건 복원', [
         ['삭제', 'WHERE 없는 DELETE로 모든 행 제거', '추가 등록한 맛집도 대상 · 테이블의 열 구조는 유지'],
         ['입력', 'INSERT의 열 순서에 맞춰 원본 값 입력', 'id 1·2·3을 명시 · 메뉴는 text[] · image는 기존 외부 URL 문자열']]),
     ('Data Operations in the Reset Function', 'Remove current rows and restore the three originals', [
         ['Delete', 'DELETE without WHERE removes every row', 'Includes newly created restaurants while preserving the table structure'],
         ['Insert', 'Values follow the explicit INSERT column order', 'Restore IDs 1, 2, 3, text[] menus, and existing external image URLs']]),
     [PG+'sql-delete.html', PG+'sql-insert.html'],
     table=({'head': ['명시한 id', '원본 이름', '평점'], 'rows': [['1', '송림식당', '4.99'], ['2', '별미떡볶이', '4.92'], ['3', 'SOGO', '4.89']]},
            {'head': ['Explicit ID', 'Original name', 'Rating'], 'rows': [['1', '송림식당', '4.99'], ['2', '별미떡볶이', '4.92'], ['3', 'SOGO', '4.89']]}),
     note='전체 INSERT 값은 pwd-week7/supabase/schema.sql 원문. POST /api/restaurants/reset-demo의 기존 동작을 유지하기 위한 함수이며 데이터 유지 검증에서 호출하지 않는다.')

page('reset-transaction',
     ('초기화의 실행 단위', '한 호출 안에서 삭제와 입력을 함께 처리', [
         ['행 변경의 원자성', '처리되지 않은 오류가 나면 삭제·입력 롤백', '삭제만 반영되고 원본 입력은 빠지는 중간 상태 방지'],
         ['테이블 잠금', '초기화 동안 다른 쓰기 작업의 진행 제한', 'EXCLUSIVE 잠금은 트랜잭션 종료까지 유지 · 일반 SELECT는 가능']]),
     ('Execution Unit of the Reset', 'Delete and insert within one function call', [
         ['Atomic row changes', 'An unhandled error rolls back the deletes and inserts', 'Prevents committing a deletion without restoring the original rows'],
         ['Table lock', 'Restrict concurrent writes while resetting', 'An EXCLUSIVE lock lasts until transaction end; ordinary SELECT remains possible']]),
     [PG+'tutorial-transactions.html', PG+'explicit-locking.html', PG+'functions-sequence.html'],
     code='begin\n  lock table public.restaurants\n    in exclusive mode;\n  delete from public.restaurants;',
     label=('schema.sql · 함수 본문 시작 부분 발췌', 'schema.sql · Beginning of the function body'),
     note='BEGIN/END는 PL/pgSQL 블록. 함수 호출은 호출한 SQL의 트랜잭션 안에서 실행된다. 시퀀스 setval 변경은 롤백되지 않으므로 행 변경의 롤백과 구별한다.')

page('reset-sequence',
     ('초기 ID와 시퀀스 맞추기', '명시한 1·2·3 다음 번호를 4로 설정', [
         ['시퀀스 찾기', 'pg_get_serial_sequence로 id에 연결된 객체 확인', '수동으로 ID를 입력해도 시퀀스 번호가 자동으로 맞춰지는 것은 아님'],
         ['setval', '현재 번호 3 · 이미 사용한 상태 true로 설정', '다음 자동 번호는 4 · 시퀀스 상태 변경은 트랜잭션 롤백 대상이 아님']]),
     ('Align Seed IDs with the Sequence', 'Set the next number to 4 after explicit IDs 1, 2, 3', [
         ['Find the sequence', 'pg_get_serial_sequence identifies the sequence for id', 'Explicitly inserting an ID does not automatically align sequence state'],
         ['setval', 'Set the current value to 3 and is_called to true', 'The next generated value is 4; sequence state changes are not rolled back']]),
     [PG+'functions-sequence.html', PG+'functions-info.html'],
     code="perform pg_catalog.setval(\n  pg_catalog.pg_get_serial_sequence(\n    'public.restaurants', 'id'),\n  3, true);",
     label=('schema.sql · 초기화 함수의 번호 재설정', 'schema.sql · Sequence reset in the function'))

page('function-privileges',
     ('초기화 함수의 실행 권한', '함수 호출도 EXECUTE 권한으로 제어', [
         ['권한 회수', 'PUBLIC·anon·authenticated의 호출 권한 회수', '여기서 PUBLIC은 모든 역할 · public 스키마 이름과 다른 의미'],
         ['서버 호출', 'service_role에 EXECUTE 허용', '기존 reset-demo API가 SDK의 rpc로 호출 · 함수 내부 작업 권한도 필요']]),
     ('Reset Function Execution Privileges', 'EXECUTE controls who may call a function', [
         ['Revoke', 'Remove calls by PUBLIC, anon, and authenticated', 'PUBLIC means every role here, distinct from the public schema name'],
         ['Server call', 'Grant EXECUTE to service_role', 'The existing reset-demo API calls SDK rpc; privileges for the operations inside are also needed']]),
     [PG+'ddl-priv.html', PG+'sql-grant.html', SB+'reference/javascript/rpc'],
     code='revoke all on function\n  public.reset_restaurant_demo_data()\n  from public, anon, authenticated;\ngrant execute on function\n  public.reset_restaurant_demo_data()\n  to service_role;',
     label=('schema.sql · 함수 권한', 'schema.sql · Function privileges'))

page('seed-block',
     ('최초 데이터의 조건부 입력', 'seed.sql은 테이블이 비어 있을 때만 실행', [
         ['DO 블록', '이름을 저장하지 않는 일회성 PL/pgSQL 실행', 'IF NOT EXISTS는 SELECT 1 결과 행의 존재 여부 검사'],
         ['PERFORM', '반환값을 받지 않고 함수 실행', '빈 테이블이면 원본 3건 복원 · 행이 있으면 생략하므로 재실행 시 기존 데이터 유지']]),
     ('Conditional Initial Data', 'seed.sql runs the reset only for an empty table', [
         ['DO block', 'Execute an anonymous PL/pgSQL block once', 'IF NOT EXISTS tests whether SELECT 1 returns any row'],
         ['PERFORM', 'Run a function without consuming its result', 'Restore three originals only when empty; existing rows survive repeated seeding']]),
     [PG+'sql-do.html', PG+'plpgsql-statements.html', PG+'functions-subquery.html'],
     code='do $$\nbegin\n  if not exists (\n    select 1 from public.restaurants\n  ) then\n    perform public.reset_restaurant_demo_data();\n  end if;\nend;\n$$;',
     label=('seed.sql · 전체 · 줄바꿈 조정', 'seed.sql · Complete script · Reflowed'),
     note='순차 재실행에서 기존 행을 유지하는 초기 데이터 입력용. schema.sql의 CREATE TABLE IF NOT EXISTS는 객체 존재 검사, seed.sql의 IF NOT EXISTS는 행 존재 검사.')

page('verify-query',
     ('저장 결과의 SQL 조회', '원본 3건과 이후 등록 행을 같은 테이블에서 확인', [
         ['SELECT', '필요한 열을 골라 저장된 행 조회', 'FROM으로 테이블 선택 · ORDER BY id로 식별자 순서 정렬'],
         ['확인 기준', '이름·가격대·평점·메뉴 배열의 값 확인', '입력하지 않은 새 맛집 ID가 DB에서 자동 생성되는지도 확인']]),
     ('Query the Stored Results', 'Inspect seed and newly created rows in the same table', [
         ['SELECT', 'Read selected columns from stored rows', 'FROM selects the table; ORDER BY id orders rows by identifier'],
         ['Verification', 'Check names, price ranges, ratings, and menu arrays', 'Also verify that the DB generates an omitted ID for a new restaurant']]),
     [PG+'sql-select.html'],
     code='select id, name, price_range,\n       rating, recommended_menu\nfrom public.restaurants\norder by id;',
     label=('실습 확인용 SQL · 데이터 변경 없음', 'Practice verification SQL · Read only'))

page('server-mapping',
     ('DB 행과 기존 API의 대응', '저장 형태를 바꾸어도 클라이언트의 약속 유지', [
         ['입력', '서버가 기존 요청을 검증한 뒤 DB 열 이름으로 변환', 'ID는 생략해 DB에서 생성 · insert 후 저장된 행 반환'],
         ['출력', 'DB 행을 Restaurant 모델의 기존 필드로 변환', '목록·상세·인기 응답은 { data: ... } 유지 · 등록 성공 201 유지']]),
     ('Map Database Rows to the Existing API', 'Keep the client contract while changing persistence', [
         ['Input', 'Validate existing requests and map to DB column names', 'Omit ID for database generation and return the inserted row'],
         ['Output', 'Convert rows into existing Restaurant fields', 'Keep { data: ... } for list, detail, and popular responses, and 201 for creation']]),
     [SB+'reference/javascript/insert'],
     table=({'head': ['DB 열', '기존 API 필드'], 'rows': [['price_range', 'priceRange'], ['recommended_menu', 'recommendedMenu'], ['name · rating · image 등', '동일한 이름 유지']]},
            {'head': ['DB column', 'Existing API field'], 'rows': [['price_range', 'priceRange'], ['recommended_menu', 'recommendedMenu'], ['name · rating · image, etc.', 'Keep the same names']]}),
     note='대응 코드: pwd-week7/src/services/restaurants.service.ts 및 src/models/restaurant.model.ts. 인기 목록은 기존처럼 서버에서 rating 내림차순 정렬.')

page('server-persistence',
     ('서버 재시작과 영구 저장 검증', '프로세스를 바꾸어도 동일한 DB 행 유지', [
         ['검증 절차', '등록 → 반환 ID 조회 → 종료 → 새 프로세스로 재시작', '재시작 후 같은 ID·필드 조회 · Supabase의 실제 행과 비교'],
         ['확인 결과', 'id 4의 등록 데이터가 재시작 후에도 동일', '원본 3건도 유지 · 전체 4건 확인 · 초기화 API 호출 없이 검증']]),
     ('Verify Persistence Across a Restart', 'Keep the same database row across server processes', [
         ['Procedure', 'Create → read returned ID → stop → start a new process', 'Read the same ID and fields, then compare with the actual Supabase row'],
         ['Observed result', 'The created row with ID 4 remained identical', 'The three originals also remained; four total rows, without calling reset']]),
     steps=([['등록', 'POST 응답 201 · id 4'], ['재시작', '서버 프로세스 완전 종료 후 새로 실행'], ['대조', '같은 상세 응답 · 실제 Supabase 행 일치']],
            [['Create', 'POST returns 201 and ID 4'], ['Restart', 'Stop the process completely and start a new one'], ['Compare', 'Same detail response and matching actual Supabase row']]),
     note='완료된 검증 기록 기준. 연결 대상은 실제 Supabase이며 이 강의 작성 중 추가 등록·초기화를 실행하지 않았다. 이후 데이터가 바뀌면 행 수와 ID는 달라질 수 있다.')

page('deploy-verification',
     ('배포 환경의 연결 설정', 'Vercel은 Express 주소 · Render는 Supabase 자격 증명', [
         ['Vercel', 'VITE_API_BASE_URL에 기존 Render 주소 설정', 'https://ajou-food-map.onrender.com · 기존 클라이언트 API 경로 유지'],
         ['Render', 'pwd-week7 서버에 DB 환경변수 설정', 'SUPABASE_URL · SUPABASE_SECRET_KEY · 배포 후 DB 목록과 상세로 확인']]),
     ('Connection Settings in Deployment', 'Vercel uses the Express URL; Render holds Supabase credentials', [
         ['Vercel', 'Set VITE_API_BASE_URL to the existing Render URL', 'https://ajou-food-map.onrender.com with the same client API paths'],
         ['Render', 'Set database environment variables for the pwd-week7 server', 'SUPABASE_URL and SUPABASE_SECRET_KEY; verify using database-backed list and detail responses']]),
     note='/health는 Express 프로세스 응답이며 DB 연결 증거가 아니다. Render 소스는 pwd-week7/main. 공개 API만으로 배포 커밋 SHA를 판별했다고 주장하지 않는다.')

page('failure-cases',
     ('실제로 확인한 연결 오류', '오류가 난 계층과 설정의 대응', [
         ['점검 순서', '서버 실행 → 환경변수 → DB 권한 → API → 화면', '연결 실패를 화면 문제로 단정하지 않고 실제 오류와 설정 대조']]),
     ('Connection Errors Observed in Practice', 'Match each failure to the responsible setting', [
         ['Check order', 'Server → environment → DB privileges → API → UI', 'Compare actual errors with settings before diagnosing a UI failure']]),
     [SB+'guides/getting-started/api-keys'],
     table=({'head': ['관찰한 문제', '확인·해결한 내용'], 'rows': [
         ['Publishable key 사용 · 42501', 'Express에 서버용 Secret key 설정'],
         ['Render에 DB 환경변수 없음', '해당 서비스에 두 SUPABASE 변수 추가·재배포'],
         ['API 3건 · DB 4건', 'Render 소스 저장소와 Live 배포 확인']]},
            {'head': ['Observed issue', 'Check and resolution'], 'rows': [
         ['Publishable key used · 42501', 'Set a server secret key in Express'],
         ['Missing DB variables on Render', 'Add both SUPABASE variables to that service and redeploy'],
         ['API has 3 rows; DB has 4', 'Check the Render source repository and live deployment']]}))

page('lab-check',
     ('7주차 실습의 완료 기준', 'SQL 정의부터 기존 화면까지 결과 대조', [
         ['SQL 이해', '테이블·열·제약·권한·초기화·시딩의 역할 설명', 'schema.sql은 구조 정의 · seed.sql은 조건부 입력 · reset-demo는 전체 초기화'],
         ['동작 확인', 'DB와 API와 Vercel 화면의 같은 맛집 정보 확인', '목록·상세·평점순 인기 목록 · 재시작 후 등록 행 유지'],
         ['검증된 범위', '실제 DB 4건과 공개 API·클라이언트 조회 일치', '이미지 URL 표시 유지 · 파일 업로드·제보·좋아요의 DB 이전은 이번 완료 범위 밖']]),
     ('Week 7 Practice Completion Criteria', 'Compare results from SQL definitions to the existing UI', [
         ['SQL understanding', 'Explain columns, constraints, privileges, reset, and seed', 'schema.sql defines structure; seed.sql conditionally inserts; reset-demo resets all rows'],
         ['Behavior', 'Match restaurant data in the DB, API, and Vercel UI', 'Lists, details, rating-based popularity, and created-row persistence after restart'],
         ['Verified scope', 'Four actual DB rows match the public API and client', 'Existing image URL display remains; file upload and DB migration of submissions or likes are outside this completed practice']]),
     note='검증 완료 시점의 결과. 기존 API와 클라이언트 동작 유지. 새 기능을 구현하거나 현재 공개 데이터를 변경하는 작업은 포함하지 않는다.')
