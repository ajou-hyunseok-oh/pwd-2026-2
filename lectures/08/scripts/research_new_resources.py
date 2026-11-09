"""Research candidates for the 44 Week 8 slides without placed PDF resources.

This produces review records only. It does not modify the slide body or renderer.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from title_outline import proposal

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'materials/new-resource-research'
DATE = '2026-11-07'


def source(ident, title, url, section, use):
    return dict(id=ident, title=title, url=url, section=section, use=use,
                checked_on=DATE)


SOURCES = [
    source('authn', 'OWASP · Authentication',
           'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html',
           'User IDs / Login Throttling / Secure Federated Account Linking',
           '사용자 식별, 계정 연결, 로그인 제한의 근거. FoodMap 표·도식은 자체 설계.'),
    source('authz', 'OWASP · Authorization',
           'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html',
           'Least Privilege / Deny by Default / Validate Permissions on Every Request',
           '기본 거부·요청별 권한 판단의 근거. 역할표와 업무 정책은 강의 사례로 작성.'),
    source('password', 'OWASP · Password Storage',
           'https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html',
           'Hashing vs Encryption / Salting / Password Hashing Algorithms',
           '전용 비밀번호 해시와 솔트의 역할. 원문 그림이나 구현 코드를 복사하지 않음.'),
    source('session', 'OWASP · Session Management',
           'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html',
           'Automatic Session Expiration: Idle Timeout / Absolute Timeout',
           '서버가 적용하는 세션 만료를 시간축으로 재구성.'),
    source('http', 'MDN · Overview of HTTP',
           'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview#http_is_stateless_but_not_sessionless',
           'HTTP is stateless, but not sessionless',
           '서로 다른 요청 사이의 인증 상태 연결 문제를 설명하는 근거.'),
    source('jws', 'IETF · RFC 7515 JSON Web Signature',
           'https://www.rfc-editor.org/rfc/rfc7515.html#section-3',
           '§3 Overview', '서명 또는 MAC의 무결성 역할만 참조. 직렬화 수식은 제외.'),
    source('refresh', 'IETF · RFC 6749 OAuth 2.0',
           'https://www.rfc-editor.org/rfc/rfc6749.html#section-1.5',
           '§1.5 Figure 2: Refreshing an Expired Access Token',
           '실제 시퀀스 원형. 갱신 자격을 받는 인증 서버와 데이터 API의 구분을 유지.'),
    source('oidc', 'OpenID Foundation · OpenID Connect Core 1.0',
           'https://openid.net/specs/openid-connect-core-1_0.html',
           '§2 ID Token / §5.7 Claim Stability and Uniqueness',
           'ID 토큰의 목적과 (iss, sub) 식별 기준. 토큰 원문이나 제공자 화면 대신 비교표로 변환.'),
    source('rls', 'Supabase · Row Level Security',
           'https://supabase.com/docs/guides/database/postgres/row-level-security',
           'Enabling RLS / SELECT policies / auth.uid() returns null when unauthenticated',
           '공식 SELECT 정책 예제를 FoodMap reports.user_id로 수정한 코드 후보.'),
    source('pg-rls', 'PostgreSQL · Row Security Policies',
           'https://www.postgresql.org/docs/current/ddl-rowsecurity.html',
           '정책 조건·테이블 권한·default deny·BYPASSRLS·permissive policies',
           'RLS 적용 범위 검토. TRUE인 행만 허용되며 NULL을 거짓과 같은 값이라고 설명하지 않음.'),
    source('keys', 'Supabase · Understanding API keys',
           'https://supabase.com/docs/guides/getting-started/api-keys',
           'Publishable and secret keys / application vs user authentication',
           '현재 publishable·secret 키 구분과 서버 전용 키의 RLS 우회 범위를 표로 정리.'),
    source('platform', 'Supabase · Access control',
           'https://supabase.com/docs/guides/platform/access-control',
           'Organization and project roles',
           '플랫폼 관리 권한과 앱 내부 운영자 역할이 다른 대상임을 보여주는 참조.'),
    source('workflow', 'OWASP · Transaction Authorization',
           'https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html',
           '§2.5 Application should control which transaction state transitions are allowed',
           '허용된 업무 순서를 서버가 확인한다는 원칙만 참조. 금융 거래 인증 절차는 가져오지 않음.'),
    source('transaction', 'PostgreSQL · Transactions',
           'https://www.postgresql.org/docs/current/tutorial-transactions.html',
           'All-or-nothing / BEGIN / COMMIT / ROLLBACK',
           '두 DB 변경의 원자성을 FoodMap 승인 업무로 재구성.'),
    source('idempotency', 'Stripe · Idempotent requests',
           'https://docs.stripe.com/api/idempotent_requests',
           'Idempotency key and retry handling',
           '요청 식별자와 결과 재사용 사례. Stripe SDK·보관 기간·API별 세부 규칙은 강의 정책으로 복사하지 않음.'),
    source('logging', 'OWASP · Logging',
           'https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html',
           'Event attributes / Data to exclude',
           '행위자·대상·행동·시각·결과를 담은 가상 감사 기록의 필드 선정.'),
    source('input', 'OWASP · Input Validation',
           'https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html',
           'Input Validation Strategies / Implementing Input Validation',
           '형식·자료형·범위 검사 원칙. 길이 제한 수치는 자체 FoodMap 예시.'),
    source('pg-query', 'node-postgres · Queries',
           'https://node-postgres.com/features/queries#parameterized-query',
           'Parameterized query',
           'SQL과 값 배열을 분리하는 공식 API 사용법. 테이블과 검색어는 FoodMap으로 변경.'),
    source('react', 'React · Common components',
           'https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html',
           'children / Dangerously setting the inner HTML',
           '문자열 자식과 HTML 해석의 차이. 텍스트 출력 예제는 자체 작성.'),
    source('origin', 'MDN · Origin',
           'https://developer.mozilla.org/en-US/docs/Glossary/Origin',
           'scheme / hostname / port', 'URL 구성 요소를 색으로 대응시키는 표의 근거.'),
    source('site', 'MDN · Site',
           'https://developer.mozilla.org/en-US/docs/Glossary/Site',
           'Schemeful same-site / registrable domain',
           '출처 비교표에 사이트 판단 열을 추가. 공개 접미사 기준을 보존.'),
    source('sop', 'MDN · Same-origin policy',
           'https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy',
           'Cross-origin network access',
           '요청 전송과 스크립트의 응답 읽기를 다른 화살표로 표시.'),
    source('cors', 'MDN · Cross-Origin Resource Sharing',
           'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS',
           'Simple requests / Preflighted requests / Requests with credentials',
           '실제 SVG 2개 확보. FoodMap 주소와 필수 헤더만 남기는 편집 가능한 재구성 권장.'),
    source('csrf', 'OWASP · Cross-Site Request Forgery Prevention',
           'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html',
           'Synchronizer Token Pattern / Verifying Origin With Standard Headers',
           '자동 첨부 자격과 요청 검증의 차이를 3개 주체 도식으로 설명.'),
    source('environments', 'Supabase · Managing environments',
           'https://supabase.com/docs/guides/deployment/managing-environments',
           'Local development, staging and production diagram',
           '실제 SVG 확보. 환경별 분리 관계를 참조하고 Git 브랜치 흐름은 제거.'),
    source('vite', 'Vite · Env Variables and Modes',
           'https://vite.dev/guide/env-and-mode#env-variables',
           'Env Variables / Security Notes',
           '브라우저 번들에 포함되는 VITE_ 값과 서버 전용 비밀정보의 전달 경로 비교.'),
    source('secrets', 'OWASP · Secrets Management',
           'https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html',
           'Secret lifecycle / Rotation / Revocation',
           '노출된 키의 폐기·교체 원칙. 실제 비밀키나 대시보드 화면은 사용하지 않음.'),
    source('migrations', 'Supabase · Database migrations',
           'https://supabase.com/docs/guides/deployment/database-migrations',
           'Schema migrations / Creating migration files',
           '변경 이력과 SQL 파일의 역할. 명령 실행 절차 대신 열 추가의 전후 비교.'),
    source('telemetry', 'OpenTelemetry · Signals',
           'https://opentelemetry.io/docs/concepts/signals/',
           'Metrics / Logs',
           '측정값과 사건 기록의 역할 참조. 차트 값은 가상 데이터로 직접 구성.'),
    source('backups', 'Supabase · Database backups',
           'https://supabase.com/docs/guides/platform/backups',
           'Backup scope / Restore / Storage objects exclusion',
           '데이터 백업·복원의 범위. DB 사본에 Storage 파일 바이트가 포함되지 않는 제한 보존.'),
    source('rollback', 'Vercel · Performing an Instant Rollback',
           'https://vercel.com/docs/instant-rollback',
           'Previous production deployment / Verify the information',
           '배포 버전 복귀 사례. 외부 DB와 설정의 호환성은 별도 검토 대상으로 표시.'),
]

FAMILIES = {
    'identity': '사용자·계정·제보 연결: 같은 ID와 레코드 카드를 이어 사용',
    'password': '비밀번호 검증: 1.5의 해시 흐름에 1.6에서 솔트 추가',
    'request': '요청·응답 시퀀스: 기존 resource_blocks.py의 레인과 화살표 재사용',
    'time': '시간축: 유효 시간·반복 시도·관측·백업 시점을 같은 읽기 방향으로 표현',
    'policy': '정책 표와 판단 분기: 행위자·행동·대상·조건을 고정된 순서로 배치',
    'operations': '운영 업무: 제보 r101의 화면·상태·DB 변경·이력을 이어 사용',
    'browser': '브라우저 경계: 동일 URL 집합과 브라우저·서버 레인 재사용',
    'environment': '환경·버전·데이터: 개발/검증/운영의 3열을 고정하고 필요한 요소만 추가',
}


def candidate(number, kind, family, name, sources, specification, observation,
              boundary, reuse, priority='보통', effort='소', code=None, figures=()):
    return dict(outline_number=number, resource_type=kind, family=family,
                candidate=name, source_ids=sources.split(), specification=specification,
                intended_observation=observation, learning_boundary=boundary,
                reuse_plan=reuse, priority=priority, effort=effort,
                code_id=code, figure_files=list(figures))


ROWS = [
    candidate('1.1', '관계도', 'identity', '사용자와 제보의 연결 전후', 'authn',
              '맛집 목록 옆에 작성자를 알 수 없는 제보 r101을 놓고, 사용자 u123과 연결한 후의 모습을 비교. 계정 속성은 아직 펼치지 않음.',
              '데이터가 존재하는 것과 그 데이터를 보낸 사람을 구분하는 것은 별개의 문제.',
              '07주차 테이블·관계와 HTTP만 사용. 역할·허용/거부·로그인 토큰은 표시하지 않음.',
              '07주차 데이터 카드 형식; 이후 1.2·3.7·4.3에서도 u123/r101 유지.'),
    candidate('1.2', '표', 'identity', '이름 변경 전후의 사용자 ID와 제보 연결', 'authn',
              '두 시점의 user_id=u123, display_name=민수/민수의 맛지도와 r101.user_id=u123을 나란히 표시.',
              '이름이 달라져도 ID와 제보 연결은 유지됨.',
              '고유 ID는 식별 수단. 비밀번호 증명·외부 계정 연결을 미리 설명하지 않음.',
              '1.1 카드의 사용자 부분만 확장.'),
    candidate('1.3', '도식', 'identity', '클라이언트의 주장과 서버의 확인 경계', 'authn authz',
              '브라우저가 보낸 userId=u999에 ‘변경 가능’ 표시. 서버 경계 너머에는 ‘요청의 주장만으로 신원 확정 불가’ 표시.',
              '요청 본문에 적힌 ID를 곧바로 요청자의 ID로 믿을 수 없음.',
              '해결 방법을 인증·JWT 검증 코드로 앞당기지 않음. 1.4에서 증거 확인을 설명할 여지 유지.',
              '1.1 레코드의 ID를 변경하는 사례만 추가.', priority='우선'),
    candidate('1.5', '흐름도', 'password', '비밀번호 원문과 검증용 값의 저장 경로', 'password',
              '입력 비밀번호 → 비밀번호 전용 해시 처리 → 검증 정보 저장. 원문을 그대로 보관하는 대안과 저장 대상만 비교.',
              '검증 정보를 저장해 입력을 확인하며, 해시도 추측 공격에 대비해야 함.',
              '솔트의 구조는 1.6에 배치. SHA-256 단독 예제·복호화 화살표·자체 암호 구현 제외.',
              '1.6에서 같은 해시 처리 상자에 솔트 입력만 더하고, 기존 1.7 로그인 흐름으로 연결.', priority='우선'),
    candidate('1.6', '표', 'password', '같은 비밀번호·서로 다른 솔트·서로 다른 저장 결과', 'password',
              '열: 계정 / 입력 비밀번호 / 계정별 솔트 / 저장 결과. 두 행은 동일 비밀번호, 서로 다른 salt-A·salt-B와 hash-A·hash-B. 값은 계산 결과가 아닌 도식용 기호로 명시.',
              '솔트는 비밀키가 아니며 같은 비밀번호의 저장 결과를 계정마다 다르게 함.',
              '솔트는 해시와 함께 보관. 검증 시 저장된 솔트를 사용하며 매번 새 솔트로 비교하지 않음. pepper는 제외.',
              '1.5와 같은 입력·처리·저장 색상 사용.', priority='우선'),
    candidate('2.1', '시퀀스', 'request', '로그인 요청과 다음 조회 요청의 분리', 'http',
              '같은 브라우저→서버 레인에 ① 로그인 요청·결과 ② 맛집 조회 요청을 표시. 두 번째 요청에서 이전 결과를 자동으로 알 수 없는 지점에 표시.',
              '로그인 한 번과 여러 요청의 사용자 연결은 서로 다른 문제.',
              '다음 장의 Set-Cookie·Cookie·세션 저장소는 아직 넣지 않음.',
              '기존 2.2~2.4 시퀀스와 주체 위치·화살표 스타일 통일.'),
    candidate('2.5', '비교도', 'request', '토큰 내용 유지와 변조의 검증 결과', 'jws',
              '발급된 ‘사용자 u123 + 서명’과 내용만 u999로 바꾼 증표를 같은 검증 상자에 통과시켜 성공/실패 비교. 검증 상자에는 신뢰하는 발급자의 키 표시.',
              '서명 검증은 변조를 탐지하며 내용을 숨기는 기능과 구분됨.',
              'JWT의 세 부분·Base64url·알고리즘 수식은 2.6 이후. 특정 키 방식의 세부를 섞지 않고 일반 서명 원리로 한정.',
              '기존 2.4 토큰 모양과 2.7 검증 단계의 시각 표현 재사용.'),
    candidate('2.8', '시간축', 'time', '서버 세션과 JWT의 만료 시점', 'session oidc',
              '위에는 서버 세션의 마지막 활동/최대 수명 기준, 아래에는 JWT exp 기준 시간축. 만료 뒤 같은 증표를 제출하는 요청을 거부로 표시.',
              '브라우저에 값이 남아 있어도 서버에서 유효하지 않을 수 있음.',
              '수명 숫자는 설명용으로만 표시. 쿠키 Max-Age를 서버의 인증 만료와 동일시하지 않음.',
              '기존 2.3 세션·2.7 exp 검증 라벨 연결; 2.9 갱신 도식으로 이어짐.'),
    candidate('2.9', '시퀀스', 'request', '만료된 액세스 토큰의 갱신', 'refresh',
              'RFC 6749 Figure 2의 클라이언트/데이터 API/인증 시스템 레인 유지. 데이터 요청→만료 응답→인증 시스템에 갱신 자격 제출→새 액세스 토큰→데이터 요청 순서.',
              '갱신 자격의 제출 대상은 일반 데이터 API가 아니라 인증 시스템.',
              '원본의 Authorization Grant 시작 단계와 OAuth 역할명은 제거. 3.2의 외부 권한 위임은 아직 설명하지 않음.',
              '기존 resource-sequence 블록 확장; RFC ASCII 도식 전체 스크린샷은 불필요.', effort='중'),
    candidate('3.3', '비교도', 'request', 'ID 토큰과 외부 API 액세스 토큰의 목적지', 'oidc',
              '제공자에서 나온 두 증표를 분기: ID 토큰→FoodMap의 신원 확인, 액세스 토큰→외부 API 데이터 접근. 목적/수신 대상 두 행 표를 함께 사용.',
              '같은 로그인 과정에 있어도 토큰의 목적과 받아들이는 곳은 다름.',
              '2.7의 검증 항목만 참조. code·state·PKCE는 3.4~3.6에 남김.',
              '기존 3.2 외부 API 주체를 유지하고 색이 아닌 텍스트로 두 토큰 구분.', priority='우선'),
    candidate('3.7', '표', 'identity', '외부 식별자와 내부 계정의 대응', 'oidc authn',
              '열: issuer / subject / FoodMap user_id. 공급자 A의 sub=42와 공급자 B의 sub=42를 서로 다른 내부 계정으로 대응. 같은 이메일 사례에는 자동 병합 금지 라벨.',
              '발급자와 사용자 식별자 조합이 외부 계정의 기준이며, 내부 ID는 별도로 유지됨.',
              '기존 계정에 새 외부 신원을 추가할 때는 양쪽의 확인이 필요함을 메모. 이메일 일치만으로 합치는 코드 제외.',
              '1.2 계정 카드에 외부 식별자 두 열만 추가.', priority='우선'),
    candidate('3.8', '시퀀스', 'request', '외부 인증 완료에서 FoodMap 로그인 상태로', 'oidc session',
              '검증된 외부 신원→3.7 계정 대응→내부 u123→FoodMap 세션 또는 토큰→FoodMap API. 외부 액세스 토큰→외부 API 경로는 옆에 별도 표시.',
              '비밀번호 로그인과 소셜 로그인이 내부 사용자 ID라는 같은 결과로 모임.',
              '외부 액세스 토큰을 FoodMap API의 사용자 인증에 그대로 대입하지 않음. 세션/토큰 중 선택 가능한 구조로 표시.',
              '기존 1.7·2.3·2.4의 끝부분을 연결; 새로운 SDK 초기화 코드 불필요.', priority='우선'),
    candidate('4.2', '표', 'policy', '역할별 기능 허용표', 'authz',
              '행: 일반 사용자/운영자. 열: 제보 작성/전체 제보 조회. 예시 정책에 따라 허용·거부 표시하고 서버가 확인한 역할이라는 표제 추가.',
              '역할이 행동의 허용 범위를 결정함.',
              '자기 제보만 허용하는 행 조건은 4.3에서 추가. 승인·반려 상태는 5.3에 남김.',
              '4.8 종합 정책표의 역할·행동 열을 먼저 사용.'),
    candidate('4.3', '표', 'identity', '확인된 사용자와 대상 행의 소유자 비교', 'authz',
              '요청자 u123 고정. r101 소유자 u123은 허용, r102 소유자 u456은 거부. 비교선의 출발점을 서버가 확인한 사용자에 연결.',
              '같은 일반 사용자 역할이어도 대상 행에 따라 권한이 달라짐.',
              '요청 본문의 owner_id를 믿거나 데이터 전체를 내려받아 화면에서만 걸러내지 않음. RLS 문법은 4.6에 배치.',
              '1.1의 u123/r101 카드 확장.', priority='우선'),
    candidate('4.4', '판단도', 'policy', '명시적 허용 조건과 나머지 요청', 'authz',
              '요청→정해진 허용 조건 충족?→예: 허용 / 아니오·정보 없음: 거부. 공개 맛집 조회도 명시한 허용 분기에 포함.',
              '규칙이 없거나 판단 정보가 부족한 경우가 허용으로 빠지지 않음.',
              '기본 거부를 모든 요청에 로그인 강제로 설명하지 않음.',
              '4.2·4.3의 역할/소유자 사례를 분기 조건으로 사용.', priority='우선'),
    candidate('4.5', '시퀀스', 'request', '화면 숨김과 서버의 요청별 검사', 'authz',
              '숨긴 수정 버튼 옆에서 직접 API 요청 경로를 표시. API→사용자 확인→행동·대상 권한 확인→DB 처리, 실패는 DB 앞에서 중단.',
              '권한 없는 요청을 실제로 막는 지점은 서버의 처리 경계.',
              'authorize() 한 줄을 완전한 구현처럼 제시하지 않음. RLS와 특권 키는 아직 추가하지 않음.',
              '2.7의 인증 검사 뒤에 4.2·4.3 조건을 붙임.', priority='우선'),
    candidate('4.6', '코드', 'policy', '자기 제보 SELECT 정책과 반환 행', 'rls pg-rls',
              'RLS 활성화·SELECT 정책 코드와 u123/u456/u123 소유 행 3개를 나란히 배치. u123 요청에서는 첫째·셋째 행만 결과로 연결. 이 표의 u123·u456은 실제 UUID를 줄인 표시 이름으로 명시.',
              '애플리케이션 조건 외에 DB가 행 접근 조건을 적용하는 위치를 이해.',
              'Supabase Auth의 검증된 사용자 문맥, SELECT 기본 권한, RLS 적용 역할 전제 명시. NULL 비교 결과를 false 값이라고 쓰지 않음. UPDATE 정책은 제외.',
              '4.3의 동일 행을 코드 결과로 재사용. 4.7에서 특권 키의 예외를 확장.', priority='우선', effort='중', code='rls-select'),
    candidate('4.7', '표', 'policy', '공개 앱 키·서버 키·사용자 자격의 차이', 'keys',
              '열: publishable key / secret key / 사용자 로그인 JWT. 행: 식별 대상, 노출 위치, DB 사용자 문맥, RLS 적용 여부. 특권 서버 경로에는 별도의 API 인가 필요 표시.',
              '앱 접근 키와 로그인한 개인의 신원을 구분하고 서버 키의 우회 범위를 이해.',
              '현재 키 명칭 사용. 공개 키가 임의 접근 허용을 뜻하지 않으며 secret 키는 브라우저에 배치하지 않음. 실제 키 문자열은 표시하지 않음.',
              '4.5 API와 4.6 DB 경계에 이 표의 경로를 대응.', priority='우선'),
    candidate('4.8', '표', 'policy', 'FoodMap의 행위자·행동·대상·조건 정책표', 'authz rls keys',
              '행: 비로그인 공개 맛집 조회 / 작성자 본인 제보 조회·수정 / 운영자 전체 제보 조회. 열: 대상 조건, API 검사, RLS 적용 경로의 DB 조건.',
              '기능별 접근 정책을 하나의 검토 가능한 명세로 표현.',
              '강의용 설계 정책임을 명시. 4.6 코드는 SELECT 예시이므로 수정 작업의 SQL 구현이 끝난 것처럼 보이지 않게 함. 공개 상태의 구체 기준은 5.4에 남김.',
              '4.2~4.7 표를 합성. 새 권한 체계나 전체 CRUD 코드 추가 불필요.', effort='중'),
    candidate('5.1', '와이어프레임', 'operations', '사용자 화면과 운영자 화면의 업무 구분', 'authz',
              '사용자: 맛집 목록·제보. 운영자: 전체 제보 목록·상세 보기. 아래 공통 서버/DB와 운영자 전용 권한 경계 표시.',
              '화면과 업무는 나뉘어도 서버·DB를 공유할 수 있음.',
              'Supabase 대시보드를 자체 관리자 시스템으로 대체하지 않음. 승인 버튼·상태 칩은 5.3에서 추가.',
              '기존 로그인 UI 블록의 창틀만 활용하고 FoodMap 가상 화면 제작.', effort='중'),
    candidate('5.2', '표', 'policy', '서비스·DB·플랫폼 관리 권한의 대상', 'platform authz',
              '행: FoodMap 운영자 / DB 구조 변경 권한 / 배포 플랫폼 관리 권한. 열: 관리 대상·할 수 있는 일·자동으로 따라오지 않는 권한.',
              '앱의 운영자 역할과 인프라 관리 권한은 서로 다른 권한 부여.',
              '서비스 내부 admin을 DB superuser나 플랫폼 Owner와 동일시하지 않음. 복잡한 클라우드 IAM 구성은 생략.',
              '5.1의 화면·서버·DB 경계를 표의 관리 대상으로 연결.'),
    candidate('5.3', '상태도', 'operations', '검토 대기에서 승인 또는 반려로', 'workflow',
              'pending→approved / pending→rejected 두 화살표. 화살표 위에 운영자·현재 상태 조건. 이미 승인된 r101에 같은 변경을 다시 요청하면 조건 불충족.',
              '업무 행동에는 허용된 시작 상태와 도착 상태가 있음.',
              'FoodMap의 예시 업무 규칙으로 명시. 보편적인 필수 상태 구조나 결제 인증 절차라고 설명하지 않음.',
              '5.1 제보 상세에 상태 표시를 추가; 5.5·5.6에서도 r101 유지.'),
    candidate('5.4', '표', 'operations', '검토 결과와 공개 여부의 두 축', 'workflow',
              '열: 검토 상태 / 공개 여부 / 사용자 목록 노출. 승인+공개와 승인+비공개를 비교하고 ‘승인 이력 유지, 노출 중지’ 사례 강조.',
              '업무의 승인 결정과 사용자에게 보여주는 결정은 구분됨.',
              '두 축의 구체 정책은 자체 FoodMap 설계. 원문 OWASP에 동일한 공개 상태표가 있다고 표기하지 않음.',
              '5.3 상태를 바꾸지 않고 visibility 열만 추가.'),
    candidate('5.5', '도식', 'operations', '승인 변경과 맛집 등록의 단일 트랜잭션', 'transaction',
              '하나의 DB 트랜잭션 괄호 안에 제보 승인 UPDATE와 맛집 INSERT. 모두 성공: 둘 다 반영 / 두 번째 실패: 둘 다 취소를 전후 표로 비교.',
              '연관된 두 DB 변경 중 하나만 남지 않도록 원자성을 적용.',
              '다른 DB·외부 API·브라우저 저장까지 자동 원자화하지 않음. 조건 확인 없이 INSERT하는 불완전한 SQL 예제는 제외.',
              '07주차 트랜잭션 개념을 5.3의 r101 업무에 적용.'),
    candidate('5.6', '시퀀스', 'operations', '응답 유실 후 같은 승인 요청 재전송', 'idempotency',
              '첫 요청 operation=approve:r101 처리→결과 저장→응답 유실. 같은 키로 재전송→저장한 결과 반환. 맛집은 1건 유지.',
              '한 번의 원자적 처리와 반복 요청의 중복 방지는 별도 문제.',
              '헤더만 추가하면 해결되는 것으로 그리지 않음. 서버의 키/요청 일치 확인·중복 제약·원자적 결과 기록이 필요. Stripe 보관 시간은 차용하지 않음.',
              '5.5 트랜잭션 상자를 첫 요청 안에 넣고 두 번째 요청에서는 재실행하지 않는 경로 표시.', effort='중'),
    candidate('5.7', '기록표', 'operations', '제보 승인 감사 기록 한 행', 'logging',
              '가상 행: 시각 2026-11-07T10:00:00+09:00 / 행위자 op-01 / 대상 r101 / 행동 approve / 결과 success / 사유 정보 확인. 필드를 상태 전이와 연결.',
              '최종 상태만으로는 알 수 없는 변경 경위를 기록으로 재구성.',
              '실제 운영 기록이 아닌 예시 데이터 표시. 비밀번호·토큰·불필요한 개인정보 제외. 모니터링 지표는 7.7에서 다룸.',
              '5.3~5.6의 동일 작업에 감사 필드 연결.'),
    candidate('6.1', '코드', 'policy', '서버 입력 검사와 정상·거부 입력', 'input',
              '이름의 자료형·빈값·길이, 위도의 유한한 수·범위를 확인하는 짧은 JS와 입력/결과 표. 이름 100자 제한은 예시 정책.',
              '로그인·권한 검사와 입력값 유효성 검사는 별도 판단.',
              '서버에서 파싱한 값을 검사하는 발췌. 클라이언트 검증으로 서버를 대신하지 않으며 SQL/XSS 처리 코드는 다음 장에 남김.',
              '공용 코드 블록과 입력/결과 표 활용.', code='input-check'),
    candidate('6.2', '코드', 'request', '검색 SQL과 입력값 배열의 분리', 'pg-query',
              'node-postgres client.query의 SQL $1과 [searchTerm]을 두 색으로 대응. 검색어 김\'s 식당을 값으로 전달하는 경우와 문자열 결합 구조를 비교.',
              '따옴표가 있는 정상 데이터도 명령문 구조와 분리해 처리.',
              '연결된 서버 pg client와 restaurants.name 열 전제. 값 매개변수는 테이블·열 이름의 치환 수단이 아님. 위험 쿼리는 실행 예제로 제공하지 않음.',
              '07주차 SELECT에 값 배열 한 줄만 추가.', code='parameter-query'),
    candidate('6.3', '코드', 'browser', '문자열 자식과 HTML 해석의 출력 차이', 'react',
              'report.description에 <strong>추천</strong> 문자열을 넣고 <p>{report.description}</p>의 결과를 태그까지 보이는 텍스트로 표시. HTML 해석 경로는 별도 경고 도식.',
              '사용자 내용을 텍스트로 표시하는 것과 브라우저가 HTML로 해석하는 것을 구분.',
              '텍스트 자식 문맥으로 한정. React만 쓰면 모든 URL·HTML·스크립트 문맥이 안전하다는 설명 제외. 실행 공격 코드는 불필요.',
              '기존 React 코드·결과 병렬 형식; 원문 dangerouslySetInnerHTML은 참조만 하고 정답 코드로 배치하지 않음.', code='jsx-text'),
    candidate('6.4', '표', 'browser', '프로토콜·호스트·포트별 출처 판정', 'origin',
              '기준 https://app.example.com. /map, /reports, :443, :8443, api.example.com, http://app.example.com을 비교. 경로와 기본 포트를 분리 표시.',
              '경로가 달라도 동일 출처일 수 있고 포트가 다르면 다른 출처.',
              '사이트·CORS·쿠키 규칙은 아직 설명하지 않음. https 기본 포트 443의 생략 표기를 정확히 대응.',
              '6.5에서도 같은 URL 행을 유지.', priority='우선'),
    candidate('6.5', '표', 'browser', '같은 URL에 출처와 사이트 판정 두 열', 'site origin',
              '6.4 표에 same-site 열 추가. HTTPS app/api.example.com은 다른 출처·같은 사이트, HTTP/HTTPS는 다른 사이트. example.co.kr을 등록 가능 도메인 보조 예시로 표시.',
              '출처와 사이트는 서로 다른 기준이며 쿠키 정책 이해에 모두 필요.',
              'schemeful site 기준. 도메인의 마지막 두 조각만 취하는 공식은 사용하지 않음. SameSite 속성값은 6.9에서 설명.',
              '6.4 표에 한 열만 추가해 차이 강조.', priority='우선'),
    candidate('6.6', '시퀀스', 'browser', '요청 도착과 응답 읽기 제한의 위치', 'sop',
              '외부 페이지→FoodMap 요청은 도착할 수 있음. 서버 응답→외부 페이지 스크립트 읽기는 브라우저 경계에서 차단. 전송/읽기 화살표를 각각 표시.',
              '동일 출처 정책이 모든 교차 출처 요청 자체를 막는 것은 아님.',
              'CORS 헤더는 6.7에서 추가. 인증이 자동으로 보장된다고 표시하지 않음.',
              '6.7에서 응답 허용 조건을, 6.8에서 쿠키 자동 첨부 경로를 같은 레인에 추가.', priority='우선'),
    candidate('6.7', '시퀀스', 'browser', 'CORS 응답 허용과 필요한 경우의 사전 확인', 'cors',
              'MDN simple SVG를 주자료로 단순화: Origin 요청 헤더→서버의 허용 출처 응답→브라우저의 읽기 판단. preflight SVG는 JSON POST 등 필요한 경우의 OPTIONS 단계를 추가하는 보조 원형.',
              '응답을 읽을 수 있게 하는 브라우저 규칙이며 사용자 권한 검사와 별개.',
              '모든 요청에 OPTIONS가 있는 것처럼 그리지 않음. 자격정보 요청에 ACAO:* 사용 불가. 허용 목록 없이 요청 Origin을 그대로 반사하는 코드 제외.',
              '6.6 레인을 재사용. 원본의 foo/bar 주소·XML·X-PINGOTHER·장황한 헤더를 FoodMap에 맞춰 줄이고 전체 그림 2개를 한 장에 억지로 배치하지 않음.',
              priority='우선', effort='중', figures=('mdn-cors-simple.svg', 'mdn-cors-preflight.svg')),
    candidate('6.8', '시퀀스', 'browser', '다른 페이지가 유발한 로그인 브라우저의 요청', 'csrf',
              '외부 페이지→피해자 브라우저→FoodMap 상태 변경 API. 조건에 따라 첨부된 로그인 쿠키와 별도로 CSRF 확인값·요청 출처 검증을 서버 경계에 표시.',
              '자격이 첨부되었다는 사실만으로 사용자의 의도에 맞는 요청이라 판단할 수 없음.',
              '쿠키가 모든 상황에 무조건 붙는다고 단정하지 않음. 실제 적용 조건과 SameSite 속성은 6.9로 연결. XSS 공격 코드나 전체 토큰 발급 구현은 제외.',
              '6.6의 요청/읽기 구분을 그대로 두고 서버의 상태 변경 위치만 강조.', priority='우선'),
    candidate('6.10', '시간축', 'time', '관찰 구간의 로그인 실패와 지연·제한', 'authn',
              '같은 계정으로 반복되는 실패 시점과 점진적 지연을 표시. 요청 출처가 바뀌어도 계정 기준 관측이 이어지는 보조 표시.',
              '계정과 출처 등을 함께 보고 반복 추측 비용을 높임.',
              '표시 횟수·시간은 예시 정책. IP만 제한하거나 타인 계정을 무기한 잠그는 단순 구현은 제외.',
              '2.8 시간축의 스타일을 반복 요청 관찰에 재사용.'),
    candidate('7.1', '구성도', 'environment', '세 실행 환경과 각 환경 안의 두 업무 화면', 'environments',
              '개발/검증/운영 3열. 각 열 안에 사용자 화면·관리자 화면을 함께 표시하고 목적 라벨 추가. Supabase 원본의 3개 환경 구분만 참조.',
              '기능에 따른 사용자/관리자 구분과 실행 목적에 따른 환경 구분은 서로 다른 축.',
              'Git main/develop/feature와 CI 상세는 원본에서 제거. DB·자격 분리의 구체 내용은 7.4에 추가.',
              '5.1 화면 두 개를 각 환경에 재배치. 7.4~7.6·7.9~7.10의 기본 판으로 사용.',
              priority='우선', effort='중', figures=('supabase-environments.svg',)),
    candidate('7.3', '흐름도', 'environment', '환경 변수에서 서버 또는 브라우저로 향하는 경로', 'vite secrets',
              '서버 전용 secret→서버 프로세스, VITE_공개설정→빌드→브라우저 번들 경로를 비교. 노출된 키는 폐기→교체 단계로 표시.',
              '환경 변수라는 보관 형태만으로 비밀성이 보장되지는 않음.',
              '실제 키 대신 SERVER_SECRET 같은 이름만 표시. 모든 프레임워크의 규칙이 VITE_라고 일반화하지 않음.',
              '기존 7.2 환경 설정 코드에 전달 대상 도식 추가.'),
    candidate('7.4', '구성도', 'environment', '환경별 서버·DB·접근 자격의 분리', 'environments',
              '7.1의 3열 각각에 서버→해당 DB와 해당 자격만 연결. 개발 서버→운영 DB의 잘못된 교차 연결은 별도의 실패 사례로 한 번 비교.',
              '주소만 다르고 DB가 같으면 운영 데이터가 분리되지 않음.',
              'DB 분리와 접근 자격을 함께 표시. 운영 데이터 전체를 개발로 그대로 복사하는 절차는 제외.',
              'Supabase 환경 그림의 세 저장소 관계를 7.1 기본 판에 추가.', priority='우선', figures=('supabase-environments.svg',)),
    candidate('7.5', '흐름도', 'environment', '검증한 버전의 운영 반영과 주요 요청 확인', 'environments',
              '버전 v2+대상 설정→검증 환경의 로그인·조회·관리 기능 확인→운영 반영→같은 주요 요청 확인. 연결 대상 DB도 확인 항목으로 표시.',
              '프로세스 실행과 서비스 기능의 정상 동작을 구분.',
              'CI YAML·특정 호스팅 클릭 절차·배포 명령은 실습 세션에 남김. 운영의 파괴적 테스트 데이터 초기화 제외.',
              '7.1·7.4의 환경 구성에 코드 버전 이동 화살표만 추가.'),
    candidate('7.6', '코드', 'environment', '검토 상태 열 추가와 변경 이력', 'migrations',
              '버전이 붙은 SQL 파일명과 열 추가 코드, schema v1/v2 표를 병렬 배치. 기존 행 보완→새 코드→추가 제약 검토 순서를 보조 라벨로 표시.',
              'DB 구조 변경도 이력·실행 순서·기존 데이터와의 호환성을 관리해야 함.',
              '코드는 확장 첫 단계만. 모든 기존 제보를 pending으로 덮어쓰지 않음. db reset이나 운영 DB 실행 명령 제외.',
              '5.3에서 배운 상태를 열로 표현하고 7.5의 버전 흐름에 연결.', effort='중', code='migration-expand'),
    candidate('7.7', '차트', 'time', '배포 시점 전후의 실패율과 지연·오류 기록', 'telemetry',
              '가상 10분 관측값: 요청 수, 5xx 수, p95 응답 시간. 동일 x축의 작은 그래프 2개와 배포 시점 선·DB 연결 오류 한 줄 연결.',
              '상태 변화는 지표로 관측하고 구체 사건은 오류 기록으로 확인.',
              '실제 FoodMap 측정값이 아닌 설명용 데이터 표시. 배포 뒤 증가했다는 상관관계를 원인 확정으로 단정하지 않음. 감사 로그와 목적 구분.',
              '공용 HTML/SVG 차트로 간단히 제작; 외부 모니터링 제품의 복잡한 대시보드 캡처는 불필요.', effort='중'),
    candidate('7.8', '시간축', 'time', '마지막 백업 이후의 정상 변경과 손실 가능 구간', 'backups',
              '09:00 백업→09:15 새 제보→09:30 장애. 백업 사본이 포함하는 시점과 이후 별도 보존해야 할 변경을 색·라벨로 구분.',
              '사본의 존재뿐 아니라 복원할 수 있는 시점과 범위가 중요.',
              '시간은 예시. 요금제별 자동 백업·보관 기간을 보편 보장하지 않음. Supabase DB 백업과 Storage 파일 바이트 백업 범위를 구분.',
              '2.8의 시간축을 사본·데이터 변경에 적용; 7.10에서 같은 시점을 재사용.'),
    candidate('7.9', '비교도', 'environment', '앱 버전 복귀와 그대로 남는 DB', 'rollback migrations',
              '운영 앱 v2→v1 화살표, 아래 DB는 현재 스키마·데이터 유지. v1과 현재 DB 사이에 호환성 확인 지점 표시.',
              '배포 버전을 되돌리는 것과 DB 변경을 되돌리는 것은 서로 다른 작업.',
              'Vercel은 배포 복귀의 사례이며 모든 호스팅의 설정 동작을 동일시하지 않음. DB 복원 기능이 함께 실행되는 버튼처럼 표현하지 않음.',
              '7.5 버전 화살표 방향만 바꾸고 7.6 DB 변경 상태를 유지.', priority='우선'),
    candidate('7.10', '흐름도', 'environment', '백업을 격리 환경에서 검증한 뒤 필요한 데이터 반영', 'backups',
              '선택한 시점 사본→격리 DB 복원→데이터·앱 검증→반영 범위 결정→선별 병합 또는 전환. 백업 이후 정상 제보는 별도로 보존.',
              '코드 버전 복귀와 달리 데이터 자체를 되살리며 복원 이후의 정상 변경도 고려.',
              '강의용 대응 설계로 명시. 서비스별 복원 가능 방식이 다르므로 운영 DB 덮어쓰기 명령은 포함하지 않음.',
              '7.8 시간축의 사본과 7.4의 격리된 DB 표현을 연결.', priority='우선', effort='중'),
]

CODE_CANDIDATES = [
    dict(id='rls-select', slide='4.6', language='sql', source_ids=['rls', 'pg-rls'],
         provenance='공식 SELECT 정책의 테이블·정책 이름을 FoodMap에 맞춘 발췌',
         code='''alter table public.reports enable row level security;

create policy "read own reports"
on public.reports for select
to authenticated
using ((select auth.uid()) = user_id);''',
         conditions='Supabase Auth가 확인한 사용자 문맥. public.reports.user_id는 uuid. authenticated의 SELECT 기본 권한이 있고, 해당 역할은 RLS 적용 대상이며, 이 예시에서는 다른 허용 SELECT 정책이 없음.',
         expected='인증 사용자 ID와 user_id가 같은 행만 반환. 미인증 요청은 이 authenticated 정책의 허용 대상이 아님.',
         limits='SELECT 전용. SQL을 그대로 실행해 모든 CRUD 보안이 완성되지 않음. 정책 결합·소유자·BYPASSRLS 예외는 제작 메모와 4.7에서 구분.'),
    dict(id='input-check', slide='6.1', language='javascript', source_ids=['input'],
         provenance='입력 검증 원칙을 적용한 자체 FoodMap 코드 발췌',
         code='''const nameOK = typeof name === 'string'
  && name.trim().length > 0 && name.length <= 100;
const latitudeOK = Number.isFinite(latitude)
  && latitude >= -90 && latitude <= 90;

if (!nameOK || !latitudeOK) {
  throw new Error('Invalid report input');
}''',
         conditions='서버가 요청을 파싱해 얻은 name, latitude 값. 숫자로 받는 JSON API 예시. 에러를 입력 오류 응답으로 바꾸는 핸들러는 생략.',
         expected='[아주식당, 37.28] 통과 / [공백만, 37.28] 거부 / [아주식당, 91] 거부 / [아주식당, 문자열 37.28] 거부.',
         limits='100은 예시 길이. 인증·인가·다른 필드 검증을 대체하지 않으며 이 발췌만으로 API가 완성되지 않음.'),
    dict(id='parameter-query', slide='6.2', language='javascript', source_ids=['pg-query'],
         provenance='node-postgres의 매개변수화 API 사용법을 FoodMap 검색 사례로 변경',
         code='''const result = await client.query(
  'SELECT name FROM restaurants WHERE name = $1',
  [searchTerm]
);''',
         conditions='서버의 연결된 node-postgres client, restaurants.name 열과 검색 문자열 searchTerm. await가 가능한 함수 안의 발췌.',
         expected='검색어에 따옴표가 있어도 $1의 값으로 전달되어 SQL 구조를 바꾸지 않음. 결과 행 유무는 실제 데이터에 따름.',
         limits='이름 완전 일치 검색 예시. 테이블명·열명은 값 매개변수로 바꿀 수 없음. 입력 검증과 접근 권한도 별도 적용.'),
    dict(id='jsx-text', slide='6.3', language='jsx', source_ids=['react'],
         provenance='공식 문자열 children·HTML 주입 설명을 바탕으로 자체 작성',
         code='<p>{report.description}</p>',
         conditions='React 컴포넌트의 반환 JSX 일부. report.description은 사용자 입력 문자열이며 예시는 <strong>추천</strong>.',
         expected='strong 요소를 생성하지 않고 <strong>추천</strong> 문자를 그대로 화면에 표시.',
         limits='텍스트 자식 문맥의 예시. 모든 URL·HTML·스크립트 출력 문맥을 자동 보호한다고 일반화하지 않음.'),
    dict(id='migration-expand', slide='7.6', language='sql', source_ids=['migrations'],
         provenance='공식 마이그레이션 파일 개념을 FoodMap 제보 상태 열 추가로 적용',
         code='''-- 20261107_add_report_review_status.sql
alter table public.reports
add column review_status text;''',
         conditions='reports 테이블에 아직 review_status가 없는 가상의 이전 버전. 검토용 SQL이며 실제 현재 스키마에 대한 실행 지시가 아님.',
         expected='열이 추가되며 기존 행의 새 열 값은 NULL. 즉시 모든 행에 상태가 생기는 것은 아님.',
         limits='확장 첫 단계. 기존 데이터 의미를 확인한 보완, 새 코드 배포, 제약 추가는 별도로 설계. 운영 환경 실행·복원 명령 제외.'),
]


def outputs():
    plan = proposal(historical=True)
    concepts = [s for c in plan['chapters'] for s in c['concepts']]
    by_number = {s['outline_number']: s for s in concepts}
    by_id = {s['id']: s for s in concepts}
    # Original 60-slide research is historical, not the active classroom scope.
    from audit_week6_assets import SLIDE_MAP
    from paragraph_outline import HISTORICAL_PARAGRAPHS
    remaining = {by_number[r['outline_number']]['id'] for r in SLIDE_MAP if not r['assets']}
    screens = {}
    number = 2
    for chapter in plan['chapters']:
        number += 1
        for slide in chapter['concepts']:
            screens[slide['id']] = number
            number += 1
    paragraphs = HISTORICAL_PARAGRAPHS
    sources = {s['id']: s for s in SOURCES}
    codes = {s['id']: s for s in CODE_CANDIDATES}
    figures = json.loads((DEST/'reference-figures/sources.json').read_text())
    for item in figures:
        data = (DEST/'reference-figures'/item['file']).read_bytes()
        assert len(data) == item['bytes'], item['file']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['file']
    assert len(ROWS) == 44 and len({r['outline_number'] for r in ROWS}) == 44
    assert {by_number[r['outline_number']]['id'] for r in ROWS} == remaining
    assert len(codes) == 5 and len(sources) == len(SOURCES)
    rows = []
    for r in ROWS:
        s = by_number[r['outline_number']]
        assert set(r['source_ids']) <= sources.keys(), s['id']
        assert r['family'] in FAMILIES
        assert set(r['figure_files']) <= {f['file'] for f in figures}
        if r['code_id']:
            assert codes[r['code_id']]['slide'] == r['outline_number']
        requirements = [by_id[k]['outline_number']+' '+by_id[k]['title'][0]
                        if k in by_id else plan['prior_learning'][k] for k in s['requires']]
        rows.append(dict(**r, id=s['id'], slide_number=screens[s['id']],
                         title=s['title'][0], subtitle=s['lead'][0],
                         requires=s['requires'], prerequisite_locations=requirements,
                         approved_paragraph=paragraphs[s['id']],
                         status='조사 완료 · 실제 반영 상태는 resource-placements.json에서 관리'))
    assert [r['slide_number'] for r in rows] == sorted(r['slide_number'] for r in rows)
    assert {r['code_id'] for r in rows if r['code_id']} == codes.keys()
    assert {sid for r in rows for sid in r['source_ids']} == sources.keys()
    counts = dict(Counter(r['resource_type'] for r in rows))
    data = dict(stage='new-resource-research', researched_on=DATE,
                scope='기존 PDF 자료 16장을 제외한 본문 44장의 조사 기록. 현재 배치 상태는 resource-placements.json 참조.',
                body_slide_count=60, already_placed=16, researched_slide_count=44,
                archived_reference_figures=3, code_candidate_count=5,
                resource_type_counts=counts, families=FAMILIES,
                sources=SOURCES, reference_figures=figures,
                code_candidates=CODE_CANDIDATES, slides=rows)
    lines = [
        '8주차 · 나머지 44장 신규 자료 조사', '',
        f'조사일: {DATE} / 본문 60장 중 기존 PDF 자료 배치 16장 + 신규 자료 조사 44장.',
        '설계 번호와 실제 화면 번호를 함께 표기. 확정한 제목·부제·문단·순서를 유지.',
        '이 문서는 자료 후보와 수정 방법의 조사 기록. 후속 반영은 resource-placements.json과 slide-references.html에서 확인.',
        'FoodMap 화면·업무 정책·ID·관측값은 강의용 확장 사례이며 현재 실습의 구현·측정 결과가 아님.',
        '실제 외부 도식 3개 보관, RFC 시퀀스 1개를 추가 원형으로 선정, 짧은 코드 후보 5개 준비.',
        '사진·제품 대시보드 캡처보다 해당 판단을 직접 보여주는 편집 가능한 도식·표·코드 권장.',
        '출처는 아래 원자료 목록과 행별 근거에 기록. 원자료에 없는 FoodMap 사례는 자체 설계안으로 구분.', '',
        '선정한 실제 외부 도식', '',
        '- 6.7: MDN simple-request.svg — 기본 CORS 응답 읽기 경로. 주자료 원형.',
        '- 6.7: MDN preflight-correct.svg — 필요한 경우에만 OPTIONS를 추가하는 보조 원형.',
        '- 7.1·7.4: Supabase local-dev-environment SVG — 개발/검증/운영과 DB 분리 관계. 브랜치 그림은 강의용 재구성에서 제거.',
        '- 2.9: RFC 6749 §1.5 Figure 2 — 갱신 요청 목적지 구분. OAuth 용어·초기 권한 부여 단계는 이 장에서 제외.',
        'SVG 원본은 reference-figures/에 수정 없이 보관. 브라우저 렌더를 육안 확인했고 출처·크기·SHA-256은 sources.json에 기록.',
        '이미지 파일의 확보와 슬라이드 사용 준비 완료는 구분. MDN 도식은 한글화·주소·헤더 정리, Supabase 도식은 브랜치 제거 후 네이티브 재구성이 필요.', '',
        '전체 대응표', '',
        '| 설계 | 화면 | 타이틀 | 주자료 | 구체 후보 | 우선순위 | 작업량 |',
        '| --- | --- | --- | --- | --- | --- | --- |',
    ]
    for r in rows:
        lines.append(f'| {r["outline_number"]} | {r["slide_number"]} | {r["title"]} | {r["resource_type"]} | {r["candidate"]} | {r["priority"]} | {r["effort"]} |')
    lines += ['', '제작 순서와 공용화', '',
              '우선순위는 발표 순서가 아니라 도식 제작·내용 검토 순서. 실제 강의 순서는 확정안을 유지.',
              '1) 1.3·1.5~1.6과 3.3·3.7~3.8: 주장/검증, 해시/솔트, 외부 신원/내부 계정의 혼동 방지.',
              '2) 4.3~4.7: 같은 사용자·행 데이터로 소유자 판단→API 검사→RLS→특권 키 범위를 연결.',
              '3) 6.4~6.8: 하나의 URL 표와 브라우저 경계를 확장해 출처→사이트→SOP→CORS→CSRF 연결.',
              '4) 7.1·7.4·7.9~7.10: 사용자/관리자 기능 구분과 실행 환경 구분, 코드 복귀와 데이터 복원을 분리.',
              '5) 나머지 장: 같은 레코드·상태도·시간축을 변형해 제작.',
              '작업량 소: 기존 표·코드·흐름 블록의 내용 교체. 중: 새 연결 관계 또는 복합 결과 검토 필요. 시간 견적은 아님.', '']
    lines.extend(f'- {key}: {value}' for key, value in FAMILIES.items())
    lines += ['', '슬라이드별 상세 조사', '']
    for r in rows:
        lines += [f'{r["outline_number"]} · 화면 {r["slide_number"]} · {r["title"]}',
                  f'부제: {r["subtitle"]}',
                  f'확정 문단: {r["approved_paragraph"]}',
                  f'선수 개념: {" / ".join(r["prerequisite_locations"])}',
                  f'추천 자료: {r["resource_type"]} — {r["candidate"]}',
                  f'구성·사례: {r["specification"]}',
                  f'학생이 확인할 차이: {r["intended_observation"]}',
                  f'학습 범위·제외: {r["learning_boundary"]}',
                  f'수정·재사용: {r["reuse_plan"]}']
        if r['code_id']:
            lines.append(f'코드 후보: code-candidates.ko.txt · {r["code_id"]}')
        if r['figure_files']:
            lines.append('확보 파일: '+', '.join('reference-figures/'+f for f in r['figure_files']))
        lines.append('근거: '+' / '.join(f'[{sid}] {sources[sid]["url"]}' for sid in r['source_ids']))
        lines.append('')
    lines += ['원자료 목록', '']
    for s in SOURCES:
        lines += [f'[{s["id"]}] {s["title"]}', s['url'],
                  f'확인 위치: {s["section"]}', f'사용 방식: {s["use"]}', '']
    lines += ['검토 범위와 재생성', '',
              '- 44장과 기존 미배치 목록의 완전 대응, 제목·화면 번호·선수 관계·출처 ID·그림 해시·코드 연결을 검사.',
              '- 기술 검토: RLS 적용 전제, 키 권한, 토큰 수신 대상, 출처/사이트, CORS/CSRF, 배포/DB 복원 범위를 분리.',
              '- 학습 순서 검토: 각 후보의 학습 범위·제외에 후속 개념을 앞당기지 않는 수정 조건 기록.',
              '- 코드 5개는 이론용 발췌. DB·Auth·실제 배포에 연결해 실행한 결과가 아님.',
              '- 조사 단계에서는 슬라이드를 변경하지 않음. 후속 배치의 화면 검토는 resource-layout-review.json에서 관리.',
              '생성: python3 lectures/08/scripts/research_new_resources.py',
              '검증: python3 lectures/08/scripts/research_new_resources.py --check']
    code_lines = ['8주차 · 신규 코드 후보 5개', '',
                  '자료 조사용 발췌. 실제 실습 코드를 변경하거나 DB/서버에 실행하지 않음.',
                  '서버·DB·React 실행 조건, 관찰할 결과, 생략 범위를 함께 표기.',
                  '본문은 먼저 개념을 설명하고 코드는 해당 개념의 사례로 배치. 모든 장에 코드 추가하지 않음.', '']
    for c in CODE_CANDIDATES:
        code_lines += [f'{c["slide"]} · {c["id"]}', f'출처 적용: {c["provenance"]}',
                       f'전제: {c["conditions"]}', '', f'```{c["language"]}', c['code'], '```', '',
                       f'관찰 결과: {c["expected"]}', f'범위: {c["limits"]}',
                       '근거: '+' / '.join(sources[sid]['url'] for sid in c['source_ids']), '']
    return {
        DEST/'research.json': json.dumps(data, ensure_ascii=False, indent=2)+'\n',
        DEST/'research.ko.txt': '\n'.join(lines)+'\n',
        DEST/'code-candidates.ko.txt': '\n'.join(code_lines)+'\n',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in outputs().items():
        if args.check:
            assert path.read_text() == content, f'Stale {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print('Week 8 new resource research: 44 slides, 31 primary sources, 3 SVG references, 5 code candidates.')
