/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { isString } from "./types";

export function isHTMLElement(v: any): v is HTMLElement {
    return typeof HTMLElement === "object" && v instanceof HTMLElement;
}

/**
 * Shortcut for getElementById and querySelector
 */
export function $<E extends Element = Element>(x: string | E): E | null {
    if (isHTMLElement(x)) {
        return x;
    } else if (isString(x)) {
        return (document.getElementById(x) ??
            document.querySelector<E>(x)) as E | null;
    }
    return x;
}

/**
 * Shortcut for querySelectorAll
 */
export function $$<E extends Element = Element>(
    selector: string,
): NodeListOf<HTMLElement>;
export function $$<E extends Element = Element>(
    parent: HTMLElement,
    selector: string,
): NodeListOf<HTMLElement>;
export function $$<E extends Element = Element>(
    selectorOrParent: string | HTMLElement,
    selector?: string,
): NodeListOf<E> {
    if (isHTMLElement(selectorOrParent)) {
        return selectorOrParent.querySelectorAll<E>(selector!);
    } else {
        return document.querySelectorAll<E>(selectorOrParent);
    }
}

export function removeAllChildren(node: Node) {
    var range = document.createRange();
    range.selectNodeContents(node);
    range.deleteContents();
}
