"""Editable diagrams, flow charts, sequence diagrams, and notes for Week 10."""

import html
from pathlib import Path

_WEEK10_ROOT = Path(__file__).resolve().parent.parent


def render_resource(item, key, tr):
    kind = item['kind']
    if kind == 'resource-row':
        parts = ['<div class="w10-resource-row">']
        for i, column in enumerate(item['columns']):
            parts.append('<div class="w10-resource-column">')
            for j, child in enumerate(column):
                markup = render_resource(child, f'{key}_{i}_{j}', tr)
                assert markup is not None, child['kind']
                parts.append(markup)
            parts.append('</div>')
        return '\n'.join(parts + ['</div>'])

    if kind == 'resource-note':
        return tr(key, item['text'], 'p', 'w10-caption w10-resource-note')

    if kind == 'resource-evidence':
        src = item['src']
        assert (_WEEK10_ROOT / src).is_file(), src
        href = html.escape(item['url'], quote=True)
        img_src = html.escape(src, quote=True)
        link = tr(
            f'{key}_link',
            item['headline'],
            'a',
            'w10-evidence-link',
            f' href="{href}" target="_blank" rel="noopener noreferrer"',
        )
        return (
            '<figure class="w10-evidence-card">'
            f'<div class="w10-evidence-thumb"><img src="{img_src}" alt=""></div>'
            '<figcaption class="w10-evidence-body">'
            + tr(f'{key}_meta', item['meta'], 'p', 'w10-evidence-meta')
            + link
            + tr(f'{key}_summary', item['summary'], 'p', 'w10-evidence-summary')
            + '</figcaption></figure>'
        )

    if kind == 'resource-branches':
        parts = [
            '<figure class="w10-branches"><div class="w10-branch-root">',
            tr(key + '_title', item['title'], 'strong'),
            tr(key + '_body', item['body']),
            '</div><div class="w10-branch-children">',
        ]
        for i, child in enumerate(item['children']):
            parts += [
                '<div class="w10-branch-child">',
                tr(f'{key}_{i}_title', child['title'], 'strong'),
                tr(f'{key}_{i}_body', child['body']),
                '</div>',
            ]
        return '\n'.join(parts + ['</div>', tr(key + '_caption', item['caption'], 'figcaption', 'w10-caption'), '</figure>'])

    if kind == 'resource-flow':
        parts = ['<figure class="w10-flow"><ol>']
        for i, step in enumerate(item['items']):
            parts += ['<li>', tr(f'{key}_{i}_title', step['title'], 'strong'), tr(f'{key}_{i}_body', step['body']), '</li>']
        caption = tr(key + '_caption', item['caption'], 'figcaption', 'w10-caption') if item.get('caption') else ''
        return '\n'.join(parts + ['</ol>', caption, '</figure>'])

    if kind != 'resource-sequence':
        return None

    actors, rows = item['actors'], item['rows']
    count = len(actors)
    assert 2 <= count <= 4
    position = lambda index: 12 + index * 76 / (count - 1)
    parts = [f'<figure class="w10-sequence" data-actors="{count}">', '<div class="w10-actors">']
    for i, actor in enumerate(actors):
        parts.append(tr(f'{key}_actor{i}', actor, 'p', 'w10-actor', f' style="left:{position(i):g}%"'))
    parts.append('</div><div class="w10-sequence-track">')
    for i in range(count):
        parts.append(f'<div class="w10-lifeline" style="left:{position(i):g}%" aria-hidden="true"></div>')
    parts.append('<ol class="w10-messages">')
    for i, row in enumerate(rows):
        start, end = row['from'], row['to']
        assert 0 <= start < count and 0 <= end < count
        note = start == end
        route = tuple(actors[start][lang] if note else actors[start][lang] + ' → ' + actors[end][lang] for lang in range(2))
        focus = ' w10-message--focus' if row.get('focus') else ''
        parts.append('<li>')
        parts.append(tr(f'{key}_route{i}', route, 'p', 'w10-mobile-route'))
        if note:
            anchor = 'left:0' if start == 0 else 'right:0' if start == count - 1 else 'left:30%'
            width = 46 if count == 2 else 38
            cls = 'w10-local' + focus
            parts.append(tr(f'{key}_row{i}', row['text'], 'p', cls, f' style="{anchor};width:{width}%"'))
        else:
            left = min(position(start), position(end))
            width = abs(position(start) - position(end))
            direction = 'right' if end > start else 'left'
            reply = ' w10-message--reply' if row.get('reply') else ''
            parts.append(f'<div class="w10-message w10-message--{direction}{focus}{reply}" style="left:{left:g}%;width:{width:g}%">')
            parts.append(tr(f'{key}_row{i}', row['text'], 'p', 'w10-message-text'))
            parts.append('<span class="w10-message-line" aria-hidden="true"></span></div>')
        parts.append('</li>')
    caption = tr(key + '_caption', item['caption'], 'figcaption', 'w10-caption') if item.get('caption') else ''
    parts += ['</ol></div>', caption, '</figure>']
    return '\n'.join(parts)
