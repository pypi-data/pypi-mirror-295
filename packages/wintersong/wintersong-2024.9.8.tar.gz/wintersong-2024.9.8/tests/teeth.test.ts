/*
    Copyright (c) 2021 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { assert } from "@esm-bundle/chai";

import Teeth from "../src/scripts/teeth";

function* generate_data(length) {
    for (let i = 0; i < length; i++) {
        yield i % 256;
    }
}

function* generate_random_data(length) {
    for (let i = 0; i < length; i++) {
        yield Math.floor(Math.random() * 255);
    }
}

suite("teeth", function () {
    test("Encode/decode", function () {
        for (let n = 1; n < 128; n++) {
            const original = Uint8Array.from(generate_data(n));
            const encoded = Teeth.encode(original);
            const decoded = Teeth.decode(encoded);

            assert.equal(encoded.length, Teeth.encodedLength(original));
            assert.deepEqual(decoded, original);
        }
    });

    test("Encode/decode (randomized)", () => {
        for (let n = 1; n < 128; n++) {
            const original = Uint8Array.from(generate_random_data(n));
            const encoded = Teeth.encode(original);
            const decoded = Teeth.decode(encoded);

            assert.equal(encoded.length, Teeth.encodedLength(original));
            assert.deepEqual(decoded, original);
        }
    });
});
