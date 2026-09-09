"""Reference-code checks, including parity faults and over-radius failures."""

import random
import unittest

if __package__:
    from . import mri_rs_reference as r
else:
    import mri_rs_reference as r


def independent_parity(data, nsym):
    """Solve the parity-check equations directly with polynomial GF arithmetic.

    No log table, polynomial division, or production encoder is used here.
    """
    def power(a, exponent):
        value = 1
        for _ in range(exponent):
            value = r.slow_mul(value, a)
        return value

    n = len(data)+nsym
    equations = []
    for j in range(nsym):
        root = power(2, j)
        rhs = 0
        for i, byte in enumerate(data):
            rhs ^= r.slow_mul(byte, power(root, n-1-i))
        equations.append([power(root, nsym-1-i) for i in range(nsym)]+[rhs])
    for col in range(nsym):
        pivot = next(row for row in range(col, nsym) if equations[row][col])
        equations[col], equations[pivot] = equations[pivot], equations[col]
        inverse = power(equations[col][col], 254)
        equations[col] = [r.slow_mul(a, inverse) for a in equations[col]]
        for row in range(nsym):
            if row != col:
                factor = equations[row][col]
                equations[row] = [a ^ r.slow_mul(factor, b)
                                  for a, b in zip(equations[row], equations[col])]
    return bytes(row[-1] for row in equations)


class FieldAndEncoder(unittest.TestCase):
    def test_all_field_products_and_primitive_generator(self):
        self.assertEqual(set(r.EXP[:255]), set(range(1, 256)))
        for a in range(256):
            for b in range(256):
                self.assertEqual(r.mul(a, b), r.slow_mul(a, b))
        for a in range(1, 256):
            self.assertEqual(r.mul(a, r.div(1, a)), 1)

    def test_encoder_against_independent_linear_system(self):
        rng = random.Random(20260909)
        for nsym in (2, 4):
            for length in (1, 3, 17, 255-nsym):
                data = rng.randbytes(length)
                codeword = r.encode(data, nsym)
                self.assertEqual(codeword, data+independent_parity(data, nsym))
                self.assertFalse(any(r.syndromes(codeword, nsym)))
                self.assertEqual(r.decode(codeword, nsym), data)

    def test_invalid_profile_and_length(self):
        for nsym in (0, 1, 3, 5):
            with self.assertRaises(ValueError):
                r.encode(b"abc", nsym)
        for nsym in (2, 4):
            for data in (b"", bytes(256-nsym)):
                with self.assertRaises(ValueError):
                    r.encode(data, nsym)


class SymbolCorrections(unittest.TestCase):
    def test_exhaustive_one_symbol_including_parity(self):
        data = bytes((i*37+11) % 256 for i in range(253))
        encoded = r.encode(data, 2)
        # 255 codeword positions x 255 nonzero XOR changes = 65,025.
        for position in range(255):
            for error in range(1, 256):
                received = bytearray(encoded)
                received[position] ^= error
                self.assertEqual(r.decode(received, 2), data, (position, error))

    def test_every_pair_on_shortened_word_including_zero_sum_syndrome(self):
        data = b"ABCDEFGHIJK"  # 15-symbol shortened RS word.
        encoded = r.encode(data, 4)
        for first in range(15):
            for second in range(first+1, 15):
                for e1, e2 in ((1, 1), (2, 7), (255, 255), (255, 19)):
                    received = bytearray(encoded)
                    received[first] ^= e1
                    received[second] ^= e2
                    self.assertEqual(r.decode(received, 4), data)

    def test_seeded_two_symbol_errors_full_length(self):
        rng = random.Random(20260910)
        for _ in range(1000):
            data = rng.randbytes(251)
            encoded = r.encode(data, 4)
            positions = rng.sample(range(255), 2)
            received = bytearray(encoded)
            for position in positions:
                received[position] ^= rng.randrange(1, 256)
            self.assertEqual(r.decode(received, 4), data)

    def test_rs_alone_can_miscorrect_beyond_radius(self):
        data = bytes(range(253))
        received = bytearray(r.encode(data, 2))
        received[0] ^= 1
        received[1] ^= 3
        wrong = r.decode(received, 2)
        self.assertNotEqual(wrong, data)
        self.assertEqual(wrong[2], data[2] ^ 2)

    def test_external_checks_allow_zero_locator_but_are_not_in_band_rs(self):
        data = bytes(range(256))
        reference = r.gf_checks(data)
        for position in range(256):
            for error in (1, 2, 128, 255):
                received = bytearray(data)
                received[position] ^= error
                self.assertEqual(r.recover_gf_checks(received, reference), data)
        # Alter a check instead: it can cause a false repair. No hash here.
        self.assertNotEqual(r.recover_gf_checks(data, (reference[0] ^ 1, reference[1])), data)


class PacketIntegrity(unittest.TestCase):
    def test_corrects_data_parity_and_inband_integrity_bytes(self):
        rng = random.Random(20260911)
        payload = rng.randbytes(16384)
        for nsym, integrity in ((2, "sha256"), (4, "sha256"), (4, "crc32-frame")):
            blocks = r.encode_packet(payload, nsym, integrity)
            damaged = []
            for block in blocks:
                result = bytearray(block)
                for position in rng.sample(range(len(block)), nsym//2):
                    result[position] ^= rng.randrange(1, 256)
                damaged.append(bytes(result))
            self.assertEqual(r.decode_packet(damaged, len(payload), nsym, integrity), payload)
            # SHA/CRC inside the last block, not an untouched external reference.
            damaged = list(blocks)
            last = bytearray(damaged[-1])
            last[-nsym-1] ^= 47
            damaged[-1] = bytes(last)
            self.assertEqual(r.decode_packet(damaged, len(payload), nsym, integrity), payload)

    def test_sha_rejects_demonstrated_rs_miscorrection(self):
        payload = bytes(range(256))*2
        blocks = list(r.encode_packet(payload, 2))
        first = bytearray(blocks[0])
        first[0] ^= 1
        first[1] ^= 3
        self.assertNotEqual(r.decode(first, 2), payload[:253])
        blocks[0] = bytes(first)
        self.assertIsNone(r.decode_packet(blocks, len(payload), 2))

    def test_rejects_reordering_missing_block_and_wrong_length(self):
        payload = bytes(range(256))*4
        for integrity in ("sha256", "crc32-frame"):
            blocks = list(r.encode_packet(payload, 4, integrity))
            blocks[0], blocks[1] = blocks[1], blocks[0]
            self.assertIsNone(r.decode_packet(blocks, len(payload), 4, integrity))
            blocks = r.encode_packet(payload, 4, integrity)
            self.assertIsNone(r.decode_packet(blocks[:-1], len(payload), 4, integrity))
            self.assertIsNone(r.decode_packet(blocks, len(payload)-1, 4, integrity))

    def test_coherent_new_packet_is_not_authenticated(self):
        original, replacement = b"abc", b"abd"
        blocks = r.encode_packet(replacement)
        self.assertEqual(r.decode_packet(blocks, len(original)), replacement)

    def test_same_payload_budgets_with_shortened_last_block(self):
        payload = bytes(16384)
        for nsym, integrity, count, overhead in (
            (2, "sha256", 65, 162),
            (4, "sha256", 66, 296),
            (4, "crc32-frame", 67, 536),
        ):
            blocks = r.encode_packet(payload, nsym, integrity)
            self.assertEqual(len(blocks), count)
            self.assertEqual(sum(map(len, blocks))-len(payload), overhead)
            self.assertEqual(r.decode_packet(blocks, len(payload), nsym, integrity), payload)


if __name__ == "__main__":
    unittest.main()
