"""Five beginner-facing report and approval workflow slides."""
from chapter03_content import P, G, B, concept, Q, M


def branches(title, body, children, caption):
    return dict(kind='resource-branches', title=title, body=body,
                children=[dict(title=t, body=b) for t,b in children], caption=caption)


CHAPTER = dict(number=5,
    connection='챕터 4의 사용자·관리자 권한을 실제 제보 작성과 승인 업무에 적용.',
    scope='제보와 관리자 업무 → 처리 상태 → RPC 승인 흐름 → 트랜잭션 → 중복 승인. 공개 상태·감사 로그·잠금과 범용 멱등성 키는 보충 자료.',
    concepts=[
        concept('admin-system', P('사용자 제보와 관리자 업무', 'User Submissions and Admin Tasks'), P('등록 요청과 서비스 데이터 반영의 구분', 'Submitting a restaurant for review and adding it to the public list'), 'role-access api-access', '로그인 사용자 제보 → pending 저장 → 관리자 검토'),
        concept('workflow-state', P('제보의 처리 상태', 'Submission Review Status'), P('대기·승인·거절로 구분하는 검토 결과', 'Review status: pending, approved and rejected'), 'admin-system', 'pending에서 승인 또는 거절 · 승인 시에만 맛집 생성'),
        concept('approval-flow', P('제보 승인의 구현 흐름', 'How Submission Approval Works'), P('관리자 화면에서 서버와 DB 함수를 거쳐 승인 결과 반영', 'From the admin interface through Express and the database function to the response'), 'workflow-state api-access', 'POST /api/submissions/:id/approve → rpc → approve_foodmap_submission → 목록 갱신'),
        concept('admin-transaction', P('승인 작업의 트랜잭션', 'The Approval Transaction'), P('맛집 등록과 제보 상태 변경의 전부 반영 또는 전부 취소', 'Commit restaurant creation and the submission update together, or roll back both'), 'approval-flow prior-data', 'DB 함수 안의 맛집 생성과 승인 상태·검토자·검토 시각 저장'),
        concept('idempotency', P('중복 승인 요청의 처리', 'Handling Repeated Approval Requests'), P('승인을 다시 눌러도 맛집 추가 생성 방지', 'Approving again does not create another restaurant'), 'admin-transaction workflow-state', '대기: 새 등록 · 승인 완료: 연결된 기존 맛집 반환 · 거절: 승인 거부'),
    ])

BODY = {
    'admin-system': B('wide',
        G(P('제보 - 사용자가 서비스에 등록을 요청한 맛집 정보', 'Submission - restaurant information submitted by a user for review'),
          P('로그인 사용자가 작성 · 서버가 확인한 작성자와 대기 상태로 저장', 'Submitted by a signed-in user and saved as pending under the authenticated user’s ID')),
        G(P('관리자 업무 - 제보 검토 후 서비스 데이터 반영', 'Admin task - review submissions and manage application data'),
          P('제보 저장과 맛집 등록은 별개 · 승인한 제보의 정보로 맛집 생성', 'Saving a submission and creating a restaurant are separate; approval creates the restaurant'))),
    'workflow-state': B('wide',
        G(P('상태(status) - 제보의 현재 처리 단계', 'Status - the current processing stage of a submission'),
          P('pending: 검토 대기 · approved: 승인 완료 · rejected: 거절 완료', 'pending: awaiting review · approved: accepted for listing · rejected: not accepted')),
        G(P('검토 기록 - 처리한 관리자와 처리 시각', 'Review metadata - the reviewer and review timestamp'),
          P('reviewed_by: 관리자 ID · reviewed_at: 검토 시각', 'reviewed_by: admin ID · reviewed_at: review time'))),
    'approval-flow': B('wide',
        G(P('RPC(Remote Procedure Call) - 원격 프로그램의 함수를 호출하는 방식', 'RPC (Remote Procedure Call) - invoke a function on a remote system'),
          P('실습은 Express가 Supabase API로 승인 DB 함수 호출 · 함수에서 조건 검사와 데이터 변경', 'In this project, Express calls a DB function through the Supabase API to check conditions and update data'),
          P('/api/submissions/:id/approve의 :id는 선택한 제보의 ID가 들어갈 자리', ':id in /api/submissions/:id/approve is replaced with the selected submission’s ID'))),
    'admin-transaction': B('wide',
        G(P('트랜잭션(transaction) - 여러 DB 변경을 하나로 묶는 처리 단위', 'Transaction - a single, all-or-nothing unit of database work'),
          P('모두 성공하면 함께 반영 · 중간 오류가 나면 해당 작업의 변경을 모두 취소', 'Commit all changes on success; roll back the transaction if any step fails'),
          P('하나의 승인 요청에서 맛집 등록과 제보 변경이 따로 남는 결과 방지', 'Prevent partial updates: restaurant creation and the submission update must succeed together'))),
    'idempotency': B('wide',
        G(P('중복 요청 - 같은 작업을 다시 보내는 요청', 'Repeated request - sending the same operation again'),
          P('버튼 재클릭·응답 유실 후 재시도 가능 · DB의 현재 상태로 처리 결정', 'Clicks and retries after a lost response can repeat requests; use the current DB state')),
        G(P('승인 완료 시의 재요청 - 연결된 기존 맛집 재사용', 'Retry after approval - reuse the linked restaurant'),
          P('이미 승인한 제보는 기존 맛집 반환 · 같은 제보의 맛집을 다시 만들지 않음', 'For an approved submission, return the linked restaurant without creating another'))),
}

MEDIA = {
    'admin-system': [[Q([P('사용자 화면', 'User interface'), P('Express 서버', 'Express server'), P('관리자 화면', 'Admin interface')], [
        M(0,1,'제보 작성 · POST /api/submissions','Create submission · POST /api/submissions'),
        M(1,1,'작성자 확인 후 pending 저장','Identify the submitter and save with pending status',focus=True),
        M(2,1,'관리자 권한으로 제보 목록 요청','Request submissions with admin permission'),
        M(1,2,'검토할 제보 목록 반환','Return submissions for review',reply=True),
    ], P('제보 저장만으로 공개 맛집 목록에 추가되지 않음', 'Saving a submission alone does not add it to the public restaurant list'))]],
    'workflow-state': [[branches(P('pending · 검토 대기', 'pending · Awaiting review'), P('관리자가 내용 확인 후 처리 선택', 'The administrator reviews the submission and chooses an action'), [
        (P('승인 → approved', 'Approve → approved'), P('맛집 생성 + 승인 상태·검토 기록 저장', 'Create a restaurant and save the approval and review metadata')),
        (P('거절 → rejected', 'Reject → rejected'), P('맛집 생성 없이 거절 상태·검토 기록 저장', 'Save the rejection and review metadata without creating a restaurant')),
    ], P('새 승인·거절은 대기 상태에서 처리 · 삭제는 별도 작업', 'Only pending submissions can be newly approved or rejected; deletion is separate'))]],
    'approval-flow': [[Q([P('관리자 화면', 'Admin interface'), P('Express 서버', 'Express server'), P('Supabase DB', 'Supabase DB')], [
        M(0,1,'승인 클릭 · POST /api/submissions/:id/approve','Click Approve · POST /api/submissions/:id/approve'),
        M(1,1,'isAuthenticated → requireAdmin','isAuthenticated → requireAdmin',focus=True),
        M(1,2,'rpc("approve_foodmap_submission") 호출','Call rpc("approve_foodmap_submission")',focus=True),
        M(2,2,'관리자·제보 상태 확인 → 승인 처리','Verify admin privileges and submission status → approve',focus=True),
        M(2,1,'등록한 맛집 반환','Return the restaurant',reply=True),
        M(1,0,'성공 응답 → 제보·맛집 목록 갱신','Success → refresh submission and restaurant lists',reply=True),
    ], P('브라우저는 Express API 호출 · DB 함수는 Express 서버가 호출', 'The browser calls Express; the Express server calls the DB function'))]],
    'admin-transaction': [[dict(kind='resource-transaction', operations=[
        P('① 제보 정보로 restaurants에 맛집 생성', '① Create a restaurant from the submission in restaurants'),
        P('② submissions에 승인 상태·검토자·검토 시각 저장', '② Save approval status, reviewer and review time in submissions'),
    ], results=[
        (P('모두 성공 → 함께 반영', 'All steps succeed → commit'), P('맛집 등록 + 제보 승인·검토 기록', 'Restaurant creation + submission approval and review metadata')),
        (P('중간 오류 → 모두 취소', 'Any step fails → roll back'), P('이번 승인 작업 전의 DB 상태 유지', 'Leave the database unchanged by this approval attempt')),
    ])]],
    'idempotency': [[branches(P('같은 제보의 승인 요청', 'Approval request for the same submission'), P('DB 함수가 현재 제보 상태 확인', 'The DB function checks the current submission state'), [
        (P('pending · 대기', 'pending · Awaiting review'), P('맛집 새 등록 후 승인 상태 저장', 'Create a restaurant and mark the submission approved')),
        (P('approved · 승인 완료', 'approved · Already approved'), P('연결된 기존 맛집 반환 · 추가 등록 없음', 'Return the linked restaurant; no new restaurant')),
        (P('rejected · 거절 완료', 'rejected · Already rejected'), P('승인 거부 · 맛집 등록 없음', 'Reject the request; do not create a restaurant')),
    ], P('화면의 버튼 비활성화와 별개로 서버·DB에서 중복 처리 방지', 'The server and DB prevent duplicates independently of disabled UI buttons'))]],
}

PARAGRAPHS = {
    'admin-system': '제보는 사용자가 등록을 요청한 맛집 정보이며 서비스의 공개 맛집과 구분한다. 로그인 사용자의 POST /api/submissions 요청은 서버가 확인한 사용자 ID를 submitter_id로 붙이고 pending으로 저장한다. 관리자 업무는 이 제보를 검토한 후 승인 또는 거절하는 과정이다. 조회와 처리에는 관리자 권한이 필요하며 플랫폼 운영자 권한과 혼동하지 않는다. 승인 시에만 제보를 바탕으로 restaurants에 맛집을 생성한다.',
    'workflow-state': 'status는 현재 처리 단계를 저장한 값이다. pending은 검토 대기, approved는 승인 완료, rejected는 거절 완료다. 대기 제보의 승인 시 맛집을 생성하고 승인 상태와 reviewed_by·reviewed_at을 저장한다. 거절은 맛집을 만들지 않고 거절 상태와 검토 기록을 저장한다. reviewed_by는 관리자 사용자 ID이고 reviewed_at은 검토 시각이다. 삭제는 별도 작업이며 삭제됨이라는 상태는 구현에 없다. 승인 완료 요청의 재시도는 뒤의 중복 요청 장에서 다룬다. 별도 공개 여부 열과 전체 감사 로그는 현재 구현에 없으므로 확장 설계로 분리한다.',
    'approval-flow': '이 장은 관리자 화면에서 Express와 DB 함수까지 이어지는 요청 경로를 설명한다. URL의 :id는 선택한 제보 ID가 들어갈 자리임을 본문에 명시한다. RPC는 Remote Procedure Call의 약자로 원격 기능 호출이다. 본문은 이 실습에서 API로 DB의 저장된 함수를 호출한다는 의미를 먼저 정의한다. 관리자 화면 승인 → POST /api/submissions/:id/approve → isAuthenticated와 requireAdmin → submissions.service.ts의 rpc → approve_foodmap_submission 함수의 관리자 및 제보 상태 확인과 승인 처리 → 맛집 결과 반환 순서다. 성공 후 클라이언트는 submissions·restaurants 쿼리를 무효화해 목록에 변경을 반영한다. 브라우저가 DB 함수를 직접 호출하거나 클라이언트가 검토자 ID를 신뢰 가능한 값으로 정하는 구조가 아니다. DB 함수의 세부 원자적 변경은 다음 장에서 설명한다.',
    'admin-transaction': '트랜잭션은 여러 DB 변경을 전부 반영하거나 전부 취소하는 단위다. 실제 approve_foodmap_submission 함수는 restaurants에 먼저 맛집을 생성한 다음 submissions의 승인 상태·검토자·시각을 변경한다. 같은 함수 실행의 DB 트랜잭션에서 오류가 발생하면 해당 작업의 변경을 취소한다. 별도 외부 API의 효과나 이미 끝난 이전 작업까지 취소한다는 의미가 아니다. 트랜잭션은 불완전한 반영 방지이며 중복 요청 처리는 별도 개념이다.',
    'idempotency': '중복 요청은 버튼 재클릭이나 응답 유실 후 재시도처럼 같은 작업이 다시 전달되는 상황이다. 본문에서는 멱등성 용어를 제외하고 승인을 다시 눌러도 맛집을 추가 생성하지 않는 결과에 집중한다. 멱등성 정의는 보충 자료에서 다룬다. 실제 DB 함수는 pending이면 새 맛집을 생성하고 approved이면 연결된 기존 맛집을 반환하며 rejected이면 거부한다. 이미 승인했지만 연결 맛집이 삭제된 비정상 상태는 오류를 반환하므로 모든 approved 요청의 성공을 보장하지 않는다. FOR UPDATE 잠금과 source_submission_id UNIQUE가 동시 실행의 중복 방지를 보강한다. 일반 멱등성 키 저장소는 현재 구현이 아니며 보충 자료에만 둔다. 검토한 코드는 읽기 대조이며 실환경 DB 실행 결과가 아니다.',
}

SOURCES = [('Supabase RPC', 'https://supabase.com/docs/reference/javascript/rpc'), ('PostgreSQL Transactions', 'https://www.postgresql.org/docs/current/tutorial-transactions.html'), ('PostgreSQL Explicit Locking', 'https://www.postgresql.org/docs/current/explicit-locking.html')]
REVIEW = dict(assessment='본문 7장을 실제 제보·승인 흐름의 5장으로 통합. 정의 → 상태 → RPC 흐름 → 트랜잭션 → 중복 승인 순서.', boundary='공개 상태·감사 로그와 플랫폼 관리 권한은 현재 기능과 구분해 보충 자료로 분리. 잠금·격리 수준·멱등성 키는 심화 범위.', caution='실제 클라이언트·Express·스키마를 읽어 대조. 실환경 DB 변경이나 로그인 실행 검증은 수행하지 않음.')
