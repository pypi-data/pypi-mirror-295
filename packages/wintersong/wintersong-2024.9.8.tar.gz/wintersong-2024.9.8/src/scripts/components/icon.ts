/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, css, html } from "lit";
import { customElement } from "lit/decorators.js";

@customElement("winter-icon")
export class WinterIconElement extends LitElement {
    static override styles = [
        css`
            :host {
                display: inline-block;
                box-sizing: content-box;
                font-family: "Material Symbols Outlined";
                font-weight: normal;
                font-style: normal;
                font-size: inherit;
                line-height: 1;
                letter-spacing: normal;
                text-transform: none;
                white-space: nowrap;
                word-wrap: normal;
                direction: ltr;
                -webkit-font-feature-settings: "liga";
                -moz-font-feature-settings: "liga";
                font-feature-settings: "liga";
                -webkit-font-smoothing: antialiased;
                user-select: none;
            }
        `,
    ];

    override render() {
        return html`<slot></slot>`;
    }
}
