"""Small auditable RS reference, not a production codec.

GF(256): polynomial 0x11d, generator 2. Systematic shortened RS, roots
alpha^0,...,alpha^(nsym-1); only nsym=2 or 4. Corrects one or two unknown
symbol substitutions, including parity. No erasure, insertion or soft decoder.
The packet hash/CRC is IN-BAND and encoded too; framing is assumed trusted.
"""

import hashlib
from functools import lru_cache
import zlib


def slow_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 256:
            a ^= 0x11d
        b >>= 1
    return result


EXP, LOG = [1]*510, [0]*256
for i in range(1, 255):
    EXP[i] = slow_mul(EXP[i-1], 2)
for i in range(255):
    LOG[EXP[i]] = i
    EXP[i+255] = EXP[i]


def mul(a, b):
    return EXP[LOG[a]+LOG[b]] if a and b else 0


def div(a, b):
    if not b:
        raise ValueError("GF division by zero")
    return EXP[(LOG[a]-LOG[b]) % 255] if a else 0


def evaluate(coefficients, x):
    value = 0
    for coefficient in coefficients:
        value = mul(value, x)^coefficient
    return value


@lru_cache(None)
def generator(nsym):
    if nsym not in (2, 4):
        raise ValueError("Only one- and two-symbol correction are implemented")
    result = [1]
    for root in EXP[:nsym]:
        updated = [0]*(len(result)+1)
        for i, coefficient in enumerate(result):
            updated[i] ^= coefficient
            updated[i+1] ^= mul(coefficient, root)
        result = updated
    return tuple(result)


def encode(data, nsym):
    g = generator(nsym)
    if not 1 <= len(data) <= 255-nsym:
        raise ValueError("Invalid shortened RS data length")
    remainder = list(data)+[0]*nsym
    for i in range(len(data)):
        factor = remainder[i]
        for j in range(1, len(g)):
            remainder[i+j] ^= mul(factor, g[j])
    return bytes(data)+bytes(remainder[-nsym:])


def syndromes(codeword, nsym):
    generator(nsym)  # Validate profile.
    return tuple(evaluate(codeword, root) for root in EXP[:nsym])


def decode(received, nsym):
    if not nsym < len(received) <= 255:
        raise ValueError("Invalid shortened RS word length")
    s = syndromes(received, nsym)
    if not any(s):
        return bytes(received[:-nsym])
    # Error locator X_i=alpha^(n-1-position_i); S_j=sum e_i*X_i^j.
    locations = {EXP[len(received)-1-i]: i for i in range(len(received))}
    if s[0]:
        locator = div(s[1], s[0])
        if locator in locations:
            candidate = bytearray(received)
            candidate[locations[locator]] ^= s[0]
            if not any(syndromes(candidate, nsym)):
                return bytes(candidate[:-nsym])
    if nsym == 2:
        raise ValueError("Not a one-error syndrome")
    determinant = mul(s[1], s[1])^mul(s[0], s[2])
    if not determinant:
        raise ValueError("No two-error locator")
    sigma1 = div(mul(s[1], s[2])^mul(s[0], s[3]), determinant)
    sigma2 = div(mul(s[1], s[3])^mul(s[2], s[2]), determinant)
    roots = [x for x in locations if mul(x, x)^mul(sigma1, x)^sigma2 == 0]
    if len(roots) != 2:
        raise ValueError("Two distinct error locations not found")
    x1, x2 = roots
    e1 = div(s[1]^mul(s[0], x2), x1^x2)
    e2 = s[0]^e1
    candidate = bytearray(received)
    candidate[locations[x1]] ^= e1
    candidate[locations[x2]] ^= e2
    if any(syndromes(candidate, nsym)):
        raise ValueError("Candidate has nonzero syndrome")
    return bytes(candidate[:-nsym])


def packet_digest(payload):
    return hashlib.sha256(b"MRI-OFFLINE-V1"+len(payload).to_bytes(8, "little")+payload).digest()


def encode_packet(payload, nsym=4, integrity="sha256"):
    if integrity == "sha256":
        protected = payload+packet_digest(payload)
        chunk = 255-nsym
        return tuple(encode(protected[i:i+chunk], nsym) for i in range(0, len(protected), chunk))
    if integrity == "crc32-frame":
        chunk = 255-nsym-4
        return tuple(
            encode(data+zlib.crc32(index.to_bytes(8, "little")+data).to_bytes(4, "little"), nsym)
            for index, offset in enumerate(range(0, len(payload), chunk))
            for data in (payload[offset:offset+chunk],)
        )
    raise ValueError("Unknown integrity profile")


def decode_packet(blocks, payload_length, nsym=4, integrity="sha256"):
    """Return None on rejection. Hash/CRC protects accidents, not an adversary."""
    try:
        decoded = [decode(block, nsym) for block in blocks]
    except ValueError:
        return None
    if integrity == "sha256":
        candidate = b"".join(decoded)
        if len(candidate) != payload_length+32:
            return None
        payload = candidate[:-32]
        return payload if packet_digest(payload) == candidate[-32:] else None
    if integrity == "crc32-frame":
        result = []
        for index, data in enumerate(decoded):
            if len(data) < 5:
                return None
            payload, reference = data[:-4], data[-4:]
            if zlib.crc32(index.to_bytes(8, "little")+payload).to_bytes(4, "little") != reference:
                return None
            result.append(payload)
        candidate = b"".join(result)
        return candidate if len(candidate) == payload_length else None
    raise ValueError("Unknown integrity profile")


def gf_checks(data):
    """Two EXTERNAL trusted checks, not a length-258 ordinary RS codeword.

    Locators are all field elements 0..255, so 256 data positions are possible;
    the log(alpha^i) convention unnecessarily excludes locator zero.
    """
    if len(data) > 256:
        raise ValueError("GF(256) provides 256 distinct locators")
    s0 = s1 = 0
    for i, byte in enumerate(data):
        s0 ^= byte
        s1 ^= mul(i, byte)
    return s0, s1


def recover_gf_checks(data, reference):
    current = gf_checks(data)
    e, weighted = (a^b for a, b in zip(current, reference))
    if not e:
        if weighted:
            raise ValueError("Outside single-data-symbol model")
        return bytes(data)
    position = div(weighted, e)
    if position >= len(data):
        raise ValueError("Location outside frame")
    candidate = bytearray(data)
    candidate[position] ^= e
    return bytes(candidate)
