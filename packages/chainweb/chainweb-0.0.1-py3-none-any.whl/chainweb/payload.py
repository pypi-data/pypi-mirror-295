import json
import math
from dataclasses import dataclass, field
from typing import NewType
from struct import unpack, unpack_from, calcsize, pack

from chainweb.utils import decode_base64, encode_base64_bytes, json_decode_bytes
from chainweb.primitives import ChainId, ChainwebDbContent, Sha512t256, PayloadHash, ChainwebException
from chainweb.primitives import sha512t256_from_b64

# ############################################################################ #
# Utils

def encode_len_prefixed(o: bytearray, s: bytes | bytearray):
    o += pack('>Q {len(s)}s', len(s), s)

def decode_len_prefixed(state):
    s = decode(state, '>Q')[0]
    return decode(state, f'{s}s')

def decode(state: list, fmt) -> tuple:
    bs, offset = state
    x = unpack_from(fmt, bs, offset)
    state[1] += calcsize(fmt)
    return x

def json_decode_transaction(b):
    tx = json_decode_bytes(b)
    cmdstr = tx['cmd']
    if cmdstr is not None:
        tx['cmd'] = json.loads(cmdstr)
    return tx

def get_meta(tx: dict) -> dict | None:
    if 'cmd' in tx and 'meta' in tx['cmd']:
        return tx['cmd']['meta']

def get_chainid(tx: dict) -> ChainId | None:
    if 'cmd' in tx and 'meta' in tx['cmd']:
        return tx['cmd']['meta']['chainId']

# ############################################################################ #
# Basic Types

BlockTransactionsHash = NewType('BlockTransactionsHash', Sha512t256) # SHA512/256
BlockOutputsHash = NewType('BlockOutputsHash', Sha512t256) # SHA512/256

TransactionBytes = NewType('TransactionBytes', bytes)
MinerDataBytes = NewType('MinerDataBytes', bytes)
OutputBytes = NewType('OutputBytes', bytes)
CoinbaseBytes = NewType('CoinbaseBytes', bytes)

# ############################################################################ #
# Exceptions

class PayloadException(ChainwebException):
    """Base class for payload exceptions."""
class PayloadDecodeException(PayloadException):
    """Exception raised for errors in the decoding of a payload."""

# ############################################################################ #
# Block Payload

@dataclass(frozen=True, eq=True)
class BlockPayload(ChainwebDbContent[PayloadHash]):
    """Chainweb Block Payload"""

    payload_hash: PayloadHash = field(compare = True, hash = True)
    transactions_hash: BlockTransactionsHash = field(compare = False)
    outputs_hash: BlockOutputsHash = field(compare = False)

    SIZE_IN_BYTES : int = 96

    @property
    def cls(self):
        return BlockPayload

    @property
    def content_hash(self) -> PayloadHash:
        return self.payload_hash

    @classmethod
    def payload_from_bytes(cls, bs: bytes | bytearray | str):
        """Try to construct a block payload from the input bytes or string by guessing the encoding"""
        if len(bs) == cls.SIZE_IN_BYTES:
            if isinstance(bs, bytes):
                return cls.decode(bs)
            if isinstance(bs, bytearray):
                return cls.decode(bytes(bs))
            if isinstance(bs, str):
                raise PayloadDecodeException(f'unsupported type for constructing BlockPayload object: {type(bs)}')
            raise PayloadDecodeException(f'unsupported type for constructing BlockPayload object: {type(bs)}')

        if len(bs) == cls.SIZE_IN_BYTES * 2:
            if isinstance(bs, str):
                return cls.decode(bytes.fromhex(bs))
            raise PayloadDecodeException('unicode strings are not yet supported')

        if len(bs) == math.ceil(cls.SIZE_IN_BYTES * 4 / 3):
            if isinstance(bs, str):
                return cls.decode(decode_base64(bs))
            raise PayloadDecodeException('unicode strings are not yet supported')

        raise PayloadDecodeException(f'BlockPayload bytes have wrong length. Expected {cls.SIZE_IN_BYTES}, but got {len(bs)}')

    def encode(self):
        """Custom binary encoding that is used in the chainweb database"""
        return pack('32s 32s 32s',
            self.payload_hash,
            self.transactions_hash,
            self.outputs_hash,
        )

    @classmethod
    def decode(cls, b: bytes):
        """Custom binary encoding that is used in the chainweb database"""
        props = list(unpack('32s 32s 32s', b))
        return cls(
            payload_hash = props[0],
            transactions_hash = props[1],
            outputs_hash = props[2],
        )

    def encode_json(self) -> bytes:
        return json.dumps({
            'payloadHash': encode_base64_bytes(self.payload_hash),
            'transactionsHash': encode_base64_bytes(self.transactions_hash),
            'outputsHash': encode_base64_bytes(self.outputs_hash),
        }).encode('utf-8')

    @classmethod
    def decode_json(cls, b : bytes):
        """JSON encoding that is used on the REST API and in the legacy database format"""
        j = json_decode_bytes(b)
        return cls(
            payload_hash = PayloadHash(sha512t256_from_b64(j['payloadHash'])),
            transactions_hash = BlockTransactionsHash(sha512t256_from_b64(j['transactionsHash'])),
            outputs_hash = BlockOutputsHash(sha512t256_from_b64(j['outputsHash'])),
        )

# ############################################################################ #
# Block Transactions

@dataclass(frozen=True, eq=True)
class BlockTransactions(ChainwebDbContent[BlockTransactionsHash]):
    """
    Chainweb Block Transactions

    From the chainweb point of view the transactions and minder data are just
    binary blobs and hashed as such. This class decodes the actual JSON content
    to make it easier to work with the data.  The original byte representation
    is retained, too.
    """

    transactions_hash: BlockTransactionsHash = field(compare = True, hash = True)
    transactions: list[dict] = field(compare = False)
    transactions_bytes: list[TransactionBytes] = field(compare = False)
    miner_data: dict = field(compare = False)
    miner_data_bytes: MinerDataBytes = field(compare = False)

    @property
    def cls(self):
        return BlockTransactions

    @property
    def content_hash(self) -> BlockTransactionsHash:
        return self.transactions_hash

    def encode(self):
        """Custom binary encoding that is used in the chainweb database"""
        b = bytearray()
        b += pack('>32s Q', self.transactions_hash, len(self.transactions_bytes))
        for i in self.transactions_bytes:
            encode_len_prefixed(b, i)
        encode_len_prefixed(b, self.miner_data_bytes)
        return bytes(b)
    
    @classmethod
    def decode(cls, b: bytes):
        """Custom binary encoding that is used in the chainweb database"""
        state = [b, 0]
        h, c = decode(state, '>32s Q')
        txs = [decode_len_prefixed(state)[0] for _ in range(c)]
        md, = decode_len_prefixed(state)
        return cls(
            transactions_hash = h,
            transactions = [json_decode_transaction(i) for i in txs],
            transactions_bytes = txs,
            miner_data = json_decode_bytes(md),
            miner_data_bytes = md,
        )

    def encode_json(self) -> bytes:
        return json.dumps({
            'transactionHash': encode_base64_bytes(self.transactions_hash),
            'transaction': [encode_base64_bytes(i) for i in self.transactions_bytes],
            'minerData': encode_base64_bytes(self.miner_data_bytes),
        }).encode('utf-8')

    @classmethod
    def decode_json(cls, b : bytes):
        """JSON encoding that is used on the REST API and in the legacy database format"""
        j = json_decode_bytes(b)
        th = BlockTransactionsHash(sha512t256_from_b64(j['transactionHash']))
        txs_bytes = [TransactionBytes(decode_base64(i)) for i in j['transaction']]
        md_bytes = MinerDataBytes(decode_base64(j['minerData']))
        return cls(
            transactions_hash = th,
            transactions = [json_decode_bytes(i) for i in txs_bytes],
            transactions_bytes = txs_bytes,
            miner_data = json_decode_bytes(md_bytes),
            miner_data_bytes = md_bytes,
        )

# ############################################################################ #
# Block Outputs

@dataclass(frozen=True, eq=True)
class BlockOutputs(ChainwebDbContent[BlockOutputsHash]):
    """
    Chainweb Block Outputs

    From the chainweb point of view the outputs and coinbase are just binary
    blobs and hashed as such. This class decodes the actual JSON content to
    make it easier to work with the data.  The original byte representation is
    retained, too.
    """

    outputs_hash: BlockOutputsHash = field(compare = True, hash = True)
    outputs: list[dict] = field(compare = False)
    outputs_bytes: list[OutputBytes] = field(compare = False)
    coinbase: dict = field(compare = False)
    coinbase_bytes: CoinbaseBytes = field(compare = False)

    @property
    def cls(self):
        return BlockOutputs

    @property
    def content_hash(self) -> BlockOutputsHash:
        return self.outputs_hash

    def encode(self):
        """Custom binary encoding that is used in the chainweb database"""
        b = bytearray()
        b += pack('>32s Q', self.outputs_hash, len(self.outputs_bytes))
        for i in self.outputs_bytes:
            encode_len_prefixed(b, i)
        encode_len_prefixed(b, self.coinbase_bytes)
        return bytes(b)

    @classmethod
    def decode(cls, b: bytes):
        """Custom binary encoding that is used in the chainweb database"""
        state = [b, 0]
        h, c = decode(state, '>32s Q')
        txs = [decode_len_prefixed(state)[0] for _i in range(c)]
        md, = decode_len_prefixed(state)
        return cls(
            outputs_hash = h,
            outputs = [json_decode_bytes(i) for i in txs],
            outputs_bytes = txs,
            coinbase = json_decode_bytes(md),
            coinbase_bytes = md,
        )

    def encode_json(self) -> bytes:
        return json.dumps({
            'outputsHash': encode_base64_bytes(self.outputs_hash),
            'output': [encode_base64_bytes(i) for i in self.outputs_bytes],
            'coinbase': encode_base64_bytes(self.coinbase_bytes),
        }).encode('utf-8')

    @classmethod
    def decode_json(cls, b : bytes):
        """JSON encoding that is used on the REST API and in the legacy database format"""
        j = json_decode_bytes(b)
        th = BlockOutputsHash(sha512t256_from_b64(j['outputsHash']))
        txs_bytes = [OutputBytes(decode_base64(i)) for i in j['output']]
        md_bytes = CoinbaseBytes(decode_base64(j['coinbase']))
        return cls(
            outputs_hash = th,
            outputs = [json_decode_bytes(i) for i in txs_bytes],
            outputs_bytes = txs_bytes,
            coinbase = json_decode_bytes(md_bytes),
            coinbase_bytes = md_bytes,
        )