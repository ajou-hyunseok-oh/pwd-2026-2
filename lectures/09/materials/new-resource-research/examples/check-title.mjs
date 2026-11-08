import assert from 'node:assert/strict';
import { isValidTitle, isValidTitleBeforeRepair } from './title-validation.mjs';

const cases = [
  { label: 'empty', input: '', expected: false },
  { label: 'three spaces', input: '   ', expected: false },
  { label: 'one character', input: 'A', expected: true },
  { label: 'twenty characters', input: 'A'.repeat(20), expected: true },
  { label: 'twenty-one characters', input: 'A'.repeat(21), expected: false },
  { label: 'normal title', input: '공지사항', expected: true },
  { label: 'padded normal title', input: '  공지사항  ', expected: true },
  { label: 'padded twenty characters', input: `  ${'A'.repeat(20)}  `, expected: true },
];

const rows = cases.map(({ label, input, expected }) => {
  const before = isValidTitleBeforeRepair(input);
  const after = isValidTitle(input);
  assert.equal(after, expected, label);
  return { label, input, expected, before, after };
});
assert.deepEqual(rows.filter(row => row.before !== row.expected).map(row => row.label),
  ['three spaces', 'padded twenty characters']);
console.log(JSON.stringify({
  kind: 'local-code-check',
  checked_on: '2026-11-07',
  node_version: process.version,
  case_count: rows.length,
  corrected_function_passes: rows.length,
  deliberate_baseline_failures: 2,
  note: 'Actual local JavaScript output; no AI agent was run to create this trace.',
  rows,
}, null, 2));
