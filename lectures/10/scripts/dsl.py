"""Concise bilingual slide builders for Week 10."""


def P(ko, en):
    return (ko, en)


def chapter(ident, ko, en):
    return dict(id=ident, kind='chapter', title=(ko, en))


def concept(term, *details):
    return dict(term=term, details=list(details))


def concepts_block(*items):
    return dict(kind='concepts', items=list(items))


def table_block(head, rows):
    return dict(kind='table', head=head, rows=rows)


def code_block(label, text, language='javascript', width=64):
    pair = (text, text) if isinstance(text, str) else text
    return dict(kind='code', label=label, text=pair, language=language, width=width)


def flow_block(items, caption=None):
    return dict(
        kind='resource-flow',
        items=[dict(title=t, body=b) for t, b in items],
        caption=caption,
    )


def msg(fr, to, text, *, reply=False, focus=False):
    return dict(from_=fr, to=to, text=text, reply=reply, focus=focus)


def seq_block(actors, rows, caption=None):
    return dict(
        kind='resource-sequence',
        actors=actors,
        rows=[
            {
                'from': r['from_'],
                'to': r['to'],
                'text': r['text'],
                'reply': r['reply'],
                'focus': r['focus'],
            }
            for r in rows
        ],
        caption=caption,
    )


def branches_block(title, body, children, caption):
    return dict(
        kind='resource-branches',
        title=title,
        body=body,
        children=[dict(title=t, body=b) for t, b in children],
        caption=caption,
    )


def note_block(text):
    return dict(kind='resource-note', text=text)


def evidence_block(src, meta, headline, url, summary):
    return dict(kind='resource-evidence', src=src, meta=meta, headline=headline, url=url, summary=summary)


def slide(ident, title, lead, layout, columns, *, sources=None, note=''):
    return dict(
        id=ident,
        kind='content',
        title=title,
        lead=lead,
        layout=layout,
        columns=columns,
        sources=sources or [],
        note=note,
    )
