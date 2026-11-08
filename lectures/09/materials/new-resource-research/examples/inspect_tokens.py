"""Reproducible teaching data for slide 3.2; no model API or API key.

The filename deliberately avoids shadowing Python's standard tokenize module.
"""
import json
from importlib.metadata import version
import tiktoken

encoding = tiktoken.get_encoding('cl100k_base')
examples = []
for value in ['unhappiness!', '제목: 안녕하세요!']:
    ids = encoding.encode(value)
    pieces = []
    for token_id in ids:
        raw = encoding.decode_single_token_bytes(token_id)
        try:
            decoded = raw.decode('utf-8')
        except UnicodeDecodeError:
            decoded = None
        pieces.append({'id': token_id, 'text_if_complete_utf8': decoded,
                       'bytes_hex': raw.hex()})
    assert encoding.decode(ids) == value
    examples.append({'text': value, 'token_count': len(ids), 'tokens': pieces})
print(json.dumps({'encoding': encoding.name, 'tiktoken_version': version('tiktoken'),
                  'checked_on': '2026-11-07',
                  'note': 'One named encoding, not all models. Some tokens contain incomplete UTF-8 bytes.',
                  'examples': examples}, ensure_ascii=False, indent=2))
