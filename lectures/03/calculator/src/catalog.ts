import type { Operation } from './types.js';

export const operationCatalog: readonly Operation[] = [
  { kind: 'binary', id: 'add', label: '+' },
  { kind: 'binary', id: 'subtract', label: '−' },
  { kind: 'binary', id: 'multiply', label: '×' },
  { kind: 'binary', id: 'divide', label: '÷' },
  { kind: 'unary', id: 'square', label: 'x²' },
  { kind: 'unary', id: 'sqrt', label: '√x' },
  { kind: 'unary', id: 'sin', label: 'sin' },
  { kind: 'unary', id: 'cos', label: 'cos' },
  { kind: 'unary', id: 'tan', label: 'tan' },
  { kind: 'unary', id: 'ln', label: 'ln' },
  { kind: 'unary', id: 'log10', label: 'log₁₀' },
];
