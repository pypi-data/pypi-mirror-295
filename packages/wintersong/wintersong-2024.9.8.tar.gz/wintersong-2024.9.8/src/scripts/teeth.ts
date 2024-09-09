/*
    Copyright (c) 2021 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

/**
 * Teeth encoding/decoding routines
 *
 * > What the heck is Teeth encoding?
 *
 * It's a really dumb encoding scheme designed to deal with sending data over
 * MIDI SysEx which is limited to 7-bit values. It encodes each 32-bit (4 byte)
 * value using 5 bytes, therefore, it has a 25% overhead. It's designed to
 * be deterministic so that C implementations can avoid dynamic allocation -
 * regardless of the number of items in the encoder input, the encoded output
 * is *always* a deterministic multiple of 5.
 *
 * The basic scheme is that the following 32-bit value:
 *
 *     0x1AAA AAAA
 *     0x2BBB BBBB
 *     0x3CCC CCCC
 *     0x4DDD DDDD
 *
 * Gets encoded as:
 *
 *     0x4A <--- header byte
 *     0x0AAA AAAA
 *     0x0BBB BBBB
 *     0x0CCC CCCC
 *     0x0DDD DDDD
 *
 * The header byte's upper nibble is number of following bytes, its max value is
 * 4. This allows encoding and decoding arrays that aren't a multiple of 4 bytes
 * in length and preserving the length during decoding.
 *
 * The second nibble contains the most significant bit for each of the
 * directly following bytes as 0b1234.
 *
 * > Why the HECK did you name it Teeth?
 *
 * It works on 32-bit values and humans happen to have 32 teeth, also, it takes
 * one more byte than usual to encode so it's an *overbyte*...
 *
 */
export default class Teeth {
    static encodedLength(src_len: number | Uint8Array): number {
        if (src_len instanceof Uint8Array) {
            src_len = src_len.length;
        }
        return Math.floor((src_len + 4 - 1) / 4) * 5;
    }

    static encode(src: Uint8Array): Uint8Array {
        const src_len = src.length;
        let dst = new Uint8Array(this.encodedLength(src_len));
        let src_idx = 0;
        let dst_idx = 0;

        while (src_idx < src_len) {
            // There's 4 or more bytes left
            if (src_idx + 4 <= src_len) {
                // First byte carries the leftover bits.
                dst[dst_idx] =
                    0x40 |
                    ((src[src_idx]! & 0x80) >> 4) |
                    ((src[src_idx + 1]! & 0x80) >> 5) |
                    ((src[src_idx + 2]! & 0x80) >> 6) |
                    ((src[src_idx + 3]! & 0x80) >> 7);
                // Subsequent bytes carry their lower 7 bits.
                dst[dst_idx + 1] = src[src_idx]! & 0x7f;
                dst[dst_idx + 2] = src[src_idx + 1]! & 0x7f;
                dst[dst_idx + 3] = src[src_idx + 2]! & 0x7f;
                dst[dst_idx + 4] = src[src_idx + 3]! & 0x7f;
                dst_idx += 5;
                src_idx += 4;
            }
            // There's only 3 bytes left
            else if (src_idx + 3 == src_len) {
                dst[dst_idx] =
                    0x30 |
                    ((src[src_idx]! & 0x80) >> 4) |
                    ((src[src_idx + 1]! & 0x80) >> 5) |
                    ((src[src_idx + 2]! & 0x80) >> 6);
                dst[dst_idx + 1] = src[src_idx]! & 0x7f;
                dst[dst_idx + 2] = src[src_idx + 1]! & 0x7f;
                dst[dst_idx + 3] = src[src_idx + 2]! & 0x7f;
                dst_idx += 4;
                src_idx += 3;
            }
            // There's only 2 bytes left
            else if (src_idx + 2 == src_len) {
                dst[dst_idx] =
                    0x20 |
                    ((src[src_idx]! & 0x80) >> 4) |
                    ((src[src_idx + 1]! & 0x80) >> 5);
                dst[dst_idx + 1] = src[src_idx]! & 0x7f;
                dst[dst_idx + 2] = src[src_idx + 1]! & 0x7f;
                dst_idx += 3;
                src_idx += 2;
            }
            // There's only 1 byte left
            else if (src_idx + 1 == src_len) {
                dst[dst_idx] = 0x10 | ((src[src_idx]! & 0x80) >> 4);
                dst[dst_idx + 1] = src[src_idx]! & 0x7f;
                dst_idx += 2;
                src_idx += 1;
            } else {
                break;
            }
        }

        return dst;
    }

    static decode(src: Uint8Array): Uint8Array {
        const src_len = src.length;
        const dst_len = (src_len / 5) * 4;
        let dst = new Uint8Array(dst_len);
        let src_idx = 0;
        let dst_idx = 0;

        while (src_idx < src_len) {
            dst[dst_idx] = ((src[src_idx]! & 0x8) << 4) | src[src_idx + 1]!;
            dst[dst_idx + 1] = ((src[src_idx]! & 0x4) << 5) | src[src_idx + 2]!;
            dst[dst_idx + 2] = ((src[src_idx]! & 0x2) << 6) | src[src_idx + 3]!;
            dst[dst_idx + 3] = ((src[src_idx]! & 0x1) << 7) | src[src_idx + 4]!;
            let len_marker = src[src_idx]! >> 4;
            dst_idx += len_marker;
            src_idx += 5;
        }

        return dst.slice(0, dst_idx);
    }
}
