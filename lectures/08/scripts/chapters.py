"""Approved Week 8 cover and chapter definitions, shared with the title outline."""

WEEK = 8
SUBTITLE = ('웹 서비스 인증과 보안', 'Web Service Authentication and Security')
CHAPTER_SLIDES = [
    dict(id='chapter-01', kind='chapter',
         title=('사용자 인증의 원리', 'Principles of User Authentication'),
         lead=('요청한 사용자의 신원을 확인하는 원리',
               'Verifying the identity of the user making a request')),
    dict(id='chapter-02', kind='chapter',
         title=('로그인 상태의 유지', 'Maintaining Login State'),
         lead=('이후 요청에서도 인증된 사용자를 식별하는 방법',
               'Identifying authenticated users across requests')),
    dict(id='chapter-03', kind='chapter',
         title=('외부 인증과 소셜 로그인', 'External Authentication and Social Login'),
         lead=('외부 서비스의 인증 결과와 서비스 사용자 계정의 연결',
               'Connecting an external identity to an application user')),
    dict(id='chapter-04', kind='chapter',
         title=('권한과 데이터 접근 제어', 'Authorization and Data Access Control'),
         lead=('사용자에게 허용할 기능과 데이터의 범위',
               'Defining which actions and data each user can access')),
    dict(id='chapter-05', kind='chapter',
         title=('관리자 시스템과 운영 업무', 'Administration Systems and Workflows'),
         lead=('운영자의 권한을 서비스 관리 업무로 연결하는 구조',
               'Organizing service management around administrator responsibilities')),
    dict(id='chapter-06', kind='chapter',
         title=('웹 공격과 방어 원리', 'Web Attacks and Defense Principles'),
         lead=('인증과 데이터 처리 과정의 위협과 보호 원리',
               'Threats and protections in authentication and data processing')),
    dict(id='chapter-07', kind='chapter',
         title=('환경 분리와 서비스 운영', 'Environment Separation and Service Operations'),
         lead=('개발·운영 환경의 분리와 서비스의 변경·복구',
               'Separating environments and managing service changes and recovery')),
]
