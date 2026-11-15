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
        concept('identity-need', '서비스의 사용자 식별', 'Identifying Users',
                '저장된 데이터와 요청한 사용자를 연결할 필요',
                'Associating data operations with the user making the request',
                'prior-web prior-data', '7주차 공개 맛집 생성 API가 요청 사용자 확인 없이 입력 검증을 통과한 데이터를 저장하는 상황'),
        concept('user-account', '사용자 계정', 'User Accounts',
                '사용자 정보를 관리하는 계정과 요청을 연결하는 고유 ID',
                'User records and unique IDs for linking requests',
                'identity-need prior-data', '같은 표시 이름의 두 계정을 고유 ID로 구분하고 맛집 생성 요청을 각 계정에 연결하는 설계 예시'),
        concept('trust-boundary', '클라이언트 입력의 신뢰 경계', 'The Trust Boundary for Client Input',
                '사용자가 보낸 주장과 서버가 확인한 사실의 구분',
                'Distinguishing client claims from facts verified by the server',
                'user-account prior-web', '맛집 생성 요청 본문의 사용자 ID를 u123에서 u999로 바꾸어 다른 계정에 연결될 위험을 보이는 가정 사례'),
        concept('authentication', '사용자 인증', 'User Authentication',
                '계정에 대한 증거를 확인해 요청자의 신원을 판단하는 과정',
                'Verifying account credentials to authenticate the requester',
                'user-account trust-boundary', 'minsu@example.com으로 u123 계정을 지정한 뒤 서버의 비밀번호 증거 검증 성공·실패에 따라 요청자 인정 여부를 판단하는 사례'),
        concept('password-hash', '비밀번호 해시', 'Password Hashing',
                '비밀번호 원문 대신 검증용 값을 생성해 저장하는 원리',
                'Storing a password hash instead of the plaintext password',
                'authentication', 'u123 계정에 원문 대신 해시를 저장하는 도식과 DB 유출 위험 비교'),
        concept('password-salt', '비밀번호 솔트', 'Password Salting',
                '같은 비밀번호도 서로 다른 해시가 되도록 더하는 계정별 값',
                'A per-account value that makes identical passwords produce different hashes',
                'password-hash user-account', 'u123·u999의 같은 입력 비밀번호와 서로 다른 저장 솔트·해시를 구분한 비교 표'),
        concept('password-login', '비밀번호 로그인', 'Password-Based Login',
                '이메일로 조회한 계정의 해시·솔트로 입력 비밀번호를 검증하는 흐름',
                'Look up the account by email and verify its password using the stored hash and salt',
                'authentication password-hash password-salt', 'minsu@example.com → u123 조회 → 해당 계정의 salt-A·hash-A로 검증 → 조회한 계정의 ID 인정 또는 인증 거부'),
    ]),
    dict(number=2,
         connection='챕터 1에서 확인한 u123을 이후 맛집 생성 요청에서도 확인하고, 그 로그인 자격의 만료·갱신·종료를 관리하는 원리로 확장.',
         scope='쿠키는 값 전달, 세션은 서버 상태 관리, 토큰은 자격정보, JWT는 토큰 형식으로 구분. 현재 요청의 사용자 확인까지 다루며 작업 허용 정책은 챕터 4, 쿠키 보호 속성과 공격 방어는 챕터 6에 유지.',
         concepts=[
        concept('http-stateless', 'HTTP의 무상태성', 'HTTP Statelessness',
                '이전 요청의 인증 결과가 새 요청에 자동으로 이어지지 않는 특성',
                'Why authentication from one request does not automatically carry into the next',
                'password-login prior-web', '로그인에서 확인한 u123과 사용자 확인 정보 없는 다음 맛집 생성 요청 사이의 연결 부재'),
        concept('cookies', '쿠키', 'Cookies',
                '브라우저에 보관한 작은 데이터를 이후 요청에 자동 전달하는 수단',
                'Small pieces of browser-stored data sent automatically with matching requests',
                'http-stateless', '응답의 Set-Cookie → 브라우저 저장 → 이후 요청의 Cookie'),
        concept('server-session', '세션', 'Server-Side Sessions',
                '세션 식별자로 서버에 보관한 로그인 상태를 찾는 구조',
                'Using a session ID to look up server-side login state',
                'cookies password-login', '예측하기 어려운 세션 식별자를 u123과 연결해 저장하고 이후 요청에서 해당 서버 기록 조회'),
        concept('auth-token', '토큰', 'Tokens',
                '사용자 확인이나 자원 접근을 위해 요청에 제시하는 증표',
                'A credential presented in requests to identify a user or access a resource',
                'server-session trust-boundary prior-web', 'u123 인증 후 발급된 토큰을 맛집 생성 요청의 Authorization 헤더에 첨부. 세션 식별자도 토큰이며 액세스 토큰의 형식과 전달 수단은 별도 선택'),
        concept('token-signature', '토큰의 서명', 'Token Signatures',
                '정보를 직접 담은 토큰의 내용이 바뀌었는지 검증하는 원리',
                'Verifying whether information carried in a token has been altered',
                'auth-token', 'u123의 발급 당시 내용과 u999로 바꾼 내용에 같은 signature-A를 첨부해 검증 결과 비교. 변조 탐지와 내용의 비밀 보장 구분'),
        concept('jwt-structure', 'JWT', 'JWT',
                '정보와 조건을 JSON 기반으로 표현해 전달하는 표준 토큰 형식',
                'A standard token format for representing JSON claims',
                'token-signature prior-web', 'API 액세스 토큰으로 사용하는 서명형 JWT의 헤더·페이로드·서명 역할과 sub=u123·iss·aud·exp의 의미'),
        concept('jwt-validation', 'JWT 검증', 'JWT Validation',
                '서명과 발급 조건을 확인해 토큰의 수용 여부를 판단하는 과정',
                'Deciding whether to accept a token by checking its signature and claims',
                'jwt-structure trust-boundary', 'JWT 수신 → sub=u123 읽기 → 서명·iss·aud·exp 검증 → 모두 통과하면 u123 수용, 하나라도 실패하면 인증 거부'),
        concept('auth-expiry', '인증 상태의 만료', 'Session and Token Expiration',
                '한 번 확인한 인증 결과를 계속 신뢰할 수 있는 시간의 제한',
                'Limiting how long authentication credentials remain valid',
                'server-session jwt-validation', 'u123의 세션 또는 JWT 발급 후 시간이 경과해 같은 자격으로 요청해도 인증을 거부하는 시간선'),
        concept('refresh-token', '리프레시 토큰', 'Refresh Tokens',
                '비밀번호 재입력 없이 새 액세스 토큰을 발급받는 자격정보',
                'A credential for obtaining a new access token without re-entering a password',
                'auth-expiry auth-token', '데이터 API의 액세스 토큰과 인증 시스템의 리프레시 토큰을 구분. 유효한 갱신 자격으로만 재발급하고 만료·철회된 자격은 거부'),
        concept('logout', '로그아웃과 인증 철회', 'Logout and Revocation',
                '인증 방식에 따라 사용 중인 로그인 자격을 종료하는 방법',
                'Ending active login credentials according to the authentication design',
                'server-session refresh-token jwt-validation', '현재 로그인 자격의 사용 종료와 자격 자체의 유효성을 구분. 브라우저 삭제·세션 무효화·갱신 자격 철회 및 이미 발급된 JWT의 남은 효력 비교'),
    ]),
    dict(number=3,
         connection='챕터 1의 직접 비밀번호 검증 대신 외부 인증 결과를 검증해 내부 사용자 u123에 연결하고, 챕터 2의 FoodMap 로그인 자격으로 이후 요청을 확인하는 흐름으로 확장.',
         scope='외부 신원 검증·내부 계정 연결·서비스 로그인 상태 생성까지. OAuth의 외부 API 접근과 OIDC의 신원 확인을 구분하고, 인가 코드·state·PKCE의 역할을 순서대로 설명. 실제 구현이 아닌 개념 설계 사례이며 내부 권한은 챕터 4에 유지. nonce를 사용하면 검증해야 하지만 새 독립 개념으로 추가하지 않고 제공자별 설정·SDK 세부와 함께 범위를 한정.',
         concepts=[
        concept('identity-provider', '외부 인증 제공자', 'External Identity Providers',
                '다른 서비스가 확인한 사용자 신원을 활용하는 구조',
                'Using a user identity verified by another service',
                'authentication password-login', 'FoodMap의 소셜 로그인 선택 화면과 제공자·계정 표를 유지하며 외부 비밀번호 확인과 내부 계정 관리의 책임 구분'),
        concept('oauth-delegation', 'OAuth의 접근 권한 위임', 'OAuth Access Delegation',
                '사용자가 동의한 범위의 외부 API 접근을 허용하는 방식',
                'Delegating access to an external API within the user-approved scope',
                'identity-provider auth-token prior-web', '외부 프로필 읽기 동의 → 해당 범위의 액세스 토큰 → 외부 API 검증 후 허용된 프로필 반환'),
        concept('oidc', 'OIDC의 사용자 인증', 'User Authentication with OIDC',
                '외부 인증 제공자의 ID 토큰으로 사용자 신원을 확인하는 방식',
                'Verifying a user identity through an ID token from an identity provider',
                'oauth-delegation jwt-validation', 'ID 토큰의 iss=provider-A·sub=42·aud=foodmap-client와 외부 프로필 API용 액세스 토큰의 목적·수신 대상 비교'),
        concept('authorization-code', '인가 코드 흐름', 'The Authorization Code Flow',
                '브라우저가 전달한 임시 코드를 토큰으로 교환하는 과정',
                'Exchanging a temporary code returned through the browser for tokens',
                'oidc prior-web', '브라우저로 코드를 받은 FoodMap 서버가 액세스 토큰 및 OIDC 사용 시 ID 토큰으로 교환. 코드 수신과 서비스 로그인 완료를 구분'),
        concept('oauth-state', '로그인 요청의 state', 'State in Login Requests',
                '로그인을 시작한 요청과 돌아온 응답을 연결하는 값',
                'A value that correlates a login response with the initiating request',
                'authorization-code', '해당 브라우저의 로그인 시도에 연결해 보관한 state-A와 복귀값 비교. 누락·불일치 거부 후 일치한 요청의 코드만 교환'),
        concept('pkce', '인가 코드의 PKCE 보호', 'Protecting Authorization Codes with PKCE',
                '코드 발급 요청과 코드 교환 요청을 같은 시작 주체에 연결하는 증명',
                'Binding code issuance and exchange to the same initiating client',
                'authorization-code oauth-state', '무작위 verifier를 서버에 보관하고 challenge를 먼저 전달. 코드 교환 시 변환값 대조와 불일치 거부'),
        concept('account-link', '외부 계정과 서비스 계정의 연결', 'Linking External and Local Accounts',
                '인증 제공자와 사용자 식별자로 내부 계정을 연결하는 기준',
                'Mapping a provider and its user identifier to a local account',
                'oidc pkce user-account prior-data', 'ID 토큰 검증 → 검증된 provider-A+42로 기존 연결 조회 → u123 확인. 외부 로그인 연결 추가 시 양쪽 계정 확인'),
        concept('social-session', '소셜 로그인 이후의 서비스 인증', 'Service Authentication After Social Login',
                '외부 인증 결과를 서비스의 로그인 상태로 이어가는 과정',
                'Turning an external authentication result into an application login state',
                'account-link server-session auth-token', 'provider-A/42를 u123에 연결하고 FoodMap 자격 발급. 맛집 생성 요청의 FoodMap 자격 검증으로 u123 재확인'),
    ]),
    dict(number=4,
         connection='앞 챕터에서 맛집 생성 요청의 사용자를 u123으로 확인한 결과를 이어받아, 요청별로 허용할 행동과 데이터를 정하고 서버에서 강제하는 기준을 학습.',
         scope='역할·소유 관계와 기본 거부를 먼저 정의하고 API·RLS·API 키의 적용 경로로 확장. 제보 소유자 정책은 확장 설계 사례이며, 제보 승인 상태와 공개 상태는 5장에서 처음 설명.',
         concepts=[
        concept('authorization', '요청의 인가', 'Request Authorization',
                '사용자·행동·대상을 기준으로 요청 허용 여부를 결정하는 과정',
                'Deciding whether a user may perform an action on a resource',
                'social-session authentication', '원본 인증·인가 비교 이미지 보존. u123임을 확인한 뒤에도 맛집 생성의 허용 여부는 별도로 판단'),
        concept('role-access', '역할 기반 접근 제어', 'Role-Based Access Control',
                '역할에 부여된 권한으로 기능 사용 범위를 정하는 방식',
                'Determining available actions through permissions assigned to roles',
                'authorization', 'FoodMap 정책 설계 표. 일반 사용자의 맛집 생성은 거부하고 운영자는 허용하며 제보 작성·전체 제보 조회 권한과 비교'),
        concept('owner-access', '소유자 기반 접근 제어', 'Ownership-Based Access Control',
                '요청자와 데이터 소유자의 관계로 접근 범위를 정하는 방식',
                'Determining access from the relationship between a requester and a record owner',
                'authorization role-access user-account prior-data', '확장 설계 사례. u123의 r101 조회·수정은 허용하고 u456이 소유한 r102는 거부'),
        concept('default-deny', '기본 거부 정책', 'Deny by Default',
                '명시적으로 허용한 규칙이 없으면 요청을 거부하는 기준',
                'Rejecting requests when no explicit allow rule applies',
                'role-access owner-access', '공개 맛집 조회는 로그인 없이 허용, 일반 사용자 u123의 r102 수정은 소유 조건 불충족으로 거부. 필요한 근거를 확인하지 못한 요청도 거부'),
        concept('api-access', 'API 접근 제어', 'API Access Control',
                '요청별 허용 규칙을 서버에서 검사하고 강제하는 구조',
                'Checking and enforcing permission rules for each request on the server',
                'default-deny jwt-validation trust-boundary', '맛집 생성 API 직접 요청. 로그인 자격 검증과 신뢰하는 운영자 역할 검사를 통과한 경우에만 DB 생성 작업 실행'),
        concept('rls', '행 수준 보안 정책', 'Row-Level Security Policies',
                '데이터베이스의 각 행에 접근 규칙을 적용하는 방식',
                'Applying access rules to individual database rows',
                'api-access owner-access prior-data', 'Supabase의 자기 제보 SELECT 정책. DB에 전달한 검증된 u123 문맥으로 r101·r103 반환, r102 제외. 테이블 권한과 RLS 적용 역할이 전제'),
        concept('api-keys', 'API 키의 권한 범위', 'The Authority of API Keys',
                '애플리케이션의 API 접근 자격과 사용자 인증의 구분',
                'Distinguishing application API credentials from user authentication',
                'rls auth-token api-access', 'publishable key 단독의 anon과 사용자 JWT를 함께 보낸 authenticated 문맥 비교. secret key의 특권 경로는 RLS를 우회하므로 API에서 인가'),
        concept('foodmap-policy', 'FoodMap의 접근 정책', 'FoodMap Access Policies',
                '역할과 데이터 소유 관계를 조합한 요청별 허용 기준',
                'Combining roles and ownership into request-level access rules',
                'role-access owner-access default-deny api-access rls api-keys', '공개 맛집 조회·운영자 맛집 생성·자기 제보 조회와 수정·운영자 전체 조회를 묶은 확장 설계 표. RLS 적용 경로와 특권 키 경로의 API 인가 구분'),
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

from chapter03_content import CHAPTER as BEGINNER_CHAPTER
HISTORICAL_CHAPTERS = CHAPTERS.copy()
CHAPTERS[2] = BEGINNER_CHAPTER
from chapter04_content import CHAPTER as BEGINNER_CHAPTER4
CHAPTERS[3] = BEGINNER_CHAPTER4
from chapter05_content import CHAPTER as BEGINNER_CHAPTER5
CHAPTERS[4] = BEGINNER_CHAPTER5
# Keep the original source numbering for archived asset and research lookup.
CHAPTERS = [dict(c, number=6, source_number=7) if c['number'] == 7 else c
            for c in CHAPTERS if c['number'] != 6]
from chapter06_content import CHAPTER as BEGINNER_CHAPTER6
CHAPTERS[5] = BEGINNER_CHAPTER6

SEQUENCE_REVIEW = [
    '1장에서는 인증 결과로 확인한 사용자까지만 다룬다. 역할·소유자별 허용 규칙은 4장, 세션 발급은 2장.',
    '비밀번호 검증 도식보다 해시·솔트가 먼저 온다. 비밀번호 해시에는 전용 함수를 사용한다는 범위를 유지하고 직접 암호 구현은 제외.',
    '쿠키 설명의 첫 사례는 값의 저장·첨부만 사용한다. 세션 ID는 서버 세션에서 설명. 쿠키 보호 속성은 다음 주 보안 강의로 분리.',
    'JWT 서명 원리 → 구조와 claim의 의미 → 검증 순서. 서명형 JWT를 사례로 명시하고 Base64url 표기는 암호화나 검증으로 설명하지 않음.',
    'JWT 검증에서는 exp의 조건을 배운 뒤 적용한다. 만료 장은 세션을 포함한 수명 관리, 갱신·철회 장은 그 이후의 처리로 범위를 구분.',
    'OAuth에서 위임·scope를 처음 정의한다. 4장의 서비스 역할·데이터 소유 정책을 이해해야 하는 예제를 사용하지 않음.',
    '챕터 3은 외부 제공자·Auth·SDK → OAuth/OIDC → 실제 로그인·복귀 → 인증 계정·프로필 → API 요청 순서.',
    'state·PKCE 내부 계산·클레임 검증은 초심자 본문에서 제외. SDK와 인증 서비스를 사용하는 실제 실습 경로를 구분.',
    '3장 마지막은 외부 인증의 결과를 2장의 로그인 상태로 연결한다. 서비스 권한은 검증된 사용자 식별 이후 4장에서 판단.',
    '챕터 4는 인증·인가 → 역할 → 본인 프로필 → 미들웨어 → 키와 DB 접근 순서. RLS 정책 SQL은 보충 자료.',
    '현재 라우트의 권한 표를 사용. 제보 조회·관리는 관리자 기능이며 본인 정보 사례는 프로필 수정으로 설명. 승인 업무 조건은 5장에 유지.',
    '5장 트랜잭션은 지난주 전부 반영/취소 범위에서 사용. 트랜잭션만으로 중복 요청이나 동시 실행 문제가 모두 해결된다고 설명하지 않음.',
    '6장의 환경별 설정은 3장의 복귀 주소와 4장의 API 키를 재사용. 관리자 화면을 운영 환경과 같은 뜻으로 쓰지 않음.',
    '6장은 실제 로컬 설정 → Vercel·Render 빌드·배포 → 주소 연결 → 기능 확인. 별도 검증 환경·복구 심화는 보충 자료.',
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


def proposal(historical=False):
    chapters = {slide['id']: slide for slide in CHAPTER_SLIDES}
    assert len(chapters) == 7 and len(CHAPTERS) == 6
    assert [chapter['number'] for chapter in CHAPTERS] == list(range(1, 7))
    seen = set(PRIOR_LEARNING)
    result = []
    for chapter in (HISTORICAL_CHAPTERS if historical else CHAPTERS):
        header = chapters[f'chapter-{chapter.get("source_number", chapter["number"]):02}']
        items = []
        for index, item in enumerate(chapter['concepts'], 1):
            if not historical:
                redirect = {'foodmap-policy':'api-keys', 'default-deny':'api-access', 'rls':'api-keys', 'audit-log':'workflow-state', 'admin-boundary':'admin-system', 'publication-state':'workflow-state', 'login-rate-limit':'authentication'}
                item = dict(item, requires=[redirect.get(key,key) for key in item['requires']])
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
                body_slide_count=count, projected_deck_slide_count=count + len(result) + 1,
                current_deck_slide_count=count + len(result) + 1, chapters=result, prior_learning=PRIOR_LEARNING,
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
        f'본문 {data["body_slide_count"]}장 확정. 표지 1장·챕터 6장을 포함한 전체 {data["projected_deck_slide_count"]}장.',
        '6개 챕터와 내부 제목·순서는 확정. 1.1 등의 번호는 챕터 내부 설계 번호이며 현재 화면 번호가 아님.',
        '현재 HTML에 제목과 재사용 자료를 우선 배치. 이 파일에는 제목·학습 범위·선수 관계·설계 사례를 기록.',
        '챕터 3은 실제 8주차 구현 경로를 반영. 다른 챕터의 확장 설계 사례는 구현 완료를 뜻하지 않음.',
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
