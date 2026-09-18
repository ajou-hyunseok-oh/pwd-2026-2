import { mountCalculator } from '../src/app.js';
import { createCalculator } from '../src/calculator.js';
import { parseNumber } from './validation.js';
import { operations } from './operations.js';

mountCalculator(createCalculator(parseNumber, operations));
