export type Result<T> =
  { ok: true; data: T } | { ok: false; code: ErrorCode; message: string };
export type ErrorCode =
  | 'EMPTY_INPUT'
  | 'INVALID_NUMBER'
  | 'UNKNOWN_OPERATION'
  | 'INVALID_UNIT'
  | 'DIVISION_BY_ZERO'
  | 'DOMAIN'
  | 'NON_FINITE_RESULT'
  | 'NOT_IMPLEMENTED';
export type AngleUnit = 'deg' | 'rad';
export type BinaryOperation = 'add' | 'subtract' | 'multiply' | 'divide';
export type UnaryOperation = 'square' | 'sqrt' | 'sin' | 'cos' | 'tan' | 'ln' | 'log10';
export type OperationId = BinaryOperation | UnaryOperation;
export type Operation =
  | { kind: 'binary'; id: BinaryOperation; label: string }
  | { kind: 'unary'; id: UnaryOperation; label: string };
export type RawInput = { operation: string; x: string; y: string; unit: string };
export type Calculation = { expression: string; value: number };
export type BinaryStrategy = (x: number, y: number) => Result<number>;
export type UnaryStrategy = (x: number, unit: AngleUnit) => Result<number>;
export type OperationRegistry = {
  binary: Record<BinaryOperation, BinaryStrategy>;
  unary: Record<UnaryOperation, UnaryStrategy>;
};
export type NumberParser = (raw: string) => Result<number>;
export type Calculator = (input: RawInput) => Result<Calculation>;
export type ViewState =
  | { status: 'idle' }
  | { status: 'success'; calculation: Calculation }
  | { status: 'error'; message: string };
