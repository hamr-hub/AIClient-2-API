#!/usr/bin/env node
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);
const testType = args[0] || 'all';

let testPatterns = [];
let verbose = false;

switch (testType) {
    case '--unit':
        testPatterns = ['tests/**/*.unit.test.js'];
        break;
    case '--integration':
        testPatterns = ['tests/**/*.integration.test.js', 'tests/**/api-integration.test.js'];
        break;
    case '--security':
        testPatterns = ['tests/**/security*.test.js'];
        break;
    default:
        testPatterns = ['tests/**/*.test.js'];
        verbose = true;
}

const jestArgs = [
    ...testPatterns,
    verbose ? '--verbose' : '',
    '--testEnvironment=node'
].filter(Boolean);

const jestProcess = spawn('npx', ['jest', ...jestArgs], {
    cwd: __dirname,
    stdio: 'inherit',
    shell: true
});

jestProcess.on('close', (code) => {
    process.exit(code);
});