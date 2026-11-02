"""Week 7 lab overview, following Week 5's single-slide guide.

Scope, deadline, and deliverables follow pwd-week7/README.md.
"""

PRACTICE = dict(
    goals_label=('학습 목표', 'Learning goals'),
    goals=[
        ('SQL로 맛집 저장 구조와 접근 권한 정의',
         'Define restaurant storage and access privileges with SQL'),
        ('기존 Express API와 React 화면을 유지하며 DB 연결',
         'Connect the DB while keeping the existing Express API and React UI'),
        ('서버 재시작과 배포 환경에서 데이터 영구 저장 확인',
         'Verify persistence after server restarts and in deployment')],
    requirements_label=('요구사항', 'Requirements'),
    requirements=[
        ('Supabase에 맛집 테이블 생성 및 원본 데이터 입력',
         'Create the restaurant table in Supabase and load the original data'),
        ('맛집 등록 후 서버 재시작 · DB·API·화면의 데이터 대조',
         'Create a restaurant, restart the server, and compare DB, API, and UI data'),
        ('타입 검사·테스트·빌드 통과 후 Render·Vercel 배포 확인',
         'Pass type checks, tests, and build before verifying Render and Vercel')],
    deadline_label=('제출 마감', 'Submission deadline'),
    deadline=('2026년 11월 8일 23:59', 'November 8, 2026 · 23:59 KST'),
    deliverables_label=('제출물', 'Deliverables'),
    deliverables=[
        ('서버 GitHub URL · pwd-week7', 'Server GitHub URL · pwd-week7'),
        ('클라이언트 GitHub URL · pwd-week7-client', 'Client GitHub URL · pwd-week7-client'),
        ('Render API URL', 'Render API URL'),
        ('Vercel 서비스 URL', 'Vercel site URL')],
    reference_label=('실습 자료', 'Lab materials'),
    reference_title=('pwd-week7 · README', 'pwd-week7 · README'),
    reference_url='https://github.com/ajou-hyunseok-oh/pwd-week7#readme',
    scope=('맛집은 Supabase · 제보·좋아요는 기존 브라우저 저장',
           'Restaurants: Supabase · Submissions and likes: browser'))

PRACTICE_SLIDE = {
    'id': 'practice-week7', 'type': 'content',
    'ko': {'title': '실습 안내 · pwd-week7',
           'lead': 'Supabase로 푸드맵 데이터 영구 저장 및 기존 서비스 배포',
           'concepts': []},
    'en': {'title': 'Lab Guide · pwd-week7',
           'lead': 'Persist Foodmap data with Supabase and deploy the existing service',
           'concepts': []},
    'practice': PRACTICE,
    'source_urls': [PRACTICE['reference_url']],
    'note': '기존 53~82쪽을 이 실습 안내 한 장으로 대체. 상세 절차·SQL·코드는 pwd-week7 실습 자료 참조.'}
