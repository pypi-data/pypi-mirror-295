/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

const FFT_SIZE = 4096;
const HAS_AUDIO_CONTEXT = window.AudioContext !== undefined;

/**
 * Since browsers limit the number of AudioContexts a page can use, this manages
 * a single AudioContext that can be used across multiple elements without
 * needing to create an AudioContext for each one.
 */
export class AudioContextManager {
    private static _instance: AudioContextManager;
    context: AudioContext;
    analyser: AnalyserNode;
    fftData: Uint8Array;
    private _activeSource?: MediaElementAudioSourceNode;

    private constructor() {
        if (HAS_AUDIO_CONTEXT) {
            this.createContext();
        }
    }

    static get instance() {
        if (!this._instance) {
            this._instance = new this();
        }
        return this._instance;
    }

    private createContext() {
        this.context = new window.AudioContext();
        this.analyser = this.context.createAnalyser();
        this.analyser.smoothingTimeConstant = 1;
        this.analyser.fftSize = FFT_SIZE;
        this.analyser.connect(this.context.destination);
        this.fftData = new Uint8Array(this.analyser.frequencyBinCount);
        this.activeSource = undefined;
    }

    private checkContext() {
        if (!this.context) {
            throw new Error("Audio context unavailable");
        }
    }

    createSource(mediaElement: HTMLMediaElement): MediaElementAudioSourceNode {
        this.checkContext();
        return this.context.createMediaElementSource(mediaElement);
    }

    get activeSource() {
        return this._activeSource;
    }

    set activeSource(src: MediaElementAudioSourceNode | undefined) {
        this.checkContext();

        if (this.activeSource) {
            this.activeSource.disconnect();
        }

        this._activeSource = src;

        if (this._activeSource) {
            this._activeSource.connect(this.analyser);
            this.context.resume();
        }
    }

    get analyzerData(): Uint8Array {
        this.analyser.getByteTimeDomainData(this.fftData);
        return this.fftData;
    }

    static findFirstPositiveZeroCrossing(data: Uint8Array) {
        let n = -1;
        for (let i = 0; i < data.length; i++) {
            const val = data[i]!;
            if (val < 128) {
                n = i;
            } else if (val >= 128 && n > -1) {
                return n;
            }
        }
        return 0;
    }
}
