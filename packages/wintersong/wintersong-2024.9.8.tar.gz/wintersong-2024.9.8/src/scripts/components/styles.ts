/*
    Copyright (c) 2024 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { css } from "lit";

export default css`
    :host {
        box-sizing: border-box;
        display: block;
    }

    :host *,
    :host *::before,
    :host *::after {
        box-sizing: inherit;
    }

    [hidden] {
        display: none !important;
    }

    .elevated {
        box-shadow: var(--elevation-shadow, none);
    }
`;
