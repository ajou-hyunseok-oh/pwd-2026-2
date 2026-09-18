const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { createRequire } = require('node:module');
const ts = require('../practice/node_modules/typescript');
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
    if (panel.kind !== 'code' || panel.language === 'bash') return;
    const entry = { ...panel, number: Number(number), index };
    if (['typescript', 'tsx'].includes(panel.language)) {
      const folder = path.join(temp, number === '29' ? 'modules' : `${number}-${index}`);
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
  '3-1': [[6000]], '4-0': [['number','string'],[undefined,null]],
  '5-0': [['21'],[1],[3],[0],[NaN]], '6-0': [['ready']], '7-0': [[10500]],
  '8-0': [[6000],['ready']], '9-0': [[[2700,5400]]], '10-0': [['Notebook',true]],
  '11-0': [[0],[false],[true]], '12-0': [[['Notebook']]], '15-0': [[1],[1]],
  '16-0': [['23'],[NaN],[0]], '19-0': [[6000]], '19-1': [[6000]],
  '24-0': [[3000]], '25-0': [['quantity: 2']], '26-1': [['not a string']],
  '27-0': [['30001'],['invalid price']], '28-0': [[3000],['note'],[undefined]],
  '29-1': [['Notebook']], '31-0': [[4500],[2]], '32-0': [[1]],
  '34-1': [[6000],[9000]], '37-0': [[6000],[5400]], '44-0': [['31'],[NaN]],
  '47-1': [['product not found']], '48-0': [[6000],[5400],[2700]],
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
    console: { log: (...values) => logs.push(values) },
    require: (name) => name === './types.js' ? { label: item => item.name } : externalRequire(name),
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
  for (const entry of cases) {
    if (entry.errors?.length || entry.context === 'dom' || entry.context === 'fetch') continue;
    const key = `${entry.number}-${entry.index}`;
    const additions = {
      '30-0': "console.log((await submitOrder('2')).total);",
      '34-0': "console.log(OrderButton({busy: true}).props.disabled); console.log(OrderButton({busy: false}).props.children);",
      '38-0': "console.log(toProduct({product_name: 'Notebook', unit_price: 3000}).price);",
      '45-0': "console.log(parseQuantity('2',5).data); console.log(parseQuantity('6',5).ok); console.log(parseQuantity(' ',5).ok);",
      '49-0': "console.log(toProduct({id: 'note', product_name: 'Notebook', unit_price: 3000, stock: 5}).name);",
    }[key] || '';
    const logs = await execute(entry, additions, entry.number === 30 ? { saveOrder: async () => {} } : {});
    const expected = expectedLogs[key] || ({ '30-0': [[6000]], '34-0': [[true],['Order']], '38-0': [[3000]], '45-0': [[2],[false],[false]], '49-0': [['Notebook']] }[key]);
    if (expected) assert.deepEqual(canonical(logs), canonical(expected), `Outputs ${key}`);
  }
  const dom = cases.find(c => c.context === 'dom');
  let handler;
  let registrationLogs;
  const domLogs = await execute(dom, '', { document: { querySelector: selector => selector === '#quantity' ? { value: '2' } : { addEventListener: (_event, callback) => { handler = callback; } } } });
  assert.equal(domLogs.length, 0, 'Registration must not run the handler');
  handler();
  assert.deepEqual(canonical(domLogs), [[2]]);
  const fetchExample = cases.find(c => c.context === 'fetch');
  for (const [fetch, expected] of [
    [async () => ({ok:true,json:async()=>[{}]}),[[1]]],
    [async () => ({ok:false}),[['load failed']]],
    [async () => {throw new Error('network');},[['load failed']]],
  ]) assert.deepEqual(canonical(await execute(fetchExample,'',{fetch})),expected);
  const asyncExample = cases.find(c => c.number === 33);
  let resolveA, resolveB;
  const rendered=[];
  await execute(asyncExample, "const a=search('a'); const b=search('b'); finishB(); await b; finishA(); await a;", {
    loadProducts: query => new Promise(resolve => { if(query==='a')resolveA=resolve;else resolveB=resolve; }),
    renderProducts: values => rendered.push(values),
    finishA:()=>resolveA(['a']),finishB:()=>resolveB(['b']),
  });
  assert.deepEqual(rendered,[['b']]);
  console.log(`PASS approved headings; ${cases.length} code examples; ${files.length} TS/TSX modules; ${expectedErrors} intended diagnostics; ${executions} executions including DOM, Fetch, React, Vue, and stale responses`);
})().catch(error => { console.error(error); process.exitCode = 1; });
