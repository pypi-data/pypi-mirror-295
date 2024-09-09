/*
    Copyright (c) 2023 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { isArray, isIterable } from "./types";

export function asArray<T>(x: T | T[]): T[];
export function asArray<T>(x: T | readonly T[]): readonly T[];
export function asArray<T>(x: T | T[]): T[] {
    if (isArray(x)) {
        return x;
    }
    return [x];
}

export function iterableAsArray<T>(x: T | T[] | Iterable<T>): T[] {
    if (isArray(x)) {
        return x;
    }
    if (isIterable(x)) {
        return Array.from(x);
    }
    return [x];
}

const collator = new Intl.Collator(undefined, { numeric: true });

export function sortedByNumericStrings<T>(
    array: T[],
    getter: (item: T) => string,
) {
    return array.slice().sort((a, b) => collator.compare(getter(a), getter(b)));
}

export function uint8ArrayToHex(buf: Uint8Array): string {
    return Array.prototype.map
        .call(buf, (x) => ("00" + x.toString(16)).slice(-2))
        .join("");
}
