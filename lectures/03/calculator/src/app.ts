import { operationCatalog } from './catalog.js';
import { CalculationHistory } from './history.js';
import { createUI } from './ui.js';
import type { Calculator, OperationId, ViewState } from './types.js';

export function mountCalculator(calculate: Calculator): void {
  const ui = createUI();
  const history = new CalculationHistory();
  let operation: OperationId = 'add';
  let state: ViewState = { status: 'idle' };

  function render(): void {
    ui.render(state, history.list());
  }
  function invalidate(): void {
    state = { status: 'idle' };
    render();
  }
  ui.buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const selected = operationCatalog.find(
        (item) => item.id === button.dataset.operation,
      );
      if (!selected) return;
      operation = selected.id;
      ui.selectOperation(selected);
      invalidate();
    });
  });
  ui.form.addEventListener('submit', (event) => {
    event.preventDefault();
    const result = calculate({
      operation,
      x: ui.x.value,
      y: ui.y.value,
      unit: ui.unit.value,
    });
    if (result.ok) {
      history.add(result.data);
      state = { status: 'success', calculation: result.data };
    } else {
      state = { status: 'error', message: result.message };
    }
    render();
  });
  ui.x.addEventListener('input', invalidate);
  ui.y.addEventListener('input', invalidate);
  ui.unit.addEventListener('change', invalidate);
  ui.clear.addEventListener('click', () => {
    ui.x.value = '';
    ui.y.value = '';
    invalidate();
    ui.x.focus();
  });
  ui.clearHistory.addEventListener('click', () => {
    history.clear();
    render();
  });
  render();
}
