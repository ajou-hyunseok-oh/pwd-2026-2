# Supabase 챕터 자료

[사용자 제공 조사 문서](research.ko.md)를 바탕으로 45~55쪽에 Supabase 챕터를 신설했다. 45쪽은 챕터 표지, 46~55쪽은 개념별 본문 10장이다. 앞의 PostgreSQL 챕터와 같은 공용 개념 설명·표·흐름·JSON 예제 형식을 재사용한다. 전체 56장이며 56쪽에 기존 FoodMap 실습 안내가 이어진다.

| 화면 | 제목 | 구체적 사례·시각 자료 |
| --- | --- | --- |
| 45 | Supabase | 챕터 표지 |
| 46 | Supabase 개요 | 공식 워드마크, PostgreSQL DBMS와 플랫폼의 관계 |
| 47 | 백엔드의 반복 작업 | 식당 저장·로그인·파일 보관·앱 고유 규칙의 역할 분담 |
| 48 | Supabase의 출발과 성장 | 2020 개발 시작→2024 GA→2026 커뮤니티 발표 |
| 49 | Supabase의 주요 기능 | 서비스 역할과 식당 목록·프로필 사진·채팅 등의 활용 표 |
| 50 | 테이블과 자동 API | restaurants 두 행과 동일한 JSON 응답, 요청 경로 |
| 51 | 사용자 로그인 | Auth 확인 흐름, 로그인 전후 화면 차이 |
| 52 | 행별 데이터 접근 | U1·U2 개인 메모의 허용·제외, 서버 비밀 키의 위치 |
| 53 | Supabase의 대중화 배경 | PostgreSQL·통합 기능·공개 자료·무료 시작의 의미 |
| 54 | AI 개발 도구와의 연결 | 요구사항→코드 작성→연결→검증, 개발자 확인 사례 |
| 55 | 무료 시작과 사용량 관리 | 무료 플랜 일부 조건과 식당 서비스의 사용량 변화 |

## 참고 원고와 수업 요구사항의 구분

제공 문서의 슬라이드 10장 구성안과 회원제 게시판 과제는 참고 제안이다. 현재 FoodMap 과제·실습 서버·스키마·제출물·마감은 바꾸지 않는다. Auth·Storage·Realtime·Edge Functions와 개인 메모는 플랫폼을 이해하기 위한 기능·개념 예제이며 실습의 새 요구사항이 아니다. 실습은 기존 Database·Data API와 Express 서버 경로를 사용한다.

전문적인 서비스 내부 이름·배치, JWT·OAuth·MCP의 프로토콜 내부, 연결 풀·성능 튜닝, 임베딩·RAG는 설명하지 않는다. 외부 기관의 추정 ARR·성장률·AI 생성 비중과 초기 데이터베이스 수는 넣지 않았다. Firebase는 등장 배경에서만 언급하며 넓은 제품군 전체를 문서형 DB 하나로 단정하지 않는다. PostgreSQL과 Supabase는 DBMS와 이를 포함하는 플랫폼의 관계로 설명한다.

## 이미지와 기술 근거

[공식 브랜드 자료](https://supabase.com/brand)의 [밝은 배경용 워드마크 SVG](https://supabase.com/brand-assets/supabase-logo-green-black-transparent.svg)를 원본 색·형태 그대로 사용했다. [출처 목록](source-manifest.json)에 다운로드 URL·해시·슬라이드 대응을 보존한다. 그 밖의 표와 흐름은 제공 조사 문서 및 공식 문서에 근거한 편집 가능한 HTML이며 실제 클라우드 실행 화면으로 표시하지 않는다.

- [공식 아키텍처](https://supabase.com/docs/guides/getting-started/architecture): PostgreSQL 기반, 오픈소스 구성, Dashboard의 관리 역할
- [Data API](https://supabase.com/docs/guides/api): 테이블 구조에서 API를 생성하고 브라우저 또는 기존 서버와 연결하는 두 구성. 50쪽은 일반적인 직접 요청 예이며 실제 FoodMap 경로와 구별
- [Auth](https://supabase.com/docs/guides/auth): 사용자 확인·로그인 상태. U1·U2는 실제 UUID의 약식 표기
- [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security): 테이블 권한과 행 정책을 함께 적용. 52쪽은 RLS 활성화·조회 권한·자기 행 정책이 있는 비우회 사용자 예. 관리자 비밀 키는 서버에 보관
- [Storage](https://supabase.com/docs/guides/storage), [Realtime](https://supabase.com/docs/guides/realtime), [Edge Functions](https://supabase.com/docs/guides/functions): 파일 보관, 연결된 클라이언트의 메시지·변경 전달, 서버 측 함수 실행의 역할
- [2020년 개발 시작 기록](https://supabase.com/blog/supabase-how-we-launch), [2024 GA](https://supabase.com/ga), [2026-04-02 GitHub 별 10만 발표](https://supabase.com/blog/100000-github-stars): 발표 날짜의 사건으로 표시. GitHub 별은 현재 사용자 수·시장점유율·매출과 구별
- [AI Tools](https://supabase.com/docs/guides/ai-tools): 개발 도구와 프로젝트 연결의 가능성. 생성 결과를 실제 배포 전 확인하는 사례로 단순화
- [공식 요금표](https://supabase.com/pricing): 2026-11-02 확인한 무료 플랜의 기본 요금 $0/월, DB 크기 500MB, 파일 저장 1GB, 1주 비활성 후 일시 정지. 일부 조건이며 모든 한도·지원 기능의 목록은 아님. 미래에도 고정된 조건이나 자동 유료 전환으로 설명하지 않음

대중화 요인은 참고 원고의 설명을 제품 기능·공개 커뮤니티 발표에 연결한 해석이며 인과 효과를 통계적으로 검증한 결과가 아니다. 공식 자료의 확인 날짜는 2026-11-02다. 각 슬라이드의 숨김 노트·슬라이드 맵에도 직접 출처를 보존한다.
