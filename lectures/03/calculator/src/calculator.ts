import { operationCatalog } from './catalog.js';
import { failure, success } from './result.js';
import type { Calculator, NumberParser, OperationRegistry, Result } from './types.js';

// 제공: 실행 순서를 읽는 코드. DOM이나 계산 이력을 변경하지 않음.
export function createCalculator(
  parseNumber: NumberParser,
  strategies: OperationRegistry,
): Calculator {
  return (input) => {
    const operation = operationCatalog.find((item) => item.id === input.operation);
    if (!operation) return failure('UNKNOWN_OPERATION', '지원하지 않는 연산입니다.');
    if (input.unit !== 'deg' && input.unit !== 'rad') {
      return failure('INVALID_UNIT', '각도 단위는 DEG 또는 RAD여야 합니다.');
    }
    const x = parseNumber(input.x);
    if (!x.ok) return x;

    let result: Result<number>;
    let expression: string;
    if (operation.kind === 'binary') {
      const y = parseNumber(input.y);
      if (!y.ok) return y;
      result = strategies.binary[operation.id](x.data, y.data);
      expression = `${x.data} ${operation.label} ${y.data}`;
    } else {
      result = strategies.unary[operation.id](x.data, input.unit);
      const isAngle = ['sin', 'cos', 'tan'].includes(operation.id);
      const argument = isAngle ? `${x.data} ${input.unit.toUpperCase()}` : `${x.data}`;
      expression =
        operation.id === 'square'
          ? `(${x.data})²`
          : operation.id === 'sqrt'
            ? `√(${x.data})`
            : `${operation.label}(${argument})`;
    }
    if (!result.ok) return result;
    if (!Number.isFinite(result.data)) {
      return failure(
        'NON_FINITE_RESULT',
        '계산 결과가 유한한 실수 범위를 벗어났습니다.',
      );
    }
    return success({ expression, value: result.data });
  };
}
