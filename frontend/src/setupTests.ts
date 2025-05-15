import '@testing-library/jest-dom';
import { TextEncoder, TextDecoder } from 'node:util';

// @ts-expect-error - TextEncoder is not defined in the global scope
global.TextEncoder = TextEncoder;
// @ts-expect-error - TextDecoder is not defined in the global scope
global.TextDecoder = TextDecoder; 