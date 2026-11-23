"""Visual chart and provider card renderer for Week 10 review supplement."""
import html


def render_resource(item, key, tr):
    if item['kind'] == 'link-table':
        head = ''.join(tr(f'{key}_h{i}', cell, 'th', attrs=' scope="col"') for i, cell in enumerate(item['head']))
        rows = []
        for i, row in enumerate(item['rows']):
            assert len(row) == len(item['head']), key
            cells = []
            for j, cell in enumerate(row):
                tag = 'th' if j == 0 else 'td'
                attrs = ' scope="row"' if j == 0 else ''
                if isinstance(cell, dict) and 'href' in cell:
                    href = html.escape(cell['href'], quote=True)
                    link = tr(f'{key}_r{i}_{j}', cell['label'], 'a', 'r10-table-link', f' href="{href}" target="_blank" rel="noopener noreferrer"')
                    cells.append(f'<{tag}{attrs}>{link}</{tag}>')
                else:
                    cells.append(tr(f'{key}_r{i}_{j}', cell, tag, attrs=attrs))
            rows.append('<tr>' + ''.join(cells) + '</tr>')
        return '<table class="wd-lesson-table"><thead><tr>' + head + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'

    if item['kind'] != 'model-eval-board':
        return None

    parts = ['<div class="r10-visual-grid">']

    # Left: Bar chart groups
    parts.append('<div class="r10-chart-panel">')
    for gi, group in enumerate(item['groups']):
        parts.append('<div class="r10-chart-group">')
        parts.append(tr(f'{key}_g{gi}_title', group['title'], 'p', 'r10-chart-heading'))
        parts.append('<ul class="r10-bars">')
        for bi, bar in enumerate(group['bars']):
            top = ' r10-bar-fill--top' if bar.get('top') else ''
            pct = max(5, min(100, bar['pct']))
            icon = f'<img class="r10-bar-icon" src="{html.escape(bar["icon"], quote=True)}" alt="">' if bar.get('icon') else ''
            parts.append('<li class="r10-bar-row">')
            parts.append('<span class="r10-bar-model">' + icon + tr(f'{key}_g{gi}_b{bi}_label', bar['label'], 'span', 'r10-bar-label') + '</span>')
            parts.append(f'<div class="r10-bar-track"><div class="r10-bar-fill{top}" style="width:{pct:g}%"></div></div>')
            parts.append(tr(f'{key}_g{gi}_b{bi}_val', bar['value'], 'span', 'r10-bar-value'))
            parts.append('</li>')
        parts.append('</ul></div>')
    if item.get('caption'):
        parts.append(tr(f'{key}_caption', item['caption'], 'p', 'r10-chart-caption'))
    parts.append('</div>')

    # Right: Provider tier cards
    parts.append('<div class="r10-cards">')
    for ci, card in enumerate(item['cards']):
        icon = f'<img class="r10-card-icon" src="{html.escape(card["icon"], quote=True)}" alt="">' if card.get('icon') else ''
        parts.append('<div class="r10-card">')
        parts.append('<div class="r10-card-header">')
        parts.append('<span class="r10-card-brand">' + icon + tr(f'{key}_c{ci}_name', card['provider'], 'strong', 'r10-card-provider') + '</span>')
        parts.append(tr(f'{key}_c{ci}_tier', card['tier'], 'span', 'r10-card-tier'))
        parts.append('</div>')
        parts.append(tr(f'{key}_c{ci}_models', card['models'], 'p', 'r10-card-models'))
        parts.append(tr(f'{key}_c{ci}_strength', card['strength'], 'p', 'r10-card-strength'))
        parts.append('</div>')
    parts.append('</div>')

    parts.append('</div>')
    return '\n'.join(parts)
