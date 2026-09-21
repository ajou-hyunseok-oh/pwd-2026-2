const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const { createRequire } = require('node:module');
const ts = require('../../../packages/web-deck/node_modules/typescript');
const root = path.resolve(__dirname, '..');
const temp = process.env.WEEK3_CHECK_ROOT || path.join(os.tmpdir(), 'week3-code-review');
fs.mkdirSync(temp, { recursive: true });
const externalRequire = createRequire(path.join(temp, 'package.json'));
const body = JSON.parse(fs.readFileSync(path.join(root, 'materials/lesson-body.json'), 'utf8'));
const headingHash = crypto.createHash('sha256').update(fs.readFileSync(path.join(root, 'materials/slide-draft.json'))).digest('hex');
assert.equal(headingHash, fs.readFileSync(path.join(root, 'materials/approved-headings.sha256'), 'utf8').trim(), 'Approved headings changed');
const cases = [];
const files = [];
for (const [number, slide] of Object.entries(body.slides)) {
  slide.panels.forEach((panel, index) => {
    if (panel.kind !== 'code' || panel.language === 'bash' || panel.context === 'lab') return;
    const entry = { ...panel, number: Number(number), index };
    // Validate the original execution context before the async test wrapper.
    if (panel.language === 'javascript') {
      if (panel.executionMode === 'module' || panel.moduleGroup) {
        execFileSync(process.execPath, ['--input-type=module', '--check'], { input: panel.code });
      } else {
        new vm.Script(panel.code, { filename: `slide-${number}-${index}.js` });
      }
    }
    if (['typescript', 'tsx'].includes(panel.language)) {
      const folder = path.join(temp, panel.moduleGroup || `${number}-${index}`);
      fs.mkdirSync(folder, { recursive: true });
      const filename = path.join(folder, panel.file || `sample.${panel.language === 'tsx' ? 'tsx' : 'ts'}`);
      let source = (panel.prelude || '') + '\n' + panel.code + '\nexport {};\n';
      fs.writeFileSync(filename, source);
      entry.filename = filename;
      files.push(filename);
    }
    cases.push(entry);
  });
}
const program = ts.createProgram(files, {
  strict: true, target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS,
  moduleResolution: ts.ModuleResolutionKind.Node10, jsx: ts.JsxEmit.ReactJSX,
  noEmit: true, skipLibCheck: true, types: [],
});
const diagnostics = ts.getPreEmitDiagnostics(program);
let expectedErrors = 0;
for (const entry of cases.filter(c => c.filename)) {
  const actual = diagnostics.filter(d => d.file && path.resolve(d.file.fileName) === path.resolve(entry.filename)).map(d => d.code).sort();
  assert.deepEqual(actual, [...(entry.errors || [])].sort(), `Type diagnostics for ${entry.number}-${entry.index}: ` + diagnostics.filter(d => d.file && path.resolve(d.file.fileName) === path.resolve(entry.filename)).map(d => ts.flattenDiagnosticMessageText(d.messageText, '\n')).join('\n'));
  expectedErrors += actual.length;
}
const unexpected = diagnostics.filter(d => !files.some(file => d.file && path.resolve(file) === path.resolve(d.file.fileName)));
assert.equal(unexpected.length, 0, 'Unexpected shared diagnostics');
const expectedLogs = {
  '26-1': [['not a string']], '27-0': [['121'], ['invalid value']],
  '28-0': [[12], ['add'], [undefined]],
};
const specialExpected = {
  'array-methods': [[[1, 2]], [4], [1], [2], [undefined]],
  values: [['123', 12], ['string', 'number'], [true, undefined, null]],
  conversion: [['12'], ['123'], [15], [0], [NaN]],
  'state-errors': [['123'], [NaN], ['0']],
  prediction: [['123'], [NaN], [Infinity], [0.30000000000000004]],
};
function canonical(value) {
  if (value === undefined) return { special: 'undefined' };
  if (typeof value === 'number' && Number.isNaN(value)) return { special: 'NaN' };
  if (Array.isArray(value)) return Array.from(value, canonical);
  return value;
}
let executions = 0;
async function execute(entry, additions = '', override = {}) {
  const logs = [];
  const exports = {};
  const sandbox = {
    exports,
    structuredClone,
    console: { log: (...values) => logs.push(values) },
    require: externalRequire,
    ...override,
  };
  const source = entry.language === 'javascript' ? entry.code : ts.transpileModule(entry.code, {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX }
  }).outputText;
  let thrown;
  try { await vm.runInNewContext(`(async () => {\n${source}\n${additions}\n})()`, sandbox, { timeout: 1000 }); }
  catch (error) { thrown = error; }
  assert.equal(thrown?.name, entry.runtimeError, `Runtime ${entry.number}-${entry.index}: ${thrown?.stack}`);
  executions++;
  return logs;
}
(async () => {
  const moduleEntries = cases.filter(entry => entry.moduleGroup);
  for (const entry of moduleEntries) {
    const folder = path.join(temp, 'runtime-' + entry.moduleGroup);
    fs.mkdirSync(folder, { recursive: true });
    fs.writeFileSync(path.join(folder, 'package.json'), '{"type":"module"}');
    const source = entry.language === 'javascript' ? entry.code : ts.transpileModule(entry.code, {
      compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 }
    }).outputText;
    fs.writeFileSync(path.join(folder, entry.file.replace(/\.ts$/, '.js')), source);
  }
  for (const entry of moduleEntries.filter(entry => 'output' in entry)) {
    const filename = path.join(temp, 'runtime-' + entry.moduleGroup, entry.file.replace(/\.ts$/, '.js'));
    const output = execFileSync(process.execPath, [filename], { encoding: 'utf8' }).trimEnd();
    assert.equal(output, entry.output, `Module output ${entry.moduleGroup}`);
    executions++;
  }
  for (const entry of cases) {
    if (entry.moduleGroup) continue;
    if (entry.errors?.length || entry.context === 'dom' || entry.context === 'fetch') continue;
    const key = `${entry.number}-${entry.index}`;
    const additions = entry.verification === 'paradigm-display'
      ? "console.log(Display({input: '12'}).props.children); console.log(Display({input: '123'}).props.children);" : '';
    const logs = await execute(entry, additions, {});
    const expected = entry.expectedLogs || (entry.verification === 'paradigm-display' ? [['12'], ['123']] : undefined) || specialExpected[entry.specialExpected] || expectedLogs[key] || ({'38-0': [[12]]}[key]);
    if (expected) assert.deepEqual(canonical(logs), canonical(expected), `Outputs ${key}`);
  }
  // Exercise the visible calculator snippets through registered click handlers.
  for (const number of [30, 32, 33]) {
    const entry = cases.find(c => c.number === number && c.context === 'dom');
    const display = { textContent: '' };
    let click;
    const button = { addEventListener: (event, handler) => {
      assert.equal(event, 'click'); click = handler;
    }};
    const document = { querySelector: selector => {
      if (selector === 'button') return button;
      assert.equal(selector, 'output'); return display;
    }};
    const logs = await execute(entry, number === 33
      ? "console.log(add(12, 3), add(12, 3), state.input);" : '', { document });
    assert.equal(display.textContent, number === 30 ? '1' : '12');
    if (number === 33) assert.deepEqual(canonical(logs), [[15, 15, '12']]);
    if (number !== 32) {
      assert.equal(typeof click, 'function');
      click();
      assert.equal(display.textContent, number === 30 ? '12' : '15');
      click();
      assert.equal(display.textContent, number === 30 ? '122' : '18');
    }
  }
  const fetchExample = cases.find(c => c.context === 'fetch');
  for (const [fetch, expected] of [
    [async () => ({ok:true,json:async()=>[{}]}),[[1]]],
    [async () => ({ok:false}),[['load failed']]],
    [async () => {throw new Error('network');},[['load failed']]],
  ]) assert.deepEqual(canonical(await execute(fetchExample,'',{fetch})),expected);
  console.log(`PASS approved headings; ${cases.length} code examples; ${files.length} TS/TSX modules; ${expectedErrors} intended diagnostics; ${executions} executions including Fetch and paradigm examples`);
})().catch(error => { console.error(error); process.exitCode = 1; });
