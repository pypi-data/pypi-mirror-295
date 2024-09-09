/*
    Copyright (c) 2024 Winterbloom LLC, Alethea Katherine Flowers
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import esbuild from "esbuild";

export async function bundleCss(minify = false, options = {}) {
    options = {
        entryPoints: ["src/styles/index.css"],
        outfile: "dist/winter.css",
        supported: {
            nesting: false,
        },
        bundle: true,
        keepNames: true,
        minify: minify,
        sourcemap: !minify,
        loader: {
            ".svg": "dataurl",
        },
        ...options,
    };
    return { options: options, context: await esbuild.context(options) };
}
