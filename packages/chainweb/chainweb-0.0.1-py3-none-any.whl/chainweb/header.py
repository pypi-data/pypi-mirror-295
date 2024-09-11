import json
import math
from dataclasses import dataclass, field
from typing import NewType
from enum import Flag
from hashlib import blake2s
from time import time
from struct import unpack, pack

from chainweb.utils import decode_base64, encode_base64_bytes, json_decode_bytes
from chainweb.primitives import ChainwebDbContent, ChainwebException, sha512t256_from_b64, sha512t256_to_b64
from chainweb.primitives import ChainwebVersion, ChainId, BlockTime, BlockHeight
from chainweb.primitives import Target, PayloadHash, Weight, Nonce, BlockHash

# ############################################################################ #
# Utils

def pow2nat(t : bytes) -> int:
    """interprets the bytes as a little-endian unsigned integer"""
    return int.from_bytes(t, byteorder="little", signed=False)

# ############################################################################ #
# Exceptions

class HeaderException(ChainwebException):
    """Base class for block header exceptions."""
class HeaderDecodeException(HeaderException):
    """Exception raised for errors in the decoding of a block header."""

# ############################################################################ #
# Basic Types

Adjacents = NewType('Adjacents', dict[ChainId, BlockHash])

class FeatureFlags(Flag):
    NONE = 0

# ############################################################################ #
# Header

@dataclass(frozen=True, eq=True)
class Header(ChainwebDbContent[BlockHash]):
    """Chainweb Block Header"""

    headerbytes: bytes = field(compare = False)
    feature_flags: FeatureFlags = field(compare = False)
    creation_time: BlockTime = field(compare = False)
    parent: BlockHash = field(compare = False)
    adjacents: Adjacents = field(compare = False)
    target: Target = field(compare = False)
    payload_hash: PayloadHash = field(compare = False)
    chain_id: ChainId = field(compare = False)
    weight: Weight = field(compare = False)
    height: BlockHeight = field(compare = False)
    chainweb_version: ChainwebVersion = field(compare = False)
    epoch_start: BlockTime = field(compare = False)
    nonce: Nonce = field(compare = False)
    hash: BlockHash = field(compare = True, hash = True)

    ADJACENT_COUNT : int = 3
    SIZE_IN_BYTES : int = 208 + 2 + ADJACENT_COUNT * 36 # 318

    def check_size(self):
        assert self.headerbytes == self.SIZE_IN_BYTES

    def check_pow(self):
        powhash = blake2s(self.headerbytes).digest()
        assert pow2nat(powhash) <= pow2nat(self.target)

    def check_time(self):
        assert (self.creation_time <= time.time()) and (self.epoch_start <= self.creation_time)

    def check_height(self):
        assert self.height >= 0

    def check_adjacents(self):
        assert len(self.adjacents) == 3
        # TODO check graph

    @property
    def cls(self):
        return Header

    @property
    def content_hash(self) -> BlockHash:
        return self.hash

    @classmethod
    def header_from_bytes(cls, bs: bytes | bytearray | str):
        """Try to construct a Header object from a variety of encodings."""
        if len(bs) == cls.SIZE_IN_BYTES:
            if isinstance(bs, bytes):
                return cls.decode(bs)
            if isinstance(bs, bytearray):
                return cls.decode(bytes(bs))
            if isinstance(bs, str):
                raise HeaderDecodeException(f'unsupported type for constructing Header object: {type(bs)}')
            raise HeaderDecodeException(f'unsupported type for constructing Header object: {type(bs)}')
        if len(bs) == cls.SIZE_IN_BYTES * 2:
            if isinstance(bs, str):
                return cls.decode(bytes.fromhex(bs))
            raise HeaderDecodeException('unicode strings are not yet supported')
        if len(bs) == math.ceil(cls.SIZE_IN_BYTES * 4 / 3):
            if isinstance(bs, str):
                return cls.decode(decode_base64(bs))
            raise HeaderDecodeException('unicode strings are not yet supported')
        raise HeaderDecodeException(f'Header bytes have wrong length. Expected {cls.SIZE_IN_BYTES}, but got {len(bs)}')

    @classmethod
    def decode(cls, b : bytes):
        adjacentformat = 'H I 32s I 32s I 32s'
        hdrformat = f'<Q Q 32s {adjacentformat} 32s 32s I 32s  Q I Q 8s 32s'

        props = list(unpack(hdrformat, b))

        # assert that the number of adjacents matchs ADJACENT_COUNT
        assert props[3] == cls.ADJACENT_COUNT
        hdr = cls(
            headerbytes = b,
            feature_flags = props[0],
            creation_time = props[1],
            parent = props[2],
            adjacents = Adjacents({
                ChainId(props[4]): BlockHash(props[5]),
                ChainId(props[6]): BlockHash(props[7]),
                ChainId(props[8]): BlockHash(props[9]),
            }),
            target = props[10],
            payload_hash = props[11],
            chain_id = props[12],
            weight = props[13],
            height = props[14],
            chainweb_version = props[15],
            epoch_start = props[16],
            nonce = props[17],
            hash = props[18],
        )
        return hdr

    @classmethod
    def decode_json(cls, b : bytes):
        j = json_decode_bytes(b)
        return cls(
            headerbytes = b,
            feature_flags = FeatureFlags(j['featureFlags']),
            creation_time = BlockTime(j['creationTime']),
            parent = BlockHash(sha512t256_from_b64(j['parent'])),
            adjacents = Adjacents({
                ChainId(k): BlockHash(sha512t256_from_b64(v))
                for k, v in j['adjacents'].items()
            }),
            target = Target(decode_base64(j['target'])),
            payload_hash = PayloadHash(sha512t256_from_b64(j['payloadHash'])),
            chain_id = ChainId(j['chainId']),
            weight = Weight(decode_base64(j['weight'])),
            height = BlockHeight(j['height']),
            chainweb_version = ChainwebVersion(j['chainwebVersion']),
            epoch_start = BlockTime(j['epochStart']),
            nonce = Nonce(decode_base64(j['nonce'])),
            hash = BlockHash(sha512t256_from_b64(j['hash'])),
        )

    def encode(self) -> bytes:
        return self.headerbytes

    def encode_json(self) -> bytes:
        return json.dumps({
            'featureFlags': self.feature_flags,
            'creationTime': self.creation_time,
            'parent': sha512t256_to_b64(self.parent),
            'adjacents': {
                str(k): sha512t256_to_b64(v)
                for k, v in self.adjacents.items()
            },
            'target': encode_base64_bytes(self.target),
            'payloadHash': sha512t256_to_b64(self.payload_hash),
            'chainId': self.chain_id,
            'weight': encode_base64_bytes(self.weight),
            'height': self.height,
            'chainwebVersion': self.chainweb_version,
            'epochStart': self.epoch_start,
            'nonce': encode_base64_bytes(self.nonce),
            'hash': sha512t256_to_b64(self.hash),
        }).encode('utf-8')

    def encode_header_internal(self) -> bytes:
        adjacentformat = 'H I 32s I 32s I 32s'
        hdrformat = f'<Q Q 32s {adjacentformat} 32s 32s I 32s  Q I Q 8s 32s'

        return pack(hdrformat,
            self.feature_flags,
            self.creation_time,
            self.parent,
            self.ADJACENT_COUNT,
            self.adjacents[ChainId(0)],
            self.adjacents[ChainId(1)],
            self.adjacents[ChainId(2)],
            self.target,
            self.payload_hash,
            self.chain_id,
            self.weight,
            self.height,
            self.chainweb_version,
            self.epoch_start,
            self.nonce,
            self.hash,
        )