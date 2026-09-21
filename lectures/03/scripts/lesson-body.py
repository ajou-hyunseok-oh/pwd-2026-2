"""Concept-focused slides; source provenance is kept in authoring metadata."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
 'thinking-react': ['React · Thinking in React', 'https://react.dev/learn/thinking-in-react'],
 'elm-architecture': ['Elm · The Elm Architecture', 'https://guide.elm-lang.org/architecture/'],
 'paradigms': ['MDN · JavaScript language overview', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Language_overview'],
 'async-intro': ['MDN · Introducing asynchronous JavaScript', 'https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS/Introducing'],
 'oop': ['MDN · Object-oriented programming', 'https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object-oriented_programming'],
 'structured-clone': ['MDN · structuredClone', 'https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone'],
 'js-history': ['JavaScript: The First 20 Years', 'https://www.cs.tufts.edu/comp/150FP/archive/brendan-eich/js-hopl.pdf'],
 'js-origin-talk': ['Brendan Eich · JavaScript at 20', 'https://brendaneich.github.io/ModernWeb.tw-2015/'],
 'w3c-liaisons': ['W3C · Liaisons', 'https://www.w3.org/liaisons/'],
 'w3c-css': ['W3C · CSS', 'https://www.w3.org/Style/CSS/'],
 'whatwg-w3c': ['W3C–WHATWG · Memorandum of Understanding', 'https://www.w3.org/2019/04/WHATWG-W3C-MOU.html'],
 'es2015': ['ECMAScript 2015 · Sixth Edition', 'https://262.ecma-international.org/6.0/'],
 'ecma-org': ['Ecma International · Mission', 'https://ecma-international.org/mission/'],
 'tc39': ['Ecma International · TC39', 'https://ecma-international.org/technical-committees/tc39/'],
 'ecma': ['Ecma · ECMA-262', 'https://ecma-international.org/publications-and-standards/standards/ecma-262/'],
 'grammar': ['MDN · Grammar and Types', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types'],
 'control': ['MDN · Control Flow', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling'],
 'loops': ['MDN · Loops and Iteration', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Loops_and_iteration'],
 'functions': ['MDN · Functions', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions'],
 'const': ['MDN · const', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const'],
 'objects': ['MDN · Working with Objects', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects'],
 'spread': ['MDN · Spread Syntax', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax'],
 'filter': ['MDN · Array.filter', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter'],
 'map': ['MDN · Array.map', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map'],
 'events': ['MDN · addEventListener', 'https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener'],
 'fetch': ['MDN · Using Fetch', 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch'],
 'ts-history': ['Microsoft · Ten Years of TypeScript', 'https://devblogs.microsoft.com/typescript/ten-years-of-typescript/'],
 'basics': ['TypeScript · The Basics', 'https://www.typescriptlang.org/docs/handbook/2/basic-types.html'],
 'types': ['TypeScript · Everyday Types', 'https://www.typescriptlang.org/docs/handbook/2/everyday-types.html'],
 'narrow': ['TypeScript · Narrowing', 'https://www.typescriptlang.org/docs/handbook/2/narrowing.html'],
 'ts-functions': ['TypeScript · More on Functions', 'https://www.typescriptlang.org/docs/handbook/2/functions.html'],
 'generic': ['TypeScript · Generics', 'https://www.typescriptlang.org/docs/handbook/2/generics.html'],
 'modules': ['TypeScript · Modules', 'https://www.typescriptlang.org/docs/handbook/2/modules.html'],
 'compat': ['TypeScript · Type Compatibility', 'https://www.typescriptlang.org/docs/handbook/type-compatibility.html'],
 'classes': ['TypeScript · Classes', 'https://www.typescriptlang.org/docs/handbook/2/classes.html'],
 'pure': ['React · Keeping Components Pure', 'https://react.dev/learn/keeping-components-pure'],
 'react': ['React · Reacting to Input with State', 'https://react.dev/learn/reacting-to-input-with-state'],
 'vue': ['Vue · Computed Properties', 'https://vuejs.org/guide/essentials/computed.html'],
 'practice': ['실습 README / Lab README', 'https://github.com/ajou-hyunseok-oh/pwd-week3#readme'],
}
BODY = {}
def bi(ko,en): return {'ko':ko,'en':en}
def group(ko, en, *details):
 return {**bi(ko, en), 'details': [bi(*detail) for detail in details]}
def concepts(label, *items):
 return {'kind': 'points', 'label': bi(*label), 'items': list(items)}
def code(label,lang,value,**kw):
 return {'kind':'code','label':bi(*label),'language':lang,'code':value.strip(),**kw}
def points(label,*rows):
 return {'kind':'points','label':bi(*label),'items':[bi(*r) for r in rows]}
def table(label,headers,rows):
 return {'kind':'table','label':bi(*label),'headers':[bi(*v) for v in headers],'rows':[[bi(*v) for v in row] for row in rows]}
def flow(label,*rows):
 return {'kind':'flow','label':bi(*label),'items':[bi(*r) for r in rows]}
def add(n,panels,sources=(),layout='split'):
 BODY[str(n)]={'panels':panels,'sources':list(sources),'layout':layout}

PRACTICE = ROOT / 'materials/practice-source'
REVISION = 'a321051435d95970ac6e082b933fd49464b7e974'
def lab(filename, start, end, label):
 lines = (PRACTICE / filename).read_text(encoding='utf-8').splitlines()[start-1:end]
 value = '\n'.join(line for line in lines if not line.lstrip().startswith('//'))
 return code(label, 'typescript', value,
  context='lab', labExcerpt={'file':filename, 'start':start, 'end':end, 'omitLineComments':True},
  sourceUrl=f'https://github.com/ajou-hyunseok-oh/pwd-week3/blob/{REVISION}/{filename}#L{start}-L{end}')

add(1, [
 flow(('사용자 입력 → JavaScript 처리 → 화면 변화', 'User Input → JavaScript Processing → Screen Update'),
  ('입력에 반응하기 · 클릭이나 키보드 입력이 발생하면 정해진 코드 실행', 'Respond to input · Run code when the user clicks or types.'),
  ('데이터 처리하기 · 값을 저장하고, 조건에 따라 판단하고, 함수로 작업 수행', 'Process data · Store values, make decisions, and perform tasks with functions.'),
  ('결과 반영하기 · 처리한 결과에 맞춰 화면의 내용과 상태 갱신', 'Reflect results · Update the page content and state to match the results.')),
 points(('오늘의 학습 목표', 'Today’s Learning Goal'),
  ('JavaScript의 기본 문법과 코드 실행 순서를 배우고, 웹페이지가 변화하는 과정 이해', 'Learn JavaScript fundamentals and understand how code runs in sequence to change a web page.'))
], layout='single')

add(2, [
 flow(('1995 · Netscape', '1995 · Netscape'),
  ('정적인 문서에서 상호작용으로 · 입력에 반응할 브라우저 언어의 필요', 'From static documents to interaction · A browser language to respond to input'),
  ('Brendan Eich가 설계한 스크립트 언어 · Mocha → LiveScript → JavaScript', 'A scripting language designed by Brendan Eich · Mocha → LiveScript → JavaScript'),
  ('스크립트 언어 · 실행 환경이 코드를 읽어 동작시키는 언어. 웹페이지에 입력 처리와 동작 추가', 'Scripting language · Code executed by a host environment, adding input handling and behavior to web pages')),
 points(('10일 만에 만든 첫 프로토타입', 'The First Prototype in 10 Days'),
  ('1995년 5월 · Brendan Eich가 단 10일 동안 초기 구현 제작', 'May 1995 · Brendan Eich built the initial implementation in just 10 days'),
  ('코드를 읽는 파서와 실행하는 인터프리터까지 구현 · 이후 기능 보완과 표준화를 거쳐 발전', 'Built both a parser and an interpreter · Further development and standardization followed'))
], ['js-history', 'js-origin-talk'], layout='single')

add(3, [
 {**table(('웹 표준화 단체와 담당 표준', 'Web Standards Organizations'),
  [('단체', 'Organization'), ('담당 표준', 'Standards')], [
  [('WHATWG', 'WHATWG'), ('HTML · DOM — 웹 문서 구조와 조작 규칙', 'HTML · DOM — Document structure and manipulation')],
  [('W3C', 'W3C'), ('CSS 등 — 웹페이지 표현과 웹 기술 표준', 'CSS and other web technologies — Web page presentation')],
  [('Ecma International', 'Ecma International'), ('ECMAScript — JavaScript의 문법과 동작', 'ECMAScript — JavaScript syntax and behavior')]]),
  'explanation': bi('Ecma는 정보통신 분야의 비영리 표준화 기구. 세 단체는 서로 독립적이며 웹 표준 개발에서 협력', 'Ecma is a non-profit ICT standards organization. The three organizations are independent and cooperate on web standards.')},
 points(('공통 규칙의 제정과 구현', 'Defining and Implementing Shared Rules'),
  ('TC39 · Ecma 산하에서 ECMAScript를 개발·개정하는 기술위원회', 'TC39 · The Ecma technical committee that develops and revises ECMAScript'),
  ('ECMA-262 · ECMAScript 사양을 담은 표준 문서 번호. 1997년 초판 발행', 'ECMA-262 · The standard document number for the ECMAScript specification, first published in 1997'),
  ('표준화의 목적 · 각 브라우저가 같은 언어 규칙을 구현하도록 공통 기준 제공', 'Purpose of standardization · A shared basis for browsers to implement the same language rules'),
  ('ES6(ES2015) · 현대 JavaScript의 기반이 된 주요 기능을 대폭 도입한 전환점', 'ES6 (ES2015) · A milestone introducing major features that underpin modern JavaScript'))
], ['ecma-org','tc39','ecma','w3c-liaisons','w3c-css','whatwg-w3c','es2015'])

add(4, [
 code(('계산기 입력을 이용한 값 실험', 'Value Experiment with Calculator Input'), 'javascript', """
let input = '12';
const stored = Number(input);
const waiting = true;
let selected;
input += '3';
console.log(input, stored);
console.log(typeof input, typeof stored);
console.log(waiting, selected, null);
""", output='123 12\nstring number\ntrue undefined null', specialExpected='values'),
 {'kind': 'points', 'label': bi('값·타입·변수의 의미', 'Values, Types, and Variables'), 'items': [
  {**bi('값 - 프로그램이 다루는 데이터', 'Value - Data a program uses'), 'details': [
   bi('undefined - 아직 정해지지 않은 값', 'undefined - A value not yet defined'),
   bi('null - 의도적으로 표시한 값의 부재', 'null - Intentional absence of a value')]},
  {**bi('타입 - 값의 종류와 가능한 연산', 'Type - Value categories and supported operations'), 'details': [
   bi('string - 문자열', 'string - Text'),
   bi('number - 숫자', 'number - Numeric data'),
   bi('boolean - 참 또는 거짓', 'boolean - True or false')]},
  {**bi('변수 - 값을 가리키는 이름', 'Variable - A name bound to a value'), 'details': [
   bi('let - 다른 값으로 재할당 가능', 'let - Can be reassigned to another value'),
   bi('const - 재할당 불가', 'const - Cannot be reassigned')]}
 ]}], ['grammar','practice'])

add(5, [
 code(('문자열 연결과 숫자 변환', 'String Concatenation and Number Conversion'), 'javascript', """
let input = '1';
input += '2';
console.log(input);
console.log(input + '3');
console.log(Number(input) + 3);
console.log(Number(''));
console.log(Number('12px'));
""", output='12\n123\n15\n0\nNaN', specialExpected='conversion'),
 {'kind': 'points', 'label': bi('연산과 형변환', 'Operators and Type Conversion'), 'items': [
  {**bi('연산자 - 값에 연산을 적용하는 기호', 'Operator - A symbol for an operation'), 'details': [
   bi('+ : 한쪽이 문자열이면 연결', '+ : Concatenation if either operand is a string'),
   bi('+ : 양쪽이 숫자이면 덧셈', '+ : Addition if both operands are numbers')]},
  {**bi('형변환 - 값의 타입을 바꾸는 과정', 'Type conversion - Changing a value’s type'), 'details': [
   bi('암묵적 변환 - 언어 규칙에 따른 자동 변환', 'Implicit conversion - Automatic conversion by language rules'),
   bi('명시적 변환 - Number 등으로 직접 변환', 'Explicit conversion - Conversion requested with Number or similar functions'),
   bi('Number(\"\") → 0', 'Number(\"\") → 0'),
   bi('Number(\"12px\") → NaN (숫자 변환 실패)', 'Number(\"12px\") → NaN (failed numeric conversion)')]}
 ]}], ['grammar','practice'])

add(6, [
 code(('점수에 따른 두 가지 결과', 'Two Outcomes Based on a Score'), 'javascript', """
const score = 75;
let result;
if (score >= 60) {
  result = 'pass';
} else {
  result = 'fail';
}
console.log(result);
""", output='pass', expectedLogs=[['pass']]),
 {'kind': 'points', 'label': bi('조건에 따른 실행 분기', 'Conditional Execution'), 'items': [
  {**bi('if - 조건이 참일 때 실행', 'if - Execution when the condition is true'), 'details': [
   bi('score >= 60 - 점수가 60 이상인지 비교', 'score >= 60 - Check whether the score is at least 60'),
   bi('75점 → 참 → if 블록에서 pass 저장', 'Score 75 → true → Store pass in the if block')]},
  {**bi('else - 조건이 거짓일 때 실행', 'else - Execution when the condition is false'), 'details': [
   bi('40점으로 바꾸면 → 거짓 → else 블록에서 fail 저장', 'Change the score to 40 → false → Store fail in the else block'),
   bi('두 블록 중 하나만 실행한 뒤 결과 출력', 'Run exactly one of the two blocks, then print the result')]}
 ]}], ['control'])


# Source id 53 is inserted before topic 7; existing topic ids stay stable.
add(53, [
 code(('배열의 인덱스와 객체의 속성', 'Array Indices and Object Properties'), 'javascript', """
const items = ['A', 'B'];
console.log(items[0]);
console.log(items.length);

const user = { name: 'Kim', age: 20 };
console.log(user.name);
console.log(user['age']);
""", output='A\n2\nKim\n20', expectedLogs=[['A'],[2],['Kim'],[20]]),
 {'kind': 'points', 'label': bi('여러 값을 묶는 두 가지 방식', 'Two Ways to Group Values'), 'items': [
  {**bi('배열 - 여러 값을 순서대로 저장하는 객체', 'Array - An object that stores values in order'), 'details': [
   bi("['A', 'B'] - 대괄호 안에 원소 나열", "['A', 'B'] - Elements listed in square brackets"),
   bi('items[0] - 0부터 시작하는 인덱스로 첫 원소 접근', 'items[0] - Access the first element at index 0'),
   bi('items.length - 배열의 길이, 예제에서는 2', 'items.length - Array length, which is 2 here')]},
  {**bi('객체 - 속성 이름과 값으로 데이터를 묶는 구조', 'Object - Data grouped by property names'), 'details': [
   bi("{ name: 'Kim', age: 20 } - 중괄호 안에 이름: 값 작성", "{ name: 'Kim', age: 20 } - Name: value pairs in braces"),
   bi('user.name - 점 표기법으로 속성 값 접근', 'user.name - Access a property value using dot notation'),
   bi("user['age'] - 대괄호에 속성 이름을 넣어 접근", "user['age'] - Access a property by name in brackets")]},
  {**bi('접근 기준 - 인덱스와 속성 이름', 'Access - Indices and property names'), 'details': [
   bi('배열은 원소의 위치, 일반 객체는 속성 이름으로 값 접근', 'Access array elements by position and ordinary object values by property name')]}
 ]}], ['grammar','objects'])

add(7, [
 code(('인덱스·값·속성 이름의 순회', 'Iterating Indices, Values, and Property Names'), 'javascript', """
const items = ['A', 'B'];
for (let i = 0; i < items.length; i++) {
  console.log(i, items[i]);
}
for (const item of items) {
  console.log(item);
}
const user = { name: 'Kim', age: 20 };
for (const key in user) {
  console.log(key);
}
""", output='0 A\n1 B\nA\nB\nname\nage', expectedLogs=[[0,'A'],[1,'B'],['A'],['B'],['name'],['age']]),
 {'kind': 'points', 'label': bi('for문의 형태와 반복 제어', 'Forms of for and Loop Control'), 'items': [
  {**bi('for - 초기식·조건식·증감식으로 반복 제어', 'for - Control a loop with three expressions'), 'details': [
   bi('초기식 1회 → 조건 검사 → 본문 → 증감식 → 조건 재검사', 'Initialize once → Test → Body → Update → Test again'),
   bi('i++ : i를 1 증가 · items[i] : 0부터 시작하는 인덱스로 접근', 'i++ : Increase i by 1 · items[i] : Access by zero-based index')]},
  {**bi('for...of - 배열 등의 값을 순서대로 순회', 'for...of - Iterate values of an iterable'), 'details': [
   bi('item에 A, B를 차례로 대입', 'Assign A and then B to item')]},
  {**bi('for...in - 객체의 속성 이름을 순회', 'for...in - Iterate object property names'), 'details': [
   bi('key에 name, age를 대입 · 상속된 열거 가능 속성도 포함', 'Assign name and age to key; inherited enumerable properties are included'),
   bi('배열의 값 순회에는 for...of 사용', 'Use for...of to iterate array values')]},
  {**bi('반복 제어 - 생략 또는 종료', 'Loop control - Skip or stop'), 'details': [
   bi('continue - 현재 반복의 나머지를 생략하고 다음 반복 진행', 'continue - Skip the rest of the current iteration'),
   bi('break - 반복문 종료', 'break - Exit the loop')]}
 ]}], ['loops'])


add(8, [
 code(('매개변수와 반환값', 'Parameters and Return Values'), 'javascript', """
function formatNumber(value) {
  return Number(value.toPrecision(12)).toString();
}
const value = 0.1 + 0.2;
console.log(value);
console.log(formatNumber(value));
""", output='0.30000000000000004\n0.3', expectedLogs=[[0.30000000000000004],['0.3']]),
 {'kind': 'points', 'label': bi('함수의 입력·출력과 스코프', 'Function Inputs, Outputs, and Scope'), 'items': [
  {**bi('함수 - 호출하여 재사용하는 코드 단위', 'Function - A reusable unit of code'), 'details': [
   bi('formatNumber(value) - 이름으로 함수 호출', 'formatNumber(value) - Call the function by name'),
   bi('매개변수 - 함수가 입력을 받을 이름', 'Parameter - A name for a function input'),
   bi('인수 - 호출할 때 전달하는 실제 값', 'Argument - The actual value passed in a call'),
   bi('return - 호출한 곳으로 결과 반환', 'return - Send the result back to the caller')]},
  {**bi('스코프 - 변수 이름에 접근할 수 있는 범위', 'Scope - Where a variable name is accessible'), 'details': [
   bi('함수 안의 value - 해당 함수의 지역 매개변수', 'Inner value - A parameter local to the function'),
   bi('바깥 value와 이름은 같지만 별개의 변수', 'The same name as the outer value, but a separate variable')]}
 ]}], ['functions','grammar','practice'])

BODY['8']['panels'][0]['explanation'] = bi(
 'toPrecision(12) - 유효숫자 12자리로 반올림해 표시 · 원래 계산값의 정밀도는 그대로',
 'toPrecision(12) rounds to 12 significant digits for display; the original value is unchanged')

add(9, [
 {**lab('app.ts',22,31, ('함수 전달과 바깥 변수 참조', 'Passing Functions and Capturing Variables')),
  'annotations': [
   {'before': 'buttons.forEach', **bi('[1·2] 함수를 인수로 전달: 순회 콜백', '[1·2] Pass a function: iteration callback')},
   {'before': "button.addEventListener", **bi('[1·2] 함수를 인수로 전달: 클릭 콜백', '[1·2] Pass a function: click callback')},
   {'before': 'const key =', **bi('[3] 클릭 콜백이 바깥 button 참조: 클로저', '[3] Closure: click callback captures button')}
  ]},
 {'kind': 'points', 'label': bi('일급 함수·콜백·클로저', 'First-Class Functions, Callbacks, and Closures'), 'items': [
  {**bi('[1] 일급 함수(First-class function) - 값처럼 다루는 함수', '[1] First-class function - A function treated as a value'), 'details': [
   bi('변수에 저장 · 인수로 전달 · 반환값으로 사용', 'Store in a variable · Pass as an argument · Return as a result')]},
  {**bi('[2] 콜백(Callback) - 다른 함수에 전달해 호출을 맡기는 함수', '[2] Callback - A function passed to be called'), 'details': [
   bi('호출 시점은 전달받은 함수가 결정', 'Invocation timing determined by the receiving function'),
   bi('forEach 콜백 - 순회 중 실행', 'forEach callback - Invoked during iteration'),
   bi('클릭 콜백 - 클릭 이벤트 발생 시 실행', 'Click callback - Invoked when a click event occurs')]},
  {**bi('[3] 클로저(Closure) - 함수와 생성 당시 바깥 환경의 결합', '[3] Closure - A function with its enclosing environment'), 'details': [
   bi('함수가 생성된 바깥 스코프의 변수에 접근 가능', 'Access to variables in the scope where the function was created'),
   bi('클릭 콜백은 나중에 실행되어도 해당 button 참조', 'The click callback retains access to its button when invoked')]}
 ]}], ['functions','events','practice'])

add(10, [
 code(('여러 값을 묶는 객체', 'Grouping Values in an Object'), 'javascript', """
const state = {
  input: '0',
  stored: null,
  operator: null,
  waiting: false,
  hasOperand: false,
  error: '',
  expression: ''
};
""", sourceUrl=f'https://github.com/ajou-hyunseok-oh/pwd-week3/blob/{REVISION}/calculator.ts#L12-L20',
  adaptation='Type annotation omitted for the JavaScript introduction'),
 {'kind': 'points', 'label': bi('객체와 프로퍼티', 'Objects and Properties'), 'items': [
  {**bi('객체(Object) - 관련 데이터를 묶은 값', 'Object - A value grouping related data'), 'details': [
   bi('state - 입력값·연산자 등 계산기 상태를 모은 객체', 'state - An object holding calculator input, operator, and other state')]},
  {**bi('객체 리터럴(Object literal) - 객체 생성 표현식', 'Object literal - An expression that creates an object'), 'details': [
   bi('{ 이름: 값 } 형태로 객체를 직접 생성', 'Create an object directly with { name: value }')]},
  {**bi('프로퍼티(Property) - 이름과 값의 쌍', 'Property - A name–value pair'), 'details': [
   bi("input: '0' - 이름은 input, 값은 문자열 '0'", "input: '0' - The name is input; the value is the string '0'"),
   bi('state.input - 이름으로 접근 · 대입하면 값 변경', 'state.input - Access by name · Assign to change its value')]},
  {**bi('const - 변수의 재할당 불가', 'const - No reassignment of the variable'), 'details': [
   bi('state.count = 1 : 현재 객체의 프로퍼티 값 변경 가능', 'state.count = 1 : Changing the current object’s property is allowed'),
   bi('state = { count: 1 } : 다른 객체로 재할당 불가', 'state = { count: 1 } : Reassignment to another object is prohibited'),
   bi('설계 원리 - 변수의 참조 고정과 객체의 상태 변경을 분리', 'Design principle - Separate a fixed variable reference from changes to object state')]}
 ]},
 code(('const의 재할당과 프로퍼티 변경', 'const Reassignment and Property Updates'), 'javascript', """
const state = { count: 0 };
state.count = 1;
state = { count: 1 };
""", runtimeError='TypeError', expectedLogs=[], annotations=[
  {'before': 'state.count =', **bi('가능: 프로퍼티 값 변경', 'Allowed: update a property value')},
  {'before': 'state =', **bi('불가: 다른 객체를 재할당', 'Not allowed: reassign to another object')}
 ])
], ['objects','const','practice'], layout='object-example')

add(11, [
 code(('상태 참조 · 복사 실험', 'State References · Copy Experiment'), 'javascript', """
const state = { input: '12', view: { error: '' } };
const alias = state;
const copy = { ...state };
const deep = structuredClone(state);
alias.input = '3';
copy.view.error = 'error';
console.log(state.input, copy.input);
console.log(state.view === copy.view);
console.log(state.view === deep.view);
console.log(state.view.error, deep.view.error === '');
""", output='3 12\ntrue\nfalse\nerror true', expectedLogs=[['3','12'],[True],[False],['error',True]]),
 {'kind': 'points', 'label': bi('참조·얕은 복사·깊은 복사', 'References, Shallow Copies, and Deep Copies'), 'items': [
  {**bi('객체 참조(Object reference) - 객체를 가리키는 연결', 'Object reference - A link to an object'), 'details': [
   bi("alias = state - 같은 객체 공유 · input 변경도 공유", "alias = state - Same object, including changes to input")]},
  {**bi('얕은 복사(Shallow copy) - 최상위 값만 복사', 'Shallow copy - Copy only top-level property values'), 'details': [
   bi("{ ...state } - 새 객체 생성 · copy.input은 '12' 유지", "{ ...state } - New object · copy.input stays '12'"),
   bi('중첩된 view는 공유 → error 변경이 원본에도 반영', 'Shared nested view → error changes also affect the original')]},
  {**bi('깊은 복사(Deep copy) - 중첩 객체까지 복제', 'Deep copy - Clone nested objects too'), 'details': [
   bi('structuredClone(state) - 중첩된 view도 새로 생성', 'structuredClone(state) - A new nested view as well'),
   bi("deep.view는 별개 → error는 빈 문자열 유지", "Separate deep.view → error remains an empty string"),
   bi('structuredClone은 함수 등 일부 값은 복제 불가', 'structuredClone cannot clone functions and some other values')]}
 ]}
], ['spread','structured-clone','practice'])

add(12, [
 code(('조건 선택과 값 변환', 'Filtering Items and Transforming Values'), 'javascript', """
const keys = ['1', '+', '2', '='];
const numbers = keys
  .filter((key) => /^[0-9]$/.test(key))
  .map((key) => Number(key));
console.log(numbers);
console.log(keys.length);
const result = numbers.forEach((number) => {
  console.log(number);
});
console.log(result);
""", output='[1, 2]\n4\n1\n2\nundefined', specialExpected='array-methods'),
 {'kind': 'points', 'label': bi('선택·변환·순회의 차이', 'Selection, Transformation, and Iteration'), 'items': [
  {**bi('filter - 조건에 맞는 원소로 새 배열 생성', 'filter - A new array of matching elements'), 'details': [
   bi('콜백의 결과가 참으로 평가되는 원소만 선택', 'Keep elements whose callback result is truthy'),
   bi("한 자리 숫자 문자열만 선택 → ['1', '2']", "Keep single-digit strings → ['1', '2']")]},
  {**bi('map - 원소별 변환 결과로 새 배열 생성', 'map - A new array of transformed values'), 'details': [
   bi('각 원소에 콜백을 적용하고 반환값을 순서대로 수집', 'Apply the callback to each element and collect its return values in order'),
   bi('Number(key)로 문자열을 숫자로 변환 → [1, 2]', 'Convert strings with Number(key) → [1, 2]'),
   bi('이 예제의 콜백은 원본 keys를 변경하지 않음 · 길이 4 유지', 'These callbacks leave keys unchanged · Its length remains 4')]},
  {**bi('forEach - 원소마다 콜백 실행', 'forEach - Execute a callback for each element'), 'details': [
   bi('numbers의 원소를 차례로 출력 → 1, 2', 'Print each element of numbers in order → 1, 2'),
   bi('결과 배열을 만들지 않고 undefined 반환', 'Return undefined without creating a result array')]}
 ]}], ['filter','map','practice'])

add(13, [
 code(('버튼 생성과 클릭 로그', 'Creating a Button and Logging a Click'), 'javascript', """
const button = document.createElement('button');
button.dataset.key = '7';
button.addEventListener('click', () => {
  console.log('click', button.dataset.key);
});
console.log('ready');
button.click();
console.log('done');
""", context='dom', output='ready\nclick 7\ndone', expectedLogs=[['ready'],['click','7'],['done']]),
 {'kind': 'points', 'label': bi('DOM과 이벤트 처리', 'DOM and Event Handling'), 'items': [
  {**bi('DOM - HTML 문서를 표현한 객체 트리', 'DOM - An object tree representing an HTML document'), 'details': [
   bi('Document Object Model · 코드로 문서 읽기·변경', 'Document Object Model · Read and modify the document through code'),
   bi('createElement - 버튼 요소 생성', 'createElement - Create a button element')]},
  {**bi('이벤트(Event) - 발생한 동작을 알리는 신호', 'Event - A signal that an action has occurred'), 'details': [
   bi('click - 버튼 등을 클릭할 때 발생하는 이벤트', 'click - An event triggered by clicking a button or another element')]},
  {**bi('이벤트 핸들러(Event handler) - 이벤트 처리 함수', 'Event handler - A function that handles an event'), 'details': [
   bi('addEventListener - 핸들러 등록 · 클릭 발생 시 호출', 'addEventListener - Register the handler · Invoke it on a click'),
   bi('dataset.key - data-key 속성의 문자열 값 읽기', 'dataset.key - Read the string value of the data-key attribute'),
   bi('button.click() → 핸들러의 click 7 출력 → done 출력', 'button.click() → The handler logs click 7 → Log done')]}
 ]}], ['events'])

add(14, [
 code(('HTTP 요청과 예외 처리', 'HTTP Requests and Error Handling'), 'javascript', """
async function loadExamples() {
  const response = await fetch('/examples.json');
  if (!response.ok) throw new Error('HTTP error');
  return response.json();
}
try {
  const examples = await loadExamples();
  console.log(examples.length);
} catch (error) {
  console.log('load failed');
}
""", context='fetch', executionMode='module', annotations=[
  {'before': 'async function', **bi('[2] async', '[2] async')},
  {'before': 'const response =', 'inline': True, **bi('[1·3·6]', '[1·3·6]')},
  {'before': 'if (!response.ok)', 'inline': True, **bi('[4]', '[4]')},
  {'before': 'return response.json()', 'inline': True, **bi('[1]', '[1]')},
  {'before': 'const examples =', 'inline': True, **bi('[3]', '[3]')},
  {'before': 'console.log(examples.length)', 'inline': True, **bi('[5]', '[5]')},
  {'before': "console.log('load failed')", 'inline': True, **bi('[4]', '[4]')}
 ]),
 {'kind': 'points', 'label': bi('Promise·async·await와 예외 처리', 'Promise, async, await, and Error Handling'), 'items': [
  {**bi('[1] Promise - 비동기 작업의 결과를 나타내는 객체', '[1] Promise - An object representing an async result'), 'details': [
   bi('fetch와 response.json()의 반환값 · 성공 값 또는 실패 이유로 확정', 'Returned by fetch and response.json() · Settles with a value or rejection')]},
  {**bi('[2] async - 비동기 함수를 선언하는 키워드', '[2] async - A keyword declaring an async function'), 'details': [
   bi('반환값은 Promise의 성공 값 · 예외는 실패 이유로 전달', 'Return value → Promise fulfillment · Exception → Rejection')]},
  {**bi('[3] await - Promise의 완료를 기다리는 표현식', '[3] await - An expression that waits for a Promise'), 'details': [
   bi('현재 비동기 흐름을 멈추고 성공 값 수신 · 실패 시 예외 발생', 'Pause the current async flow · Receive its value or throw on rejection'),
   bi('대기 중에도 다른 이벤트 처리 가능', 'Other events can be handled while waiting')]},
  {**bi('[4] try/catch - 실행 중 발생한 예외 처리', '[4] try/catch - Handle exceptions during execution'), 'details': [
   bi('fetch는 HTTP 오류 응답도 반환 → response.ok 확인', 'fetch also returns HTTP error responses → Check response.ok'),
   bi('await의 실패나 직접 throw한 예외 → catch에서 처리', 'Rejected await or explicit throw → Handle in catch')]}
 ]},
 table(('동기와 비동기의 차이', 'Synchronous and Asynchronous Execution'),
  [('방식', 'Mode'), ('실행 흐름', 'Execution flow')], [
   [('[5] 동기(Synchronous)', '[5] Synchronous'),
    ('console.log 호출 완료 → 다음 코드 실행', 'Finish console.log → Continue')],
   [('[6] 비동기(Asynchronous)', '[6] Asynchronous'),
    ('fetch 응답 대기 중 다른 코드 진행 가능', 'Other code can run while fetch is pending')]
  ])
], ['fetch'], layout='async-example')
BODY['14']['panels'][1]['explanation'] = bi(
 '최상위 await는 모듈에서 사용 · 웹 서버로 열고 <script type="module">로 실행',
 'Top-level await requires a module · Serve over HTTP and use <script type="module">')

add(15, [
 code(('연산 함수를 값으로 전달 · JavaScript', 'Passing an Operation as a Value · JavaScript'), 'javascript', """
const add = (left, right) => left + right;
const multiply = (left, right) => left * right;
function calculate(left, right, operation) {
  return operation(left, right);
}
console.log(calculate(12, 3, add));
console.log(calculate(12, 3, multiply));
""", output='15\n36', expectedLogs=[[15],[36]], annotations=[
  {'before': 'const add =', 'inline': True, **bi('[1]', '[1]')},
  {'before': 'const multiply =', 'inline': True, **bi('[1]', '[1]')},
  {'before': 'function calculate', **bi('[2] 고차 함수', '[2] Higher-order function')}
 ]),
 {'kind': 'points', 'label': bi('함수를 인수로 전달하는 방법', 'Passing Functions as Arguments'), 'items': [
  {**bi('[1] 함수 값(Function value) - 값으로 다루는 함수', '[1] Function value - A function used as a value'), 'details': [
   bi('add · multiply - 연산을 수행할 함수 자체', 'add · multiply - The functions themselves'),
   bi('add(12, 3) - 함수를 호출한 결과인 15', 'add(12, 3) - The result of calling the function: 15'),
   bi('나중에 호출하려면 결과가 아닌 함수 자체를 인수로 전달', 'Pass the function itself to call it later, rather than its result')]},
  {**bi('[2] 고차 함수(Higher-order function) - 함수를 다루는 함수', '[2] Higher-order function - A function operating on functions'), 'details': [
   bi('다른 함수를 인수로 받거나 결과로 반환', 'Accept another function as an argument or return one'),
   bi('calculate - 전달받은 operation을 두 숫자로 호출', 'calculate - Call the supplied operation with two numbers'),
   bi('같은 입력·출력 형태의 함수 교체 → 호출 구조 유지 · 연산 변경', 'Swap functions with matching inputs and outputs → Change the operation, keep the call structure'),
   bi('add 전달 → 15 · multiply 전달 → 36', 'Pass add → 15 · Pass multiply → 36')]}
 ]}], ['functions','practice'])

add(16, [
 code(('계산기 상태를 이용한 오류 실험', 'Error Experiment with Calculator State'), 'javascript', """
const state = { input: '12', error: '' };
const alias = state;
console.log(state.input + 3);
console.log(Number(state.inpt));
alias.input = '0';
console.log(state.input);
""", output='123\nNaN\n0', specialExpected='state-errors', annotations=[
  {'before': 'console.log(state.input +', 'inline': True, **bi('[1]', '[1]')},
  {'before': 'console.log(Number', 'inline': True, **bi('[2]', '[2]')},
  {'before': 'const alias =', 'inline': True, **bi('[3]', '[3]')},
  {'before': 'alias.input =', 'inline': True, **bi('[3]', '[3]')}
 ], explanation=bi('논리 오류(Logic error) - 문법은 유효하지만 의도와 다른 결과 발생', 'Logic error - Valid syntax, but a result different from the intended one')),
 {'kind': 'points', 'label': bi('잘못된 결과가 생기는 원리', 'Why Incorrect Results Occur'), 'items': [
  {**bi('[1] 암묵적 변환(Implicit conversion) - 자동 타입 변환', '[1] Implicit conversion - Automatic type conversion'), 'details': [
   bi("문자열 '12'와 숫자 3의 + → 문자열 연결", "String '12' + number 3 → String concatenation"),
   bi("숫자 덧셈 결과 15 대신 문자열 '123' 생성", "The string '123' instead of the numeric sum 15")]},
  {**bi('[2] 속성 오타(Property typo) - 잘못된 속성 이름', '[2] Property typo - An incorrect property name'), 'details': [
   bi('input을 inpt로 작성 → 없는 속성이므로 undefined', 'input misspelled as inpt → Missing property yields undefined'),
   bi('Number(undefined) → 예외 없이 NaN 반환', 'Number(undefined) → NaN without throwing an exception')]},
  {**bi('[3] 참조 공유(Shared reference) - 같은 객체에 접근', '[3] Shared reference - Access to the same object'), 'details': [
   bi('alias = state - 객체 복제 없이 참조만 복사', 'alias = state - Copy the reference without cloning the object'),
   bi("alias.input 변경 → state.input도 '0'으로 변경", "Change alias.input → state.input also becomes '0'")]}
 ]}], ['basics','spread','practice'])

add(17, [
 table(('계산기 오류와 검사 위치', 'Calculator Errors and Checks'),
  [('상황', 'Situation'), ('검사', 'Check')], [
  [('add("12", 3)', 'add("12", 3)'), ('[1] 타입 검사 - number 매개변수에 문자열 전달', '[1] Type check - A string passed to a number parameter')],
  [('state.inpt 오타', 'state.inpt typo'), ('[1] 타입 검사 - 객체 타입에 없는 속성 접근', '[1] Type check - A property absent from the object type')],
  [('divide(12, 0)', 'divide(12, 0)'), ('[2] 실행 중 검사 - 나누는 값이 0인지 확인', '[2] Runtime check - Check whether the divisor is zero')],
  [('setResult(Infinity)', 'setResult(Infinity)'), ('[2] 실행 중 검사 - 결과가 유한한 수인지 확인', '[2] Runtime check - Check whether the result is finite')]]),
 {'kind': 'points', 'label': bi('정적 검사와 실행 중 검사', 'Static and Runtime Checks'), 'items': [
  {**bi('[1] 정적 타입 검사(Static type checking) - 실행 전 검사', '[1] Static type checking - Checks before execution'), 'details': [
   bi('타입 정보로 허용되지 않는 값의 사용 발견', 'Detect uses of values that violate their types'),
   bi('매개변수의 타입 불일치 · 객체 타입에 없는 속성 확인', 'Check parameter type mismatches and unknown properties')]},
  {**bi('[2] 실행 중 검사(Runtime checking) - 실제 값 검증', '[2] Runtime checking - Validation of actual values'), 'details': [
   bi('실행 시 입력·결과가 동작 규칙을 만족하는지 확인', 'Check inputs and results against program rules at runtime'),
   bi('0 · NaN · Infinity도 number에 포함', 'The number type also includes 0, NaN, and Infinity'),
   bi('값의 허용 여부는 타입과 별개로 조건문 등을 통해 검사', 'Validate allowed values with conditions in addition to types')]}
 ]}], ['basics','practice'])

BODY['17']['takeaway'] = bi(
 'JavaScript의 한계 - 기본 정적 타입 검사가 없어 타입 오류를 실행 전에 놓치기 쉬움',
 'JavaScript limitation - No built-in static type checking, so type errors can go undetected before execution')

add(18, [
 flow(('2012 · Microsoft', '2012 · Microsoft'),
  ('대규모 JavaScript 코드의 변경과 협업', 'Changes and collaboration in large JavaScript projects'),
  ('2012년 10월 1일 TypeScript 공개', 'TypeScript publicly unveiled on October 1, 2012'),
  ('타입 계약 · 편집기 지원 · 오류 조기 발견', 'Type contracts · Editor support · Earlier error detection')),
 {'kind': 'points', 'label': bi('TypeScript의 정의와 역할', 'What TypeScript Adds'), 'items': [
  {**bi('TypeScript - JavaScript에 타입 검사를 더한 언어', 'TypeScript - JavaScript with static type checking'), 'details': [
   bi('타입 문법으로 값의 종류·구조 표현', 'Type syntax describes the kinds and shapes of values'),
   bi('실행 전 오류 발견 · 편집기의 코드 작성 지원', 'Detect errors before execution · Editor assistance')]},
  {**bi('타입 계약(Type contract) - 허용할 값의 형태를 명시', 'Type contract - A specification of allowed value shapes'), 'details': [
   bi('함수의 입력·출력 타입과 객체의 속성 타입 정의', 'Define function input and output types and object property types'),
   bi('정해진 타입과 다른 사용 → 실행 전 오류 표시', 'Use that violates the declared types → An error before execution')]},
  {**bi('컴파일(Compilation) - 실행할 코드로 변환', 'Compilation - Translation into code to execute'), 'details': [
   bi('TypeScript → 타입 표기 제거 → JavaScript 출력', 'TypeScript → Remove type annotations → Output JavaScript'),
   bi('타입 표기는 실행 중 입력을 검사하지 않음 · 별도 검증 필요', 'Type annotations do not check runtime input · Separate validation needed')]}
 ]}], ['ts-history', 'basics'], layout='split')

add(19, [
 {**lab('calculator.ts',22,24, ('[1] TypeScript · 입력과 반환 타입', '[1] TypeScript · Input and Return Types')),
  'annotations': [{'before': 'function formatNumber', **bi('[1] value: number - 입력 · : string - 반환', '[1] value: number - Input · : string - Return')}]},
 code(('[2] 컴파일된 JavaScript · 타입 제거', '[2] Compiled JavaScript · Types Removed'), 'javascript', """
function formatNumber(value) {
  return Number(value.toPrecision(12)).toString();
}
""", annotations=[{'before': 'function formatNumber', **bi('[2] 타입 표기 제거 · 실행 구문 유지', '[2] Type annotations removed · Runtime code kept')}]),
 {'kind': 'points', 'label': bi('실행 전 확인하는 타입', 'Types Checked Before Execution'), 'items': [
  {**bi('[1] 정적 타입 검사(Static type checking) - 실행 전 검사', '[1] Static type checking - Checks before execution'), 'details': [
   bi('value: number - 숫자 인수만 허용', 'value: number - Accept only numeric arguments'),
   bi(': string - 문자열 반환 여부 확인', ': string - Check that the return value is a string'),
   bi('함수의 입력·출력 타입에 맞지 않는 사용 발견', 'Detect use that violates the function’s input or output types')]}
 ]},
 {'kind': 'points', 'label': bi('컴파일 뒤에 남는 동작', 'Behavior After Compilation'), 'items': [
  {**bi('[2] 컴파일(Compilation) - 실행할 코드로 변환', '[2] Compilation - Translation into code to execute'), 'details': [
   bi('매개변수·반환값의 타입 표기 제거 → JavaScript 출력', 'Remove parameter and return type annotations → Output JavaScript'),
   bi('Number·toPrecision·toString 호출은 실행 코드로 유지', 'Calls to Number, toPrecision, and toString remain'),
   bi('타입 표기는 실행 중 입력을 검사하지 않음 · 별도 검증 필요', 'Type annotations do not validate runtime input · Separate checks needed')]}
 ]},
 ], ['basics','practice'], layout='equal')

BODY['19']['panels'][1]['explanation'] = bi(
 '표시용 반올림 · 원래 계산값의 정밀도를 높이는 처리는 아님',
 'Rounding for display does not increase the precision of the original calculation')
BODY['19']['takeaway'] = bi(
 'TypeScript의 장점 - 타입 오류를 실행 전에 발견하고 코드 변경·협업의 안정성 향상',
 'TypeScript benefits - Catch type errors before execution and make code changes and collaboration safer')

add(20, [
 code(('초기값에 따른 타입 추론', 'Type Inference from Initial Values'), 'typescript', """
let input = '12';
const value = Number(input);
const waiting: boolean = true;
input = 12;
""", errors=[2322]),
 concepts(('타입 표기와 추론', 'Annotations and Inference'),
  group('[1] 타입 표기(Type annotation) - 타입을 직접 명시', '[1] Type annotation - An explicitly declared type',
   ('waiting: boolean - 참·거짓만 허용', 'waiting: boolean - Only true or false allowed')),
  group('[2] 타입 추론(Type inference) - 값에서 타입 판단', '[2] Type inference - A type determined from a value',
   ("input의 초기값 '12' → string으로 추론", "Initial input value '12' → Inferred as string"),
   ('input = 12 → 숫자 대입은 타입 오류', 'input = 12 → Assigning a number is a type error')),
  group('[3] 형변환(Type conversion) - 실제 값의 타입 변환', '[3] Type conversion - Conversion of an actual value',
   ('Number(input) - 문자열을 숫자로 변환', 'Number(input) - Convert a string to a number'),
   ('타입 표기·추론은 값 자체를 변환하지 않음', 'Annotations and inference do not convert values')))], ['types','practice'])

BODY['20']['panels'][0]['annotations'] = [
 {'before': 'let input =', 'inline': True, **bi('[2]', '[2]')},
 {'before': 'const value =', 'inline': True, **bi('[3]', '[3]')},
 {'before': 'const waiting:', 'inline': True, **bi('[1]', '[1]')},
 {'before': 'input = 12', 'inline': True, **bi('[2]', '[2]')},
]

add(21, [
 {**lab('operations.ts',3,7, ('두 인수와 반환값의 타입', 'Types of Arguments and Return Values')), 'concepts': [group('[1] 함수 타입(Function type) - 입력·출력의 타입 계약', '[1] Function type - A contract for input and output types',
 ('BinaryOperation - 두 number를 받아 number를 반환', 'BinaryOperation - Takes two numbers and returns a number'),
 ('매개변수 타입과 반환 타입을 함께 정의', 'Specify parameter types and the return type together'))]},
 {**code(('인수의 타입 검사 · 호출 실험', 'Argument Type Checking · Call Exercise'), 'typescript', """
add(12, 3);
add('12', 3);
""", prelude='declare const add: (left: number, right: number) => number;', errors=[2345]), 'concepts': [group('[2] 인수 검사 - 매개변수 타입과 일치 여부 확인', '[2] Argument checking - Check against parameter types',
 ('add(12, 3) - 숫자 인수이므로 통과', 'add(12, 3) - Numeric arguments pass'),
 ("add('12', 3) - 문자열 인수이므로 타입 오류", "add('12', 3) - A string argument causes a type error"),
 ("number 표기는 문자열 '12'를 숫자로 변환하지 않음", "A number annotation does not convert the string '12'"))]}], ['ts-functions','practice'], layout='equal')

BODY['21']['panels'][0]['annotations'] = [
 {'before': 'type BinaryOperation', 'inline': False, **bi('[1]', '[1]')},
]
BODY['21']['panels'][1]['annotations'] = [
 {'before': 'add(', 'inline': True, **bi('[2]', '[2]')},
]

add(22, [
 {**code(('interface - 객체가 갖춰야 할 구조 정의', 'interface - Define the Required Object Shape'), 'typescript', """
interface State {
  input: string;
  waiting: boolean;
}
const state: State = { input: '12', waiting: false };
console.log(state.input, state.waiting);
""", output='12 false'), 'concepts': [
  group('인터페이스(Interface) - 객체의 속성과 타입을 정하는 계약', 'Interface - A contract for object properties and types',
   ('State - input은 string · waiting은 boolean으로 정의', 'State - Define input as string and waiting as boolean'),
   ('[1] state: State - 객체가 이 구조를 갖췄는지 검사', '[1] state: State - Check that the object has this shape'),
   ('속성 누락이나 input: 12 작성 시 타입 오류', 'Missing properties or input: 12 cause a type error'))]},
 {**code(('type - 타입에 이름을 붙여 재사용', 'type - Name a Type for Reuse'), 'typescript', """
type State = {
  input: string;
  waiting: boolean;
};
const first: State = { input: '12', waiting: false };
const next: State = { input: '34', waiting: true };
console.log(first.input, next.input);
""", output='12 34'), 'concepts': [
  group('타입 별칭(Type alias) - 타입을 재사용하기 위한 이름', 'Type alias - A name for reusing a type',
   ('type State = { ... } - 객체 타입에 State라는 이름 부여', 'type State = { ... } - Name the object type State'),
   ('[1] first와 next에 State 적용 → 같은 속성·타입 검사', '[1] Apply State to first and next → Check the same shape'),
   ('객체뿐 아니라 기본 타입·유니온에도 이름 부여 가능', 'Can also name primitive types and unions'))]}
], ['types'], layout='equal')

BODY['22']['panels'][0]['annotations'] = [
 {'before': 'const state:', 'inline': False, **bi('[1]', '[1]')},
]
BODY['22']['panels'][1]['annotations'] = [
 {'before': 'const first:', 'inline': False, **bi('[1]', '[1]')},
]
BODY['22']['takeaway'] = bi(
 'interface - 객체가 갖춰야 할 구조 정의 · type - 타입에 이름을 붙여 여러 곳에서 재사용',
 'interface - Define the required object shape · type - Give a type a name for reuse')

add(23, [
 {**lab('operations.ts',2,3, ('연산 기호와 함수 타입', 'Operator Literals and Function Types')), 'concepts': [group('[1] 리터럴 타입(Literal type) - 특정 값만 허용', '[1] Literal type - Allow one exact value',
 ("'+' - 더하기 기호 하나만 허용하는 타입", "'+' - A type allowing only the plus symbol")),
 group('[2] 유니온(Union) - 여러 타입 중 하나를 허용', '[2] Union - Allow any one of several types',
 ('|로 타입 연결 · Operator는 네 연산 기호로 제한', 'Join types with | · Operator allows four operator symbols'))]},
 {**code(('허용하는 연산 기호 · 타입 실험', 'Allowed Operators · Type Exercise'), 'typescript', """
let operator: Operator | null = null;
operator = '+';
operator = '%';
""", prelude="type Operator = '+' | '-' | '*' | '/';", errors=[2322]), 'concepts': [group('[3] Operator | null - 연산 기호 또는 미선택', '[3] Operator | null - An operator or no selection',
 ("null - 미선택 · '+' - 허용된 연산 기호", "null - No selection · '+' - An allowed operator"),
 ("'%' - Operator에도 null에도 속하지 않아 타입 오류", "'%' - Neither an Operator nor null, so a type error"))]},
 ], ['types','practice'], layout='equal')

BODY['23']['panels'][0]['annotations'] = [
 {'before': 'type Operator', 'inline': False, **bi('[1·2]', '[1·2]')},
]
BODY['23']['panels'][1]['annotations'] = [
 {'before': 'let operator:', 'inline': True, **bi('[3]', '[3]')},
 {'before': "operator = '%'", 'inline': True, **bi('[3]', '[3]')},
]

add(24, [
 code(('선택적 속성 선언 → 생략 → 확인 후 사용', 'Optional Property → Omission → Checked Use'), 'typescript', """
type Button = { key?: string };
const withKey: Button = { key: 'add' };
const withoutKey: Button = {};
console.log(withKey.key);
console.log(withoutKey.key);
for (const button of [withKey, withoutKey]) {
  const key = button.key;
  if (key !== undefined) {
    console.log(key.toUpperCase());
  }
}
""", output='add\nundefined\nADD'),
 concepts(('선택적 속성과 안전한 사용', 'Optional Properties and Safe Use'),
  group('[1] 선택적 속성(Optional property) - 생략 가능한 속성', '[1] Optional property - A property that may be omitted',
   ('key?: string - 생략 가능한 문자열 속성', 'key?: string - An optional string property'),
   ("withKey는 { key: 'add' } · withoutKey는 {}로 생성", "withKey uses { key: 'add' } · withoutKey uses {}")),
  group('[2] 값의 부재 - 생략한 속성을 읽으면 undefined', '[2] Missing value - Reading an omitted property yields undefined',
   ('withKey.key는 add · withoutKey.key는 undefined 출력', 'withKey.key prints add · withoutKey.key prints undefined'),
   ('읽은 값의 타입은 string | undefined', 'The property is read as string | undefined')),
  group('[3] 값 확인 - undefined 제외 후 문자열 기능 사용', '[3] Value check - Exclude undefined before string operations',
   ('key !== undefined인 경우에만 toUpperCase() 호출', 'Call toUpperCase() only when key !== undefined'),
   ('add는 ADD 출력 · 속성을 생략한 객체는 조건문 건너뜀', 'add prints ADD · The object without key skips the block')))], ['narrow','types'])

BODY['24']['panels'][0]['annotations'] = [
 {'before': 'type Button =', 'inline': True, **bi('[1]', '[1]')},
 {'before': 'console.log(withoutKey.key)', 'inline': True, **bi('[2]', '[2]')},
 {'before': 'if (key !== undefined)', 'inline': False, **bi('[3]', '[3]')},
]

BODY['24']['takeaway'] = bi(
 '기본 설정에서는 key: undefined도 허용 · 이를 막으려면 exactOptionalPropertyTypes 활성화',
 'By default, key: undefined is also allowed · Enable exactOptionalPropertyTypes to reject it')

add(25, [
 lab('calculator.ts',84,93, ('조기 반환과 계산 실행', 'Early Return and Calculation')),
 concepts(('타입 좁히기와 가드', 'Narrowing and Guards'),
  group('[1] 타입 좁히기(Narrowing) - 가능한 타입 범위 축소', '[1] Narrowing - Reducing the possible types',
   ('조건과 실행 경로를 근거로 타입 판단', 'Determine types from conditions and control flow'),
   ('null인 경로 제외 → stored는 number · operator는 Operator', 'Exclude null paths → stored is number · operator is Operator')),
  group('[2] 가드(Guard) - 조건을 먼저 검사해 실행 제한', '[2] Guard - An initial check that restricts execution',
   ('처리할 수 없는 상태 → return으로 함수 종료', 'An invalid state → Exit the function with return'),
   ('hasOperand - 두 번째 입력이 있어야 계산하는 동작 규칙', 'hasOperand - A second operand is required for calculation')))], ['narrow','practice'])

BODY['25']['panels'][0]['annotations'] = [
 {'before': 'if (', 'inline': False, **bi('[1·2]', '[1·2]')},
 {'before': 'setResult(', 'inline': False, **bi('[1]', '[1]')},
]

add(26, [
 {**code(('any · 검사 우회', 'any · Bypassing Checks'), 'typescript', """
const raw: any = 12;
raw.toUpperCase();
""", runtimeError='TypeError'), 'concepts': [group('[1] any - 해당 값의 타입 검사 생략', '[1] any - Skip type checks on the value',
 ('없는 메서드 호출도 타입 검사 통과', 'Even a missing method passes type checking'),
 ('숫자 12의 toUpperCase 호출 → 실행 시 TypeError', 'Calling toUpperCase on 12 → A runtime TypeError'))]},
 {**code(('unknown · 검사 후 사용', 'unknown · Check Before Use'), 'typescript', """
function normalize(raw: unknown): string {
  if (typeof raw === 'string') {
    return raw.toUpperCase();
  }
  return 'not a string';
}
console.log(normalize(12));
""", output='not a string'), 'concepts': [group('[2] unknown - 확인 후 사용하는 미지의 타입', '[2] unknown - An unknown type checked before use',
 ('모든 값을 받을 수 있지만 사용 전 타입 확인 필요', 'Accept any value, but check its type before use'),
 ('typeof로 string 확인 → toUpperCase 호출 가능', 'Check string with typeof → toUpperCase becomes available'),
 ('12는 문자열이 아님 → not a string 반환', '12 is not a string → Return not a string'))]}], ['ts-functions'], layout='equal')

BODY['26']['panels'][0]['annotations'] = [
 {'before': 'const raw:', 'inline': True, **bi('[1]', '[1]')},
]
BODY['26']['panels'][1]['annotations'] = [
 {'before': 'function normalize', 'inline': False, **bi('[2]', '[2]')},
]

add(27, [
 code(('as는 값 검사나 변환이 아님', 'as Does Not Validate or Convert Values'), 'typescript', """
const raw: unknown = { value: '12' };
const claimed = raw as { value: number };
console.log(claimed.value + 1);
if (
  typeof raw === 'object' &&
  raw !== null &&
  'value' in raw &&
  typeof raw.value === 'number'
) {
  console.log(raw.value + 1);
} else {
  console.log('invalid value');
}
""", output='121\ninvalid value'),
 concepts(('타입 단언과 실제 검증', 'Type Assertions and Validation'),
  group('[1] 타입 단언(Type assertion) - 컴파일러의 타입 판단 지정', '[1] Type assertion - Tell the compiler which type to use',
   ('as - 실제 값을 검사하거나 변환하지 않음', 'as - No checking or conversion of the actual value'),
   ("claimed.value는 문자열 '12' 그대로 → + 1의 결과는 '121'", "claimed.value remains the string '12' → + 1 produces '121'")),
  group('[2] 런타임 검증(Runtime validation) - 실행 중 실제 값 검사', '[2] Runtime validation - Check actual values at runtime',
   ('객체 여부 → null 제외 → value 존재 → number 여부 확인', 'Check object → Exclude null → Check value exists → Check number'),
   ('조건 통과 시에만 숫자로 사용 · 예제는 invalid value 출력', 'Use as a number only after passing · This example prints invalid value')))], ['narrow', 'types'], layout='split')

BODY['27']['panels'][0]['annotations'] = [
 {'before': 'const claimed =', 'inline': True, **bi('[1]', '[1]')},
 {'before': 'if (', 'inline': False, **bi('[2]', '[2]')},
]

add(28, [
 code(('입력과 반환값을 연결하는 T', 'T Relates the Input and Return Value'), 'typescript', """
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const value = first([12, 3]);
const operation = first([{ id: 'add', symbol: '+' }]);
console.log(value);
console.log(operation?.id);
console.log(first<number>([]));
""", output='12\nadd\nundefined'),
 concepts(('타입 매개변수와 재사용', 'Type Parameters and Reuse'),
  group('[1] 제네릭(Generic) - 타입을 바꿔 같은 로직 재사용', '[1] Generic - Reuse logic across different types',
   ('타입 매개변수 T로 입력과 반환값의 타입 관계 유지', 'Type parameter T preserves the relation between input and output'),
   ('T[]의 원소 타입 → 반환값의 T와 연결', 'Element type of T[] → Linked to T in the return type')),
  group('[2] 타입 추론(Type inference) - 인수에서 T 결정', '[2] Type inference - Determine T from the argument',
   ('숫자 배열 → number · 객체 배열 → 해당 객체 타입', 'Number array → number · Object array → Its object type'),
   ('any와 달리 입력·출력의 타입 관계 유지', 'Preserve the input/output type relation, unlike any')),
  group('[3] T | undefined - 빈 배열의 가능성 표현', '[3] T | undefined - Account for an empty array',
   ('빈 배열의 첫 원소는 undefined · ?.로 안전하게 속성 접근', 'An empty array yields undefined · ?. accesses a property safely')))], ['generic'], layout='split')

BODY['28']['panels'][0]['annotations'] = [
 {'before': 'function first', 'inline': False, **bi('[1·3]', '[1·3]')},
 {'before': 'const value =', 'inline': True, **bi('[2]', '[2]')},
 {'before': 'const operation =', 'inline': True, **bi('[2]', '[2]')},
 {'before': 'console.log(first', 'inline': True, **bi('[3]', '[3]')},
]

add(29, [
 {**code(('필요한 속성을 가진 객체 사용', 'Use an Object with the Required Property'), 'typescript', """
type Named = { name: string };
const operation = { name: 'Add', symbol: '+' };
const named: Named = operation;
console.log(named.name);
""", output='Add', expectedLogs=[['Add']]), 'concepts': [
  group('[1] 구조적 타입(Structural typing) - 구조로 호환성 판단', '[1] Structural typing - Compatibility based on shape',
   ('Named에 필요한 속성은 name: string', 'Named requires the property name: string'),
   ('operation은 조건을 충족 → Named 변수에 대입 가능', 'operation meets the requirement → Assignable to Named'),
   ('기존 객체 변수의 추가 속성 symbol은 대입을 막지 않음', 'The extra symbol on the existing object variable is allowed'))]},
 {**code(('속성이 없거나 타입이 다르면 오류', 'Missing Properties or Wrong Types Cause Errors'), 'typescript', """
type Named = { name: string };
const missing = { symbol: '+' };
const wrong = { name: 12 };
const a: Named = missing;
const b: Named = wrong;
""", errors=[2741,2322]), 'concepts': [
  group('[2] 타입 검사 - 필수 속성과 속성 타입 확인', '[2] Type checking - Check required properties and types',
   ('missing은 name이 없음 → TS2741', 'missing has no name → TS2741'),
   ('wrong.name은 number → string 조건 위반 · TS2322', 'wrong.name is number → Violates string requirement · TS2322'))]}
], ['compat','types'], layout='equal')
BODY['29']['panels'][0]['annotations'] = [
 {'before': 'const named:', 'inline': True, **bi('[1]', '[1]')},
]
BODY['29']['panels'][1]['annotations'] = [
 {'before': 'const a:', 'inline': True, **bi('[2]', '[2]')},
 {'before': 'const b:', 'inline': True, **bi('[2]', '[2]')},
]
BODY['29']['takeaway'] = bi(
 '타입 이름이 아니라 필요한 속성과 타입으로 판단 · 새 객체 리터럴은 추가 속성 검사도 적용',
 'Required properties and types determine compatibility · Fresh object literals also receive excess property checks')

# Four connected calculator examples, simplified for the agreed learning goals.
add(30, [
 code(('숫자 2 버튼의 클릭 처리', 'Handle a Click on the Digit 2 Button'), 'typescript', """
const state = { input: '1' };
const button = document.querySelector('button')!;
const display = document.querySelector('output')!;
function render(): void {
  display.textContent = state.input;
}
button.addEventListener('click', () => {
  state.input += '2';
  render();
});
render();
""", context='dom'),
 concepts(('이벤트 → 상태 → 화면', 'Event → State → UI'),
  group('[1] 이벤트(Event) - 동작을 시작시키는 사건', '[1] Event - An occurrence that triggers an action',
   ('클릭이 발생하면 등록한 콜백 실행 · 이벤트 기반 동작', 'A click runs the registered callback · Event-driven behavior')),
  group('[2] 상태(State) - 프로그램이 현재 기억하는 데이터', '[2] State - Data the program currently remembers',
   ("state.input: '1' → '12' · 클릭 처리에서 상태 변경", "state.input: '1' → '12' · The handler changes state")),
  group('[3] 데이터 흐름 - 변경한 상태를 화면에 반영', '[3] Data flow - Reflect the updated state in the UI',
   ('render()가 현재 입력을 읽어 표시창 갱신', 'render() reads the current input and updates the display')))
], ['events','elm-architecture'])
BODY['30']['panels'][0]['explanation'] = bi(
 'HTML 요소 생성 후 실행 · !는 비-null 단언이며 요소 존재를 실행 중 검사하지 않음',
 'Run after the HTML elements exist · ! is a non-null assertion, not a runtime check')
BODY['30']['panels'][0]['annotations'] = [
 {'before':'button.addEventListener', 'inline':False, **bi('[1]', '[1]')},
 {'before':"state.input +=", 'inline':True, **bi('[2]', '[2]')},
 {'before':'display.textContent', 'inline':True, **bi('[3]', '[3]')},
]
BODY['30']['takeaway'] = bi('웹 프로그램은 사건에 반응하여 상태를 바꾸고, 그 상태를 화면에 반영', 'Web programs respond to events by changing state and reflecting it in the UI')

add(31, [
 code(('입력값을 보관하고 표시 문자열 계산', 'Store Input and Derive Display Text'), 'typescript', """
const state = { input: '1234' };
function displayText(input: string): string {
  return Number(input).toLocaleString('en-US');
}
console.log(state.input);
console.log(displayText(state.input));
state.input = '5678';
console.log(displayText(state.input));
""", output='1234\n1,234\n5,678', expectedLogs=[['1234'],['1,234'],['5,678']]),
 concepts(('기억할 값과 계산할 값', 'Stored Values and Derived Values'),
  group('[1] 최소 상태 - 다음 동작에 필요한 값만 기억', '[1] Minimal state - Remember what later actions need',
   ('입력·이전 숫자·연산 등 · 예제에서는 정수 입력만 표시', 'Input, previous number, operator · This example shows integer input')),
  group('[2] 파생 값(Derived value) - 상태에서 계산하는 값', '[2] Derived value - A value computed from state',
   ("'1234' → '1,234' · 표시 문자열을 별도 상태로 저장하지 않음", "'1234' → '1,234' · No separate state for display text")),
  group('중복 상태 - 같은 정보를 따로 저장하면 불일치 가능', 'Duplicate state - Separate copies can disagree',
   ('입력만 바꾸고 표시 문자열 갱신을 빠뜨리면 이전 값 표시', 'Updating input but forgetting stored display text leaves a stale value')))
], ['thinking-react'])
BODY['31']['panels'][0]['explanation'] = bi(
 '웹에서는 입력이 자주 바뀌므로, 파생 값을 다시 계산해 데이터와 화면의 불일치를 줄임',
 'Deriving values from state keeps the UI consistent as user input changes')
BODY['31']['panels'][0]['annotations'] = [
 {'before':'const state', 'inline':True, **bi('[1]', '[1]')},
 {'before':'return Number', 'inline':True, **bi('[2]', '[2]')},
]
BODY['31']['takeaway'] = bi('연산 결과도 다음 계산에 필요하면 상태로 저장 · 기존 상태로 구할 수 있는 값은 파생', 'Store arithmetic results when later work needs them · Derive values available from existing state')

add(32, [
 {**code(('명령형 · DOM 변경을 직접 지정', 'Imperative · Specify DOM Updates'), 'typescript', """
const display = document.querySelector('output')!;
function render(input: string): void {
  display.textContent = input;
}
render('12');
""", context='dom'), 'concepts': [
  group('명령형(Imperative) - 실행할 변경 단계를 지정', 'Imperative - Specify the update steps',
   ('표시창을 찾고 textContent에 입력값 대입', 'Find the display and assign input to textContent')),
  group('상태 중심 설계 - 화면 변경을 render에 모으기', 'State-driven UI updates - Gather updates in render',
   ('변경을 한곳에 모아도 DOM 조작 자체는 명령형', 'Centralizing updates does not make DOM operations declarative'))]},
 {**code(('선언형 · React에서 상태에 맞는 화면 기술', 'Declarative · Describe UI with React'), 'tsx', """
function Display({ input }: { input: string }) {
  return <output>{input}</output>;
}
""", context='react', verification='paradigm-display'), 'concepts': [
  group('선언형(Declarative) - 원하는 화면 결과를 기술', 'Declarative - Describe the desired UI result',
   ('input이 화면 내용이 되는 관계를 JSX로 표현', 'JSX expresses that input becomes the display content')),
  group('상태와 화면의 대응 - 전달된 값으로 화면 결정', 'State-to-UI mapping - Supplied values determine the UI',
   ("부모의 상태 setter 호출 → 새 input prop으로 재렌더링", "The parent’s state setter triggers a re-render with the new input prop"))]}
], ['react','thinking-react'], layout='equal')
BODY['32']['panels'][0]['explanation'] = bi(
 '사용 상황 - 입력창에 포커스를 주거나 특정 위치로 스크롤하는 등 직접 제어가 필요할 때',
 'Use when direct control is needed, such as focusing an input or scrolling to a position')
BODY['32']['panels'][1]['explanation'] = bi(
 '사용 상황 - 검색 결과·로딩·오류처럼 상태에 따라 화면 구성이 달라질 때',
 'Use when state determines the UI, such as search results, loading, or error views')
BODY['32']['takeaway'] = bi('현재 상태에서 무엇을 보여야 하는지 먼저 결정 · 같은 표시 결과, 다른 표현 방식', 'Decide what the current state should show · Same display result, different ways to express it')

add(33, [
 code(('계산한 값을 상태와 화면에 반영', 'Calculate, Then Update State and UI'), 'typescript', """
function add(a: number, b: number): number {
  return a + b;
}
const state = { input: '12' };
const button = document.querySelector('button')!;
const display = document.querySelector('output')!;
function render(): void {
  display.textContent = state.input;
}
button.addEventListener('click', () => {
  const result = add(Number(state.input), 3);
  state.input = String(result);
  render();
});
render();
""", context='dom'),
 concepts(('계산과 변경의 역할 분리', 'Separate Calculations from Changes'),
  group('[1] 순수 함수 - 같은 입력에 같은 결과 · 외부 변경 없음', '[1] Pure function - Same input, same output; no external changes',
   ('add(12, 3) → 15 · DOM 없이 계산만 검증 가능', 'add(12, 3) → 15 · Test the calculation without a DOM')),
  group('[2] 부수 효과 - 함수 밖에서 관찰되는 변경', '[2] Side effect - An observable change outside the function',
   ('state.input 변경 · render()의 DOM 수정', 'Changing state.input · Updating the DOM in render()')),
  group('[3] 역할 분리 - 계산은 값을 반환, 호출한 쪽에서 변경', '[3] Separation - Return a value, then let the caller make changes',
   ('함수형 사고의 적용 · 클릭 → 계산 → 상태 → 화면', 'Apply functional thinking · Click → Calculate → State → UI')))
], ['pure','elm-architecture'])
BODY['33']['panels'][0]['annotations'] = [
 {'before':'function add', 'inline':False, **bi('[1]', '[1]')},
 {'before':'state.input = String', 'inline':True, **bi('[2]', '[2]')},
 {'before':'button.addEventListener', 'inline':False, **bi('[3]', '[3]')},
]
BODY['33']['takeaway'] = bi('계산과 변경을 분리하면, 데이터 흐름을 따라 이해하고 각 역할을 검증하기 쉬움', 'Separate computation from changes to make data flow easier to follow and each role easier to test')

add(36, [
 concepts(('정의와 적용', 'Definition and Use'),
  group('디자인 패턴 - 반복되는 설계 문제의 해결 구조', 'Design pattern - A structure for recurring design problems',
   ('문제와 상황에 맞춰 코드의 역할과 협력 방식 구성', 'Organize responsibilities and collaboration for a given problem')),
  group('적용 방법 - 완성 코드를 복사하는 대신 구조 활용', 'Application - Adapt the structure to your code',
   ('언어와 프로젝트가 달라도 같은 해결 아이디어 적용 가능', 'The same idea can work across languages and projects'))),
 concepts(('필요성과 선택 기준', 'Benefits and Selection'),
  group('변경과 유지보수 - 고칠 부분을 찾고 영향 범위 축소', 'Maintenance - Locate changes and limit their impact',
   ('역할이 나뉘면 각 부분을 이해하고 확인하기 쉬움', 'Clear roles make each part easier to understand and check')),
  group('협업 - 설계 의도를 설명하는 공통 언어', 'Collaboration - A shared language for design intent',
   ('패턴 이름으로 문제와 해결 방향 공유', 'Use pattern names to discuss problems and solutions')),
  group('선택 기준 - 해결할 문제와 추가되는 복잡성 비교', 'Selection - Weigh the problem against added complexity',
   ('간단한 함수로 충분하면 구조를 더 늘리지 않음', 'Keep a simple function when it is enough')))])
BODY['36']['takeaway'] = bi('먼저 해결할 문제를 이해하고, 필요한 패턴을 선택', 'Understand the problem first, then choose a suitable pattern')

add(37, [
 table(('웹에서 자주 만나는 변경', 'Common Changes on the Web'),
  [('변경 상황', 'Change'), ('분리할 역할', 'Responsibility')], [
  [('상품 화면의 배치 변경', 'Change the product layout'), ('화면 표시 ↔ 데이터와 처리 규칙', 'Display ↔ Data and rules')],
  [('회원 할인 방식 추가', 'Add a member discount'), ('주문 흐름 ↔ 할인 계산', 'Order flow ↔ Discount calculation')],
  [('서버 응답의 필드 이름 변경', 'Rename server response fields'), ('외부 연결 ↔ 내부 데이터 사용', 'External integration ↔ Internal data use')]]),
 concepts(('역할과 경계', 'Roles and Boundaries'),
  group('책임 분리 - 각 부분이 맡는 일을 명확하게 구성', 'Separate responsibilities - Give each part a clear job',
   ('화면 표시 · 상태 관리 · 업무 처리 · 외부 연결', 'UI display · State · Business logic · External integration')),
  group('변경 영향 축소 - 달라지는 부분을 경계 안에서 처리', 'Limit change impact - Handle differences at a boundary',
   ('할인 계산이 바뀌어도 주문 흐름의 수정은 최소화', 'A discount change should require few order-flow changes')))])
BODY['37']['takeaway'] = bi('웹에서도 일반적인 디자인 패턴을 활용해 역할과 변경 지점을 정리', 'General design patterns help organize web responsibilities and points of change')

add(38, [
 table(('문제와 해결 아이디어', 'Problems and Solution Ideas'),
  [('패턴', 'Pattern'), ('해결 아이디어', 'Solution idea'), ('웹 사례', 'Web example')], [
  [('MVC', 'MVC'), ('데이터·화면·입력 처리의 역할 분리', 'Separate data, views, and input handling'), ('상품 데이터 / 목록 화면 / 사용자 요청 처리', 'Product data / List view / Request handling')],
  [('Observer', 'Observer'), ('변화를 관심 있는 대상에게 알림', 'Notify interested subscribers of changes'), ('장바구니 변경 → 개수·합계에 알림', 'Cart change → Notify count and total')],
  [('Strategy', 'Strategy'), ('공통 호출 방식으로 처리 방법 교체', 'Swap behavior through a shared contract'), ('일반 할인 ↔ 회원 할인', 'Regular discount ↔ Member discount')],
  [('Adapter', 'Adapter'), ('서로 다른 인터페이스를 연결', 'Connect incompatible interfaces'), ('외부 상품 필드 → 내부 상품 형식', 'External fields → Internal product shape')]])
], layout='single')
BODY['38']['takeaway'] = bi('MVC는 큰 역할 구조, 나머지 사례는 특정 협력 관계에 초점 · 이름보다 해결할 문제에 주목', 'MVC organizes broad roles; the other examples focus on specific collaborations · Start with the problem')

add(39, [
 table(('계산기의 세 가지 책임', 'Three Calculator Responsibilities'),
  [('파일', 'File'), ('맡은 일', 'Responsibility')], [
  [('app.ts', 'app.ts'), ('버튼 입력 전달 · 화면 갱신', 'Forward button input · Update the UI')],
  [('calculator.ts', 'calculator.ts'), ('입력 해석 · 상태 변경 · 계산 요청', 'Interpret input · Change state · Request arithmetic')],
  [('operations.ts', 'operations.ts'), ('사칙연산 함수 · 공통 호출', 'Arithmetic functions · Shared invocation')]]),
 flow(('12 + 3 =의 처리 흐름', 'How 12 + 3 = Runs'),
  ('클릭 → app.ts에서 handleKey 호출', 'Click → app.ts calls handleKey'),
  ('상태 처리 → calculator.ts에서 연산 선택', 'State handling → calculator.ts selects an operation'),
  ('계산 → operations.ts에서 15 반환', 'Arithmetic → operations.ts returns 15'),
  ('결과 저장 → app.ts의 render로 화면 반영', 'Store the result → app.ts renders the UI'))
], ['practice'])
BODY['39']['takeaway'] = bi('화면 표시를 바꿀 때와 연산 규칙을 바꿀 때 살펴볼 코드가 다름', 'Display changes and arithmetic changes lead to different parts of the code')

add(40, [
 lab('operations.ts',14,18, ('연산 목록과 공통 호출 함수', 'Operation Registry and Shared Invocation')),
 concepts(('Strategy로 읽는 계산기', 'Reading the Calculator as Strategy'),
  group('공통 계약 - 같은 입력과 출력의 함수 타입', 'Shared contract - A common function type',
   ('BinaryOperation: 두 number를 받아 number 반환', 'BinaryOperation: Two numbers in, one number out')),
  group('선택과 실행 - 연산 기호로 함수를 찾아 전달', 'Selection and execution - Look up and pass a function',
   ('operations[state.operator] → calculate → 연산 실행', 'operations[state.operator] → calculate → Execute')),
  group('변경 범위 - 호출 구조와 연산 구현을 분리', 'Scope of change - Separate invocation from behavior',
   ('새 연산 추가 시 함수·목록·타입·버튼·입력 분기 확인', 'New operation: Check function, registry, type, button, and input branch')))
], ['ts-functions','practice'])
BODY['40']['takeaway'] = bi('생각해 보기 · 나머지 연산을 추가할 때 바꿀 부분과 유지할 부분', 'To add a remainder operation, what would change and what would stay the same?')

add(41, [
 table(('버튼으로 확인할 완성 동작', 'Completed Behavior to Try'),
  [('버튼', 'Buttons'), ('화면', 'Display')], [
  [('12 → + → 3 → =', '12 → + → 3 → ='), ('계산식 12 + 3 = · 결과 15', 'Expression 12 + 3 = · Result 15')],
  [('12 → ÷ → 0 → =', '12 → ÷ → 0 → ='), ('Error · 0 나누기 안내', 'Error · Division-by-zero message')],
  [('오류 후 7', '7 after an error'), ('오류 해제 · 새 입력 7', 'Error cleared · New input 7')],
  [('AC · ⌫ · +/− · %', 'AC · ⌫ · +/− · %'), ('초기화 · 삭제 · 부호 · 100으로 나누기', 'Clear · Delete · Sign · Divide by 100')]]),
 concepts(('동작 요구사항과 완료 기준', 'Behavior Requirements and Acceptance Criteria'),
  group('요구사항(Requirement) - 입력에 대해 제공할 동작과 제약', 'Requirement - Required behavior and constraints',
   ('정상 계산 · 오류 안내 · 다음 입력의 복구 포함', 'Successful calculations · Error messages · Recovery')),
  group('완료 기준(Acceptance criterion) - 구현을 판단할 구체적 조건', 'Acceptance criterion - A concrete condition for completion',
   ('버튼 순서와 기대 화면을 짝지어 결과 비교', 'Compare each button sequence with its expected display'),
   ('입력 순서대로 계산 · 수학의 연산자 우선순위 미적용', 'Calculate in input order · No operator precedence')))], ['practice'])

add(42, [
 table(('12 + 3 = · 버튼 직후의 상태', '12 + 3 = · State After Each Input'),
  [('입력', 'Input'), ('input / stored / operator', 'input / stored / operator'), ('waiting / hasOperand', 'waiting / hasOperand')], [
  [('12', '12'), ('"12" / null / null', '"12" / null / null'), ('false / true', 'false / true')],
  [('+', '+'), ('"12" / 12 / "+"', '"12" / 12 / "+"'), ('true / false', 'true / false')],
  [('3', '3'), ('"3" / 12 / "+"', '"3" / 12 / "+"'), ('false / true', 'false / true')],
  [('=', '='), ('"15" / null / null', '"15" / null / null'), ('true / true', 'true / true')]]),
 concepts(('상태와 상태 전이', 'State and State Transitions'),
  group('상태(State) - 다음 동작에 필요한 기억 데이터', 'State - Stored data needed for the next action',
   ('input - 입력 문자열 · stored - 저장값 · operator - 연산 기호', 'input - Text · stored - Saved number · operator - Symbol')),
  group('상태 전이(State transition) - 입력에 따른 상태 변경', 'State transition - A state change driven by input',
   ('현재 상태 + 새 버튼 입력 → 다음 상태', 'Current state + New button input → Next state')),
  group('플래그(Flag) - 동작을 결정하는 참·거짓 값', 'Flag - A boolean that controls behavior',
   ('waiting - 다음 숫자로 새 입력 시작 여부', 'waiting - Whether the next digit starts fresh'),
   ('hasOperand - 현재 피연산자 존재 여부 · 2 + =는 계산 생략', 'hasOperand - Operand availability · 2 + = skips calculation')))], ['practice'])

add(43, [
 {**code(('설치 · 검사 · 컴파일', 'Install · Check · Compile'), 'bash', """
npm ci
npm run check
npm run build
# Open index.html in the browser
# After editing .ts files:
npm run watch
"""), 'concepts': [group('검사와 컴파일 - 타입 확인 후 실행 파일 생성', 'Check and compile - Check types and emit scripts',
   ('npm ci - 잠금 파일 기준 설치 · check - 타입 검사', 'npm ci - Install from lockfile · check - Type checking'),
   ('build - JavaScript 생성 · watch - 수정 시 재컴파일', 'build - Emit JavaScript · watch - Recompile on edits'),
   ('이 실습은 전역 스크립트 방식 · 오른쪽 순서대로 로드', 'This lab uses global scripts · Load in the order shown'))]},
 table(('작성 원본과 브라우저 실행 파일', 'Authored Files and Browser Scripts'),
  [('원본', 'Source'), ('실행 파일', 'Browser script')], [
  [('operations.ts', 'operations.ts'), ('js/operations.js · 먼저 로드', 'js/operations.js · Load first')],
  [('calculator.ts', 'calculator.ts'), ('js/calculator.js · 상태와 계산', 'js/calculator.js · State and calculation')],
  [('app.ts', 'app.ts'), ('js/app.js · 마지막 로드', 'js/app.js · Load last')],
  [('tsconfig.json', 'tsconfig.json'), ('module: none · 공통 전역 범위', 'module: none · Shared global scope')]])], ['practice'])

add(44, [
 code(('연산 결과와 오류 예측', 'Predicting Results and Errors'), 'javascript', """
const state = { input: '12' };
console.log(state.input + 3);
console.log(Number(state.inpt));
console.log(12 / 0);
console.log(0.1 + 0.2);
""", output='123\nNaN\nInfinity\n0.30000000000000004', specialExpected='prediction'),
 concepts(('특수 숫자와 부동소수점', 'Special Numbers and Floating Point'),
  group('[1] 문자열 연결(Concatenation) - 텍스트 결합', '[1] Concatenation - Join text',
   ("'12' + 3 → '123'", "'12' + 3 → '123'")),
  group('[2] NaN - 유효하지 않은 숫자 결과', '[2] NaN - An invalid numeric result',
   ('inpt는 오타 → undefined → Number 변환 시 NaN', 'inpt is a typo → undefined → Number yields NaN')),
  group('[3] Infinity - 무한대를 나타내는 number 값', '[3] Infinity - A number value representing infinity',
   ('12 / 0 → 예외 없이 Infinity 반환', '12 / 0 → Return Infinity without throwing')),
  group('[4] 부동소수점(Floating point) - 제한된 정밀도의 근삿값', '[4] Floating point - Approximation with limited precision',
   ('0.1 + 0.2 → 0.30000000000000004 · 표시 반올림과 구분', '0.1 + 0.2 → 0.30000000000000004 · Separate from display rounding')))], ['practice'])

BODY['44']['panels'][0]['annotations'] = [
 {'before': 'console.log(state.input', 'inline': True, **bi('[1]', '[1]')},
 {'before': 'console.log(Number', 'inline': True, **bi('[2]', '[2]')},
 {'before': 'console.log(12', 'inline': True, **bi('[3]', '[3]')},
 {'before': 'console.log(0.1', 'inline': True, **bi('[4]', '[4]')},
]

add(45, [
 lab('calculator.ts',53,61, ('소수점과 입력 길이 검사', 'Checking Decimal Points and Input Length')),
 concepts(('문자열 입력과 가드 조건', 'Text Input and Guard Conditions'),
  group('입력 문자열 - 작성 중인 숫자의 모양 보존', 'Input text - Preserve a number while it is being entered',
   ('"1." · "1.20" 유지 → 숫자 변환은 계산 시점까지 지연', 'Keep "1." and "1.20" → Defer conversion until calculation')),
  group('[1] 가드(Guard) - 허용하지 않는 입력을 먼저 차단', '[1] Guard - Reject disallowed input first',
   ('includes - 소수점 중복 확인 · 최대 12자리 제한', 'includes - Check duplicate decimal points · Limit to 12 digits'),
   ('정규식 /[-.]/g - 숫자 개수 계산에서 부호·소수점 제외', '/[-.]/g - Exclude the sign and point when counting digits')),
  group('[2] 문자열 연결 - 기존 입력에 숫자 추가', '[2] Concatenation - Append a digit to existing input',
   ('선행 0은 대체 · 그 외에는 state.input에 연결', 'Replace a leading zero · Otherwise append to state.input')))], ['practice'])

BODY['45']['panels'][0]['annotations'] = [
 {'before': 'if (key ===', 'inline': True, **bi('[1]', '[1]')},
 {'before': 'if (state.input.replace', 'inline': False, **bi('[1]', '[1]')},
 {'before': 'else state.input', 'inline': True, **bi('[2]', '[2]')},
]

add(46, [
 {**lab('operations.ts',2,7, ('TypeScript의 타입과 연산 함수', 'Types and Arithmetic Functions in TypeScript')), 'concepts': [group('[1] 타입 소거(Type erasure) - 컴파일 시 타입 정보 제거', '[1] Type erasure - Remove type information on compilation',
   ('Operator·BinaryOperation - 개발 중 검사에 쓰는 타입 이름', 'Operator and BinaryOperation - Names used for type checking'),
   ('타입 별칭과 변수·인수의 타입 표기는 실행 파일에서 제거', 'Aliases and annotations disappear from the emitted script'))]},
 {**code(('타입이 제거된 JavaScript', 'JavaScript with Types Removed'), 'javascript', """
const add = (left, right) => left + right;
const subtract = (left, right) => left - right;
const multiply = (left, right) => left * right;
"""), 'concepts': [group('실행 코드 - 타입 제거 후에도 유지되는 동작', 'Runtime code - Behavior retained after type erasure',
   ('함수와 연산식 유지 · 인수의 런타임 검사 자동 추가 없음', 'Functions and arithmetic remain · No automatic argument checks'),
   ('외부 값은 실행 중 조건문으로 별도 검증 필요', 'External values need separate runtime validation'))]}], ['practice','basics'], layout='equal')

BODY['46']['panels'][0]['annotations'] = [
 {'before': 'type Operator', 'inline': False, **bi('[1]', '[1]')},
]

add(47, [
 {**code(('존재 확인 없이 전달한 인수', 'An Argument Passed Without a Presence Check'), 'typescript', """
const key: string | undefined = undefined;
handleKey(key);
""", prelude='declare function handleKey(key: string): void;', errors=[2345]), 'concepts': [group('[1] 타입 오류 - 허용하지 않는 인수 전달', '[1] Type error - Pass an unsupported argument',
   ('handleKey는 string 필요 · key는 undefined', 'handleKey needs string · key is undefined'),
   ('값의 존재를 확인하지 않은 호출 → TS2345', 'Calling without a presence check → TS2345'))]},
 {**lab('app.ts',25,29, ('값의 존재 확인 후 호출', 'Calling After a Presence Check')), 'concepts': [group('[2] 타입 좁히기(Narrowing) - 검사한 경로에서 타입 제한', '[2] Narrowing - Restrict a type on a checked path',
   ('if (key) - undefined와 빈 문자열 제외', 'if (key) - Exclude undefined and the empty string'),
   ('블록 안에서는 key를 string으로 전달 가능', 'Inside the block, key can be passed as string'))]},
 ], ['practice','narrow'], layout='equal')

BODY['47']['panels'][0]['annotations'] = [
 {'before': 'handleKey(key)', 'inline': True, **bi('[1]', '[1]')},
]
BODY['47']['panels'][1]['annotations'] = [
 {'before': 'if (key)', 'inline': False, **bi('[2]', '[2]')},
]

add(48, [
 {**lab('operations.ts',8,11, ('0 나누기와 예외 발생', 'Division by Zero and Throwing an Error')), 'concepts': [group('[1] 예외(Exception) - 정상 진행을 중단하는 오류 신호', '[1] Exception - An error signal that interrupts execution',
   ('나누는 수가 0 → throw로 오류 전달', 'Zero divisor → throw signals an error'),
   ('가까운 catch로 이동 → 잘못된 나눗셈 결과 저장 방지', 'Transfer to the nearest catch → Avoid storing an invalid result'))]},
 {**lab('calculator.ts',122,122, ('오류 객체의 타입 확인', 'Checking the Error Object Type')), 'concepts': [group('[2] 오류 확인 - unknown 값을 검사한 뒤 사용', '[2] Error check - Inspect an unknown value before use',
   ('instanceof Error → message 접근 · 그 외 기본 안내', 'instanceof Error → Read message · Otherwise use fallback text'),
   ('오류 상태 표시 → 다음 숫자 입력에서 clear()로 복구', 'Display the error → clear() on the next digit restores state'))]},
 ], ['practice'])

BODY['48']['panels'][0]['annotations'] = [
 {'before': 'if (right', 'inline': False, **bi('[1]', '[1]')},
]
BODY['48']['panels'][1]['annotations'] = [
 {'before': 'state.error =', 'inline': False, **bi('[2]', '[2]')},
]

add(49, [
 lab('app.ts',15,20, ('상태를 화면에 반영', 'Rendering State to the UI')),
 concepts(('렌더링과 표시 형식', 'Rendering and Display Formatting'),
  group('[1] 렌더링(Rendering) - 상태를 화면 표현으로 변환', '[1] Rendering - Turn state into visible output',
   ('입력 중에는 원래 문자열 유지 · 계산 결과는 표시 자릿수 조정', 'Preserve input text · Format the precision of results')),
  group('[2] textContent - DOM 요소의 텍스트 읽기·변경', '[2] textContent - Read or change DOM text',
   ('결과 · 오류 안내 · 계산식을 각각의 요소에 반영', 'Update the result, error message, and expression elements')),
  group('상태와 화면 - 명시적 호출로 연결', 'State and UI - Connected by an explicit call',
   ('상태 변경 → render() 호출 → DOM 갱신', 'Change state → Call render() → Update the DOM'),
   ('표시용 쉼표는 저장된 입력 문자열과 분리', 'Display separators remain separate from stored input')))], ['practice'])

BODY['49']['panels'][0]['annotations'] = [
 {'before': 'const value', 'inline': False, **bi('[1]', '[1]')},
 {'before': 'display.textContent', 'inline': False, **bi('[2]', '[2]')},
]

add(50, [
 table(('각 행 전에 AC · 정상과 경계 입력', 'Press AC Before Each Row · Behavior Checks'),
  [('버튼', 'Buttons'), ('기대 결과', 'Expected Result')], [
  [('12 ÷ 3 = / 12 ÷ 0 =', '12 ÷ 3 = / 12 ÷ 0 ='), ('4 / Error · 이후 7로 복구', '4 / Error · Recover with 7')],
  [('2 + 3 × 4 =', '2 + 3 × 4 ='), ('20 · 입력 순서대로 계산', '20 · Calculates in input order')],
  [('2 + × 3 =', '2 + × 3 ='), ('6 · 연산자 교체', '6 · Replaces the operator')],
  [('2 + = / 2 + 3 = =', '2 + = / 2 + 3 = ='), ('2 / 5 · 불필요한 계산 없음', '2 / 5 · No extra calculation')],
  [('200 + 10 % =', '200 + 10 % ='), ('200.1 · 현재 수를 100으로 나눔', '200.1 · Divides current input by 100')]]),
 concepts(('정상·실패·경계 테스트', 'Normal, Failure, and Boundary Tests'),
  group('테스트(Test) - 실제 결과와 기대 결과 비교', 'Test - Compare actual and expected results',
   ('각 행 실행 전 AC → 같은 시작 상태에서 확인', 'Press AC before each row → Start from the same state')),
  group('정상·실패·경계 - 서로 다른 동작 조건 검사', 'Normal, failure, boundary - Check distinct conditions',
   ('정상 - 유효한 계산 · 실패 - 오류 안내와 복구', 'Normal - Valid calculation · Failure - Error and recovery'),
   ('경계 - 두 번째 입력 없음 · 연산자 연속 입력 등', 'Boundary - Missing operand · Consecutive operators')),
  group('타입 검사와 실행 검사 - 함께 필요한 검증', 'Type and execution checks - Complementary validation',
   ('타입 검사 - 값 사용 규칙 · 버튼 테스트 - 실제 동작', 'Type checks - Allowed uses · Button tests - Actual behavior')))], ['practice'])

add(51, [
 flow(('AI 코드 검토 절차', 'AI Code Review Procedure'),
  ('버튼 순서와 예상 상태 먼저 기록', 'Record the key sequence and predicted state'),
  ('특정 분기의 이유와 반례 요청', 'Ask about a branch and its counterexamples'),
  ('기존 코드와 제안의 차이 확인', 'Compare the existing code and the suggestion'),
  ('직접 실행 후 README에 결과 기록', 'Run it and record results in README')),
 concepts(('반례로 코드 제안 검증', 'Checking Suggestions with Counterexamples'),
  group('반례(Counterexample) - 제안의 문제를 드러내는 입력', 'Counterexample - An input that exposes a faulty proposal',
   ('매 입력마다 Number 변환 → "1."은 1 · "1.20"은 1.2', 'Number on each input → "1." becomes 1 · "1.20" becomes 1.2'),
   ('숫자값은 같아도 입력 중인 모양 소실', 'The numeric value remains, but the input form is lost')),
  group('변경 검증 - 요구 동작의 보존 여부 확인', 'Change verification - Check that required behavior remains',
   ('기존 코드와 제안에 같은 버튼 순서 적용 → 결과 비교', 'Run the same buttons on both versions → Compare results'),
   ('직접 실행한 결과와 변경 이유를 README에 기록', 'Record observed results and the reason in README')))], ['practice'])

add(52, [
 table(('LMS 제출과 배포 파일', 'LMS Submission and Deployed Files'),
  [('자료', 'Item'), ('내용', 'Contents')], [
  [('GitHub 저장소 URL', 'GitHub repository URL'), ('HTML · CSS · TS · 잠금 파일 · js/', 'HTML · CSS · TS · Lockfile · js/')],
  [('GitHub Pages URL', 'GitHub Pages URL'), ('공개 주소에서 계산 동작 확인', 'Verify calculations at the public URL')],
  [('README.md', 'README.md'), ('소개 · 실행법 · 동작과 담당 함수', 'Introduction · Run steps · Behavior and functions')]]),
 concepts(('코드로 설명할 실행 흐름', 'Execution Paths to Explain'),
  group('실행 흐름(Execution flow) - 입력부터 화면까지의 연결', 'Execution flow - Connect input to the displayed result',
   ('정상 - 클릭 → 상태 변경 → 전략 실행 → 화면 반영', 'Normal - Click → Change state → Run strategy → Update UI'),
   ('오류 - throw → catch → 오류 표시 → 다음 입력으로 복구', 'Error - throw → catch → Display error → Recover on input')),
  group('배포 산출물(Build artifacts) - 브라우저가 실행할 파일', 'Build artifacts - Files executed by the browser',
   ('컴파일된 js/ 포함 · 설치 의존성 node_modules 제외', 'Include compiled js/ · Exclude installed node_modules'),
   ('제출 기한 - 수업 공지 확인', 'Deadline - Check the course notice')))], ['practice'])

add(54, [
 {**code(('math.js - 함수 내보내기', 'math.js - Export a Function'), 'javascript', """
export function add(left, right) {
  return left + right;
}
""", file='math.js', moduleGroup='js-modules'), 'concepts': [
  group('[1] 내보내기(Export) - 다른 파일에서 쓸 항목 공개', '[1] Export - Expose an item to other files',
   ('함수 앞에 export → 다른 파일에서 add 사용 가능', 'export before the function → Other files can use add')),
  group('모듈(Module) - 독립된 스코프를 갖는 파일 단위', 'Module - A file with its own scope',
   ('공유할 항목을 명시해 파일 간 코드 연결', 'Explicitly expose items to connect code across files'))]},
 {**code(('main.js - 함수 가져오기와 호출', 'main.js - Import and Call the Function'), 'javascript', """
import { add } from './math.js';
console.log(add(12, 3));
""", file='main.js', moduleGroup='js-modules', output='15'), 'concepts': [
  group('[2] 가져오기(Import) - 공개된 항목을 현재 파일에서 사용', '[2] Import - Use an exported item in this file',
   ('./math.js - 같은 폴더의 파일 경로 · add - 내보낸 이름', './math.js - File in the same folder · add - Exported name'),
   ('가져온 add(12, 3) 호출 → 15 출력', 'Call the imported add(12, 3) → Print 15'))]}
], ['modules'], layout='equal')
BODY['54']['panels'][0]['annotations'] = [
 {'before': 'export function', 'inline': False, **bi('[1]', '[1]')},
]
BODY['54']['panels'][1]['annotations'] = [
 {'before': 'import', 'inline': True, **bi('[2]', '[2]')},
]
BODY['54']['takeaway'] = bi(
 '브라우저에서는 웹 서버로 페이지를 열고 <script type="module" src="./main.js"></script>로 시작',
 'In a browser, serve the page over HTTP and load <script type="module" src="./main.js"></script>')

add(55, [
 {**code(('types.ts - 객체 타입 내보내기', 'types.ts - Export an Object Type'), 'typescript', """
export type State = {
  input: string;
  waiting: boolean;
};
""", file='types.ts', moduleGroup='ts-types'), 'concepts': [
  group('[1] export type - 다른 파일에서 쓸 타입 공개', '[1] export type - Expose a type to other files',
   ('State - input과 waiting의 타입을 한 곳에서 정의', 'State - Define the input and waiting types in one place'),
   ('여러 파일에서 같은 객체 구조 검사에 재사용', 'Reuse the same object shape across files'))]},
 {**code(('main.ts - 타입 가져오기와 적용', 'main.ts - Import and Apply the Type'), 'typescript', """
import type { State } from './types.js';
const state: State = { input: '12', waiting: false };
console.log(state.input, state.waiting);
""", file='main.ts', moduleGroup='ts-types', output='12 false'), 'concepts': [
  group('[2] import type - 타입 검사를 위해 타입만 가져오기', '[2] import type - Import a type for type checking',
   ('state: State - 가져온 타입으로 객체 속성과 타입 검사', 'state: State - Check the object against the imported type'),
   ('./types.js - 컴파일 후 파일 확장자를 기준으로 표기', './types.js - Use the file extension after compilation'),
   ('input: 12 또는 속성 누락 시 컴파일 단계에서 오류', 'input: 12 or a missing property causes a compile-time error'))]}
], ['modules','types'], layout='equal')
BODY['55']['panels'][0]['annotations'] = [
 {'before': 'export type', 'inline': False, **bi('[1]', '[1]')},
]
BODY['55']['panels'][1]['annotations'] = [
 {'before': 'import type', 'inline': True, **bi('[2]', '[2]')},
]
BODY['55']['takeaway'] = bi(
 '함수 가져오기는 실행할 코드를 연결 · 타입 가져오기는 검사에 사용된 뒤 JavaScript 변환 시 제거',
 'Function imports connect executable code · Type imports are used for checking and erased from JavaScript')

chapters = json.loads((ROOT/'materials/slide-draft.json').read_text(encoding='utf-8'))
# Former practice topic bodies remain in the source as reference material.
for retired in range(41, 53):
    BODY.pop(str(retired))
assert set(BODY) == {str(t['sourcePage']) for c in chapters for t in c.get('topics', [])}
(ROOT/'materials/lesson-body.json').write_text(json.dumps({'sources':SOURCES,'slides':BODY},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Authored all {len(BODY)} topic bodies; covers and chapter dividers remain code-free.')
