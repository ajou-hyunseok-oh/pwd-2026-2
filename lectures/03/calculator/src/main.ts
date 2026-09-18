import { mountCalculator } from './app.js';
import { createCalculator } from './calculator.js';
import { parseNumber } from './validation.js';
import { operations } from './operations.js';

mountCalculator(createCalculator(parseNumber, operations));
