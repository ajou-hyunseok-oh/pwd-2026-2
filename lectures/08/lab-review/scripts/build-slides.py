"""Build the Week 7 review with the shared authoring format and frozen evidence."""
import copy
import json
import subprocess
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'authoring'))
from deck_builder import build
from lesson import WEEK, SUBTITLE, SLIDES

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SNAPSHOT = json.loads((ROOT / 'materials/code-excerpts.json').read_text())
EXCERPTS = SNAPSHOT['excerpts']
EVIDENCE = json.loads((ROOT / 'materials/sql-evidence.json').read_text())
assert SNAPSHOT['commit'] == EVIDENCE['sourceCommit'], 'Source commit mismatch'
hashes = {item['file']: item['sha256'] for item in EVIDENCE['sourceFiles']}
for item in EXCERPTS.values():
    if item.get('origin', 'server') == 'server' and item['file'] in hashes:
        assert item['sha256'] == hashes[item['file']], 'SQL/code snapshot mismatch'


def formatted_code():
    script = """const fs=require('node:fs');
const prettier=require('./packages/web-deck/node_modules/prettier');
const options=require('./packages/web-deck/code-format.json');
(async()=>{const items=JSON.parse(fs.readFileSync(0,'utf8'));const result={};
for(const [key,item] of Object.entries(items)) result[key]=item.language==='text'?item.code:(await prettier.format(item.code,{...options,parser:'typescript',printWidth:key==='db-types'?64:58})).trimEnd();
process.stdout.write(JSON.stringify(result));})();"""
    output = subprocess.run(['node', '-e', script], cwd=REPO, input=json.dumps(EXCERPTS),
                            text=True, capture_output=True, check=True)
    codes = json.loads(output.stdout)
    # This SQL excerpt contains no string literals: wrap only between SQL tokens.
    raw = codes['db-grants']
    codes['db-grants'] = '\n'.join('\n'.join(textwrap.wrap(line, width=58,
        subsequent_indent='  ', break_long_words=False, break_on_hyphens=False))
        for line in raw.splitlines())
    assert raw.split() == codes['db-grants'].split()
    return codes


def result_text(ident):
    data = EVIDENCE
    if ident == 'seed':
        return (f"schema.sql 실행 직후: {data['empty'][0]['count']}행\n"
                f"seed.sql 첫 실행: {len(data['initial'])}행\n"
                f"id=1 설명 수정 후 seed 재실행:\n  {data['reseeded'][0]['description']}",
                f"After schema.sql: {data['empty'][0]['count']} rows\n"
                f"First seed.sql run: {len(data['initial'])} rows\n"
                "Rerun seed after editing id=1:\n  edited description preserved")
    if ident == 'list':
        value = 'id | name\n' + '\n'.join(f"{row['id']}  | {row['name']}" for row in data['initial'])
        return (value, value)
    if ident == 'insert':
        row = data['inserted']
        value = '\n'.join(f'{key}: ' + json.dumps(row[key], ensure_ascii=False)
                          for key in ['id', 'price_range', 'recommended_menu'])
        return (value, value)
    if ident == 'reopen':
        before, after = data['inserted'], data['reopened'][0]
        assert before == after
        return (f"DB 종료 전: id={before['id']}\nDB 재개방 후: id={after['id']}\n"
                f"name: {after['name']}\n10개 필드 모두 일치",
                f"Before closing DB: id={before['id']}\nAfter reopening DB: id={after['id']}\n"
                f"name: {after['name']}\nAll 10 fields match")
    raise ValueError(ident)


def extra(item, key, tr):
    if item['kind'] == 'result':
        return ('<div class="review-result">' +
                tr(key + '_label', item['label'], 'p', 'wd-lesson-code-label') +
                tr(key + '_output', result_text(item['ident']), 'samp', 'review-output') + '</div>')
    return None


def prepared_slides():
    codes = formatted_code()
    slides = copy.deepcopy(SLIDES)
    for slide in slides:
        used = []
        for column in slide['columns']:
            for item in column:
                if item['kind'] != 'source':
                    continue
                ident = item.pop('ident')
                item.update(kind='code', language=EXCERPTS[ident]['language'],
                            width=64 if ident == 'db-types' else 58, text=(codes[ident], codes[ident]))
                record = EXCERPTS[ident]
                ranges = ', '.join(f"{r['startLine']}-{r['endLine']}" for r in record['selections'])
                origin = record.get('origin', 'server')
                used.append(f"{origin}/{record['file']}:{ranges} (sha256 {record['sha256']})")
        slide['note'] += '\n[Code excerpts]\n' + '\n'.join(used)
        references = []
        for source in slide['sources']:
            if source.startswith(('http', 'materials/')):
                references.append(source)
            else:
                origin = 'client' if source.startswith('client:') else 'server'
                repository = SNAPSHOT['repositories'][origin]
                references.append(f"{repository['repository']}/blob/{repository['commit']}/{source.removeprefix('client:')}")
        slide['sources'] = references
    return slides


if __name__ == '__main__':
    build(ROOT, WEEK, SUBTITLE, prepared_slides(), render_extra=extra, stylesheets=('lecture.css',))
