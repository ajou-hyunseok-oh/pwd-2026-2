"""Approved Week 8 cover and chapter definitions, shared with the title outline."""

WEEK = 8
SUBTITLE = ('웹 서비스 인증과 운영', 'Web Service Authentication and Operations')
CHAPTER_SLIDES = [
    dict(id='chapter-01', kind='chapter',
         title=('사용자 인증의 원리', 'Principles of User Authentication'),
         lead=('요청한 사용자의 신원을 확인하는 원리',
               'Verifying the identity of the user making a request')),
    dict(id='chapter-02', kind='chapter',
         title=('로그인 상태의 유지', 'Maintaining Login State'),
         lead=('이후 요청의 사용자 확인과 로그인 자격의 만료·갱신·종료',
               'Authenticating subsequent requests and handling expiration, token refresh and logout')),
    dict(id='chapter-03', kind='chapter',
         title=('외부 인증과 소셜 로그인', 'External Identity Providers and Social Login'),
         lead=('외부 로그인 용어와 Supabase Auth·SDK를 이용한 FoodMap 인증 흐름',
               'Social login in FoodMap with Supabase Auth and the browser SDK')),
    dict(id='chapter-04', kind='chapter',
         title=('권한과 데이터 접근 제어', 'Authorization and Data Access Control'),
         lead=('실습의 역할·본인 정보·미들웨어와 서버의 권한 검사',
               'User roles, profile updates, middleware and server-side authorization')),
    dict(id='chapter-05', kind='chapter',
         title=('관리자 시스템과 운영 업무', 'Admin Interfaces and Workflows'),
         lead=('제보 상태와 실제 승인·트랜잭션·중복 요청 처리 흐름',
               'Submission states, approval, transactions and repeated requests')),
    dict(id='chapter-06', kind='chapter',
         title=('웹 공격과 방어 원리', 'Web Attacks and Defense Principles'),
         lead=('인증과 데이터 처리 과정의 위협과 보호 원리',
               'Threats and protections in authentication and data processing')),
    dict(id='chapter-07', kind='chapter',
         title=('환경 분리와 서비스 운영', 'Deployment Environments and Operations'),
         lead=('실습 설정과 빌드·배포·주소 연결·동작 확인',
               'Configuration, builds, deployment, endpoint setup and functional verification')),
]
