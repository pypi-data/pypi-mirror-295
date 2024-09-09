/*
    Copyright (c) 2023 Opulo, Inc
    Published under the Mozilla Public License
    Full text available at: https://www.mozilla.org/en-US/MPL/
*/

import { bundleTs } from "./bundle-ts.js";
import { bundleCss } from "./bundle-css.js";

const ts = await bundleTs(false);
const css = await bundleCss(false);

for (const { options, context } of [ts, css]) {
    await context.watch();
    console.log(`Watching and building to ${options.outfile}`);
}
