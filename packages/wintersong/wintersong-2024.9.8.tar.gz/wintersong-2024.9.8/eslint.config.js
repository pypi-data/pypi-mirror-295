import js from "@eslint/js";
import typescriptPlugin from "@typescript-eslint/eslint-plugin";
import typescriptParser from "@typescript-eslint/parser";
import configPrettier from "eslint-config-prettier";
import litPlugin from "eslint-plugin-lit";
import mochaPlugin from "eslint-plugin-mocha";
import wcPlugin from "eslint-plugin-wc";
import globals from "globals";

export default [
    { files: ["src/**/*.ts", "tests/**/*.ts"] },
    js.configs.recommended,
    configPrettier,
    {
        languageOptions: {
            ecmaVersion: 2021,
            sourceType: "module",
            parser: typescriptParser,
            globals: {
                ...globals.browser,
                ...globals.mocha,
            },
        },
        plugins: {
            "@typescript-eslint": typescriptPlugin,
            mocha: mochaPlugin,
        },
        rules: {
            ...typescriptPlugin.configs.recommended.rules,
            ...mochaPlugin.configs.recommended.rules,
            ...litPlugin.configs.recommended.rules,
            ...wcPlugin.configs.recommended.rules,
            ...wcPlugin.configs["best-practice"].rules,
            "@typescript-eslint/no-explicit-any": "off",
            "@typescript-eslint/no-empty-function": 0,
            "@typescript-eslint/no-non-null-assertion": "off",
            "@typescript-eslint/no-unused-vars": [
                "error",
                {
                    vars: "all",
                    args: "none",
                    ignoreRestSiblings: true,
                    varsIgnorePattern: "([Ii]gnored)|([Uu]nused)|(_)",
                },
            ],
            "@typescript-eslint/no-inferrable-types": [
                "warn",
                { ignoreProperties: true, ignoreParameters: true },
            ],
            "mocha/max-top-level-suites": "off",
        },
    },
];
