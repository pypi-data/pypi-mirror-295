/*
    Copyright (c) 2024 Winterbloom LLC, Alethea Katherine Flowers
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { assert } from "@esm-bundle/chai";

import { VERSION } from "../src/scripts";

suite("wintersong", function () {
    test(".VERSION", function () {
        assert.isString(VERSION);
    });
});
