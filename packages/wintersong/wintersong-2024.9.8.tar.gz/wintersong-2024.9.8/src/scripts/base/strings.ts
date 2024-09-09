/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

/**
 * Converts camelCase to dash-case
 */
export function camelToDash(str: string): string {
    return str
        .replace(/(^[A-Z])/, ([first]) => first!.toLowerCase())
        .replace(/([A-Z])/g, ([letter]) => `-${letter!.toLowerCase()}`);
}
