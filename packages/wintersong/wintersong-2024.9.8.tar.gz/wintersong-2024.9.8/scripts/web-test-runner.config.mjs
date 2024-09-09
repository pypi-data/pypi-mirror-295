/*
    Copyright (c) 2024 Winterbloom LLC, Alethea Katherine Flowers
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { fileURLToPath } from "url";
import { defaultReporter, summaryReporter } from "@web/test-runner";
import { esbuildPlugin } from "@web/dev-server-esbuild";

// https://modern-web.dev/docs/test-runner/cli-and-configuration/

export default {
    files: "tests/**/*.test.ts",
    nodeResolve: {
        exportConditions: ["production", "default"],
    },
    debugger: true,
    plugins: [
        esbuildPlugin({
            ts: true,
            tsconfig: fileURLToPath(
                new URL("../tsconfig.json", import.meta.url),
            ),
            define: {
                DEBUG: "false",
            },
        }),
    ],
    reporters: [
        defaultReporter({ reportTestResults: true, reportTestProgress: true }),
        summaryReporter(),
    ],
    testFramework: {
        config: {
            ui: "tdd",
        },
    },
};
