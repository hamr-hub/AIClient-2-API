#!/usr/bin/env node
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const jestProcess = spawn('npx', [
    'jest',
    '--coverage',
    '--testEnvironment=node',
    '--coverageReporters=text-summary'
], {
    cwd: __dirname,
    stdio: 'inherit',
    shell: true
});

jestProcess.on('close', (code) => {
    process.exit(code);
});