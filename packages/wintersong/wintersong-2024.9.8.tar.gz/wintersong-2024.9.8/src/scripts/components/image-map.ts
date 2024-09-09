/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, css, html } from "lit";
import { customElement, property, state } from "lit/decorators.js";
import baseStyles from "./styles";

/**
 * Display a set of images in a single spot with a switcher to change between them.
 */
@customElement("winter-image-map")
export class WinterImageMapElement extends LitElement {
    static override styles = [
        baseStyles,
        css`
            :host {
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .--is-interactive-area {
                fill: #1ba8b800 !important;
                stroke-width: 10 !important;
                stroke: #1ba8b800 !important;
                mix-blend-mode: color !important;
                filter: blur(15px) !important;
                transition: 0.1s;
            }

            .--is-interactive-area.--is-active {
                fill: #1ba8b8 !important;
                stroke: #1ba8b800 !important;
            }

            div {
                width: 100%;
            }

            h3 {
                line-height: 1.5;
                font-size: 1em;
                font-weight: normal;
                border: 1px solid transparent;
                padding: 0.2em 1em;
                margin: -1em 0 0em 0;
                width: 60%;
                display: flex;
                flex-direction: row;
                justify-content: center;
                border-radius: 0.2rem;
                color: white;
                background: #1ba8b8;
            }
        `,
    ];

    private svg: HTMLElement;

    @property()
    src: string;

    private activeArea?: HTMLElement;

    @state()
    private activeText: string = "test";

    private get items() {
        return this.querySelectorAll<WinterImageMapItemElement>(
            "winter-image-map-item",
        );
    }

    override connectedCallback(): void {
        super.connectedCallback();

        if (this.src) {
            this.loadSrc();
        }
    }

    private async loadSrc() {
        const resp = await fetch(this.src, {
            mode: "same-origin",
        });

        if (!resp.ok) {
            console.error(
                `Could not fetch ${this.src}: ${resp.status} ${resp.statusText}`,
            );
        }

        const svgContents = await resp.text();

        const parser = new DOMParser();

        this.svg = parser.parseFromString(
            svgContents,
            "image/svg+xml",
        ).documentElement;

        this.prepSvg();

        this.requestUpdate();
    }

    private idToDescription: Map<string, string> = new Map();

    private prepSvg() {
        for (const item of this.items) {
            this.idToDescription.set(item.id, item.innerText);

            const itemArea = this.svg.querySelector<HTMLElement>(
                `[id=${item.id}]`,
            );

            if (!itemArea) {
                console.warn(`Area ${item.id} not found in ${this.src}`);
                continue;
            }

            itemArea.classList.add("--is-interactive-area");

            if (!this.activeArea) {
                this.setActiveArea(itemArea);
            }
        }

        this.svg.addEventListener("mouseover", (e: MouseEvent) => {
            const target = e.target as HTMLElement;
            if (target.classList.contains("--is-interactive-area")) {
                this.setActiveArea(target);
            }
        });
    }

    private setActiveArea(areaElem: HTMLElement) {
        if (this.activeArea === areaElem) {
            return;
        }

        this.activeArea?.classList.remove("--is-active");
        this.activeArea = areaElem;
        this.activeArea.classList.add("--is-active");
        this.activeText = this.idToDescription.get(areaElem.id)!;
    }

    protected override render() {
        return html`<div>${this.svg}</div>
            <h3 class="elevated">${this.activeText}</h3>`;
    }
}

@customElement("winter-image-map-item")
export class WinterImageMapItemElement extends LitElement {
    static override styles = [
        css`
            :host {
                display: none;
                visibility: hidden;
            }
        `,
    ];
}
