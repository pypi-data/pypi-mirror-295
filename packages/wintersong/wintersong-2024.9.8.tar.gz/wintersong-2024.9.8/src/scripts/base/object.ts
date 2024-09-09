/*
    Copyright (c) 2023 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { isObject } from "./types";

export function merge(dst: Record<any, any>, src?: Record<any, any>) {
    if (src == null || src == undefined) {
        return;
    }

    for (const key of Object.keys(src)) {
        if (isObject(dst[key])) {
            merge(dst[key], src[key]);
        } else {
            dst[key] = src[key];
        }
    }
}

/*
    Like Object.assign, but only updates existing properties in target- it
    does not add any new ones.
*/
export function assignOnlyExistingProperties(
    dst: Record<any, any>,
    src: Record<any, any>,
) {
    for (const prop of Object.getOwnPropertyNames(dst)) {
        if (Object.prototype.hasOwnProperty.call(src, prop)) {
            dst[prop] = src[prop];
        }
    }
}

type NestableStringKeyedRecord = {
    [property: string]: NestableStringKeyedRecord | any;
};

/**
 * Access nested object properties using a string, e.g. "order.email"
 */
export function getPropertyByPath(
    obj: NestableStringKeyedRecord,
    key: string,
    strict = true,
) {
    const key_parts = key.split(".");
    let value: any = obj;
    for (const part of key_parts) {
        if (!strict && (value === undefined || value == null)) {
            return undefined;
        }
        value = value[part];
    }
    return value;
}

/**
 * Set nested object properties using a string, e.g. "order.email"
 */
export function setPropertyByPath(
    obj: NestableStringKeyedRecord,
    key: string,
    value: any,
    strict = true,
) {
    const key_parts = key.split(".");

    let current_obj: NestableStringKeyedRecord = obj;
    for (const part of key_parts.slice(0, -1)) {
        if (!strict && (part === undefined || part == null)) {
            return;
        }
        current_obj = current_obj[part];
    }

    current_obj[key_parts.pop()!] = value;
}
