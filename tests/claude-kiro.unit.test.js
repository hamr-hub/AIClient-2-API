import { describe, expect, test, jest, beforeEach, afterEach } from '@jest/globals';

const KIRO_CONSTANTS = {
    AXIOS_TIMEOUT: 30000,
    STREAM_TIMEOUT: 300000,
    STREAM_DATA_TIMEOUT: 60000,
};

function parseKiroConstants() {
    return KIRO_CONSTANTS;
}

function detectFreeAccountRestriction(errorText) {
    const text = (errorText || '').toLowerCase();
    if (!text) return null;

    const freeAccountPatterns = [
        { pattern: 'free tier', message: 'Free tier account may have limited access' },
        { pattern: 'free account', message: 'Free account access restrictions apply' },
        { pattern: 'trial has expired', message: 'Trial period has expired' },
        { pattern: 'trial expired', message: 'Trial period has expired' },
        { pattern: 'limited access', message: 'Account has limited access privileges' },
        { pattern: 'quota exceeded', message: 'Quota exceeded, please check your plan' },
        { pattern: 'rate limit', message: 'Rate limit exceeded' },
        { pattern: 'capacity', message: 'Service capacity issues' }
    ];

    for (const { pattern, message } of freeAccountPatterns) {
        if (text.includes(pattern)) {
            return message;
        }
    }
    return null;
}

function isRefreshableForbidden(errorText) {
    const text = (errorText || '').toLowerCase();
    if (!text) return false;

    const nonRefreshablePatterns = [
        'temporarily is suspended',
        'temporarily suspended',
        'disabled',
        'violation of terms',
        'terms of service',
        'appeal',
        'quota',
        'limit exceeded',
        'payment required',
        'not authorized to access',
        'not allowed',
        'free tier',
        'free account',
        'trial expired',
        'limited access'
    ];
    if (nonRefreshablePatterns.some(pattern => text.includes(pattern))) {
        return false;
    }

    const tokenRelated = text.includes('token') ||
        text.includes('authorization') ||
        text.includes('authenticate') ||
        text.includes('credential');
    const refreshableAuthState = text.includes('expired') ||
        text.includes('invalid') ||
        text.includes('unauthorized');

    return tokenRelated && refreshableAuthState;
}

function createTimeoutError(timeoutMs) {
    const error = new Error(`Request timeout after ${timeoutMs}ms`);
    error.code = 'REQUEST_TIMEOUT';
    error.shouldSwitchCredential = true;
    error.skipErrorCount = true;
    return error;
}

describe('Claude Kiro Provider Tests', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    describe('KIRO_CONSTANTS Configuration', () => {
        test('should have correct AXIOS_TIMEOUT value', () => {
            const constants = parseKiroConstants();
            expect(constants.AXIOS_TIMEOUT).toBe(30000);
        });

        test('should have correct STREAM_TIMEOUT value (5 minutes)', () => {
            const constants = parseKiroConstants();
            expect(constants.STREAM_TIMEOUT).toBe(300000);
        });

        test('should have correct STREAM_DATA_TIMEOUT value (1 minute)', () => {
            const constants = parseKiroConstants();
            expect(constants.STREAM_DATA_TIMEOUT).toBe(60000);
        });
    });

    describe('Free Account Restriction Detection', () => {
        test('should detect free tier restriction', () => {
            const result = detectFreeAccountRestriction('Your free tier account has limited access');
            expect(result).toBe('Free tier account may have limited access');
        });

        test('should detect free account restriction', () => {
            const result = detectFreeAccountRestriction('Free account access is restricted');
            expect(result).toBe('Free account access restrictions apply');
        });

        test('should detect trial expired', () => {
            const result = detectFreeAccountRestriction('Your trial has expired');
            expect(result).toBe('Trial period has expired');
        });

        test('should detect trial expired with period', () => {
            const result = detectFreeAccountRestriction('Trial expired, please upgrade');
            expect(result).toBe('Trial period has expired');
        });

        test('should detect quota exceeded', () => {
            const result = detectFreeAccountRestriction('Quota exceeded. Please upgrade your plan.');
            expect(result).toBe('Quota exceeded, please check your plan');
        });

        test('should detect rate limit', () => {
            const result = detectFreeAccountRestriction('Rate limit exceeded. Try again later.');
            expect(result).toBe('Rate limit exceeded');
        });

        test('should return null for non-free-account errors', () => {
            const result = detectFreeAccountRestriction('Invalid token provided');
            expect(result).toBeNull();
        });
    });

    describe('Refreshable Forbidden Detection', () => {
        test('should return true for token expired error', () => {
            const result = isRefreshableForbidden('Token expired, please refresh');
            expect(result).toBe(true);
        });

        test('should return true for invalid token error', () => {
            const result = isRefreshableForbidden('Invalid authorization token');
            expect(result).toBe(true);
        });

        test('should return true for unauthorized error with token mention', () => {
            const result = isRefreshableForbidden('Unauthorized: invalid credential');
            expect(result).toBe(true);
        });

        test('should return false for free tier error', () => {
            const result = isRefreshableForbidden('Free tier access denied');
            expect(result).toBe(false);
        });

        test('should return false for quota exceeded', () => {
            const result = isRefreshableForbidden('Quota exceeded');
            expect(result).toBe(false);
        });

        test('should return false for terms of service violation', () => {
            const result = isRefreshableForbidden('Violation of terms of service');
            expect(result).toBe(false);
        });

        test('should return false for temporarily suspended', () => {
            const result = isRefreshableForbidden('Account temporarily suspended');
            expect(result).toBe(false);
        });
    });

    describe('Timeout Error Creation', () => {
        test('should create timeout error with correct properties', () => {
            const error = createTimeoutError(30000);
            
            expect(error.message).toBe('Request timeout after 30000ms');
            expect(error.code).toBe('REQUEST_TIMEOUT');
            expect(error.shouldSwitchCredential).toBe(true);
            expect(error.skipErrorCount).toBe(true);
        });

        test('should create timeout error for stream timeout', () => {
            const error = createTimeoutError(300000);
            
            expect(error.message).toBe('Request timeout after 300000ms');
            expect(error.code).toBe('REQUEST_TIMEOUT');
        });
    });

    describe('Promise.race Timeout Mechanism', () => {
        test('should resolve with actual result before timeout', async () => {
            const actualPromise = Promise.resolve('success');
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('timeout')), 1000);
            });

            const result = await Promise.race([actualPromise, timeoutPromise]);
            expect(result).toBe('success');
        });

        test('should reject with timeout error when actual promise takes too long', async () => {
            jest.useFakeTimers();
            const actualPromise = new Promise(resolve => setTimeout(resolve, 5000, 'success'));
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => {
                    const error = new Error('Request timeout after 3000ms');
                    error.code = 'REQUEST_TIMEOUT';
                    reject(error);
                }, 3000);
            });

            const racePromise = Promise.race([actualPromise, timeoutPromise]);
            
            jest.advanceTimersByTime(3000);
            
            await expect(racePromise).rejects.toThrow('Request timeout after 3000ms');
            
            jest.useRealTimers();
        });
    });

    describe('Data Chunk Timeout Reset', () => {
        test('should reset timeout timer when data is received', () => {
            jest.useFakeTimers();
            
            let timeoutTriggered = false;
            const resetTimeout = jest.fn();
            
            let timerId = setTimeout(() => {
                timeoutTriggered = true;
            }, 60000);
            
            resetTimeout.mockImplementation(() => {
                clearTimeout(timerId);
                timerId = setTimeout(() => {
                    timeoutTriggered = true;
                }, 60000);
            });

            jest.advanceTimersByTime(30000);
            resetTimeout();
            
            jest.advanceTimersByTime(30000);
            expect(timeoutTriggered).toBe(false);
            
            jest.advanceTimersByTime(30001);
            expect(timeoutTriggered).toBe(true);
            
            jest.useRealTimers();
        });
    });
});