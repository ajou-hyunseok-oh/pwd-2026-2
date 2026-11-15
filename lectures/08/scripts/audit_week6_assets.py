"""Inventory existing Week 6 PDF assets against the approved Week 8 sequence.

No new teaching visuals or executable examples are authored. --extract preserves
embedded images and extracts source code/table regions for review. It needs
PyMuPDF; normal report generation and --check use only the standard library.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from title_outline import proposal

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'materials/week6-asset-audit'


def asset(ident, page, name, kind, decision, note, **selector):
    return dict(id=ident, page=page, name=name, kind=kind, decision=decision,
                reuse_note=note, selector=selector)


ASSETS = [
    asset('I04', 4, 'Stateful/Stateless 서버 구성 비교', 'image', '제외',
          '서버 확장·상태 공유 그림. 2.1의 요청별 인증 식별 문제와 다르며, 7.1의 개발/운영 환경 분리 그림으로도 쓰지 않음.', xref=35),
    asset('I05', 5, '웹방화벽의 허용·차단 그림', 'image', '제외',
          '사용자 인증이나 API 인가의 실제 판단 구조를 보여주지 않음. WAF를 인증 시스템으로 오해할 수 있어 채택하지 않음.', xref=42),
    asset('I06', 6, 'Authentication/Authorization 비교 그림', 'image', '재사용',
          '4.1에서 이미 배운 인증과 새로 배우는 인가를 대비. 1.4에 전체 그림을 넣으면 인가가 선행하므로 넣지 않음.', xref=52),
    asset('I07', 7, '개인화 엔진과 사용자 데이터 흐름', 'image', '제외',
          '추천·활동 데이터 처리 구조가 중심. 계정 식별이나 소유자 접근 제어로 바꾸면 의미가 달라져 재사용 이득이 작음.', xref=59),
    asset('I08', 8, '감사 로그의 장점 원형 그림', 'image', '제외',
          '장점만 나열하고 기록의 필드·주체·행동을 보여주지 않음. 5.7은 원본 설명을 바탕으로 감사 기록 표를 만드는 편이 적합.', xref=66),
    asset('I09-flow', 9, '로그인 입력·신원 확인·상태 기억 흐름', 'image', '수정',
          '1.7은 입력→신원 확인 부분을 발췌하고 해시 검증·사용자 ID 결과를 설명. 상태 기억 단계는 2장에서 다룸.', xref=75),
    asset('I09-login', 9, '이메일·비밀번호와 Google/Naver 로그인 화면', 'image', '수정',
          '1.4는 입력 영역만, 3.1은 외부 로그인 버튼만 발췌. 표시된 이메일은 설명용 값으로 치환. 현재 서비스의 구현 화면이라고 소개하지 않음.', xref=76),
    asset('I11', 11, '쿠키 세션 요청 시퀀스', 'image', '수정',
          '2.3의 주자료. 로그인→세션 생성→쿠키 반환→재요청→세션 조회 순서 재사용. 원본 오른쪽 확인 문구가 잘려 있어 라벨 복원. abc123은 설명용 축약값.', xref=89),
    asset('I13', 13, '브라우저·서버·세션 저장소 그림', 'image', '재사용 후보',
          '2.3에서 저장 위치를 보조하는 대안. I11과 동시에 크게 배치하지 않음. 세션 ID와 사용자 ID의 대응은 본문에서 명확히 설명.', xref=102),
    asset('I14', 14, 'JWT 발급·Bearer 전달·검증 시퀀스', 'image', '수정',
          '2.4에서는 JWT를 일반 토큰으로 바꾸고 서명 세부를 제거. 2.7에서는 JWT 명칭을 복원하고 서명 외 발급자·대상·유효 시간 검증을 추가.', xref=112),
    asset('I15', 15, 'JWT의 세 부분 문자열 그림', 'image', '재사용',
          '2.6의 구조 그림으로 사용. aaaaa 등은 실제 토큰이 아닌 자리표시임을 명시. 원본은 692×164로 작은 보조 그림에 적합하며 색상 라벨 대비 개선은 선택.', xref=119),
    asset('I17', 17, '사용자·클라이언트·제공자·리소스 API 시퀀스', 'image', '수정',
          '3.2는 참여자와 위임·API 접근 관계만 발췌. 코드 흐름 재사용 시 브라우저 경유 복귀를 명시하고 코드 교환 요청과 토큰 응답을 분리. 3.4~3.6의 공통 원본은 I18 우선.', xref=131),
    asset('I18', 18, 'state·PKCE를 포함한 OAuth 코드 흐름', 'image', '수정',
          '3.4~3.6의 공통 바탕. 최초에는 state·PKCE 세부를 빼고 단계별 추가. state 비교와 verifier 검증 위치를 보강. S256 식에는 Base64url 변환이 빠져 있고 id_token은 OIDC일 때로 한정.', xref=138),
    asset('C12', 12, 'Set-Cookie 헤더 예제', 'code-block', '수정',
          '2.2는 name=value와 전달 구조만, 6.9는 보호 속성까지 확장. 원본 날짜의 요일 불일치와 긴 한 줄은 그대로 복사하지 않음. 텍스트로 재사용하고 코드 이미지로 붙이지 않음.',
          rect=[26,272,695,325]),
    asset('C13', 13, 'Express sessionConfig 설정 객체', 'code-block', '분리 수정',
          '6.9는 cookie 보호 속성, 7.2는 process.env 참조만 발췌. 하드코딩된 secret 대체값 제거. production이면 SameSite=None이라는 규칙은 채택하지 않음. cookie.maxAge를 서버 세션 만료 보장으로 설명하지 않음.',
          rect=[338,227,706,383], text_rect=[340,253,704,381]),
    asset('C13-object', 13, '세션 객체의 인라인 예', 'code-inline', '수정',
          '2.3에서 사용자 ID를 보관한다는 예로 축소. role은 4장 이전이고 cart는 이 강의 사례에 필요하지 않아 제거.',
          verbatim='{ userId, role, cart, ... }'),
    asset('C15-header', 15, 'JWT Header JSON', 'code-inline', '재사용 후보',
          '2.6의 헤더 설명에 사용. HS256은 선택한 예시 알고리즘임을 명시하고 모든 JWT에 일반화하지 않음.',
          verbatim='{"alg":"HS256","typ":"JWT"}'),
    asset('C15-payload', 15, 'JWT Payload JSON 표기', 'code-inline', '수정',
          '2.6에 활용하되 role 제거, 현재 원고의 sub·iss·aud·exp로 정리. 원본의 ...은 유효한 JSON 값이 아니므로 실행 예제로 소개하지 않음.',
          verbatim='{"sub":"u123","role":"user","iat":...,"exp":...}'),
    asset('C15-signature', 15, 'HMACSHA256 서명 식', 'code-inline', '보류',
          '2.5에서는 아직 헤더·페이로드를 배우지 않아 그대로 사용 불가. 2.6 이후에도 암호 계산이 핵심 목표가 아니므로 본문 필수 자료에서 제외. HMAC 방식 한정이며 직렬화된 서명에는 인코딩도 필요.',
          verbatim='HMACSHA256(base64Url(header)+"."+base64Url(payload), secret)'),
    asset('T16', 16, '세션과 JWT 비교표', 'table', '부분 수정',
          '2.10에서 무효화 행의 비교 구도만 사용. JWT는 상태 저장 불필요·세션 ID 노출은 위험이 작다는 인상을 주는 원본 전체 표는 채택하지 않음.',
          rect=[46,120,674,303]),
    asset('T27-global', 27, '국외 로그인 제공자 표', 'table', '발췌',
          '3.1에서 익숙한 제공자 이름 2~3개만 소개하는 근거. 인기 순위·연계 API 기능 목록은 현재 개념과 무관하므로 제외.',
          rect=[26,90,683,234]),
    asset('T27-korea', 27, '국내 로그인 제공자 표', 'table', '발췌',
          '3.1에서 Naver/Kakao 등 이름만 발췌 가능. 국내 최다 사용 등의 서술은 근거 없이 재사용하지 않음. OIDC 지원 여부를 이 표로 판단하지 않음.',
          rect=[26,268,683,361]),
]


def mapping(number, status, assets, pages, plan, constraint=''):
    return dict(outline_number=number, status=status, assets=assets.split(),
                text_pages=pages, use=plan, prerequisite_or_correction=constraint)


# Status measures existing visual/code/table coverage, not merely topic overlap.
SLIDE_MAP = [
    mapping('1.1','설명 활용','',[3,7], '인증 필요성과 개인 데이터 예시 문장 활용. 사용자와 기록의 관계를 짧은 사례로 구성.', '개인화 엔진 그림 I07은 제외.'),
    mapping('1.2','대응 없음','',[], '계정 ID와 표시 이름의 관계를 보여주는 자료는 원본에 없음.'),
    mapping('1.3','대응 없음','',[], '클라이언트의 주장과 서버 검증을 대비하는 자료 없음.', 'WAF 그림 I05로 대체하지 않음.'),
    mapping('1.4','수정 활용','I09-login',[9], '로그인 화면의 이메일·비밀번호 입력 영역만 발췌.', '외부 로그인 버튼은 3.1에서, 실제 이메일은 설명용 값으로 치환.'),
    mapping('1.5','대응 없음','',[], '비밀번호 전용 해시와 검증을 설명하는 도식·코드 없음.'),
    mapping('1.6','대응 없음','',[], '계정별 솔트와 서로 다른 해시 결과를 보여주는 자료 없음.'),
    mapping('1.7','수정 활용','I09-flow',[9], '입력→신원 확인 두 단계와 문장 활용. 비밀번호 검증과 사용자 ID 결과를 보강.', '세 번째 상태 기억 단계는 2장 범위. 원문 DB 비교를 평문 비밀번호 비교로 설명하지 않음.'),
    mapping('2.1','설명 활용','',[4], 'HTTP 요청별 사용자 식별 필요성 문장 활용. 두 요청을 대비하는 단순 사례가 필요.', 'I04는 서버 확장 그림이므로 제외. 무상태성을 연결 종료나 서버 기억 소실로 설명하지 않음.'),
    mapping('2.2','수정 활용','C12',[12], 'Set-Cookie 헤더 앞부분을 텍스트 코드로 발췌. 이후 Cookie 전달과 대응.', 'Secure·HttpOnly·SameSite는 6.9까지 설명 보류.'),
    mapping('2.3','수정 활용','I11 I13 C13-object',[11,13], 'I11을 주 시퀀스로 사용. 저장 위치 보충이 필요할 때만 I13 또는 세션 객체를 선택.', '원본 잘린 라벨 복원. 객체에서 role·cart 제거. sessionConfig 전체는 사용하지 않음.'),
    mapping('2.4','수정 활용','I14',[14], '같은 요청 시퀀스에서 JWT를 일반 토큰으로 바꾸고 전달·확인 관계에 집중.', '서명 원리와 JWT 구조는 2.5~2.7. 로컬 저장소가 필수라는 원문은 제외.'),
    mapping('2.5','설명 활용','',[15], '위변조 방지라는 원문 설명 활용. 내용·키·검증값의 간단한 관계 표현 필요.', 'C15-signature는 아직 배우지 않은 header/payload를 사용하므로 채택하지 않음.'),
    mapping('2.6','수정 활용','I15 C15-header C15-payload',[15], 'I15 그림은 구조용으로 직접 활용 가능. JSON 예시는 원고의 필드에 맞춰 수정.', 'role 제거, iss/aud 보강, ...을 실제 예시 값으로 교체. 서명형 JWT라는 범위 명시.'),
    mapping('2.7','수정 활용','I14',[14,15], '2.4의 시퀀스에 JWT 명칭과 구체적 검증 조건을 추가.', '서명 확인만으로 끝내지 않고 발급자·대상·유효 시간까지 확인.'),
    mapping('2.8','설명 활용','',[22,23], '토큰 만료·세션 Timeout 설명을 짧은 시간선의 근거로 활용.', 'cookie.maxAge 코드만으로 서버 세션 수명을 설명하지 않음. 고정 권장 분 단위 수치는 제외.'),
    mapping('2.9','설명 활용','',[22], '액세스·리프레시 토큰 수명과 보관 역할 설명 활용.', '원본에 갱신 시퀀스는 없음. I18의 최초 코드 교환을 갱신 흐름으로 바꾸어 읽지 않음.'),
    mapping('2.10','수정 활용','T16',[16,22], '무효화 행의 비교 구조와 로그아웃 문장을 발췌해 종료 방식 비교.', '브라우저 삭제·서버 세션 종료·갱신 철회·기존 JWT 유효 시간을 구분.'),
    mapping('3.1','수정 활용','I09-login T27-global T27-korea',[17,27], '외부 로그인 버튼과 익숙한 제공자 이름만 발췌. 인증 책임의 분리를 본문과 연결.', '제공자 기능 나열·인기 순위·OIDC 일괄 적용 금지.'),
    mapping('3.2','수정 활용','I17',[18], '참여자와 허용된 API 접근 관계를 원본에서 가져와 단순화.', '코드 교환·state·PKCE는 아직 다루지 않음. OAuth를 인증 프로토콜로만 부르는 문장 교정.'),
    mapping('3.3','대응 없음','',[], 'OIDC와 ID 토큰의 역할·검증을 설명하는 독립 자료 없음.', '18쪽의 id_token 단어는 설명을 대신하지 못함.'),
    mapping('3.4','수정 활용','I18 I17',[17,18], 'I18의 참여자·기본 화살표를 공통 도식으로 재구성하고 코드 교환만 표시.', 'state·PKCE 세부는 제외. 브라우저 경유 복귀와 토큰 응답을 구분. 서버가 교환하는 선택 사례로 한정.'),
    mapping('3.5','수정 활용','I18',[18], '3.4의 공통 도식에 요청·복귀의 state와 일치 검사만 추가.', '원본에는 값은 있지만 검사 단계가 없음. PKCE 표기는 아직 제외.'),
    mapping('3.6','수정 활용','I18',[18], '같은 도식에 challenge·verifier 생성/교환/검증을 단계적으로 추가.', 'S256의 Base64url 변환 보강. id_token은 OIDC 조건부. 세부 수식보다 보호 관계를 우선.'),
    mapping('3.7','대응 없음','',[], '외부 발급자·사용자 식별자와 내부 계정을 매핑하는 자료 없음.'),
    mapping('3.8','대응 없음','',[], '외부 토큰과 FoodMap 자체 로그인 자격의 분리를 보여주는 자료 없음.', 'I17/18의 외부 Resource API를 FoodMap API로 이름만 바꾸어 재사용하지 않음.'),
    mapping('4.1','직접 활용','I06',[6], '인증과 인가를 대비하는 그림을 그대로 보조 자료로 활용.', '그림의 빈 기능 칸은 구체 정책 자체가 아니므로 주체·행동·대상 설명은 본문에서 수행.'),
    mapping('4.2','설명 활용','',[6], '일반 사용자·관리자 기능 목록을 역할별 권한 표의 근거로 활용.', '승인 상태 전이는 5장 이전이므로 여기서는 기능 사용 범위만 표시.'),
    mapping('4.3','대응 없음','',[], '사용자 ID와 행 소유자 ID를 비교하는 자료 없음.', '개인화 그림은 소유자 접근 제어와 다름.'),
    mapping('4.4','대응 없음','',[], '명시적 허용 규칙과 기본 거부를 보여주는 자료 없음.'),
    mapping('4.5','대응 없음','',[], '화면 표시와 서버 API 인가를 분리해 보여주는 자료·코드 없음.', '5쪽의 일반적 위험 설명은 참고 가능하지만 웹방화벽 그림은 채택하지 않음.'),
    mapping('4.6','대응 없음','',[], 'RLS 정책·행 필터링 도식·SQL 없음.'),
    mapping('4.7','대응 없음','',[], 'API 키와 사용자 토큰의 권한 차이·RLS 우회를 설명하는 자료 없음.', '21쪽에 API Key 이름만 등장함.'),
    mapping('4.8','설명 활용','',[6], '역할별 기능 사례를 통합 정책 표의 일부로 활용.', '소유 관계와 실제 API/DB 검사 열은 원본에 없어 보완 필요.'),
    mapping('5.1','설명 활용','',[6], '이용자 기능과 운영자 기능을 분리한 목록 활용.', '관리자 화면 캡처는 원본에 없음. 화면 분리와 서버 권한을 함께 설명.'),
    mapping('5.2','대응 없음','',[], '앱 운영자·DB 관리자·클라우드 관리자 권한 경계 자료 없음.'),
    mapping('5.3','설명 활용','',[6], '원문의 맛집 승인·거절 업무를 상태 전이 사례의 출발점으로 활용.', '상태·허용 전이·서버 검사 도식은 기존 자료에 없음.'),
    mapping('5.4','대응 없음','',[], '검토 결과와 공개 상태를 나누는 자료 없음.'),
    mapping('5.5','대응 없음','',[], '운영 작업 트랜잭션의 도식·코드 없음.'),
    mapping('5.6','대응 없음','',[], '중복 요청·멱등성의 도식·코드 없음.'),
    mapping('5.7','설명 활용','',[8,24], '누가·언제·무엇을 기록한다는 문장과 민감정보 제외 기준 활용.', 'I08은 장점 그림이므로 제외. 실제 감사 기록 행은 별도 구성 필요.'),
    mapping('6.1','대응 없음','',[], '서버 입력 검증의 조건·전후 사례·코드 없음.'),
    mapping('6.2','설명 활용','',[20], 'SQL 인젝션 정의를 명령/입력 분리 설명의 근거로 활용.', '공격 흐름 그림·SQL 예제·매개변수화 코드는 원본에 없음.'),
    mapping('6.3','설명 활용','',[20], 'XSS 정의와 피해 사례를 제보 표시 맥락에 적용.', '브라우저 실행 도식·텍스트/HTML 비교·코드 예제는 원본에 없음.'),
    mapping('6.4','대응 없음','',[], '프로토콜·호스트·포트로 출처를 비교하는 자료 없음.'),
    mapping('6.5','대응 없음','',[], '출처와 사이트의 경계 비교 자료 없음.', '23쪽 SameSite 속성 설명만으로 정의를 대신하지 않음.'),
    mapping('6.6','대응 없음','',[], '동일 출처 정책의 읽기 제한·요청 전송 비교 자료 없음.'),
    mapping('6.7','대응 없음','',[], 'CORS 헤더·허용 출처·사전 요청 도식 없음.'),
    mapping('6.8','설명 활용','',[20], '로그인 상태를 악용한 요청 위조 정의 활용.', '공격 페이지·브라우저·서버 관계도는 원본에 없음.'),
    mapping('6.9','수정 활용','C12 C13',[12,13,23], '2.2의 헤더 예제에 보호 속성을 확장. 필요하면 C13의 cookie 부분만 별도 발췌.', 'SameSite=Non을 None으로 교정하고 Secure 조건 설명. C13의 환경 분기는 7장 이전이므로 제거.'),
    mapping('6.10','설명 활용','',[20,24], '반복 추측 정의와 로그인 실패 관찰을 연결.', '시도 횟수·시간창·제한 동작을 보여주는 자료는 없음.'),
    mapping('7.1','설명 활용','',[21], 'dev/stage/prod 환경별 분리 문장을 세 환경 비교의 근거로 활용.', '관리자 화면과 운영 환경은 서로 다른 분리 축. I04의 서버 여러 대 그림은 제외.'),
    mapping('7.2','수정 활용','C13',[21], 'process.env.SESSION_SECRET 참조를 코드/설정 분리의 작은 예로 활용.', '전체 sessionConfig를 복사하지 않음. 하드코딩된 대체 키 제거, SameSite 설정은 환경 이름으로 결정하지 않음.'),
    mapping('7.3','설명 활용','',[21,22,24], '저장소 노출·과거 커밋·키 폐기/재발급·민감정보 로그 제외 설명 활용.', '.env라는 파일 이름만으로 비밀이 보호된다는 인상을 주지 않음. 네트워크 탭에서 숨기라는 문장은 제외.'),
    mapping('7.4','대응 없음','',[], '개발/운영 DB와 자격정보를 실제로 나눈 구성 그림 없음.'),
    mapping('7.5','대응 없음','',[], '검증→배포→동작 확인 흐름 자료 없음.', '30쪽은 이전 과제 제출 URL·기한이며 배포 과정의 시각 자료가 아님.'),
    mapping('7.6','대응 없음','',[], 'DB 마이그레이션과 기존 데이터·코드 호환성 자료 없음.'),
    mapping('7.7','설명 활용','',[24], '로그인 실패·권한 오류·이상 패턴 탐지 문장 활용.', '모니터링 화면이나 지표 시계열은 원본에 없음. 제품 이름을 대시보드 자료로 간주하지 않음.'),
    mapping('7.8','대응 없음','',[], '데이터 백업 자료 없음.'),
    mapping('7.9','대응 없음','',[], '코드·설정 롤백 자료 없음.'),
    mapping('7.10','대응 없음','',[], '데이터 복원 자료 없음.'),
]

PAGE_NOTES = {
    1:'2025학년도 6주차 표지. 이번 표지로 재사용하지 않음.',
    2:'학습 목표 텍스트. 별도 시각 자료 없음.',
    3:'인증 필요성 텍스트. 도입 설명의 근거로 활용.',
    4:'서버 확장 비교 그림은 제외. HTTP 설명은 개념 교정 후 활용.',
    5:'WAF 그림은 제외. 인증과 인가를 한 문제로 처리하는 설명도 분리 필요.',
    6:'인증/인가 그림과 역할별 FoodMap 기능 목록 활용.',
    7:'개인화 엔진 그림은 제외. 개인 기록의 필요성 문장은 참고.',
    8:'감사 로그의 장점 그림은 제외. 기록 목적 문장 활용.',
    9:'로그인 화면과 3단계 흐름도 각각 추출. 해당 학습 범위만 발췌.',
    10:'세션·토큰·OAuth를 같은 분류로 나열하므로 현재 개념 구조에 채택하지 않음.',
    11:'세션 요청 시퀀스 재사용 우선. 오른쪽 잘린 라벨 확인.',
    12:'쿠키 헤더 코드 재사용 우선. 학습 단계에 따라 속성 분리.',
    13:'세션 저장 위치 그림, 설정 객체, 짧은 세션 객체 예를 각각 추출.',
    14:'토큰 요청 시퀀스의 골격 활용. JWT 검증과 저장 위치 표현 수정.',
    15:'JWT 구조 그림·JSON·서명 식을 분리. 서명 식은 필수 자료에서 제외.',
    16:'비교표의 무효화 관점만 발췌. 전체 이분법 표는 그대로 사용하지 않음.',
    17:'OAuth 참여자·코드 흐름의 대안 원본. 토큰 응답과 브라우저 경유를 명확히 해야 함.',
    18:'3.4~3.6 공통 시퀀스 원본. state 검사·PKCE 변환·조건부 ID 토큰 표현 보강.',
    19:'보안·운영 챕터 표지. 현재 챕터 디자인으로 대체되어 재사용 대상 아님.',
    20:'공격 정의 텍스트만 있음. 공격 그림·실행 코드 없음. Directory Traversal은 현재 60장 범위 밖.',
    21:'환경·비밀정보 관리 텍스트만 있음. 설정/환경 분리 설명의 근거.',
    22:'토큰 수명·보관·로그아웃 텍스트만 있음. 고정 만료 권장 수치와 네트워크 탭 은폐 문구는 제외.',
    23:'쿠키 속성·외부 스토어·Timeout 텍스트. SameSite=Non 오타와 항상 전송 표현 교정.',
    24:'로그/모니터링 텍스트. 실제 로그 행·대시보드·지표 그림 없음.',
    25:'실습 챕터 표지. 별도 실습 세션 범위.',
    26:'Passport 개념과 짧은 API 표기만 있음. 완전한 로그인 구현 코드 없음. 현재 이론 필수 자료에서 제외.',
    27:'국외/국내 제공자 표 2개. 이름 중심으로 발췌 가능.',
    28:'Google 콘솔 URL만 있음. 콘솔 화면 캡처가 아님.',
    29:'Naver 개발자 URL만 있음. 설정 화면 캡처가 아님.',
    30:'이전 실습 과제와 제출 기한·URL. 이번 이론 자료로 복사하지 않음.',
    31:'Q&A 표지. 재사용할 개념 자료 없음.',
}

CORRECTION_SOURCES = [
    ('PKCE S256 변환과 verifier 검증', 'https://www.rfc-editor.org/rfc/rfc7636.html'),
    ('OAuth 위에 추가되는 OIDC와 ID 토큰', 'https://openid.net/specs/openid-connect-core-1_0.html'),
    ('SameSite=None; Secure 및 브라우저의 쿠키 전송 조건', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie'),
    ('cookie.maxAge·sameSite·secret 설정의 실제 의미', 'https://expressjs.com/en/resources/middleware/session/'),
]


def source_pdf():
    paths = list((ROOT / 'materials').glob('[[]PWD Week6]*.pdf'))
    assert len(paths) == 1
    return paths[0]


def extract():
    import pymupdf
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / 'source-assets'
    folder.mkdir(exist_ok=True)
    pdf = source_pdf()
    doc = pymupdf.open(pdf)
    assert len(doc) == 31 and list(doc[0].rect) == [0,0,720,405]
    manifest = []
    for item in ASSETS:
        page = doc[item['page'] - 1]
        selector = item['selector']
        info = dict(id=item['id'], page=item['page'], files=[])
        stem = f'p{item["page"]:02}-{item["id"].lower()}'
        if item['kind'] == 'image':
            xref = selector['xref']
            img = next(row for row in page.get_images(full=True) if row[0] == xref)
            original = doc.extract_image(xref)
            if img[1]:
                pix = pymupdf.Pixmap(pymupdf.Pixmap(doc,xref), pymupdf.Pixmap(doc,img[1]))
                path = folder / f'{stem}.png'
                pix.save(path)
            else:
                path = folder / f'{stem}.jpg'
                assert original['ext'] == 'jpeg'
                path.write_bytes(original['image'])
            info.update(xref=xref, width=img[2], height=img[3],
                        has_alpha=bool(img[1]), pdf_rects=[list(r) for r in page.get_image_rects(xref)])
            info['files'].append(path.relative_to(OUT).as_posix())
        elif 'rect' in selector:
            rect = pymupdf.Rect(selector['rect'])
            path = folder / f'{stem}-source.png'
            page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=rect,alpha=False).save(path)
            text_rect = pymupdf.Rect(selector.get('text_rect',selector['rect']))
            text_path = folder / f'{stem}-source.txt'
            text_path.write_text(page.get_text(clip=text_rect))
            info.update(pdf_rect=list(rect), text_rect=list(text_rect), render_dpi=216)
            info['files'] += [p.relative_to(OUT).as_posix() for p in (path,text_path)]
            if item['kind'] == 'table':
                tables=page.find_tables(clip=rect, vertical_strategy='lines_strict',
                                        horizontal_strategy='lines_strict').tables
                assert len(tables)==1, f'Table extraction failed: {item["id"]}'
                cells=tables[0].extract()
                expected_rows={'T16':6,'T27-global':5,'T27-korea':3}[item['id']]
                assert len(cells)==expected_rows and all(len(row)==3 for row in cells)
                info['table_cells']=cells
        else:
            snippet = selector['verbatim']
            assert snippet in page.get_text(), f'Unmatched source fragment: {item["id"]}'
            path = folder / f'{stem}-source.txt'
            path.write_text(snippet + '\n')
            info['files'].append(path.relative_to(OUT).as_posix())
        info['sha256'] = {name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in info['files']}
        manifest.append(info)
    all_images = [(n+1,img[0]) for n,p in enumerate(doc) for img in p.get_images(full=True)
                  if (img[2],img[3]) != (409,55)]
    expected = [(a['page'],a['selector']['xref']) for a in ASSETS if a['kind']=='image']
    assert sorted(all_images) == sorted(expected), 'Unreviewed embedded image'
    inventory = dict(source=pdf.name, sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                     pdf_pages=len(doc), assets=manifest,
                     pages=[dict(number=n+1,text=p.get_text(),note=PAGE_NOTES[n+1]) for n,p in enumerate(doc)])
    (OUT/'extraction.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')


def report():
    outline = proposal(historical=True)
    slides = [dict(chapter=ch['number'],**s) for ch in outline['chapters'] for s in ch['concepts']]
    assert [s['outline_number'] for s in slides] == [m['outline_number'] for m in SLIDE_MAP]
    assert set(PAGE_NOTES) == set(range(1,32))
    asset_ids = {a['id'] for a in ASSETS}
    assert len(asset_ids) == len(ASSETS)
    for row in SLIDE_MAP:
        assert set(row['assets']) <= asset_ids
        assert all(1 <= p <= 31 for p in row['text_pages'])
        assert row['status'] in {'직접 활용','수정 활용','설명 활용','대응 없음'}
    extraction = json.loads((OUT/'extraction.json').read_text())
    assert extraction['sha256'] == hashlib.sha256(source_pdf().read_bytes()).hexdigest()
    indexed = {a['id']:a for a in extraction['assets']}
    assert set(indexed) == asset_ids
    for item in indexed.values():
        for name, digest in item['sha256'].items():
            assert hashlib.sha256((OUT/name).read_bytes()).hexdigest() == digest, name
    rows = [dict(**slide, **{k:v for k,v in mapped.items() if k != 'outline_number'})
            for slide,mapped in zip(slides,SLIDE_MAP)]
    counts = dict(Counter(row['status'] for row in rows))
    data = dict(stage='existing-source-asset-audit', date='2026-11-07',
                source=extraction['source'], source_sha256=extraction['sha256'], pdf_pages=31,
                scope='자료 제작 전의 기존 PDF 조사·원본 추출 기록. 현재 반영 상태는 ../resource-placements.json 참조.',
                counts=counts, visual_review='31쪽 렌더 전체 및 이미지 13개 개별 원본 확인. 코드·표 영역은 별도 추출 대조.',
                assets=[dict(**a, extraction=indexed[a['id']]) for a in ASSETS],
                slides=rows, page_review=PAGE_NOTES, correction_sources=CORRECTION_SOURCES)
    lines = ['8주차 · PWD Week6 기존 애셋 재사용 조사', '',
             '검토일: 2026-11-07 / PDF 31쪽 / 현재 본문 구성 60장',
             '자료 제작 전 조사 판단을 보존한 기록. 현재 슬라이드 반영 상태는 ../resource-placements.ko.txt 참조.',
             f'원본: {extraction["source"]}',
             '쪽수는 PDF의 1부터 센 페이지. 1.1 등의 번호는 현재 8주차 챕터 내부 설계 번호.',
             '학교 로고를 제외한 이미지 13개, 독립 코드 영역 2개, 짧은 코드/식 4개, 표 3개를 조사·추출.',
             '이미지 13개 중 9개는 재사용·수정 후보, 4개는 현재 개념 설명과 맞지 않아 제외.',
             '원본 추출본에는 지적한 오류·선행 개념·잘림이 그대로 남아 있음. 최종 수업용 자료로 바로 넣지 않음.',
             '코드와 표의 PNG는 원문 대조용. 최종 사용 시 편집 가능한 텍스트·표로 반영.',
             '검토를 위해 PDF를 렌더했으며 페이지 전체 이미지를 수업용 애셋으로 채택하지 않음.', '',
             '60장 기준 대응 분류',
             *[f'- {name}: {counts.get(name,0)}장' for name in ['직접 활용','수정 활용','설명 활용','대응 없음']],
             '직접/수정 활용은 원본 그림·표·코드가 존재하는 경우. 설명 활용은 텍스트만 있어 시각 표현은 추가로 구성해야 하는 경우.',
             '대응 없음은 현재 슬라이드를 설명할 적합한 원본 자료가 없다는 뜻이며, 모든 빈자리에 새 이미지를 만들라는 뜻은 아님.', '',
             '우선 재사용 묶음',
             '- 9쪽: 로그인 입력 화면·흐름을 1.4/1.7/3.1에 범위를 나눠 활용.',
             '- 11/13쪽: 세션 시퀀스와 저장 위치. 2.3의 설명 목적에 맞춰 하나를 주자료로 선택.',
             '- 12/13/23쪽: 하나의 쿠키 예제를 2.2→6.9에서 확장하고, 환경 참조 부분만 7.2에서 활용.',
             '- 14/15쪽: 같은 요청 시퀀스에 일반 토큰→JWT 검증을 단계적으로 추가하고 JWT 구조 그림·JSON을 조합.',
             '- 18쪽: 공통 도식 한 번 재구성 후 3.4 코드 교환→3.5 state→3.6 PKCE로 확장. 17쪽은 참여자 설명의 대안.',
             '- 6쪽: 인증/인가 그림은 4.1에서, 역할별 기능 문장은 4.2/4.8/5.1의 표에 활용.', '',
             '원본 애셋별 판단']
    for a in data['assets']:
        e=a['extraction']
        size=f' / {e["width"]}×{e["height"]}' if 'width' in e else ''
        lines.extend(['',f'{a["id"]} · PDF {a["page"]}쪽 · {a["name"]} · {a["decision"]}{size}',
                      a['reuse_note'], '추출 파일: '+', '.join(e['files'])])
    lines.extend(['','현재 60장과의 대응'])
    for ch in outline['chapters']:
        lines.extend(['',f'{ch["number"]:02}. {ch["title"][0]}', '',
                      '| 현재 장 | 타이틀 | 분류 | 원본 자료 | 활용 방법 | 학습 순서·수정 조건 |',
                      '| --- | --- | --- | --- | --- | --- |'])
        for s in rows:
            if s['chapter'] != ch['number']:
                continue
            refs=', '.join(s['assets']) or '시각/코드 없음'
            if s['text_pages']:
                refs+='; PDF '+','.join(map(str,s['text_pages']))+'쪽 설명'
            lines.append(f'| {s["outline_number"]} | {s["title"][0]} | {s["status"]} | {refs} | {s["use"]} | {s["prerequisite_or_correction"]} |')
    lines.extend(['','페이지별 검토 기록',''])
    lines.extend(f'{p:02}쪽: {note}' for p,note in PAGE_NOTES.items())
    lines.extend(['','내용 교정 확인 근거',''])
    lines.extend(f'- {label}: {url}' for label,url in CORRECTION_SOURCES)
    lines.extend(['','조사 시점의 후속 제작 범위',
                  '원본 후보를 곧바로 덱에 삽입하지 않고 위 대응표의 학습 범위·오류 수정 조건을 적용. 새 애셋 검토는 원본에 없는 해시·솔트, 계정 연결, 소유자/RLS, 운영 상태, 브라우저 경계, DB 환경 분리·복구 등에 한정.',
                  '기존 이미지에 섞인 한국어는 EN 모드에서 별도 번역이 필요하므로, 라벨 수정이 많은 시퀀스는 공용 편집 가능한 도식으로 재구성하는 편이 후속 비용이 낮음.',
                  '원본 그림 자체에 별도 제작자·라이선스 출처가 기재되지 않은 경우 원저작자는 확인되지 않은 상태로 기록하고, 출처를 임의로 만들지 않음.',
                  '실습 라이브러리 선택, 제공자 콘솔 조작, 과제 기한·제출 방식은 이번 이론 자료 조사에서 제외.'])
    return {'audit.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n',
            'reuse-review.ko.txt':'\n'.join(lines)+'\n'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.extract:
        extract()
    for name,content in report().items():
        path=OUT/name
        if args.check:
            assert path.read_text()==content, f'Regenerate {path}'
        else:
            path.write_text(content)
    print(f'Week 6 source audit: {len(ASSETS)} assets, {len(SLIDE_MAP)} slide mappings, 31 pages reviewed.')
