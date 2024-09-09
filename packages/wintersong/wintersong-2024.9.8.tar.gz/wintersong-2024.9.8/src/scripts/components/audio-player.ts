/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, css, html, type TemplateResult } from "lit";
import { html as staticHtml } from "lit/static-html.js";
import { customElement, property, query } from "lit/decorators.js";
import { AudioContextManager } from "../audio/context-manager";
import { WinterAudioOscilloscopeElement } from "./audio-oscilloscope";
import baseStyles from "./styles";

/**
 * Audio player element with oscilloscope view
 */
@customElement("winter-audio-player")
export class WinterAudioPlayerElement extends LitElement {
    private static instances: Set<WinterAudioPlayerElement> = new Set();

    static override styles = [
        baseStyles,
        css`
            div {
                display: flex;
                flex-direction: column;
                width: 100%;
                max-width: 100%;
                padding: 0;
                color: white;
                background-color: #408d94;
                border: 0px solid transparent;
                border-radius: 0.2em;
            }

            audio {
                display: block;
                width: 90%;
                margin: 1em auto;
            }

            winter-audio-oscilloscope {
                background-color: inherit;
                color: inherit;
                margin: 2em 0 0.5em 0;
            }

            p {
                font-size: 1.25em;
                text-align: center;
                margin: 0 0 0.75em 0;
            }
        `,
    ];

    @query("audio")
    private audio!: HTMLAudioElement;

    @query("winter-audio-oscilloscope")
    private oscilloscope: WinterAudioOscilloscopeElement;

    private audioSourceNode: MediaElementAudioSourceNode;

    @property()
    src: string;

    @property({ type: Boolean })
    loop: boolean;

    public get currentTime() {
        return this.audio?.currentTime;
    }

    public set currentTime(value: number) {
        this.audio.currentTime = value;
    }

    public get duration() {
        return this.audio?.duration;
    }

    public get ended() {
        return this.audio?.ended;
    }

    public get networkState() {
        return this.audio?.networkState;
    }

    public get paused() {
        return this.audio?.paused;
    }

    public get readyState() {
        return this.audio?.readyState;
    }

    public get volume() {
        return this.audio?.volume;
    }

    public set volume(value: number) {
        this.audio.volume = value;
    }

    public play() {
        this.audio?.play();
    }

    public pause() {
        this.audio?.pause();
    }

    private pauseOthers() {
        const staticThis = this.constructor as typeof WinterAudioPlayerElement;
        for (const instance of staticThis.instances) {
            if (instance !== this) {
                instance.pause();
            }
        }
    }

    private connectSource() {
        const manager = AudioContextManager.instance;

        if (!this.audioSourceNode) {
            this.audioSourceNode = manager.createSource(this.audio);
        }

        manager.activeSource = this.audioSourceNode;
    }

    private onAudioPlay() {
        this.pauseOthers();
        this.connectSource();
        this.oscilloscope.start();
    }

    private onAudioPauseOrEnd() {
        this.oscilloscope.stop();
    }

    override connectedCallback(): void {
        super.connectedCallback();
        const staticThis = this.constructor as typeof WinterAudioPlayerElement;
        staticThis.instances.add(this);
    }

    override disconnectedCallback(): void {
        super.disconnectedCallback();
        const staticThis = this.constructor as typeof WinterAudioPlayerElement;
        staticThis.instances.delete(this);
    }

    override render() {
        let sources: NodeListOf<HTMLElement> | TemplateResult =
            this.querySelectorAll("source");

        if (!sources.length) {
            sources = staticHtml`<source src="${this.src}" />`;
        }

        return html`<div class="elevated">
            <winter-audio-oscilloscope></winter-audio-oscilloscope>
            <audio
                controls
                crossorigin="anonymous"
                ?loop=${this.loop}
                title="${this.title}"
                @play=${this.onAudioPlay}
                @pause=${this.onAudioPauseOrEnd}
                @ended=${this.onAudioPauseOrEnd}>
                ${sources}
            </audio>
            <p>${this.title}</p>
        </div>`;
    }
}
