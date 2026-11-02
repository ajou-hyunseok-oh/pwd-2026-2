"""Check the teaching data, declared dependencies, and lossless examples.

This checks relational models, not the deployed FoodMap database.
Use --write to retain the verification report in materials/.
"""
import argparse
import json
from itertools import combinations, product
from pathlib import Path
from design_examples import EXAMPLES


def rows(block):
    return [[value[0] for value in row] for row in block['rows']]


def holds(data, fds, order):
    for left, right in fds:
        indexes = [order.index(a) for a in left]
        targets = [order.index(a) for a in right]
        seen = {}
        for row in data:
            x = tuple(row[i] for i in indexes)
            y = tuple(row[i] for i in targets)
            if x in seen and seen[x] != y:
                return False
            seen[x] = y
    return True


def normal_forms(order, fds):
    attrs = frozenset(order)
    subsets = [frozenset(c) for n in range(len(attrs)+1) for c in combinations(order, n)]

    def closure(x):
        result = set(x)
        while True:
            previous = set(result)
            for left, right in fds:
                if set(left) <= result:
                    result.update(right)
            if previous == result:
                return result

    supers = [x for x in subsets if closure(x) == attrs]
    keys = [x for x in supers if not any(y < x for y in supers)]
    prime = set().union(*keys)
    violations = {name: [] for name in ('2NF', '3NF', 'BCNF')}
    for x in subsets:
        for a in sorted(closure(x)-x):
            if x in supers:
                continue
            fd = ''.join(c for c in order if c in x)+' → '+a
            violations['BCNF'].append(fd)
            if a not in prime:
                violations['3NF'].append(fd)
                if any(x < k for k in keys):
                    violations['2NF'].append(fd)
    return dict(candidate_keys=[''.join(c for c in order if c in k) for k in keys],
                prime_attributes=''.join(c for c in order if c in prime),
                normal_forms={name: not invalid for name, invalid in violations.items()},
                violations=violations)


def check_decomposition(slide):
    before, after = slide['items'][:2]
    heads = [p[0] for p in before['head']]
    original = {tuple(r) for r in rows(before)}
    parts = after['items']
    records = []
    for table in parts:
        fields = [p[0] for p in table['head']]
        records.append([dict(zip(fields, r)) for r in rows(table)])
    joined = set()
    for left, right in product(*records):
        common = set(left) & set(right)
        if all(left[k] == right[k] for k in common):
            merged = {**left, **right}
            joined.add(tuple(merged[k] for k in heads))
    assert joined == original, 'Decomposition loses or adds rows'
    return dict(before_rows=len(original), restored_rows=len(joined), exact_reconstruction=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Save the verification report')
    args = parser.parse_args()
    report = dict(scope='Illustrative relational models; no service or live DB access', models={}, checks={})
    models = [
        ('restaurant_menu', 'RMNP', [('R','N'),('RM','P')], rows(EXAMPLES['prime-attribute']['items'][0]), ['RM'], {'2NF':False,'3NF':False,'BCNF':False}),
        ('restaurant_region', 'RCN', [('R','C'),('C','N')], rows(EXAMPLES['transitive-dependency']['items'][0]), ['R'], {'2NF':True,'3NF':False,'BCNF':False}),
        ('enrollment', 'SCP', [('SC','P'),('P','C')], rows(EXAMPLES['bcnf']['items'][0]['items'][0]), ['SC','SP'], {'2NF':True,'3NF':True,'BCNF':False})]
    for name, order, fds, data, expected_keys, expected_forms in models:
        assert holds(data, fds, order), name+' violates a declared FD'
        result = normal_forms(order, fds)
        assert result['candidate_keys'] == expected_keys, (name,result)
        assert result['normal_forms'] == expected_forms, (name,result)
        report['models'][name] = dict(attributes=order, declared_dependencies=[x+' → '+y for x,y in fds], data=data, **result)
    bad_menu = rows(EXAMPLES['normalization']['items'][0]['items'][1])
    assert not holds(bad_menu, [('R','N')], 'RMNP')
    report['checks']['update_anomaly_detected'] = True
    for ident in ('second-normal-form','third-normal-form'):
        report['checks'][ident] = check_decomposition(EXAMPLES[ident])
    before, after = EXAMPLES['first-normal-form']['items'][0]['items']
    expanded = {(r[0], phone.strip()) for r in rows(before) for phone in r[1].split(',')}
    assert expanded == {tuple(r) for r in rows(after)}
    report['checks']['phone_values_preserved'] = True
    parent, attempts = EXAMPLES['foreign-key']['items'][0]['items']
    ids = {r[0] for r in rows(parent)}
    assert rows(attempts)[0][1] in ids and rows(attempts)[1][1] not in ids
    report['checks']['foreign_key_allowed_and_missing_reference'] = True
    if args.write:
        target = Path(__file__).resolve().parents[1]/'materials/design-example-verification.json'
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
