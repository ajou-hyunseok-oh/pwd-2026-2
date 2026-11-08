"""Approved Week 8 content-title outline, shared with the presentation builder.

The seven chapter titles come from chapters.py. This outline records bilingual
titles, learning prerequisites, and conceptual examples before body authoring.
Run this file to regenerate the review JSON and Korean text, or pass --check.
"""
import argparse
import json
from pathlib import Path

from chapters import CHAPTER_SLIDES


PRIOR_LEARNING = {
    'prior-web': '06주차 9~14장: 클라이언트·서버, HTTP/HTTPS, 요청·응답, JSON, REST API',
    'prior-data': '07주차: 테이블·기본 키·외래 키·관계와 FoodMap 맛집 데이터의 영구 저장',
    'prior-sql': '07주차: SQL로 테이블 데이터를 조회·변경하는 기본 역할',
    'prior-transaction': '07주차 41장: 여러 변경을 모두 반영하거나 모두 취소하는 트랜잭션',
    'prior-ui': '04~05주차: 사용자 입력과 목록을 표시하는 React 화면',
    'prior-deploy': '06주차 25장 및 07주차 실습: 서버·클라이언트의 배포와 DB 연결',
}


def concept(ident, ko, en, subko, suben, requires, example):
    return dict(id=ident, title=(ko, en), lead=(subko, suben),
                requires=requires.split(), example=example)


CHAPTERS = [
    dict(number=1,
         connection='지난주의 데이터 저장에서 출발해, 요청한 사람이 누구인지 확인하는 문제로 확장.',
         scope='로그인 성공으로 사용자 식별이 끝나는 지점까지. 쿠키·세션 발급이나 역할 판단은 뒤 챕터에서 설명.',
         concepts=[
        concept('identity-need', '서비스의 사용자 식별', 'Identifying Service Users',
                '저장된 데이터와 요청한 사용자를 연결할 필요',
                'Why stored data needs to be associated with the requesting user',
                'prior-web prior-data', '맛집 목록은 저장되지만 누가 제보했는지는 별도로 확인해야 하는 상황'),
        concept('user-account', '사용자 계정', 'User Accounts',
                '서비스 안에서 같은 사용자를 구분하는 고유 식별자',
                'A stable identifier for the same user within a service',
                'identity-need prior-data', '표시 이름이 바뀌어도 같은 사용자 ID로 연결되는 계정'),
        concept('trust-boundary', '클라이언트 입력의 신뢰 경계', 'The Trust Boundary for Client Input',
                '사용자가 보낸 주장과 서버가 확인한 사실의 구분',
                'Distinguishing client claims from facts verified by the server',
                'user-account prior-web', '요청 본문의 사용자 ID를 다른 사람의 값으로 바꾸어 보내는 상황'),
        concept('authentication', '사용자 인증', 'User Authentication',
                '계정에 대한 증거를 확인해 요청자의 신원을 판단하는 과정',
                'Verifying evidence for an account to establish the requester’s identity',
                'user-account trust-boundary', '사용자 ID를 아는 것과 그 계정의 비밀번호를 증명하는 것의 차이'),
        concept('password-hash', '비밀번호 해시', 'Password Hashing',
                '비밀번호 원문 대신 검증용 값을 생성해 저장하는 원리',
                'Storing a verification value instead of the original password',
                'authentication', '비밀번호 원문 저장과 비밀번호 검증용 해시 저장의 비교'),
        concept('password-salt', '비밀번호 솔트', 'Password Salts',
                '같은 비밀번호도 서로 다른 해시가 되도록 더하는 계정별 값',
                'A per-account value that makes identical passwords produce different hashes',
                'password-hash user-account', '같은 비밀번호를 선택한 두 계정의 서로 다른 저장 결과'),
        concept('password-login', '비밀번호 로그인', 'Password Login',
                '입력한 비밀번호를 저장된 검증 정보와 대조하는 흐름',
                'Checking an entered password against stored verification data',
                'authentication password-hash password-salt', '가입 시 검증 정보 저장 → 로그인 시 검증 → 서버가 사용자 ID 확인'),
    ]),
    dict(number=2,
         connection='한 번 확인한 사용자를 이후 요청에서도 식별하려면 무엇을 보관하고 전달해야 하는지 설명.',
         scope='쿠키는 전달 수단, 세션은 상태 관리, JWT는 토큰 형식이라는 서로 다른 역할을 유지. 역할 claim은 사용하지 않음.',
         concepts=[
        concept('http-stateless', 'HTTP의 무상태성', 'HTTP Statelessness',
                '이전 요청의 인증 결과가 새 요청에 자동으로 이어지지 않는 특성',
                'Why authentication from one request does not automatically carry into the next',
                'password-login prior-web', '로그인 요청과 그 뒤의 맛집 조회 요청을 따로 받는 서버'),
        concept('cookies', '쿠키', 'Cookies',
                '브라우저가 값을 저장하고 조건에 맞는 요청에 첨부하는 방식',
                'How a browser stores a value and attaches it to eligible requests',
                'http-stateless', '응답의 Set-Cookie → 브라우저 저장 → 이후 요청의 Cookie'),
        concept('server-session', '서버 세션', 'Server-Side Sessions',
                '세션 식별자로 서버에 보관한 로그인 상태를 찾는 구조',
                'Looking up server-held login state using a session identifier',
                'cookies password-login', '브라우저의 임의 식별자와 서버의 사용자 연결 기록'),
        concept('auth-token', '인증 토큰', 'Authentication Tokens',
                '이후 요청에서 인증 결과를 확인하는 데 사용하는 증표',
                'A credential used to establish authentication on subsequent requests',
                'server-session trust-boundary prior-web', '요청에 첨부하는 액세스 토큰의 역할; 세션 식별자도 토큰의 한 형태이며 전달 수단과 형식은 별도 선택'),
        concept('token-signature', '토큰의 서명', 'Token Signatures',
                '키를 이용해 토큰의 변조 여부와 발급 주체를 확인하는 원리',
                'Using keys to verify token integrity and its issuer',
                'auth-token', '사용자 식별 정보를 바꾼 토큰의 검증 실패; 내용의 비밀 보장과 서명의 역할 구분'),
        concept('jwt-structure', 'JWT의 구조', 'JWT Structure',
                '서명된 토큰에 사용자 정보와 유효 조건을 담는 형식',
                'A signed token format carrying identity information and validity conditions',
                'token-signature prior-web', '서명형 JWT의 헤더·페이로드·서명과 sub·iss·aud·exp의 의미'),
        concept('jwt-validation', 'JWT 검증', 'JWT Validation',
                '서명과 발급 조건을 확인해 토큰의 수용 여부를 판단하는 과정',
                'Deciding whether to accept a token by checking its signature and claims',
                'jwt-structure trust-boundary', '읽을 수 있는 토큰이라도 서명·발급자·수신 대상·유효 시간이 맞지 않으면 거부'),
        concept('auth-expiry', '인증 상태의 만료', 'Authentication Expiration',
                '한 번 확인한 인증 결과를 계속 신뢰할 수 있는 시간의 제한',
                'Limiting how long a previous authentication remains valid',
                'server-session jwt-validation', '서버 세션의 만료와 JWT의 유효 시간 경과 후 요청 처리'),
        concept('refresh-token', '리프레시 토큰', 'Refresh Tokens',
                '비밀번호 재입력 없이 새 액세스 토큰을 발급받는 자격정보',
                'A credential for obtaining a new access token without re-entering a password',
                'auth-expiry auth-token', '짧은 수명의 액세스 토큰을 갱신하는 흐름과 갱신용 자격정보의 별도 보호'),
        concept('logout', '로그아웃과 인증 철회', 'Logout and Revocation',
                '인증 방식에 따라 사용 중인 로그인 자격을 종료하는 방법',
                'Ending active login credentials according to the authentication design',
                'server-session refresh-token jwt-validation', '브라우저 값 삭제·서버 세션 종료·갱신 자격 철회와 이미 발급된 토큰의 남은 유효 시간'),
    ]),
    dict(number=3,
         connection='서비스가 직접 비밀번호를 확인하는 구조에서 외부 인증 결과를 받아 같은 내부 사용자로 연결하는 구조로 확장.',
         scope='OAuth는 외부 API 접근 위임, OIDC는 신원 확인으로 구분. 서비스 내부 역할·RLS는 사용하지 않음. 제공자별 설정과 SDK 코드는 실습 범위.',
         concepts=[
        concept('identity-provider', '외부 인증 제공자', 'External Identity Providers',
                '다른 서비스가 확인한 사용자 신원을 활용하는 구조',
                'Using a user identity verified by another service',
                'authentication password-login', 'FoodMap과 외부 계정 제공자 사이의 비밀번호 확인 책임 구분'),
        concept('oauth-delegation', 'OAuth의 접근 권한 위임', 'OAuth Access Delegation',
                '사용자가 동의한 범위의 외부 API 접근을 허용하는 방식',
                'Delegating access to an external API within the user-approved scope',
                'identity-provider auth-token prior-web', '사용자의 비밀번호를 전달하지 않고 외부 프로필 API의 제한된 접근을 허용하는 사례'),
        concept('oidc', 'OIDC의 사용자 인증', 'User Authentication with OIDC',
                '외부 인증 제공자의 ID 토큰으로 사용자 신원을 확인하는 방식',
                'Verifying a user identity through an ID token from an identity provider',
                'oauth-delegation jwt-validation', '외부 API용 액세스 토큰과 신원 확인용 ID 토큰의 목적 비교'),
        concept('authorization-code', '인가 코드 흐름', 'The Authorization Code Flow',
                '브라우저가 전달한 임시 코드를 토큰으로 교환하는 과정',
                'Exchanging a temporary code returned through the browser for tokens',
                'oidc prior-web', '서버가 교환을 맡는 사례: 외부 화면 이동 → 등록된 복귀 주소로 코드 전달 → 토큰 교환'),
        concept('oauth-state', '로그인 요청의 state', 'State in Login Requests',
                '로그인을 시작한 요청과 돌아온 응답을 연결하는 값',
                'A value that correlates a login response with the initiating request',
                'authorization-code', '시작할 때 보관한 값과 복귀한 값이 일치하는지 확인하는 흐름'),
        concept('pkce', '인가 코드의 PKCE 보호', 'Protecting Authorization Codes with PKCE',
                '코드 발급 요청과 코드 교환 요청을 같은 시작 주체에 연결하는 증명',
                'Binding code issuance and exchange to the same initiating client',
                'authorization-code oauth-state', '일회성 검증값의 변환값을 먼저 보내고 코드 교환 때 원래 검증값을 확인하는 흐름'),
        concept('account-link', '외부 계정과 서비스 계정의 연결', 'Linking External and Local Accounts',
                '인증 제공자와 사용자 식별자로 내부 계정을 연결하는 기준',
                'Mapping a provider and its user identifier to a local account',
                'oidc pkce user-account prior-data', '검증한 제공자·사용자 식별자와 FoodMap 사용자 ID의 대응; 이메일만으로 자동 연결하지 않는 기준'),
        concept('social-session', '소셜 로그인 이후의 서비스 인증', 'Service Authentication After Social Login',
                '외부 인증 결과를 서비스의 로그인 상태로 이어가는 과정',
                'Turning an external authentication result into an application login state',
                'account-link server-session auth-token', '외부 ID 토큰·외부 API 액세스 토큰·FoodMap 로그인 자격의 사용처 구분'),
    ]),
    dict(number=4,
         connection='인증 방식과 무관하게 확인된 사용자가 생긴 뒤, 그 사용자의 개별 요청을 허용할 기준을 학습.',
         scope='역할·소유 관계를 먼저 정의하고 검사 위치로 확장. 제보 승인 상태와 공개 상태는 5장에서 처음 설명.',
         concepts=[
        concept('authorization', '요청의 인가', 'Request Authorization',
                '사용자·행동·대상을 기준으로 요청 허용 여부를 결정하는 과정',
                'Deciding whether a user may perform an action on a resource',
                'social-session authentication', '로그인한 사용자라는 사실과 특정 제보를 수정할 수 있다는 판단의 구분'),
        concept('role-access', '역할 기반 접근 제어', 'Role-Based Access Control',
                '역할에 부여된 권한으로 기능 사용 범위를 정하는 방식',
                'Determining available actions through permissions assigned to roles',
                'authorization', '일반 사용자와 운영자에게 필요한 기능만 부여하는 최소 권한의 역할 표'),
        concept('owner-access', '소유자 기반 접근 제어', 'Ownership-Based Access Control',
                '요청자와 데이터 소유자의 관계로 접근 범위를 정하는 방식',
                'Determining access from the relationship between a requester and a record owner',
                'authorization role-access user-account prior-data', '같은 일반 사용자 역할이어도 자신의 제보와 다른 사람의 제보에 다르게 적용되는 정책'),
        concept('default-deny', '기본 거부 정책', 'Deny by Default',
                '명시적으로 허용한 규칙이 없으면 요청을 거부하는 기준',
                'Rejecting requests when no explicit allow rule applies',
                'role-access owner-access', '등록된 역할이 없거나 대상 데이터의 소유 관계를 확인할 수 없는 요청'),
        concept('api-access', 'API 접근 제어', 'API Access Control',
                '서버가 요청마다 사용자와 대상 데이터의 권한을 확인하는 구조',
                'Checking user permissions for the target data on every server request',
                'default-deny jwt-validation trust-boundary', '화면의 버튼을 숨겨도 직접 보낼 수 있는 요청에 대한 서버의 권한 검사'),
        concept('rls', '행 수준 보안 정책', 'Row-Level Security Policies',
                '데이터베이스의 각 행에 접근 규칙을 적용하는 방식',
                'Applying access rules to individual database rows',
                'api-access owner-access prior-data', '테이블 접근 권한과 사용자 ID·행 소유자 비교 정책이 함께 적용되는 사례'),
        concept('api-keys', 'API 키의 권한 범위', 'The Authority of API Keys',
                '애플리케이션의 API 접근 자격과 사용자 인증의 구분',
                'Distinguishing application API credentials from user authentication',
                'rls auth-token api-access', '공개 가능한 키와 서버 전용 권한 키의 차이; RLS 우회 키를 쓰는 서버의 인가 책임'),
        concept('foodmap-policy', 'FoodMap의 접근 정책', 'FoodMap Access Policies',
                '역할과 데이터 소유 관계를 조합한 요청별 허용 기준',
                'Combining roles and ownership into request-level access rules',
                'role-access owner-access default-deny api-access rls api-keys', '사용자별 자기 제보 조회·수정과 운영자의 전체 제보 조회를 묶은 정책 표'),
    ]),
    dict(number=5,
         connection='앞서 정한 권한을 이용자가 쓰는 기능과 운영자가 수행하는 관리 업무에 적용.',
         scope='업무 화면과 기능의 분리를 설명. 개발·운영 인프라의 분리는 7장에 배치. 운영 데이터는 서버에서 일관되게 관리하는 설계 사례.',
         concepts=[
        concept('admin-system', '사용자 서비스와 관리자 시스템', 'User Services and Administration Systems',
                '이용자의 서비스 이용과 운영자의 관리 업무를 나누는 구조',
                'Separating user-facing activities from service administration',
                'foodmap-policy prior-ui', '맛집 탐색·제보 화면과 전체 제보 관리 화면; 공통 서버를 사용해도 구분되는 기능과 권한'),
        concept('admin-boundary', '관리자 권한의 경계', 'Administrator Permission Boundaries',
                '서비스 운영에 필요한 권한을 업무 범위에 맞게 제한하는 기준',
                'Restricting administrative permissions to the responsibilities of the role',
                'admin-system role-access api-keys', '제보를 관리하는 앱 운영자와 DB·클라우드 프로젝트 관리자의 권한 구분'),
        concept('workflow-state', '운영 업무의 상태 전이', 'State Transitions in Administrative Workflows',
                '제보의 처리 상태와 허용 가능한 변경을 정의하는 방식',
                'Defining submission states and the transitions allowed between them',
                'admin-boundary authorization', '검토 대기 → 승인 또는 반려; 현재 상태에 따른 허용 행동'),
        concept('publication-state', '콘텐츠 공개 상태', 'Content Publication Status',
                '검토 결과와 사용자에게 보이는 상태를 구분하는 기준',
                'Separating review outcomes from public visibility',
                'workflow-state owner-access', '승인되었지만 비공개인 맛집과 공개 중인 맛집의 구분'),
        concept('admin-transaction', '운영 작업의 트랜잭션', 'Transactions for Administrative Actions',
                '함께 성공해야 하는 데이터 변경을 하나의 작업으로 묶는 원리',
                'Grouping data changes that must succeed together into one operation',
                'workflow-state publication-state prior-transaction', '제보 승인 기록과 맛집 등록이 모두 반영되거나 모두 취소되는 서버·DB 작업'),
        concept('idempotency', '중복 요청의 처리', 'Handling Duplicate Requests',
                '같은 운영 요청이 반복되어도 결과가 중복되지 않도록 하는 기준',
                'Preventing repeated administrative requests from duplicating their effects',
                'admin-transaction workflow-state', '승인 요청 재전송으로 같은 맛집이 두 번 생성되지 않게 하는 멱등성'),
        concept('audit-log', '감사 로그', 'Audit Logs',
                '운영자의 작업 주체·대상·결과를 남기는 기록',
                'Recording who performed an administrative action, on what, and with which result',
                'idempotency user-account', '운영자·제보·승인 결과·시각·사유를 남기되 비밀번호와 토큰 원문은 제외하는 기록'),
    ]),
    dict(number=6,
         connection='완성된 인증·접근 제어·관리 업무의 구조를 대상으로 공격이 끼어드는 위치와 방어 원리를 설명.',
         scope='입력 검증을 만능 방어로 설명하지 않음. 출처·사이트 → 동일 출처 정책 → CORS → CSRF → 쿠키 보호 속성의 선수 관계 유지.',
         concepts=[
        concept('input-validation', '입력 검증', 'Input Validation',
                '서버가 받은 데이터의 형식과 허용 범위를 확인하는 절차',
                'Checking the format and permitted range of data received by the server',
                'trust-boundary api-access', '맛집 이름의 길이와 좌표의 범위를 확인하는 검증; 사용자 권한 검사와의 역할 구분'),
        concept('sql-injection', 'SQL 인젝션', 'SQL Injection',
                '입력값이 SQL 명령으로 해석될 때의 위험과 방어 원리',
                'The risk of interpreting input as SQL commands and how to prevent it',
                'input-validation prior-sql', '맛집 검색어를 SQL 구문에 섞는 구조와 매개변수로 값을 전달하는 구조의 비교'),
        concept('xss', '크로스 사이트 스크립팅', 'Cross-Site Scripting',
                '사용자 입력이 웹 페이지의 코드로 실행될 때의 위험',
                'The risk of executing user-supplied content as code in a web page',
                'input-validation prior-ui', '제보 설명을 텍스트로 표시하는 경우와 HTML로 해석하는 경우; 출력 문맥에 맞는 처리'),
        concept('origin', '웹 출처', 'Web Origins',
                '프로토콜·호스트·포트로 웹 자원의 경계를 구분하는 기준',
                'Distinguishing web resource boundaries by scheme, host, and port',
                'xss prior-web', '브라우저 화면과 API 주소를 구성 요소별로 비교해 같은 출처인지 판단'),
        concept('site', '브라우저의 사이트 구분', 'How Browsers Distinguish Sites',
                '등록 가능한 도메인과 프로토콜을 기준으로 한 사이트 경계',
                'Site boundaries based on the registrable domain and scheme',
                'origin', '서브도메인이 달라 출처는 다르지만 같은 사이트인 두 HTTPS 주소'),
        concept('same-origin-policy', '동일 출처 정책', 'The Same-Origin Policy',
                '다른 출처의 응답을 스크립트가 읽는 범위를 제한하는 원칙',
                'Restricting a script’s ability to read responses from another origin',
                'origin site', '다른 출처로 요청을 보낼 수 있는 경우와 그 응답을 읽을 수 있는 경우의 구분'),
        concept('cors', 'CORS', 'CORS',
                '서버가 허용한 출처에 브라우저의 응답 읽기를 허용하는 방식',
                'Allowing browser response access for origins approved by the server',
                'same-origin-policy api-access', 'FoodMap 화면이 별도 주소의 API 응답을 읽는 조건; 인증·인가 검사와 별개인 역할'),
        concept('csrf', '크로스 사이트 요청 위조', 'Cross-Site Request Forgery',
                '브라우저가 자동으로 보내는 인증정보를 이용한 요청 위조',
                'Forging requests by exploiting credentials attached automatically by the browser',
                'cors site cookies server-session workflow-state', '운영자가 로그인한 브라우저에서 의도하지 않은 관리 요청을 유발하는 상황과 요청 출처·확인값 검증'),
        concept('cookie-protection', '쿠키의 보호 속성', 'Cookie Protection Attributes',
                '쿠키의 전송과 스크립트 접근 범위를 제한하는 설정',
                'Settings that restrict cookie transmission and script access',
                'site csrf xss cookies prior-web', 'Secure·HttpOnly·SameSite가 각각 보호하는 경계와 각 속성만으로 막지 못하는 범위'),
        concept('login-rate-limit', '로그인 시도 제한', 'Limiting Login Attempts',
                '반복되는 인증 요청의 횟수와 속도를 제어하는 방어',
                'Defending authentication by limiting repeated request frequency',
                'cookie-protection password-login input-validation', '같은 계정과 요청 출처에 반복되는 로그인 실패의 제한·지연; 무조건 잠금의 악용 가능성'),
    ]),
    dict(number=7,
         connection='보호할 서비스 구조를 실제로 배포하고 변경하는 운영자의 관점으로 확장. 기능·권한 분리와 실행 환경 분리를 구분.',
         scope='서비스 이용 화면·관리 화면과 개발·검증·운영 환경은 서로 다른 분리 축. 배포·DB 구조 변경·코드 롤백·데이터 복원을 각각 구분.',
         concepts=[
        concept('environments', '개발·검증·운영 환경', 'Development, Staging, and Production',
                '실험과 검증이 실제 사용자 서비스에 영향을 주지 않도록 나누는 실행 공간',
                'Separating execution environments to protect live users from experimentation',
                'admin-system prior-deploy', '각 환경 안에 사용자 화면과 관리자 화면이 함께 존재하는 두 축의 구성'),
        concept('environment-config', '환경별 설정', 'Environment-Specific Configuration',
                '같은 코드를 다른 주소와 자격정보로 실행하는 구성',
                'Running the same code with different endpoints and credentials',
                'environments api-keys authorization-code', '코드는 같아도 API·DB 주소와 외부 로그인 복귀 주소가 다른 배포'),
        concept('secret-management', '비밀정보 관리', 'Secret Management',
                '외부에 공개되면 안 되는 자격정보의 보관과 교체',
                'Storing and rotating credentials that must remain confidential',
                'environment-config api-keys token-signature', '서버 전용 키의 보관, 브라우저 번들·Git 노출 방지, 유출된 키의 폐기와 교체'),
        concept('environment-data', '환경별 데이터 분리', 'Separating Data Across Environments',
                '개발·검증 작업이 운영 데이터에 닿지 않도록 저장소를 분리하는 기준',
                'Isolating data stores so development and staging cannot alter production data',
                'secret-management environments prior-data', '테스트용 제보 초기화가 운영 DB에 닿지 않는 별도 DB·자격정보 구성'),
        concept('deployment', '서비스 배포', 'Service Deployment',
                '검증한 코드와 설정을 대상 환경에 반영하는 과정',
                'Releasing verified code and configuration to a target environment',
                'environment-data environment-config prior-deploy', '검증 환경 확인 → 운영 반영 → 로그인·조회·관리 기능의 상태 확인'),
        concept('db-migration', '데이터베이스 마이그레이션', 'Database Migrations',
                '데이터베이스 구조의 변경을 순서와 이력으로 관리하는 방식',
                'Managing database schema changes through ordered, tracked steps',
                'deployment prior-data workflow-state', '제보 처리 상태 열 추가와 기존 행 처리; 앱 배포 순서와 이전 버전 호환성의 검토'),
        concept('monitoring', '운영 모니터링', 'Operational Monitoring',
                '오류와 서비스 지표로 운영 상태를 파악하는 관찰',
                'Observing errors and service metrics to assess operational health',
                'db-migration audit-log login-rate-limit', '오류율·응답 시간·로그인 실패 증가와 DB 연결 상태; 감사 기록과 장애 진단 기록의 목적 구분'),
        concept('backup', '데이터 백업', 'Data Backups',
                '운영 데이터의 사본과 복원 가능성을 확보하는 준비',
                'Preparing recoverable copies of production data',
                'monitoring environment-data prior-data', '사본의 시점·보관 위치·접근 권한·복원 검증과 허용 가능한 데이터 손실 범위'),
        concept('rollback', '배포 롤백', 'Deployment Rollback',
                '문제가 있는 배포를 이전 코드와 설정으로 되돌리는 대응',
                'Returning a faulty release to previous code and configuration',
                'deployment db-migration monitoring backup', '이전 서버 버전으로 복귀할 때 이미 변경된 DB 구조와의 호환성 확인'),
        concept('restore', '데이터 복원', 'Data Restoration',
                '백업을 사용해 손상되거나 유실된 데이터를 되살리는 절차',
                'Recovering damaged or lost data from a backup',
                'backup rollback environment-data', '잘못 삭제한 데이터의 복원과 복원 시점 이후 변경 처리; 격리된 환경에서 복원 검증'),
    ]),
]

SEQUENCE_REVIEW = [
    '1장에서는 인증 결과로 확인한 사용자까지만 다룬다. 역할·소유자별 허용 규칙은 4장, 세션 발급은 2장.',
    '비밀번호 검증 도식보다 해시·솔트가 먼저 온다. 비밀번호 해시에는 전용 함수를 사용한다는 범위를 유지하고 직접 암호 구현은 제외.',
    '쿠키 설명의 첫 사례는 값의 저장·첨부만 사용한다. 세션 ID는 서버 세션에서, SameSite는 사이트 개념 뒤에서 설명.',
    'JWT 서명 원리 → 구조와 claim의 의미 → 검증 순서. 서명형 JWT를 사례로 명시하고 Base64url 표기는 암호화나 검증으로 설명하지 않음.',
    'JWT 검증에서는 exp의 조건을 배운 뒤 적용한다. 만료 장은 세션을 포함한 수명 관리, 갱신·철회 장은 그 이후의 처리로 범위를 구분.',
    'OAuth에서 위임·scope를 처음 정의한다. 4장의 서비스 역할·데이터 소유 정책을 이해해야 하는 예제를 사용하지 않음.',
    '외부 인증 제공자 → OAuth → OIDC → 코드 흐름 → state → PKCE → 내부 계정 연결 순서. 최초 흐름도에는 아직 설명하지 않은 보호값의 내부 동작을 넣지 않음.',
    'PKCE의 변환값은 해당 장에서 일반 해시의 역할과 함께 설명. 비밀번호 저장용 해시와 같은 구현·설정이라고 가정하지 않음.',
    '3장 마지막은 외부 인증의 결과를 2장의 로그인 상태로 연결한다. 서비스 권한은 검증된 사용자 식별 이후 4장에서 판단.',
    '지난주 Auth·RLS 소개는 내부 동작을 배운 근거로 사용하지 않음. RLS는 역할·소유자 정책·API 검사를 배운 뒤 다시 정의.',
    '4장의 FoodMap 정책 표에는 아직 소개하지 않은 승인·공개 상태를 넣지 않음. 운영 업무와 상태를 배운 5장에서 조건을 확장.',
    '5장 트랜잭션은 지난주 전부 반영/취소 범위에서 사용. 트랜잭션만으로 중복 요청이나 동시 실행 문제가 모두 해결된다고 설명하지 않음.',
    '출처와 사이트를 구분한 뒤 동일 출처 정책·CORS·CSRF로 진행. CSRF 전에 쿠키 자동 첨부, 쿠키 보호 속성 전에 XSS·CSRF를 설명.',
    '7장의 환경별 설정은 3장의 복귀 주소와 4장의 API 키를 재사용. 관리자 화면을 운영 환경과 같은 뜻으로 쓰지 않음.',
    '백업 전에 복원 명령이나 복구 시나리오를 전제로 삼지 않음. 코드 롤백이 DB 변경·데이터 손실까지 되돌린다고 설명하지 않음.',
]

REFERENCES = [
    ('강의 작성 계약', '../../authoring/one-concept.md'),
    ('원본 PDF 범위', '[PWD Week6] 웹 서비스 인증과 보안.pdf'),
    ('OWASP Password Storage', 'https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html'),
    ('OWASP Session Management', 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'),
    ('JWT', 'https://www.rfc-editor.org/rfc/rfc7519.html'),
    ('OpenID Connect', 'https://openid.net/developers/how-connect-works/'),
    ('PKCE', 'https://www.rfc-editor.org/rfc/rfc7636.html'),
    ('OWASP Authorization', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'),
    ('MDN Site', 'https://developer.mozilla.org/en-US/docs/Glossary/Site'),
    ('MDN CORS', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS'),
    ('Supabase API keys', 'https://supabase.com/docs/guides/getting-started/api-keys'),
    ('Supabase environments', 'https://supabase.com/docs/guides/deployment/managing-environments'),
]


def proposal():
    chapters = {slide['id']: slide for slide in CHAPTER_SLIDES}
    assert len(chapters) == len(CHAPTERS) == 7
    assert [chapter['number'] for chapter in CHAPTERS] == list(range(1, 8))
    seen = set(PRIOR_LEARNING)
    result = []
    for chapter in CHAPTERS:
        header = chapters[f'chapter-{chapter["number"]:02}']
        items = []
        for index, item in enumerate(chapter['concepts'], 1):
            assert item['id'] not in seen, f'Duplicate ID: {item["id"]}'
            for key in ('title', 'lead'):
                assert len(item[key]) == 2 and all(value.strip() for value in item[key])
            assert item['requires'] and item['example'].strip()
            missing = set(item['requires']) - seen
            assert not missing, f'{item["id"]}: missing or later prerequisite {missing}'
            seen.add(item['id'])
            items.append(dict(outline_number=f'{chapter["number"]}.{index}', **item))
        result.append(dict(**{key: value for key, value in chapter.items() if key != 'concepts'},
                           title=header['title'], lead=header['lead'], concepts=items))
    count = sum(len(chapter['concepts']) for chapter in result)
    return dict(stage='content-title-proposal', language_order=['ko', 'en'],
                body_slide_count=count, projected_deck_slide_count=count + 8,
                current_deck_slide_count=count + 8, chapters=result, prior_learning=PRIOR_LEARNING,
                sequence_review=SEQUENCE_REVIEW, references=list(REFERENCES))


def outputs(root):
    data = proposal()
    # Resolve the actual Unicode filename instead of depending on NFC/NFD spelling.
    pdfs = list((root / 'materials').glob('[[]PWD Week6]*.pdf'))
    assert len(pdfs) == 1, 'Expected exactly one Week 6 source PDF'
    data['references'][1] = ('원본 PDF 범위', pdfs[0].name)
    labels = {item['id']: item['outline_number']
              for chapter in data['chapters'] for item in chapter['concepts']}
    lines = [
        '8주차 · 챕터 내부 제목·서브타이틀 설계안', '',
        f'본문 {data["body_slide_count"]}장 확정. 표지 1장·챕터 7장을 포함한 전체 {data["projected_deck_slide_count"]}장.',
        '7개 챕터와 내부 제목·순서는 확정. 1.1 등의 번호는 챕터 내부 설계 번호이며 현재 화면 번호가 아님.',
        '현재 HTML에 제목과 재사용 자료를 우선 배치. 이 파일에는 제목·학습 범위·선수 관계·설계 사례를 기록.',
        'FoodMap 사례는 이론 설명을 위한 확장 설계이며 현재 실습에 모두 구현되어 있다는 뜻이 아님.',
        '본문 작성 시 표·도식·코드가 추가하는 선수 개념을 다시 검토. 아래 의존성 검사는 실제 본문 검토를 대체하지 않음.',
        '작성 원본: ../scripts/title_outline.py / 재생성: python3 lectures/08/scripts/title_outline.py', '',
        '지난주까지 확인한 학습 범위',
    ]
    lines.extend(f'- {key}: {value}' for key, value in PRIOR_LEARNING.items())
    for chapter in data['chapters']:
        lines.extend(['', f'{chapter["number"]:02}. {chapter["title"][0]}',
                      chapter['lead'][0], f'연결: {chapter["connection"]}',
                      f'범위: {chapter["scope"]}', '',
                      '| 설계 번호 | 타이틀 | 서브타이틀 | 선수 개념 위치 | 연결 사례 |',
                      '| --- | --- | --- | --- | --- |'])
        for item in chapter['concepts']:
            dependencies = ', '.join(labels.get(key, key) for key in item['requires'])
            lines.append(f'| {item["outline_number"]} | {item["title"][0]} | {item["lead"][0]} | {dependencies} | {item["example"]} |')
    lines.extend(['', '학습 순서 검토 기록', ''])
    lines.extend(f'{index}. {note}' for index, note in enumerate(SEQUENCE_REVIEW, 1))
    lines.extend(['', '출처·재검토 기준', ''])
    lines.extend(f'- {label}: {url}' for label, url in data['references'])
    return {
        root / 'materials/title-outline.json': json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        root / 'materials/week-08-titles.ko.txt': '\n'.join(lines) + '\n',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for path, content in outputs(root).items():
        if args.check:
            assert path.exists() and path.read_text() == content, f'Regenerate {path}'
        else:
            path.write_text(content)
    data = proposal()
    print(f'Week 8 title proposal: {len(CHAPTERS)} chapters, {data["body_slide_count"]} content slides; prerequisites resolve to earlier material.')
