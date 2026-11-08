"""Korean paragraph drafts for checking the Week 8 lecture sequence.

These are review prose, not rendered slide bodies. Titles and numbering are
imported from title_outline.py; each planned slide has exactly one paragraph.
"""
import argparse
import json
from pathlib import Path

from title_outline import proposal


PARAGRAPHS = {
    'identity-need': (
        '지난주에는 FoodMap의 맛집 데이터를 서버와 데이터베이스에 저장해 다시 조회할 수 있게 했다. '
        '여기에 사용자의 제보를 연결하려면 데이터의 내용뿐 아니라 누가 그 데이터를 보냈는지도 구분해야 한다. '
        '사용자 식별은 여러 요청과 기록을 같은 사람에게 연결하는 출발점이며, 데이터가 저장되어 있다는 사실만으로 요청자의 신원이 확인되지는 않는다.'),
    'user-account': (
        '사용자 계정은 서비스가 한 사용자를 지속적으로 구분하기 위해 관리하는 기록이다. '
        '고유한 사용자 ID를 기준으로 이름과 연락처 같은 정보를 연결하면 표시 이름이 바뀌어도 같은 사용자의 기록을 유지할 수 있다. '
        'FoodMap의 제보도 이름 문자열보다 사용자 ID에 연결하는 편이 안정적이며, 이 ID는 사용자를 가리키는 값이다.'),
    'trust-boundary': (
        '요청에 사용자 ID가 들어 있어도 그 값을 보낸 사람이 해당 계정의 사용자라고 바로 판단할 수는 없다. '
        '브라우저에서 보내는 값은 사용자가 바꿀 수 있으므로 서버는 클라이언트의 주장과 직접 확인한 사실을 구분해야 한다. '
        'FoodMap 요청의 작성자 ID를 다른 사람의 값으로 바꾸는 사례는 식별자를 전달하는 것만으로 신원을 증명할 수 없음을 보여준다.'),
    'authentication': (
        '사용자 인증은 요청자가 주장하는 계정에 대해 적절한 증거를 제시하는지 확인하는 과정이다. '
        '비밀번호 방식에서는 서버가 계정을 찾은 뒤 그 계정의 비밀번호를 알고 있다는 증거를 검증한다. '
        '검증에 성공하면 서버는 요청을 확인된 사용자 ID와 연결할 수 있으며, 사용자 ID를 알고 있다는 사실과 그 계정의 사용자라는 사실을 구분하게 된다.'),
    'password-hash': (
        '비밀번호 해시는 비밀번호에서 계산한 검증용 값으로, 서버가 원문 비밀번호를 그대로 보관하지 않고도 입력을 확인하는 데 사용한다. '
        '비밀번호 저장에는 반복적인 추측의 비용을 높이도록 설계한 전용 해시 함수를 사용한다. '
        '로그인할 때는 저장된 원문을 꺼내 비교하는 대신 입력한 비밀번호가 저장된 검증 정보와 일치하는지 확인하며, 해시가 유출되어도 추측 위험까지 사라지는 것은 아니다.'),
    'password-salt': (
        '솔트는 비밀번호를 해시할 때 함께 사용하는 무작위 값으로, 같은 비밀번호를 선택한 계정들도 서로 다른 해시 결과를 갖게 한다. '
        '솔트는 해시와 함께 보관할 수 있으며, 입력을 검증할 때 해당 계정에 저장된 솔트를 다시 사용한다. '
        '두 사용자가 같은 비밀번호를 쓰더라도 저장 결과가 같지 않으므로, 한 번 계산한 추측 결과를 여러 계정에 그대로 대입하기 어려워진다.'),
    'password-login': (
        '비밀번호 로그인은 계정 조회와 비밀번호 검증을 거쳐 요청자의 사용자 ID를 확정하는 흐름이다. '
        '가입할 때 비밀번호 해시와 솔트 등 검증 정보를 저장하고, 로그인할 때 입력한 비밀번호를 해당 정보와 함께 검증 함수에 전달한다. '
        '검증에 성공하면 FoodMap 서버가 확인한 사용자 ID가 얻어지며, 여기까지의 결과는 현재 로그인 요청에서 사용자를 확인했다는 사실이다.'),

    'http-stateless': (
        '현재 로그인 요청에서 사용자를 확인했더라도 그 결과가 새 HTTP 요청에 자동으로 붙지는 않는다. '
        'HTTP는 각각의 요청만으로 이전 인증 결과를 보장하지 않으므로, 애플리케이션이 요청 사이를 연결할 정보를 별도로 관리해야 한다. '
        'FoodMap의 로그인 직후 맛집 목록을 다시 요청하는 상황을 통해, 한 번의 사용자 확인과 여러 요청에 걸친 로그인 유지가 다른 문제임을 이해한다.'),
    'cookies': (
        '쿠키는 브라우저가 값을 저장했다가 정해진 조건에 맞는 요청에 첨부하는 기능이다. '
        '서버가 응답의 Set-Cookie로 값을 전달하면 브라우저는 이를 저장하고, 전송 조건을 만족하는 이후 요청의 Cookie에 포함할 수 있다. '
        '쿠키 자체가 사용자의 신원을 확인하는 것은 아니며, 서버와 브라우저가 요청 사이에 값을 주고받을 수 있도록 하는 수단이다.'),
    'server-session': (
        '서버 세션은 로그인 상태를 서버에 보관하고 임의의 세션 식별자로 그 상태를 찾아 사용하는 구조다. '
        '로그인에 성공하면 서버는 세션 식별자와 사용자 ID를 연결해 저장하고 식별자를 쿠키로 전달한다. '
        '이후 FoodMap 요청에 식별자가 돌아오면 서버는 저장된 세션을 조회해 사용자를 확인하므로, 브라우저가 보낸 사용자 ID를 그대로 믿을 필요가 없다.'),
    'auth-token': (
        '토큰은 이후 요청을 처리할 때 제시하는 자격정보이며, 서버의 확인을 거쳐 사용자나 접근 자격과 연결된다. '
        '세션 식별자처럼 서버의 기록을 찾아야 의미를 알 수 있는 토큰도 있고, 토큰 자체에 확인할 정보를 담는 형식도 있다. '
        'API에 제시하는 액세스 토큰은 요청 헤더 등으로 전달할 수 있으며, 토큰의 형식과 전달 수단은 구분해서 선택한다.'),
    'token-signature': (
        '토큰에 사용자 정보를 직접 담으면 그 내용을 사용자가 바꾸지 않았는지 확인할 방법이 필요하다. '
        '서명은 발급자가 관리하는 암호학적 키를 이용해 검증 가능한 값을 붙이는 방식이며, 수신자는 신뢰하는 발급자의 검증 키와 방법으로 무결성을 확인한다. '
        'FoodMap 사용자 ID를 임의로 바꾼 토큰은 검증에 실패하도록 만들 수 있지만, 서명만으로 토큰 내용이 숨겨지는 것은 아니다.'),
    'jwt-structure': (
        'JWT는 사용자에 관한 주장과 유효 조건을 JSON 기반으로 담는 토큰 형식이다. '
        '이 강의의 서명형 JWT는 서명 방식 등을 나타내는 헤더, 주장들을 담는 페이로드, 변조를 확인하는 서명으로 구성된다. '
        '페이로드의 sub는 사용자 식별자, iss는 발급자, aud는 토큰을 받을 대상, exp는 만료 시각을 나타내며, 내용은 읽을 수 있으므로 비밀번호 같은 비밀을 넣지 않는다.'),
    'jwt-validation': (
        'JWT의 내용을 읽는 것과 그 내용을 신뢰하는 것은 별도의 단계다. '
        '서버는 미리 허용한 서명 방식과 신뢰하는 키로 서명을 검증하고, 발급자와 수신 대상이 예상과 일치하며 유효 시간이 지나지 않았는지 확인한다. '
        '이 조건을 통과한 뒤에만 토큰의 사용자 식별자를 요청 처리에 사용하므로, 형식이 맞거나 사용자 ID가 보인다는 이유만으로 인증에 성공하지 않는다.'),
    'auth-expiry': (
        '인증 상태의 만료는 과거의 인증 결과를 신뢰할 수 있는 시간을 제한하는 장치다. '
        '서버 세션은 마지막 활동이나 생성 시점을 기준으로 종료할 수 있고, JWT는 exp에 기록된 시각을 기준으로 유효성을 판단한다. '
        '서버의 인증 상태가 만료되었다면 브라우저에 식별자나 토큰이 남아 있더라도 유효한 인증으로 받아들이지 않는다.'),
    'refresh-token': (
        '액세스 토큰의 수명을 짧게 유지하면서 매번 비밀번호를 입력하지 않게 하려면 새 토큰을 발급받는 절차가 필요하다. '
        '리프레시 토큰은 이 갱신에 사용하는 별도의 자격정보로, 일반 데이터 API 대신 인증 시스템에 제출한다. '
        '인증 시스템이 갱신 자격을 확인하면 새 액세스 토큰을 발급하며, 토큰을 계속 발급받는 데 악용될 수 있는 갱신 자격은 별도로 보호해야 한다.'),
    'logout': (
        '로그아웃은 브라우저의 로그인 표시를 지우는 데서 끝나지 않고 사용하던 자격정보의 효력을 종료하는 과정이다. '
        '서버 세션은 서버의 연결 기록을 무효화할 수 있고, 토큰 방식은 보관한 토큰을 제거하면서 갱신 자격도 철회한다. '
        '다만 서명과 유효 조건만으로 검증하는 JWT는 이미 발급된 토큰이 만료까지 유효할 수 있으므로, 즉시 차단이 필요하면 서버에서 철회 여부를 추가로 확인하는 설계가 필요하다.'),

    'identity-provider': (
        '사용자를 확인하는 일을 서비스가 직접 수행하지 않고 외부 인증 제공자에게 맡길 수도 있다. '
        '외부 제공자는 자신의 계정으로 사용자를 인증하고, FoodMap은 그 제공자가 전달한 결과를 검증해 활용한다. '
        '이 구조에서는 외부 계정의 비밀번호를 FoodMap이 받아 저장하지 않으며, 외부 제공자의 책임과 서비스 내부 계정 관리의 책임이 나뉜다.'),
    'oauth-delegation': (
        '외부 서비스와 연결할 때는 먼저 그 서비스의 데이터에 접근할 자격을 위임받는 구조를 이해해야 한다. '
        'OAuth는 사용자가 동의한 범위인 scope 안에서 애플리케이션이 외부 API를 호출하도록 액세스 토큰을 발급하는 체계다. '
        '예를 들어 FoodMap은 외부 계정의 비밀번호를 받지 않고 허용된 프로필 정보에 접근할 수 있으며, 이 접근 위임만으로 서비스의 사용자 신원 확인 절차 전체가 정의되지는 않는다.'),
    'oidc': (
        'OIDC는 OAuth 기반의 흐름에 사용자 인증 결과를 전달하는 규칙을 더한 체계다. '
        '제공자가 OIDC를 지원하면 서비스는 ID 토큰의 서명과 발급자, 수신 대상, 유효 조건을 검증해 누구의 인증 결과인지 확인할 수 있다. '
        'ID 토큰은 사용자의 신원을 전달하고 외부 API용 액세스 토큰은 외부 데이터 접근에 사용되므로, 두 토큰의 목적과 받아들이는 대상을 구분한다.'),
    'authorization-code': (
        '인가 코드 흐름은 브라우저로 전달받은 짧은 수명의 일회용 코드를 토큰과 교환하는 절차다. '
        'FoodMap 서버가 교환을 맡는 사례에서는 사용자가 외부 인증 화면을 거친 뒤 등록된 복귀 주소로 돌아오고, 서버가 전달된 코드를 제공자의 토큰 발급 창구에 제출한다. '
        '코드는 해당 애플리케이션과 복귀 주소 등의 조건에 연결되며, 사용자는 외부 계정의 비밀번호를 FoodMap에 전달하지 않고 인증 결과를 이어갈 수 있다.'),
    'oauth-state': (
        '외부 화면을 거쳐 돌아온 응답은 실제로 이 브라우저에서 시작한 로그인 요청에 대한 응답인지 확인해야 한다. '
        'state는 요청을 시작할 때 예측하기 어려운 일회용 값을 만들어 해당 브라우저의 로그인 시도에 연결하고, 복귀한 값과 대조하는 데 사용한다. '
        '값이 없거나 일치하지 않으면 연결을 중단하며, state의 일치는 사용자 신원이나 토큰 서명 검증을 대신하지 않는다.'),
    'pkce': (
        'PKCE는 인가 코드를 얻은 쪽이 그 코드를 발급받기 위한 요청을 시작한 쪽인지 확인하도록 교환 절차를 보호한다. '
        '로그인 시도마다 비밀로 보관할 검증값을 만들고 그 값의 해시를 먼저 전달한 뒤, 코드를 교환할 때 원래 검증값을 제시한다. '
        '제공자는 받은 검증값으로 해시를 다시 계산해 앞서 받은 값과 비교하므로, 코드만 가로챈 상대는 교환에 필요한 증거를 갖추지 못한다.'),
    'account-link': (
        '외부 인증 결과를 검증한 뒤에는 외부의 사용자 식별자를 FoodMap 내부 계정에 연결해야 한다. '
        'OIDC에서는 발급자와 그 발급자가 부여한 사용자 식별자의 조합을 기준으로 외부 계정을 구분하고, 이를 내부 사용자 ID에 대응시킨다. '
        '표시 이름이나 이메일이 같다는 이유만으로 서로 다른 계정을 자동으로 합치지 않으며, 연결된 내부 ID를 기준으로 FoodMap의 제보와 사용자 기록을 유지한다.'),
    'social-session': (
        '외부 계정이 내부 사용자 ID에 연결되면 FoodMap은 앞서 배운 세션이나 토큰 방식으로 자신의 로그인 상태를 만들 수 있다. '
        '이후 FoodMap API 요청은 서비스가 받아들이는 로그인 자격으로 처리하고, 외부 제공자의 액세스 토큰은 필요한 외부 API 접근에 사용한다. '
        '이렇게 하면 비밀번호 로그인과 소셜 로그인 모두 확인된 내부 사용자 ID라는 공통 결과로 이어진다.'),

    'authorization': (
        '인가는 확인된 사용자가 특정 대상에 특정 행동을 해도 되는지 판단하는 과정이다. '
        '서버는 누가 요청했는지에 더해 무엇을 대상으로 어떤 작업을 하려는지 확인하고 서비스의 허용 규칙을 적용한다. '
        'FoodMap에 로그인했다는 사실만으로 모든 제보를 수정할 수 있는 것은 아니며, 사용자 확인 이후에 요청별 허용 여부를 판단해야 한다.'),
    'role-access': (
        '역할 기반 접근 제어는 사용자에게 역할을 부여하고 그 역할에 허용된 기능을 연결하는 방식이다. '
        'FoodMap의 일반 사용자는 제보 기능을 사용하고 운영자는 전체 제보 조회 같은 관리 기능을 사용하도록 범위를 정할 수 있다. '
        '역할에는 업무에 필요한 최소한의 권한을 부여하며, 역할 정보는 사용자가 요청에 임의로 적은 값이 아니라 서버가 신뢰하는 기록을 기준으로 확인한다.'),
    'owner-access': (
        '같은 역할을 가진 사용자라도 각자가 접근할 수 있는 데이터는 다를 수 있다. '
        '소유자 기반 접근 제어는 인증으로 확인한 사용자 ID와 대상 행에 저장된 소유자 ID를 비교해 허용 범위를 정한다. '
        'FoodMap에서는 자신의 제보만 조회하거나 수정하도록 정할 수 있으며, 제보를 저장할 때부터 서버가 확인한 사용자 ID를 소유자로 연결해야 이 판단의 근거가 유지된다.'),
    'default-deny': (
        '접근 정책에는 규칙이 없거나 판단에 필요한 정보가 부족할 때 어떻게 처리할지도 포함되어야 한다. '
        '기본 거부 정책은 명시적으로 허용된 조건을 충족하지 못한 요청을 거부하는 원칙이다. '
        'FoodMap에서는 알 수 없는 역할이나 확인되지 않은 소유 관계를 임의로 허용하지 않으며, 로그인 없이 가능한 맛집 공개 조회도 별도의 허용 규칙으로 표현한다.'),
    'api-access': (
        '접근 정책은 실제 데이터 처리를 수행하는 서버에서 요청마다 적용되어야 한다. '
        '서버는 로그인 자격을 검증해 사용자를 확인하고, 대상 데이터와 요청 행동에 대한 권한을 검사한 뒤 작업을 수행한다. '
        'FoodMap 화면에서 수정 버튼을 숨겼더라도 사용자가 API 요청을 직접 보낼 수 있으므로, 화면의 표시 조건과 서버의 인가 검사는 각각 자신의 역할을 맡는다.'),
    'rls': (
        '행 수준 보안인 RLS는 데이터베이스가 테이블의 개별 행에 접근 조건을 적용하는 기능이다. '
        '테이블의 기본 접근 권한에 더해 RLS 적용 대상 요청에 행 정책을 검사하며, 검증된 사용자 정보와 행의 소유자를 비교하는 규칙을 만들 수 있다. '
        'FoodMap의 자기 제보 조회 정책을 DB에서도 표현할 수 있지만, 정책이 판단에 필요한 사용자 정보를 전달받는 구조와 적용 범위를 함께 확인해야 한다.'),
    'api-keys': (
        'API 키는 애플리케이션이 API에 접근할 때 사용하는 자격정보로, 로그인한 개인의 신원과는 역할이 다르다. '
        'Supabase에서는 공개 가능한 키와 서버 전용 권한 키의 권한 범위가 다르며, 서버 전용 secret 키는 RLS를 우회할 수 있다. '
        'FoodMap 서버가 이런 키로 DB에 접근한다면 서버가 각 사용자의 요청을 먼저 인가해야 하고, 키를 브라우저에 노출해서는 안 된다.'),
    'foodmap-policy': (
        'FoodMap의 접근 정책은 사용자 종류, 요청 행동, 대상 데이터의 관계를 한 표에 모아 확인할 수 있다. '
        '공개 맛집 목록은 비로그인 사용자에게 허용하고, 개인 제보는 작성자에게 조회·수정을 허용하며, 전체 제보 조회는 운영자에게 허용하는 식으로 규칙을 정한다. '
        '각 규칙이 API와 적용 대상 DB 정책에서 어떻게 지켜지는지 확인하면 화면의 기능과 실제 데이터 접근 범위를 일치시킬 수 있다.'),

    'admin-system': (
        '관리자 시스템은 운영자가 서비스 전체를 관리하는 업무를 수행하도록 구성한 기능과 화면이다. '
        'FoodMap의 맛집 탐색·제보 기능은 이용자의 활동에 맞추고, 전체 제보 조회와 관리 기능은 운영자의 업무에 맞춰 구분한다. '
        '두 영역은 서버나 데이터베이스를 함께 사용할 수도 있지만, 진입 화면을 나누는 것과 별개로 관리 요청에는 운영자 권한을 적용해야 한다.'),
    'admin-boundary': (
        '운영자라는 이름이 모든 시스템의 권한을 한꺼번에 뜻하지는 않는다. '
        'FoodMap의 제보를 관리하는 권한과 DB 구조를 바꾸거나 배포 계정을 관리하는 권한은 서로 다른 대상에 대한 권한이다. '
        '관리자 시스템에는 해당 업무에 필요한 기능만 제공하고, 서비스 내부의 운영자 역할을 부여했다는 이유로 서버 전용 키나 클라우드 관리 권한까지 전달하지 않는다.'),
    'workflow-state': (
        '운영 업무는 처리 대상의 현재 상태와 그 상태에서 허용되는 변경으로 표현할 수 있다. '
        'FoodMap의 제보는 검토 대기에서 승인 또는 반려로 이동하도록 정하고, 서버는 운영자 권한과 현재 상태가 모두 조건에 맞는지 확인한 뒤 변경한다. '
        '이렇게 하면 버튼을 누르는 동작이 어떤 업무 결정을 뜻하는지 명확해지고, 이미 처리한 제보를 다시 처리할 수 있는지도 정책으로 정할 수 있다.'),
    'publication-state': (
        '검토 결과는 제보를 받아들였는지를 나타내고, 공개 상태는 콘텐츠를 일반 이용자에게 보여줄지를 나타낸다. '
        '두 상태를 구분하면 승인된 맛집이라도 정보 확인 중에는 비공개로 둘 수 있고, 문제가 발견되면 승인 이력을 유지한 채 노출만 중지할 수 있다. '
        '따라서 FoodMap의 공개 목록은 승인 여부만 확인하지 않고 서비스가 정한 공개 조건까지 만족하는 데이터를 대상으로 구성한다.'),
    'admin-transaction': (
        '하나의 운영 결정이 여러 데이터 변경을 요구할 때는 일부만 반영되는 상황을 막아야 한다. '
        '지난주에 배운 트랜잭션으로 제보의 승인 상태 변경과 맛집 데이터 등록을 같은 DB 작업에 묶으면 둘 다 성공하거나 둘 다 취소되게 할 수 있다. '
        '이 보장은 같은 트랜잭션 안의 변경에 적용되므로 브라우저 저장소와 서버 API를 따로 변경하는 동작까지 자동으로 묶어 주지는 않는다.'),
    'idempotency': (
        '트랜잭션으로 한 번의 처리를 일관되게 만들었더라도 같은 요청이 다시 도착하면 결과가 중복될 수 있다. '
        '멱등성은 같은 작업을 반복 요청해도 그 작업의 효과가 한 번 수행한 결과와 같도록 처리하는 성질이다. '
        'FoodMap의 승인 작업을 구분하는 식별자와 처리 결과를 서버에 기록하고 DB의 중복 제약 등을 함께 사용하면, 응답을 받지 못해 재전송해도 같은 맛집을 다시 만들지 않도록 설계할 수 있다.'),
    'audit-log': (
        '감사 로그는 운영 업무의 결과뿐 아니라 누가 어떤 대상을 언제 어떻게 처리했는지 남기는 기록이다. '
        'FoodMap의 제보 승인에는 운영자 ID, 제보 ID, 행동, 결과, 시각과 필요한 사유를 연결해 이후에 변경 경위를 확인할 수 있게 한다. '
        '이 기록에는 비밀번호나 토큰 원문을 넣지 않으며, 조회와 변경 권한도 제한해 운영 기록 자체가 임의로 훼손되지 않도록 관리한다.'),

    'input-validation': (
        '사용자와 권한을 확인한 요청이라도 그 안의 데이터가 서비스에서 처리할 수 있는 값인지는 따로 검증해야 한다. '
        '입력 검증은 서버가 필수 항목, 자료형, 길이와 허용 범위를 확인해 잘못된 값을 거부하는 절차다. '
        'FoodMap에서는 맛집 이름의 길이와 좌표 범위를 검사할 수 있으며, 브라우저의 입력 제한을 통과했다는 이유만으로 서버 검증을 생략하지 않는다.'),
    'sql-injection': (
        'SQL 인젝션은 입력 데이터가 SQL 명령문의 일부로 해석되어 원래 의도와 다른 조회나 변경을 유발하는 문제다. '
        'FoodMap의 검색어를 SQL 문자열에 직접 이어 붙이면 데이터와 명령의 경계가 흐려질 수 있다. '
        '매개변수화된 쿼리는 명령의 구조와 입력값을 분리해 값을 데이터로 처리하게 하므로, 입력 형식을 검사하는 것과 함께 DB 접근 경로에서 적용해야 한다.'),
    'xss': (
        '사용자 입력이 명령으로 해석되는 문제는 데이터베이스뿐 아니라 브라우저 화면에서도 발생한다. '
        'XSS는 공격자가 넣은 내용이 웹 페이지의 실행 코드로 처리되어 사용자의 브라우저에서 서비스의 기능에 영향을 주는 공격이다. '
        'FoodMap의 제보 설명은 기본적으로 텍스트로 출력하고, HTML을 허용할 필요가 있다면 허용 요소를 제한하는 정제 과정을 적용해 입력 내용과 실행 코드를 구분해야 한다.'),
    'origin': (
        '브라우저에서 실행되는 코드의 접근 범위를 이해하려면 먼저 웹 출처를 구분해야 한다. '
        '출처는 URL의 프로토콜, 호스트, 포트의 조합으로 정해지며, 경로가 달라도 이 조합이 같으면 같은 출처다. '
        'FoodMap 화면과 API가 서로 다른 호스트나 포트에서 제공되면 다른 출처가 되므로, 같은 서비스가 운영한다는 사실과 브라우저의 경계 판단은 별개다.'),
    'site': (
        '브라우저는 출처와 함께 사이트라는 더 넓은 경계도 사용한다. '
        '쿠키 정책에서 사용하는 사이트는 프로토콜과 등록 가능한 도메인을 기준으로 구분하므로, HTTPS의 app.example.com과 api.example.com은 출처가 다르지만 같은 사이트다. '
        '등록 가능한 도메인은 example.com이나 example.co.kr 같은 단위이며, 포트와 하위 도메인의 차이가 출처와 사이트 판정에서 다르게 반영된다는 점을 구분해야 한다.'),
    'same-origin-policy': (
        '동일 출처 정책은 한 출처에서 실행되는 스크립트가 다른 출처의 자원을 읽거나 조작하는 범위를 제한하는 브라우저의 보안 원칙이다. '
        '다른 사이트에서 실행한 코드가 사용자의 FoodMap 응답을 마음대로 읽지 못하게 하는 것이 대표적인 역할이다. '
        '다만 다른 출처로 보내는 모든 요청을 막는 것은 아니므로, 응답을 읽을 수 있는지와 요청이 서버에 도착할 수 있는지는 구분해야 한다.'),
    'cors': (
        'FoodMap 화면과 API의 출처가 다르면 서버가 허용한 범위에서 브라우저가 응답을 읽을 수 있도록 CORS를 설정할 수 있다. '
        '서버는 허용할 출처 등을 응답 헤더로 알리고 브라우저가 그 조건을 적용하며, 일부 요청은 실제 요청 전에 허용 여부를 먼저 확인한다. '
        'CORS는 브라우저의 교차 출처 접근 규칙이므로 API에 직접 보내는 요청의 사용자 인증이나 권한 검사를 대신하지 않는다.'),
    'csrf': (
        '응답을 읽지 못해도 요청을 보낼 수 있다는 점은 로그인된 브라우저에서 중요한 문제가 된다. '
        'CSRF는 다른 페이지가 사용자의 의도와 다른 요청을 유발하고, 브라우저가 조건에 따라 자동 첨부한 로그인 쿠키를 서버가 받아들이는 상황을 악용한다. '
        'FoodMap의 관리 요청에는 허용된 요청 출처와 공격자가 알 수 없는 확인값을 검증하는 방어 등을 적용해, 로그인 자격이 있다는 사실에 더해 허용된 경로의 요청인지 확인한다.'),
    'cookie-protection': (
        '쿠키 보호 속성은 이미 배운 전송 경계와 공격 경로에 맞춰 쿠키의 사용 범위를 제한한다. '
        'Secure는 HTTPS 전송으로, HttpOnly는 스크립트의 쿠키 읽기 접근 제한으로, SameSite는 사이트 관계에 따른 쿠키 첨부 제한으로 작동한다. '
        '각 속성은 보호하는 범위가 다르므로 HttpOnly가 페이지 안의 모든 악성 동작을 막거나 SameSite만으로 모든 요청 위조를 해결한다고 판단하지 않는다.'),
    'login-rate-limit': (
        '브라우저 경계와 쿠키를 보호하더라도 공격자가 로그인 API에 비밀번호를 반복해서 제출하는 시도는 별도로 통제해야 한다. '
        '로그인 시도 제한은 계정과 요청 출처 등의 기준으로 일정 시간의 실패 횟수나 요청 속도를 관찰하고 지연 또는 제한을 적용하는 방식이다. '
        'FoodMap에서는 정상 사용자의 재시도 여지를 두면서 자동 추측 비용을 높이고, 공격자가 타인의 계정을 계속 잠그는 방식으로 제한을 악용하지 못하도록 기준을 정한다.'),

    'environments': (
        '보안 기능을 갖춘 서비스도 개발 중인 변경이 실제 사용자에게 바로 영향을 주면 안정적으로 운영하기 어렵다. '
        '개발 환경은 변경을 만드는 공간, 검증 환경은 배포 전에 동작을 확인하는 공간, 운영 환경은 실제 사용자에게 서비스를 제공하는 공간으로 구분한다. '
        '각 환경 안에 사용자 화면과 관리자 화면이 함께 있을 수 있으므로, 업무에 따른 기능 분리와 실행 목적에 따른 환경 분리는 서로 다른 기준이다.'),
    'environment-config': (
        '환경을 나누어도 애플리케이션 코드는 공통으로 유지하고 실행에 필요한 설정을 환경별로 달리할 수 있다. '
        'FoodMap의 API 주소, DB 연결 대상, 외부 로그인 복귀 주소와 사용하는 자격정보를 설정으로 분리하면 같은 코드가 각 환경의 구성 요소에 연결된다. '
        '환경 변수는 이런 값을 전달하는 한 방법이며, 어떤 값이 브라우저에 전달되고 어떤 값이 서버에서만 사용되는지도 구분해야 한다.'),
    'secret-management': (
        '환경별 설정 중 서버 전용 키와 같은 비밀정보는 보관 장소와 전달 경로를 제한해야 한다. '
        '환경 변수에 넣었더라도 브라우저용 코드에 포함되어 배포되면 사용자가 읽을 수 있으므로, 비밀정보는 서버에서 관리하고 저장소와 로그에 남기지 않는다. '
        '키가 유출되면 해당 키를 폐기하고 새 키를 적용해야 하며, 공개된 파일에서 문자열만 삭제해도 이전 키의 효력이 사라지는 것은 아니다.'),
    'environment-data': (
        '서로 다른 주소로 실행되는 서비스가 같은 데이터베이스에 연결되어 있다면 개발 작업이 운영 데이터에 영향을 줄 수 있다. '
        '환경별 데이터 분리는 저장소와 접근 자격을 구분해 개발·검증 작업이 운영 데이터에 닿지 않도록 하는 구성이다. '
        'FoodMap의 테스트 제보 초기화는 테스트 DB에서만 수행되도록 만들고, 환경을 전환할 때 실제 연결 대상도 함께 확인해야 한다.'),
    'deployment': (
        '서비스 배포는 검증한 코드와 대상 환경의 설정을 실제 실행 환경에 반영하는 과정이다. '
        'FoodMap은 검증 환경에서 로그인과 데이터 조회, 관리 기능을 확인한 뒤 운영 환경에 해당 버전을 적용한다. '
        '배포 후에도 적용된 버전과 연결 대상을 확인하고 주요 요청이 정상 처리되는지 살펴야 하며, 서버 프로세스가 실행 중이라는 사실만으로 서비스 전체의 정상 동작을 판단하지 않는다.'),
    'db-migration': (
        '서비스 변경이 새 열이나 제약조건을 요구하면 코드 배포와 함께 데이터베이스 구조의 변경도 관리해야 한다. '
        '마이그레이션은 이런 변경을 순서와 이력이 있는 작업으로 남겨 각 환경에 일관되게 적용하는 방식이다. '
        'FoodMap에 제보 처리 상태 열을 추가한다면 기존 행의 값을 어떻게 채울지와 이전 코드가 변경된 구조에서도 동작하는지를 확인하고, 그 조건에 맞춰 DB 변경과 앱 배포의 실행 순서를 정한다.'),
    'monitoring': (
        '배포와 DB 변경이 끝난 뒤에는 서비스가 실제로 어떻게 동작하는지 지속적으로 관찰해야 한다. '
        '운영 모니터링은 오류 기록과 응답 시간, 실패율 같은 지표를 모아 정상 상태의 변화와 장애 징후를 파악하는 활동이다. '
        'FoodMap에서는 로그인 실패 증가나 DB 연결 오류를 확인할 수 있으며, 운영자의 변경 경위를 남기는 감사 로그와 함께 보되 각 기록의 목적은 구분한다.'),
    'backup': (
        '운영 상태를 관찰해 문제를 발견하더라도 이미 삭제되거나 손상된 데이터가 저절로 돌아오지는 않는다. '
        '백업은 이런 상황에 대비해 특정 시점의 데이터를 별도 사본으로 보관하는 준비이며, 보관 주기와 기간, 접근 권한과 복원 가능성을 함께 관리한다. '
        'FoodMap은 어느 시점까지의 데이터를 확보하는지와 그 이후 얼마나 잃을 수 있는지 정하고, 사본이 존재한다는 사실에 더해 실제로 사용할 수 있는 상태인지 확인해야 한다.'),
    'rollback': (
        '배포한 코드나 설정이 장애의 원인이라면 이전에 동작하던 버전으로 되돌리는 롤백을 고려할 수 있다. '
        'FoodMap 서버를 이전 버전으로 바꾸기 전에는 이미 적용한 DB 구조와 그 버전이 호환되는지 확인해야 한다. '
        '코드를 되돌리는 동작이 변경된 DB 구조나 삭제된 데이터까지 자동으로 되돌리지는 않으므로, 장애 원인과 되돌릴 대상을 구분해 대응한다.'),
    'restore': (
        '장애의 대상이 데이터라면 확보한 백업을 이용해 필요한 상태를 되살리는 복원 절차가 필요하다. '
        '복원할 시점을 정하고 격리된 환경에서 데이터와 서비스 동작을 확인한 뒤 반영 범위를 결정하며, 그 시점 이후에 발생한 정상 변경을 어떻게 보존할지도 검토한다. '
        'FoodMap의 잘못 삭제된 제보를 복구하는 사례를 통해, 이전 코드로 돌아가는 대응과 데이터 자체를 되살리는 대응을 구분한다.'),
}


CHAPTER_REVIEW = {
    1: dict(
        assessment='순서 유지. 저장된 데이터 → 지속적인 사용자 식별 → 입력 주장의 한계 → 증거 검증 → 안전한 검증 정보 저장 → 로그인 흐름으로 연결된다.',
        boundary='1.7은 현재 요청의 사용자 확인에서 끝낸다. 로그인 유지 수단을 끌어오지 않아 2.1의 필요성이 남는다.',
        caution='계정 인증을 실제 인물의 실명 확인과 동일하게 설명하지 않는다. 해시·솔트의 수학이나 구현 세부는 이번 문단 범위 밖이다.'),
    2: dict(
        assessment='순서 유지, 2.3→2.4 연결 보강. 세션 식별자를 토큰의 한 형태로 설명한 뒤 정보가 들어 있는 토큰과 서명의 필요성으로 확장한다.',
        boundary='2.6은 JWT 구성 요소와 필드의 뜻, 2.7은 수용 조건, 2.8은 인증 방식 전반의 수명 관리로 역할을 나눴다.',
        caution='쿠키·세션·JWT를 서로 배타적인 세 방식으로 비교하지 않는다. 토큰 수명·갱신·철회도 한 장에서 모두 설명하지 않는다.'),
    3: dict(
        assessment='순서 유지, 3.1→3.2와 3.3→3.4 연결 보강. 외부 API 접근 위임의 목적을 먼저 한정하고 OIDC의 신원 확인 목적을 추가한 뒤 코드 교환 절차를 설명한다.',
        boundary='state와 PKCE는 시작한 요청과 복귀·교환을 묶는 역할까지 다룬다. CSRF 공격의 이름과 전체 방어 구조는 6.8에서 연결한다.',
        caution='새 용어 밀도가 가장 높은 챕터다. 3.4~3.6은 같은 흐름도를 단계적으로 확장하고, 제공자별 설정·암호 계산·모든 소셜 로그인이 OIDC라는 일반화를 피한다.'),
    4: dict(
        assessment='순서 유지. 누구인지 확인한 결과 → 요청 허용 기준 → 역할과 소유 관계 → 기본값 → 검사 위치 → 실제 접근 경로 → 정책 통합으로 이어진다.',
        boundary='RLS의 일반 역할을 배운 뒤 API 키에 따른 우회 범위를 설명한다. 4.8에는 아직 배우지 않은 제보 상태나 공개 상태 조건을 넣지 않았다.',
        caution='7주차의 Auth·RLS 소개를 이번 내부 동작 학습의 대체물로 보지 않는다. RLS가 활성화되어 있으면 모든 연결이 자동으로 제한된다는 인상을 주지 않는다.'),
    5: dict(
        assessment='순서 유지. 관리할 기능과 권한 → 상태로 표현한 업무 → 공개 조건 → 한 번의 변경 일관성 → 반복 요청의 효과 → 변경 경위 기록으로 연결된다.',
        boundary='승인과 공개, 트랜잭션과 멱등성의 역할을 분리했다. 전자는 검토 결과와 노출, 후자는 한 처리의 전부 반영과 같은 요청의 반복을 각각 다룬다.',
        caution='이론상 제보 관리 모델이며 현재 실습에 모두 구현되었다는 뜻이 아니다. 트랜잭션만으로 중복·동시성 문제가 해결된다고 설명하지 않는다.'),
    6: dict(
        assessment='순서 유지, 6.3→6.4와 6.9→6.10 연결 보강. 입력이 명령으로 해석되는 공격에서 브라우저 코드의 접근 경계로 이동하고, 마지막에 로그인 API 자체의 반복 요청 통제로 확장한다.',
        boundary='출처·사이트의 정의를 먼저 확보한 뒤 동일 출처 정책·CORS·CSRF·쿠키 속성을 설명한다. 2장의 쿠키 자동 첨부와 5장의 관리 요청을 다시 사례로 사용한다.',
        caution='보안 용어를 각각 외우는 목록이 되지 않도록 검색 입력·제보 표시·관리 요청 세 경로를 재사용한다. CORS를 요청 전체 차단 장치로, 쿠키 속성을 단독 해결책으로 설명하지 않는다.'),
    7: dict(
        assessment='순서 유지. 실제 사용자 보호라는 목적 → 환경과 설정 → 비밀정보와 데이터 경계 → 배포와 구조 변경 → 관찰 → 복구 준비와 대응으로 이어진다.',
        boundary='7.5의 배포 사례는 DB 구조를 유지하는 변경으로 한정한 뒤, 7.6에서 구조 변경이 필요한 경우를 추가한다. 설명 순서가 DB 변경과 앱 배포의 고정 실행 순서를 뜻하지는 않는다.',
        caution='백업 장에서는 사본과 보관 기준까지, 복원 장에서는 적용 시점·검증·정상 변경 보존까지 다룬다. 코드 롤백을 데이터 복원과 동일하게 설명하지 않는다.'),
}

FLOW_FINDINGS = [
    dict(slides=['2.3', '2.4', '2.5'],
         issue='세션 다음에 토큰을 별도 방식으로 소개하면 세션 식별자는 토큰이 아니거나 토큰은 항상 서버 상태가 없다는 오해가 생길 수 있음.',
         resolution='2.4에서 세션 식별자를 토큰의 한 형태로 포함하고, 내부 정보를 담는 토큰에서 2.5의 변조 검증 필요성을 도출.',
         status='문단에 반영'),
    dict(slides=['2.6', '2.7', '2.8', '2.9', '2.10'],
         issue='JWT의 구조·만료·갱신·철회가 중복되거나 뒤의 개념을 앞당겨 설명할 가능성.',
         resolution='필드의 의미 → 검증 조건 → 수명 제한 → 갱신 자격 → 종료 방식으로 구분. 2.9의 선행 철회 설명 제거.',
         status='문단에 반영'),
    dict(slides=['3.1', '3.2', '3.3', '4.1'],
         issue='소셜 로그인 도입 직후 OAuth의 접근 위임으로 이동할 때 목적이 바뀌며, 4장의 서비스 인가를 먼저 알아야 하는 것처럼 보일 수 있음.',
         resolution='3.2에서 외부 API에 대한 위임·scope를 직접 정의하고, 3.3에서 신원 확인 규칙을 추가. 내부 역할·소유 정책은 4장에 유지.',
         status='문단에 반영'),
    dict(slides=['3.4', '3.5', '3.6', '6.8'],
         issue='코드 흐름에 모든 보호값을 처음부터 넣으면 state·PKCE·CSRF를 배우기 전에 이해해야 함.',
         resolution='기본 교환 관계를 먼저 설명한 뒤 state와 PKCE가 보호하는 연결을 추가. 공격 분류명은 6.8에서 제시.',
         status='문단에 반영; 본문 도식에도 같은 순서 적용'),
    dict(slides=['4.6', '4.7', '4.8', '5.3', '5.4'],
         issue='RLS 정책이나 최종 접근 표에 secret 키의 권한·승인 상태·공개 상태가 선행 등장할 가능성.',
         resolution='4.6은 적용 대상 요청의 행 정책, 4.7은 키의 적용 범위, 4.8은 역할·소유 관계로 한정. 상태 조건은 5장에서 확장.',
         status='문단에 반영'),
    dict(slides=['5.5', '5.6'],
         issue='한 작업의 원자적 처리와 여러 번 도착한 요청의 중복 방지를 같은 효과로 설명할 가능성.',
         resolution='한 번의 처리 중 일부 실패와 처리 완료 후 같은 요청 재전송을 서로 다른 사례로 분리.',
         status='문단에 반영'),
    dict(slides=['6.3', '6.4', '6.5', '6.6', '6.7', '6.8'],
         issue='입력 공격 설명에서 주소 구성과 브라우저 정책으로 넘어갈 때 개념 목록처럼 보이는 전환.',
         resolution='브라우저에서 실행되는 코드의 접근 범위라는 연결을 6.4에 추가. 읽기 제한과 요청 전송의 차이를 6.6에서 설명해 CSRF에 연결.',
         status='문단에 반영'),
    dict(slides=['7.5', '7.6', '7.8', '7.9', '7.10'],
         issue='배포 설명이 마이그레이션을 전제로 삼거나, 백업·롤백 장이 복원 절차까지 먼저 설명할 가능성.',
         resolution='7.5는 코드·설정 반영, 7.6은 스키마 변경을 동반한 확장 사례. 백업은 사본 확보, 롤백은 코드·설정, 복원은 데이터 처리로 분리.',
         status='문단에 반영'),
]

REFERENCES = {
    'password': ('OWASP Password Storage', 'https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html'),
    'session': ('OWASP Session Management', 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'),
    'jwt': ('JWT', 'https://www.rfc-editor.org/rfc/rfc7519.html'),
    'jwt-validation': ('JWT Best Current Practices', 'https://www.rfc-editor.org/rfc/rfc8725.html'),
    'signout': ('Supabase Signing out', 'https://supabase.com/docs/guides/auth/signout'),
    'oauth': ('OAuth 2.0', 'https://www.rfc-editor.org/rfc/rfc6749.html'),
    'oidc': ('OpenID Connect Core', 'https://openid.net/specs/openid-connect-core-1_0.html'),
    'oauth-security': ('OAuth Security Best Current Practice', 'https://www.rfc-editor.org/rfc/rfc9700.html'),
    'pkce': ('PKCE', 'https://www.rfc-editor.org/rfc/rfc7636.html'),
    'authorization': ('OWASP Authorization', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'),
    'rls': ('Supabase Row Level Security', 'https://supabase.com/docs/guides/database/postgres/row-level-security'),
    'api-keys': ('Supabase API keys', 'https://supabase.com/docs/guides/getting-started/api-keys'),
    'transactions': ('PostgreSQL Transactions', 'https://www.postgresql.org/docs/current/tutorial-transactions.html'),
    'logging': ('OWASP Logging', 'https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html'),
    'sql-injection': ('OWASP SQL Injection Prevention', 'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'),
    'xss': ('OWASP Cross Site Scripting Prevention', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'),
    'origin': ('MDN Origin', 'https://developer.mozilla.org/en-US/docs/Glossary/Origin'),
    'site': ('MDN Site', 'https://developer.mozilla.org/en-US/docs/Glossary/Site'),
    'same-origin': ('MDN Same-origin policy', 'https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy'),
    'cors': ('MDN CORS', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS'),
    'csrf': ('OWASP CSRF Prevention', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html'),
    'authentication': ('OWASP Authentication', 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html'),
    'environments': ('Supabase Managing Environments', 'https://supabase.com/docs/guides/deployment/managing-environments'),
    'client-config': ('Vite Env Variables and Modes', 'https://vite.dev/guide/env-and-mode'),
    'backup': ('PostgreSQL Backup and Restore', 'https://www.postgresql.org/docs/current/backup.html'),
}

CHAPTER_SOURCES = {
    1: ['password', 'authentication'],
    2: ['session', 'jwt', 'jwt-validation', 'signout'],
    3: ['oauth', 'oidc', 'oauth-security', 'pkce'],
    4: ['authorization', 'rls', 'api-keys'],
    5: ['authorization', 'transactions', 'logging'],
    6: ['sql-injection', 'xss', 'origin', 'site', 'same-origin', 'cors', 'csrf', 'session', 'authentication'],
    7: ['environments', 'client-config', 'backup'],
}


def document():
    outline = proposal()
    expected = [item['id'] for chapter in outline['chapters'] for item in chapter['concepts']]
    assert list(PARAGRAPHS) == expected, 'Paragraph IDs/order differ from the title outline'
    assert set(CHAPTER_REVIEW) == set(CHAPTER_SOURCES) == {chapter['number'] for chapter in outline['chapters']}
    for ident, paragraph in PARAGRAPHS.items():
        assert paragraph.strip() and '\n' not in paragraph, f'{ident} must be one paragraph'
    chapters = []
    for chapter in outline['chapters']:
        rows = [dict(**item, paragraph_ko=PARAGRAPHS[item['id']]) for item in chapter['concepts']]
        sources = [dict(label=REFERENCES[key][0], url=REFERENCES[key][1])
                   for key in CHAPTER_SOURCES[chapter['number']]]
        chapters.append(dict(number=chapter['number'], title=chapter['title'], lead=chapter['lead'],
                             slides=rows, review=CHAPTER_REVIEW[chapter['number']], sources=sources))
    return dict(stage='paragraph-flow-review', language='ko',
                note='검토용 문단 초안. 현재 실습의 구현 상태를 설명하거나 발표용 본문을 렌더링한 결과가 아님.',
                body_slide_count=len(expected), current_deck_slide_count=len(expected) + 8,
                chapters=chapters, flow_findings=FLOW_FINDINGS)


def outputs(root):
    data = document()
    lines = [
        '8주차 · 슬라이드별 한 문단 원고와 흐름 검토', '',
        '7개 챕터 · 본문 60장 · 제목 설계안과 같은 순서',
        '각 문단은 개념·관계·사례를 읽으며 학습 순서를 평가하기 위한 한국어 검토 원고.',
        '문단을 정의·설명·도식으로 구성한 완성 본문은 week-08-body.ko.txt와 slide-bodies.json에서 확인.',
        'FoodMap은 이론 설명을 위한 확장 설계 사례. 현재 실습에 모든 기능이 구현되었다는 뜻이 아님.',
        '현재 HTML은 표지·챕터를 포함한 68장으로, 본문 60장에 한영 설명과 자료를 반영. 문단 원고의 번호는 챕터 내부 설계 번호.',
        '작성 원본: ../scripts/paragraph_outline.py / 제목 원본: ../scripts/title_outline.py', '',
    ]
    for chapter in data['chapters']:
        lines.extend([f'{chapter["number"]:02}. {chapter["title"][0]}', chapter['lead'][0], ''])
        for slide in chapter['slides']:
            lines.extend([f'{slide["outline_number"]} {slide["title"][0]}',
                          f'서브타이틀: {slide["lead"][0]}', '', slide['paragraph_ko'], ''])
        review = chapter['review']
        lines.extend(['챕터 흐름 평가', review['assessment'], review['boundary'], review['caution'], '',
                      '내용 확인 출처'])
        lines.extend(f'- {source["label"]}: {source["url"]}' for source in chapter['sources'])
        lines.append('')
    lines.extend(['전체 흐름 검토 기록', ''])
    for finding in FLOW_FINDINGS:
        lines.extend([f'검토 위치: {" → ".join(finding["slides"])}', f'문제: {finding["issue"]}',
                      f'조정: {finding["resolution"]}', f'상태: {finding["status"]}', ''])
    lines.extend([
        '검토 범위: 제목과 문단의 순서·선수 개념·사례 연결을 수동 검토. 자동 확인은 60장 대응·순서·단일 문단 형식·재생성 일치만 확인.',
        '본문 제작 시 남은 검토: 실제 도식의 라벨·예제 코드·설정값이 새 선수 개념을 요구하는지 재검토. 3장과 6장은 용어 밀도가 높아 같은 사례를 단계적으로 확장.',
    ])
    return {
        root / 'materials/paragraph-outline.json': json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        root / 'materials/week-08-paragraphs.ko.txt': '\n'.join(lines) + '\n',
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
    print(f'Week 8 paragraph draft: {len(PARAGRAPHS)} paragraphs in title order, {len(CHAPTER_REVIEW)} chapter reviews.')
