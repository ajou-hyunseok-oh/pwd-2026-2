import { formatNumber } from './format.js';
import type { Calculation, Operation, ViewState } from './types.js';

function element(id: string): HTMLElement {
  const found = document.getElementById(id);
  if (!found) throw new Error(`요소 없음: ${id}`);
  return found;
}
function input(id: string): HTMLInputElement {
  const found = element(id);
  if (!(found instanceof HTMLInputElement)) throw new Error(`input 아님: ${id}`);
  return found;
}

export function createUI() {
  const form = element('calculator');
  const x = input('x');
  const y = input('y');
  const unit = element('unit');
  if (!(unit instanceof HTMLSelectElement)) throw new Error('select 아님: unit');
  const buttons = Array.from(
    document.querySelectorAll<HTMLButtonElement>('[data-operation]'),
  );
  const output = element('result');
  const expression = element('expression');
  const status = element('status');
  const entries = element('history');
  const clearHistory = element('clear-history');
  if (!(clearHistory instanceof HTMLButtonElement)) throw new Error('button 아님');

  return {
    form,
    x,
    y,
    unit,
    buttons,
    clear: element('clear'),
    clearHistory,
    selectOperation(operation: Operation): void {
      buttons.forEach((button) =>
        button.setAttribute(
          'aria-pressed',
          String(button.dataset.operation === operation.id),
        ),
      );
      y.disabled = operation.kind === 'unary';
      element('y-field').hidden = operation.kind === 'unary';
      const isAngle = ['sin', 'cos', 'tan'].includes(operation.id);
      unit.disabled = !isAngle;
      element('selection').textContent =
        operation.kind === 'binary'
          ? `x ${operation.label} y`
          : operation.id === 'square' || operation.id === 'sqrt'
            ? operation.label
            : `${operation.label}(x)`;
    },
    render(state: ViewState, history: Calculation[]): void {
      output.dataset.state = state.status;
      if (state.status === 'success') {
        output.textContent = formatNumber(state.calculation.value);
        expression.textContent = state.calculation.expression;
        status.textContent = '계산 완료';
      } else {
        output.textContent = '—';
        expression.textContent = '';
        status.textContent =
          state.status === 'error' ? state.message : '숫자와 연산을 선택하세요.';
      }
      status.dataset.state = state.status;
      clearHistory.disabled = history.length === 0;
      element('empty-history').hidden = history.length > 0;
      entries.replaceChildren(
        ...history.map((entry) => {
          const item = document.createElement('li');
          const label = document.createElement('span');
          label.textContent = entry.expression;
          const value = document.createElement('strong');
          value.textContent = formatNumber(entry.value);
          item.append(label, value);
          return item;
        }),
      );
    },
  };
}
