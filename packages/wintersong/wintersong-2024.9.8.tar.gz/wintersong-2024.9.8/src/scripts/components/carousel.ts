/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, css, html, type PropertyValueMap } from "lit";
import { customElement, property } from "lit/decorators.js";
import baseStyles from "./styles";
import { map } from "../base/iterator";

/**
 * Display a set of images in a single spot with a switcher to change between them.
 */
@customElement("winter-carousel")
export class WinterCarouselElement extends LitElement {
    static override styles = [
        baseStyles,
        css`
            :host {
                width: 100%;
                --button-fg: white;
                --button-bg: rgb(94, 64, 158);
                --button-bg-active: rgb(163, 138, 214);
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .navigation {
                margin: -0.5em 0 0em 0;
                width: fit-content;
                display: flex;
                flex-direction: row;
                justify-content: center;
                border-radius: 0.2rem;
            }

            .navigation button {
                font-family: inherit;
                line-height: 1.5;
                font-size: 1em;
                color: var(--button-fg);
                background: var(--button-bg);
                border: 1px solid transparent;
                padding: 0.2em 1em;
                transition: background 300ms ease;
            }

            .navigation button:hover,
            .navigation button:focus,
            .navigation button.--is-active {
                background: var(--button-bg-active);
            }

            .navigation button:first-child {
                border-top-left-radius: 0.2em;
                border-bottom-left-radius: 0.2em;
            }

            .navigation button:last-child {
                border-top-right-radius: 0.2em;
                border-bottom-right-radius: 0.2em;
            }

            ::slotted(img) {
                width: 100%;
                display: none !important;
            }

            ::slotted(img.--is-active) {
                display: block !important;
            }
        `,
    ];

    private _activeIndex: number = 0;

    @property({ type: Number })
    set activeIndex(val: number) {
        this.activeImage?.classList.remove("--is-active");
        this.images[val]?.classList.add("--is-active");
        this._activeIndex = val;
    }

    get activeIndex() {
        return this._activeIndex;
    }

    onNavigationClick(e: MouseEvent) {
        const index = parseInt((e.target as HTMLElement).dataset["index"]!, 10);
        this.activeIndex = index;
    }

    get images() {
        return this.querySelectorAll("img");
    }

    get activeImage() {
        return this.querySelector("img.--is-active");
    }

    protected override render() {
        return html`<div class="elevated">
                <slot></slot>
            </div>
            <div @click="${this.onNavigationClick}" class="navigation elevated">
                ${map(this.images, (image, n) => {
                    return html`<button
                        type="button"
                        data-index="${n}"
                        class="${this.activeIndex == n ? "--is-active" : ""}">
                        ${n + 1}
                    </button>`;
                })}
            </div>`;
    }

    protected override firstUpdated(
        _changedProperties: PropertyValueMap<any> | Map<PropertyKey, unknown>,
    ): void {
        const images = this.images;

        if (images.length) {
            images[0]?.classList.add("--is-active");
        }
    }
}
