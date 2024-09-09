/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, css, html } from "lit";
import { customElement } from "lit/decorators.js";
import { prefersDarkScheme } from "../base/media-queries";
import "./icon";
import baseStyles from "./styles";

/**
 * Light/dark mode switcher
 */
@customElement("winter-dark-mode")
export class WinterDarkModeElement extends LitElement {
    static override styles = [
        baseStyles,
        css`
            :host {
                color: inherit;
                font-family: inherit;
                font-size: inherit;
                display: inline-block;
                line-height: 0;
            }

            button {
                background: transparent;
                display: inline-block;
                border: none;
                font-family: inherit;
                font-size: inherit;
                padding: 0;
                align-items: unset;
                color: inherit;
                line-height: inherit;
            }

            button:hover {
                font-size: inherit;
                cursor: pointer;
            }

            winter-icon {
                font-size: inherit;
            }
        `,
    ];

    override connectedCallback(): void {
        super.connectedCallback();

        const mediaPrefersDark = prefersDarkScheme.matches;
        const storedPreference = window.localStorage.getItem("color-scheme");
        let useDark =
            storedPreference === "dark" ||
            (storedPreference !== "light" && mediaPrefersDark);

        if (useDark) {
            document.documentElement.classList.add("dark");
        }
    }

    private onClick(e: MouseEvent) {
        if (document.documentElement.classList.contains("dark")) {
            document.documentElement.classList.remove("dark");
            localStorage.setItem("color-scheme", "light");
        } else {
            document.documentElement.classList.add("dark");
            localStorage.setItem("color-scheme", "dark");
        }
    }

    override render() {
        return html`
            <button
                @click=${this.onClick}
                type="button"
                aria-label="switch between dark and light mode">
                <winter-icon>dark_mode</winter-icon>
            </button>
        `;
    }
}
