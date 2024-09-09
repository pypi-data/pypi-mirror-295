/*
    Copyright (c) 2022 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

export type Primitive =
    | null
    | undefined
    | boolean
    | number
    | string
    | symbol
    | bigint;

export function isPrimitive(value: unknown): value is Primitive {
    return (
        value === null ||
        (typeof value != "object" && typeof value != "function")
    );
}

export function isString(value: unknown): value is string {
    return typeof value === "string";
}

export function isNumber(value: unknown): value is number {
    return typeof value === "number" && !isNaN(value);
}

export function isIterable<T>(value: unknown): value is Iterable<T> {
    return (
        Array.isArray(value) ||
        typeof (value as any)?.[Symbol.iterator] === "function"
    );
}

export function isArray<T = unknown>(value: unknown): value is T[] {
    return Array.isArray(value);
}

// eslint-disable-next-line @typescript-eslint/ban-types
export function isObject(value: unknown): value is Object {
    return (
        typeof value === "object" &&
        value !== null &&
        !Array.isArray(value) &&
        !(value instanceof RegExp) &&
        !(value instanceof Date)
    );
}

export type Constructor<T = unknown> = new (...args: any[]) => T;
export type AnyFunction = (...args: any[]) => any;
export type InferArgs<T> = T extends (...t: [...infer Arg]) => any
    ? Arg
    : never;
export type InferReturn<T> = T extends (...t: [...infer Arg]) => infer Res
    ? Res
    : never;
