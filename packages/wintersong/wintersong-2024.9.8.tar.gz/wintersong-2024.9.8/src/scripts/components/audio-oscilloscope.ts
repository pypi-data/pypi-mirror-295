/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, css, html, type PropertyValueMap } from "lit";
import { customElement, query } from "lit/decorators.js";
import { prefersReducedMotion } from "../base/media-queries";
import { AudioContextManager } from "../audio/context-manager";
import baseStyles from "./styles";

/**
 * Audio oscilloscope, used by WinterAudioPlayerElement
 */
@customElement("winter-audio-oscilloscope")
export class WinterAudioOscilloscopeElement extends LitElement {
    static override styles = [
        baseStyles,
        css`
            :host {
                display: block;
                width: 100%;
                aspect-ratio: 8 / 1;
            }

            canvas {
                width: 100%;
                height: 100%;
            }
        `,
    ];

    @query("canvas")
    private canvas!: HTMLCanvasElement;

    private ctx: CanvasRenderingContext2D;
    private scope: Oscilloscope;

    public start() {
        this.scope.start();
    }

    public stop() {
        this.scope.stop();
    }

    override render() {
        const width = Math.floor(800 * window.devicePixelRatio);
        const height = Math.floor(100 * window.devicePixelRatio);

        return html`<canvas width="${width}" height="${height}"></canvas>`;
    }

    protected override firstUpdated(
        _changedProperties: PropertyValueMap<any> | Map<PropertyKey, unknown>,
    ): void {
        const computedStyles = window.getComputedStyle(this);
        this.ctx = this.canvas.getContext("2d", { alpha: false })!;
        this.scope = new Oscilloscope(
            this.ctx,
            computedStyles.backgroundColor ?? "#333333",
            computedStyles.color ?? "#FF0000",
            6,
        );
    }
}

class Oscilloscope {
    public width: number;
    public height: number;
    public active: boolean = false;

    constructor(
        public ctx: CanvasRenderingContext2D,
        public backgroundColor: string,
        public strokeColor: string,
        public strokeWidth: number,
    ) {
        this.width = ctx.canvas.width;
        this.height = ctx.canvas.height;
        this.clear();
        this.drawSine();
    }

    start() {
        this.active = true;
        window.requestAnimationFrame(() => this.draw());
    }

    stop() {
        this.active = false;
    }

    clear() {
        this.ctx.beginPath();
        this.ctx.fillStyle = this.backgroundColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
    }

    draw() {
        if (!prefersReducedMotion.matches) {
            this.drawAnalyzer();
        } else {
            this.drawSine();
        }
    }

    drawAnalyzer() {
        const data = AudioContextManager.instance.analyzerData;
        const zeroCrossing =
            AudioContextManager.findFirstPositiveZeroCrossing(data);

        this.clear();
        this.ctx.lineJoin = "round";
        this.ctx.lineWidth = this.strokeWidth;
        this.ctx.strokeStyle = this.strokeColor;

        // this.ctx.beginPath();
        // this.ctx.moveTo(0, this.height / 2);
        // this.ctx.lineTo(this.width, this.height / 2);
        // this.ctx.stroke();

        this.ctx.beginPath();

        const ymid = this.height / 2;

        for (let x = 0; x < this.width; x++) {
            let sampleIdx = Math.round((x / this.width) * data.length);
            sampleIdx = (zeroCrossing + sampleIdx) % data.length;
            const sample = data[sampleIdx] ?? 0;
            const sampleNorm = (sample - 127) / 127;
            const y = ymid + sampleNorm * 1.6 * ymid;

            if (x === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        }

        this.ctx.lineTo(this.width + 10, ymid);
        this.ctx.stroke();

        if (this.active) {
            window.requestAnimationFrame(() => this.drawAnalyzer());
        }
    }

    private sineOffset = 0;

    drawSine() {
        this.clear();
        this.ctx.lineWidth = this.strokeWidth;
        this.ctx.strokeStyle = this.strokeColor;
        this.ctx.beginPath();

        const divider = 4;
        const width = this.width / divider;

        for (let i = -2; i < width + 2; i++) {
            var v = Math.sin(8 * Math.PI * (i / width) + this.sineOffset / 8);
            var y = this.height / 2 + ((v * this.height) / 2) * 0.9;
            if (i === -2) {
                this.ctx.moveTo(i * divider, y);
            } else {
                this.ctx.lineTo(i * divider, y);
            }
        }

        this.ctx.stroke();

        this.sineOffset++;

        if (this.active) {
            window.requestAnimationFrame(() => this.drawSine());
        }
    }
}
