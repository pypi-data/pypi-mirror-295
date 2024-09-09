/*
    Copyright (c) 2022 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import type { AnyFunction, InferArgs, InferReturn } from "./types";

export function noop() {}

/**
 * Prevents a function from being executed while its already running.
 */
export function preventConcurrentCalls<T extends AnyFunction>(target: T) {
    let isRunning = false;

    return (...args: InferArgs<T>): InferReturn<T> | undefined => {
        if (isRunning) {
            return;
        }

        try {
            isRunning = true;
            return target(...args);
        } finally {
            isRunning = false;
        }
    };
}
