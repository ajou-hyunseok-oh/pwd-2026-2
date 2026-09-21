// 계산 상태와 입력 처리: DOM을 직접 다루지 않습니다.
interface CalculatorState {
  input: string;
  stored: number | null;
  operator: Operator | null;
  waiting: boolean;
  hasOperand: boolean;
  error: string;
  expression: string;
}

const state: CalculatorState = {
  input: '0',
  stored: null,
  operator: null,
  waiting: false,
  hasOperand: false,
  error: '',
  expression: '',
};

function formatNumber(value: number): string {
  return Number(value.toPrecision(12)).toString();
}

// 순수 함수: 전달받은 상태를 읽어 문자열을 반환하고 원본은 바꾸지 않습니다.
function pendingExpression(current: CalculatorState): string {
  if (current.stored === null || current.operator === null) return current.expression;
  const symbols = { '+': '+', '-': '−', '*': '×', '/': '÷' };
  const right = current.hasOperand ? ` ${current.input}` : '';
  return `${formatNumber(current.stored)} ${symbols[current.operator]}${right}`;
}

function clear(): void {
  state.input = '0';
  state.stored = null;
  state.operator = null;
  state.waiting = false;
  state.hasOperand = false;
  state.error = '';
  state.expression = '';
}

// 숫자 입력: 문자열 연결과 숫자 덧셈의 차이를 관찰하세요.
function inputDigit(key: string): void {
  if (state.error) clear();
  if (state.operator === null) state.expression = '';
  if (state.waiting) {
    state.input = '0';
    state.waiting = false;
  }
  state.hasOperand = true;
  if (key === '.') {
    if (!state.input.includes('.')) state.input += '.';
    return;
  }
  // 부호와 소수점을 제외하고 직접 입력은 최대 12자리입니다.
  if (state.input.replace(/[-.]/g, '').length >= 12) return;
  if (state.input === '0') state.input = key;
  else if (state.input === '-0') state.input = '-' + key;
  else state.input += key;
}

function setResult(value: number): void {
  if (!Number.isFinite(value)) {
    throw new Error('계산 가능한 숫자 범위를 벗어났습니다.');
  }
  state.input = String(value);
  state.waiting = true;
  state.hasOperand = true;
}

function selectOperator(operator: Operator): void {
  const value = Number(state.input);
  if (state.operator !== null && state.stored !== null && state.hasOperand) {
    setResult(calculate(state.stored, value, operations[state.operator]));
  }
  state.stored = Number(state.input);
  state.operator = operator;
  state.hasOperand = false;
  state.waiting = true;
}

function equals(): void {
  // 두 번째 숫자 없이 =를 누르면 기다립니다. 반복 =는 계산을 반복하지 않습니다.
  if (state.operator === null || state.stored === null || !state.hasOperand) return;
  const right = Number(state.input);
  const formula = pendingExpression(state);
  setResult(calculate(state.stored, right, operations[state.operator]));
  state.stored = null;
  state.operator = null;
  state.expression = `${formula} =`;
}

// 전달받은 키에 따라 상태를 변경하고 계산 오류를 상태에 저장합니다.
function handleKey(key: string): void {
  try {
    if (/^[0-9.]$/.test(key)) inputDigit(key);
    else if (key === 'clear') clear();
    else if (state.error) return;
    else if (key === '+' || key === '-' || key === '*' || key === '/') {
      selectOperator(key);
    } else if (key === '=') equals();
    else if (key === 'delete') {
      if (!state.waiting) {
        state.input = state.input.slice(0, -1);
        if (state.input === '' || state.input === '-') state.input = '0';
      }
    } else if (key === 'sign') {
      if (state.operator === null) state.expression = '';
      if (state.waiting && !state.hasOperand) {
        state.input = '0';
        state.waiting = false;
      }
      state.hasOperand = true;
      state.input = state.input.startsWith('-') ? state.input.slice(1) : '-' + state.input;
    } else if (key === 'percent') {
      if (state.operator === null) state.expression = '';
      setResult(Number(state.input) / 100);
    }
  } catch (error) {
    state.error = error instanceof Error ? error.message : '계산 오류입니다.';
  }
}
