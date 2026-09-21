const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const ts = require('../../../packages/web-deck/node_modules/typescript');
const prettier = require('../../../packages/web-deck/node_modules/prettier');
const options = require('../../../packages/web-deck/code-format.json');
const root = path.resolve(__dirname, '../materials/practice-source');
const names = ['operations.ts', 'calculator.ts', 'app.ts'];
const files = names.map(name => path.join(root, name));
const sources = Object.fromEntries(names.map((name, i) => [name, fs.readFileSync(files[i], 'utf8')]));

(async () => {
  const program = ts.createProgram(files, {
    strict: true, target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.None,
    noEmit: true, types: [],
  });
  const diagnostics = ts.getPreEmitDiagnostics(program);
  assert.equal(diagnostics.length, 0, ts.formatDiagnosticsWithColorAndContext(diagnostics, {
    getCurrentDirectory: () => root, getCanonicalFileName: name => name, getNewLine: () => '\n',
  }));
  if (process.env.WEEK3_PRACTICE_ROOT) {
    for (const name of names) {
      assert.equal(sources[name], fs.readFileSync(path.join(process.env.WEEK3_PRACTICE_ROOT, name), 'utf8'), `Source drift: ${name}`);
    }
  }
  const body = JSON.parse(fs.readFileSync(path.join(root, '../lesson-body.json'), 'utf8'));
  let excerpts = 0;
  for (const slide of Object.values(body.slides)) {
    for (const panel of slide.panels) {
      if (!panel.labExcerpt) continue;
      const { file, start, end, omitLineComments } = panel.labExcerpt;
      const lines = sources[file].split(/\r?\n/).slice(start - 1, end);
      const raw = lines.filter(line => !omitLineComments || !line.trimStart().startsWith('//')).join('\n');
      const expected = (await prettier.format(raw, { ...options, parser: 'typescript', printWidth: 56 })).trimEnd();
      assert.equal(panel.code, expected, `Excerpt mismatch: ${file}:${start}-${end}`);
      excerpts++;
    }
  }

  const nodes = Object.fromEntries(['#display', '#expression', '#message'].map(id => [id, { textContent: '' }]));
  const keys = ['0','1','2','3','4','5','6','7','8','9','.','+','-','*','/','=','clear','delete','sign','percent'];
  const handlers = {};
  const buttons = keys.map(key => ({ dataset: { key }, addEventListener(event, callback) {
    assert.equal(event, 'click'); handlers[key] = callback;
  } }));
  const context = vm.createContext({ document: {
    querySelector: id => nodes[id], querySelectorAll: () => buttons,
  } });
  const source = names.map(name => sources[name]).join('\n');
  const compiled = ts.transpileModule(source, {
    compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.None },
  }).outputText;
  vm.runInContext(compiled, context, { timeout: 1000 });
  const evaluate = expression => vm.runInContext(expression, context, { timeout: 1000 });
  const readState = () => JSON.parse(evaluate('JSON.stringify(state)'));
  const press = sequence => sequence.forEach(key => handlers[key]());
  assert.equal(nodes['#display'].textContent, '0');
  assert.equal(Object.keys(handlers).length, 20);
  const scenarios = [
    [['1','2','+','3','='], '15'], [['1','2','-','3','='], '9'],
    [['1','2','*','3','='], '36'], [['1','2','/','3','='], '4'],
    [['0','.','1','+','0','.','2','='], '0.3'],
    [['2','+','3','*','4','='], '20'], [['2','+','*','3','='], '6'],
    [['2','+','='], '2'], [['2','+','3','=','='], '5'],
    [['2','0','0','+','1','0','percent','='], '200.1'],
    [['1','2','3','delete'], '12'], [['5','sign'], '-5'], [['5','0','percent'], '0.5'],
    [['6','1','1','0','0','0','0'], '6,110,000'],
    [['1','.','2','0'], '1.20'], [['1','.','.','2'], '1.2'],
    [['1','2','/','0','='], 'Error'],
  ];
  for (const [sequence, expected] of scenarios) {
    press(['clear', ...sequence]);
    assert.equal(nodes['#display'].textContent, expected, sequence.join(' '));
  }
  assert.equal(nodes['#message'].textContent, '0으로 나눌 수 없습니다.');
  press(['7']);
  assert.equal(nodes['#display'].textContent, '7');
  assert.equal(nodes['#message'].textContent, '');
  press(['clear']);
  for (const [sequence, expected] of [
    [['1','2'], ['12',null,null,false,true]],
    [['+'], ['12',12,'+',true,false]],
    [['3'], ['3',12,'+',false,true]],
    [['='], ['15',null,null,true,true]],
  ]) {
    press(sequence);
    const { input, stored, operator, waiting, hasOperand } = readState();
    assert.deepEqual([input,stored,operator,waiting,hasOperand], expected);
  }
  assert.equal(nodes['#expression'].textContent, '12 + 3 =');
  const previous = readState();
  assert.equal(evaluate('pendingExpression(state)'), '12 + 3 =');
  assert.deepEqual(readState(), previous, 'Pure expression function changed state');
  assert.equal(evaluate('calculate(12, 3, multiply)'), 36);
  assert.throws(() => evaluate('setResult(Infinity)'), /계산 가능한 숫자 범위/);
  assert.deepEqual(readState(), previous, 'Invalid result changed state');
  press(['clear', ...'1234567890123']);
  assert.equal(readState().input, '123456789012');
  console.log(`PASS ${excerpts} exact lab excerpts; strict types; 20 click handlers; ${scenarios.length} UI sequences; state trace, error recovery, precision, purity, Strategy, finite results, input limit`);
})().catch(error => { console.error(error); process.exitCode = 1; });
