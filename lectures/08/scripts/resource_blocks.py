"""Editable Week 6-derived diagrams and screen excerpts for the Week 8 deck.

All visible strings use the shared translation binding. The original raster
files stay untouched in the audit; these are teaching adaptations, not photos
of an implemented FoodMap application.
"""


def render_resource(item, key, tr):
    kind = item['kind']
    if kind == 'table':
        head = ''.join(tr(f'{key}_h{i}', cell, 'th', attrs=' scope="col"')
                       for i, cell in enumerate(item['head']))
        rows = []
        for i, row in enumerate(item['rows']):
            assert len(row) == len(item['head']), key
            rows.append('<tr>' + ''.join(
                tr(f'{key}_r{i}_{j}', cell, 'th' if j == 0 else 'td',
                   attrs=' scope="row"' if j == 0 else '')
                for j, cell in enumerate(row)) + '</tr>')
        return '<table class="wd-lesson-table"><thead><tr>' + head + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
    if kind == 'resource-row':
        parts = ['<div class="w8-resource-row">']
        for i, column in enumerate(item['columns']):
            parts.append('<div class="w8-resource-column">')
            for j, child in enumerate(column):
                markup = render_resource(child, f'{key}_{i}_{j}', tr)
                assert markup is not None, child['kind']
                parts.append(markup)
            parts.append('</div>')
        return '\n'.join(parts + ['</div>'])
    if kind == 'resource-note':
        return tr(key, item['text'], 'p', 'w8-caption w8-resource-note')
    if kind == 'resource-branches':
        parts = ['<figure class="w8-branches"><div class="w8-branch-root">',
                 tr(key+'_title', item['title'], 'strong'),
                 tr(key+'_body', item['body']), '</div><div class="w8-branch-children">']
        for i, child in enumerate(item['children']):
            parts += ['<div class="w8-branch-child">',
                      tr(f'{key}_{i}_title', child['title'], 'strong'),
                      tr(f'{key}_{i}_body', child['body']), '</div>']
        return '\n'.join(parts + ['</div>', tr(key+'_caption', item['caption'], 'figcaption', 'w8-caption'), '</figure>'])
    if kind == 'resource-timeline':
        parts = ['<figure class="w8-timeline"><ol>']
        for i, event in enumerate(item['events']):
            parts += ['<li>', tr(f'{key}_{i}_time', event['time'], 'p', 'w8-time'),
                      tr(f'{key}_{i}_title', event['title'], 'strong'),
                      tr(f'{key}_{i}_detail', event['detail']), '</li>']
        parts.append('</ol>')
        if item.get('caption'):
            parts.append(tr(key+'_caption', item['caption'], 'figcaption', 'w8-caption'))
        return '\n'.join(parts + ['</figure>'])
    if kind == 'resource-workspaces':
        parts = ['<figure class="w8-workspaces"><div class="w8-workspace-panes">']
        for i, pane in enumerate(item['panes']):
            parts += ['<div class="w8-workspace">', tr(f'{key}_{i}_title', pane['title'], 'p', 'w8-workspace-title'),
                      tr(f'{key}_{i}_role', pane['role'], 'p', 'w8-workspace-role'), '<ul>']
            parts += [tr(f'{key}_{i}_row{j}', row, 'li') for j, row in enumerate(pane['rows'])]
            parts += ['</ul></div>']
        return '\n'.join(parts + ['</div>', tr(key+'_caption', item['caption'], 'figcaption', 'w8-caption'), '</figure>'])
    if kind == 'resource-transaction':
        parts = ['<figure class="w8-transaction"><div class="w8-transaction-scope">',
                 tr(key+'_scope', ('같은 DB 트랜잭션', 'One database transaction'), 'p', 'w8-scope-title'), '<ol>']
        parts += [tr(f'{key}_op{i}', op, 'li') for i, op in enumerate(item['operations'])]
        parts += ['</ol></div><div class="w8-transaction-results">']
        for i, (title, result) in enumerate(item['results']):
            parts += ['<div>', tr(f'{key}_{i}_title', title, 'strong'), tr(f'{key}_{i}_result', result), '</div>']
        return '\n'.join(parts + ['</div></figure>'])
    if kind == 'resource-environments':
        parts = ['<figure class="w8-environments">']
        for i, (title, purpose, db) in enumerate([
            (('개발', 'Development'), ('변경을 만드는 공간', 'Create changes'), 'dev_db'),
            (('검증', 'Staging'), ('배포 전에 확인하는 공간', 'Verify before deployment'), 'stage_db'),
            (('운영', 'Production'), ('실제 사용자에게 제공', 'Serve real users'), 'prod_db'),
        ]):
            parts += ['<div class="w8-environment">', tr(f'{key}_{i}_title', title, 'p', 'w8-environment-title'),
                      tr(f'{key}_{i}_purpose', purpose, 'p', 'w8-environment-purpose'),
                      '<div class="w8-environment-ui">',
                      tr(f'{key}_{i}_user', ('사용자 화면', 'User interface')),
                      tr(f'{key}_{i}_admin', ('관리자 화면', 'Admin interface')), '</div>']
            if item['database']:
                parts += ['<div class="w8-environment-server">',
                          tr(f'{key}_{i}_server', ('해당 환경의 서버', 'Server for this environment')), '</div>',
                          '<div class="w8-environment-db">', tr(f'{key}_{i}_db', (db, db), 'strong'),
                          tr(f'{key}_{i}_credentials', ('전용 접근 자격', 'Dedicated credentials')), '</div>']
            parts += ['</div>']
        return '\n'.join(parts + ['</figure>'])
    if kind == 'resource-metrics':
        parts = ['<figure class="w8-metrics">']
        for i, series in enumerate(item['series']):
            parts += ['<div class="w8-metric">', tr(f'{key}_{i}_title', series['title'], 'p', 'w8-metric-title'),
                      tr(f'{key}_{i}_range', (f'0–{series["max"]} {series["unit"]}',)*2, 'p', 'w8-metric-range'),
                      '<div class="w8-bars">']
            for j, value in enumerate(series['values']):
                height = value / series['max'] * 100
                deploy = ' w8-bar--deploy' if j == item['deploy_index'] else ''
                parts += [f'<div class="w8-bar-column{deploy}"><div class="w8-bar-track">',
                          f'<div class="w8-bar" style="height:{height:g}%">',
                          tr(f'{key}_{i}_{j}_value', (str(value),)*2, 'span', 'w8-bar-value'), '</div></div>',
                          tr(f'{key}_{i}_{j}_time', (item['times'][j],)*2, 'p', 'w8-bar-time'), '</div>']
            parts += ['</div></div>']
        return '\n'.join(parts + ['</figure>'])
    if kind == 'login-screen':
        social = item.get('social', False)
        parts = ['<figure class="w8-login-example"><div class="w8-login-screen">',
                 tr(key + '_heading', ('로그인', 'Log in'), 'p', 'w8-login-heading')]
        if social:
            for i, pair in enumerate([('Google로 로그인', 'Continue with Google'),
                                      ('네이버로 로그인', 'Continue with Naver')]):
                parts.append(tr(f'{key}_provider{i}', pair, 'p', 'w8-provider-choice'))
        else:
            for i, (label, value) in enumerate([
                (('이메일', 'Email'), (item.get('email', 'student@example.com'),) * 2),
                (('비밀번호', 'Password'), ('••••••••',) * 2),
            ]):
                parts.append(tr(f'{key}_field{i}', label, 'p', 'w8-input-label'))
                parts.append(tr(f'{key}_value{i}', value, 'p', 'w8-input-value'))
            parts.append(tr(key + '_submit', ('로그인', 'Log in'), 'p', 'w8-login-submit'))
        parts.append('</div>')
        parts.append(tr(key + '_caption', item['caption'], 'figcaption', 'w8-caption'))
        return '\n'.join(parts + ['</figure>'])

    if kind == 'resource-flow':
        parts = ['<figure class="w8-flow"><ol>']
        for i, step in enumerate(item['items']):
            parts += ['<li>', tr(f'{key}_{i}_title', step['title'], 'strong'),
                      tr(f'{key}_{i}_body', step['body']), '</li>']
        return '\n'.join(parts + ['</ol>', tr(key + '_caption', item['caption'], 'figcaption', 'w8-caption'), '</figure>'])

    if kind != 'resource-sequence':
        return None
    actors, rows = item['actors'], item['rows']
    count = len(actors)
    assert 2 <= count <= 4
    position = lambda index: 10 + index * 80 / (count - 1)
    parts = [f'<figure class="w8-sequence" data-actors="{count}">', '<div class="w8-actors">']
    for i, actor in enumerate(actors):
        parts.append(tr(f'{key}_actor{i}', actor, 'p', 'w8-actor', f' style="left:{position(i):g}%"'))
    parts.append('</div><div class="w8-sequence-track">')
    for i in range(count):
        parts.append(f'<div class="w8-lifeline" style="left:{position(i):g}%" aria-hidden="true"></div>')
    parts.append('<ol class="w8-messages">')
    for i, row in enumerate(rows):
        if row.get('phase'):
            parts.append(tr(f'{key}_phase{i}', row['phase'], 'li', 'w8-sequence-phase'))
        start, end = row['from'], row['to']
        assert 0 <= start < count and 0 <= end < count
        note = start == end
        route = tuple(actors[start][lang] if note else actors[start][lang] + ' → ' + actors[end][lang] for lang in range(2))
        focus = ' w8-message--focus' if row.get('focus') else ''
        parts.append('<li>')
        parts.append(tr(f'{key}_route{i}', route, 'p', 'w8-mobile-route'))
        if note:
            anchor = 'left:0' if start == 0 else 'right:0' if start == count - 1 else 'left:33%'
            width = 44 if count == 2 else 34
            cls = 'w8-local' + focus
            parts.append(tr(f'{key}_row{i}', row['text'], 'p', cls, f' style="{anchor};width:{width}%"'))
        else:
            left = min(position(start), position(end))
            width = abs(position(start) - position(end))
            direction = 'right' if end > start else 'left'
            reply = ' w8-message--reply' if row.get('reply') else ''
            parts.append(f'<div class="w8-message w8-message--{direction}{focus}{reply}" style="left:{left:g}%;width:{width:g}%">')
            parts.append(tr(f'{key}_row{i}', row['text'], 'p', 'w8-message-text'))
            parts.append('<span class="w8-message-line" aria-hidden="true"></span></div>')
        parts.append('</li>')
    parts += ['</ol></div>', tr(key + '_caption', item['caption'], 'figcaption', 'w8-caption'), '</figure>']
    return '\n'.join(parts)
