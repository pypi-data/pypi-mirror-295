/*
    Copyright (c) 2024 Winterbloom LLC, Alethea Katherine Flowers
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { bundleTs } from "./bundle-ts.js";
import { bundleCss } from "./bundle-css.js";

const ts = await bundleTs(true);
const css = await bundleCss(true);

for (const { options, context } of [ts, css]) {
    console.log(`Building to ${options.outfile}`);
    let result = await context.rebuild();

    console.log(`Build complete!`);

    if (result.warnings) {
        console.log(`${result.warnings.length} warnings`);
        for (const msg of result.warnings) {
            console.log("- ", msg);
        }
    }

    if (result.errors) {
        console.log(`${result.errors.length} errors`);
        for (const msg of result.errors) {
            console.log("- ", msg);
        }
    }

    console.log();

    context.dispose();
}
