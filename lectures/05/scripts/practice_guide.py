"""Week 5 lab guide; requirements come from the lab README and the user."""
from slide_body import P

PRACTICE = [dict(
    kind='practice',
    goals_label=P('학습 목표', 'Learning goals'),
    goals=[
        P('컴포넌트·Props·State·Hooks로 맛집 화면 구성', 'Build restaurant UI with components, props, state, and Hooks'),
        P('사용자 입력에 따른 화면 갱신과 브라우저 저장 구현', 'Update UI from user input and persist data in the browser'),
        P('GitHub 버전 관리와 Vercel 자동 배포', 'Manage versions on GitHub and deploy automatically with Vercel')],
    requirements_label=P('요구사항', 'Requirements'),
    requirements=[
        P('맛집 목록·카테고리 필터·좋아요·인기 TOP 5·제보 동작 확인', 'Verify listings, category filters, likes, top 5, and restaurant submissions'),
        P('제보를 localStorage에 저장하고 새로고침 후 유지 확인', 'Save submissions in localStorage and verify persistence after reload'),
        P('빌드 오류 없이 배포하고 Vercel 사이트에서 기능 확인', 'Build without errors and verify the deployed Vercel site')],
    deadline_label=P('제출 마감', 'Submission deadline'),
    deadline=P('2026년 10월 18일 23:59', 'October 18, 2026 · 23:59 KST'),
    deliverables_label=P('제출물', 'Deliverables'),
    deliverables=[P('GitHub 저장소 URL', 'GitHub repository URL'),
                  P('Vercel 서비스 URL', 'Vercel site URL')],
    reference_label=P('실습 자료', 'Lab materials'),
    reference_title=P('pwd-week5 · README', 'pwd-week5 · README'),
    reference_url='https://github.com/ajou-hyunseok-oh/pwd-week5#readme',
    scope=P('가상 맛집 목록 사용 · 제보는 현재 브라우저에 저장',
            'Use mock restaurant data; submissions stay in the current browser'))]
