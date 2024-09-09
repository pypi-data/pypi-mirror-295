/*
    Copyright (c) 2024 Winterbloom LLC, Alethea Katherine Flowers
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import esbuild from "esbuild";

export async function bundleTs(minify = false, options = {}) {
    options = {
        entryPoints: ["src/scripts/index.ts"],
        outfile: "dist/winter.js",
        bundle: true,
        format: "esm",
        target: "es2022",
        keepNames: true,
        minify: minify,
        sourcemap: !minify,
        metafile: true,
        loader: {
            ".js": "ts",
            ".css": "text",
        },
        plugins: [CSSMinifyPlugin],
        ...options,
    };
    return { options: options, context: await esbuild.context(options) };
}

// Minify CSS when used with the text loader.
export const CSSMinifyPlugin = {
    name: "CSSMinifyPlugin",
    setup(build) {
        const options = build.initialOptions;

        build.onLoad({ filter: /\.css$/ }, async (args) => {
            let output = await readFile(args.path);
            let sourcemap = "";
            const { code, map } = await esbuild.transform(output, {
                loader: "css",
                minify: options.minify,
                sourcemap: options.sourcemap,
                sourcefile: args.path,
            });
            if (options.sourcemap) {
                sourcemap = toSourceMapURL(map);
            }

            output = sanitize(code);
            return `import { css } from '${this.specifier}';
        export const styles = css\`${output}\`;
        export default styles;${sourcemap}`;
        });
    },
};

function sanitize(input) {
    return input.replace(/(\$\{|`)/g, "\\$1");
}

function toSourceMapURL(map) {
    return (
        "\n" +
        `//# sourceMappingURL=data:application/json;base64,${Buffer.from(
            map,
        ).toString("base64")}`
    );
}
