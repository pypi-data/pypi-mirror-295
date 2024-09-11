from abc import abstractmethod
from dataclasses import dataclass, field
from collections.abc import Iterator
from typing import Generic, Literal, Type, TypeVar, cast

from rocksdbpy import RocksDB, open_default

from chainweb.primitives import ChainwebDbContent, BlockHeight, ChainId, ChainwebException
from chainweb.primitives import decode_block_height, encode_block_height
from chainweb.primitives import BlockHash, Sha512t256, PayloadHash
from chainweb.payload import BlockOutputs, BlockPayload, BlockTransactions
from chainweb.payload import BlockTransactionsHash, BlockOutputsHash
from chainweb.header import Header

# ############################################################################ #
# Exception Types
# ############################################################################ #

class ChainwebDbException(ChainwebException):
    """Chainweb database exception"""

# ############################################################################ #
# Synthetic Payload Types
# ############################################################################ #

@dataclass(frozen=True, eq=True)
class BlockPayloadData:
    """Block PayloadData"""
    payload_hash: PayloadHash = field(compare = True, hash = True)
    transactions_hash: BlockTransactionsHash = field(compare = False)
    outputs_hash: BlockOutputsHash = field(compare = False)
    transactions: list[dict] = field(compare = False)
    miner_data: dict = field(compare = False)

    @classmethod
    def create(cls, block_payload: BlockPayload, block_transactions: BlockTransactions):
        if block_payload.transactions_hash != block_transactions.transactions_hash:
            raise ChainwebDbException(f"BlockTransactions do not match the BlockPayload. Expected {block_payload.transactions_hash}, but got {block_transactions.transactions_hash}.")
        return cls(
            payload_hash = block_payload.payload_hash,
            transactions_hash = block_payload.transactions_hash,
            outputs_hash = block_payload.outputs_hash,
            transactions = block_transactions.transactions,
            miner_data = block_transactions.miner_data
        )

@dataclass(frozen=True, eq=True)
class BlockPayloadDataWithOutputs:
    """Block PayloadData With Outputs"""
    payload_hash: PayloadHash = field(compare = True, hash = True)
    transactions_hash: BlockTransactionsHash = field(compare = False)
    outputs_hash: BlockOutputsHash = field(compare = False)
    transactions: list[tuple[dict,dict]] = field(compare = False)
    miner_data: dict = field(compare = False)
    coinbase: dict = field(compare = False)

    @classmethod
    def create(cls, block_payload: BlockPayload, block_transactions: BlockTransactions, block_outputs: BlockOutputs):
        if block_payload.transactions_hash != block_transactions.transactions_hash:
            raise ChainwebDbException(f"BlockTransactions do not match the BlockPayload. Expected {block_payload.transactions_hash}, but got {block_transactions.transactions_hash}.")
        if block_payload.outputs_hash != block_outputs.outputs_hash:
            raise ChainwebDbException(f"BlockOutputs do not match the BlockPayload. Expected {block_payload.outputs_hash}, but got {block_outputs.outputs_hash}.")
        return cls(
            payload_hash = block_payload.payload_hash,
            transactions_hash = block_payload.transactions_hash,
            outputs_hash = block_payload.outputs_hash,
            transactions = list(zip(block_transactions.transactions, block_outputs.outputs)),
            miner_data = block_transactions.miner_data,
            coinbase = block_outputs.coinbase
        )

@dataclass(frozen=True, eq=True)
class Block:
    """Block"""
    hash: BlockHash = field(compare = True, hash = True)
    height: BlockHeight = field(compare = False)
    header: Header = field(compare = False)
    payload: BlockPayloadDataWithOutputs = field(compare = False)

    @classmethod
    def create(cls, header: Header, payload: BlockPayloadDataWithOutputs):
        if header.payload_hash != payload.payload_hash:
            raise ChainwebDbException(f"Payload hash in header does not match the payload hash. Expected {header.payload_hash}, but got {payload.payload_hash}.")
        return cls(
            hash = header.hash,
            height = header.height,
            header = header,
            payload = payload
        )

# ############################################################################ #
# Chainweb Db Tables
# ############################################################################ #

class ChainwebDbTable:
    """Chainweb Chain Database Table"""

    def __init__(self, db : RocksDB, name : bytes):
        self.db = db
        self.__name = name

    @property
    def name(self) -> bytes:
        return self.__name

    @property
    def startKey(self) -> bytes:
        return b'-' + self.name + b'$'

    @property 
    def endKey(self) -> bytes:
        return b'-' + self.name + b'%'

    def __iter__(self) -> Iterator[tuple[bytes, bytes]]:
        it = self.db.iterator(mode='from', key=self.startKey)
        try:
            for k, v in it: # type: ignore
                # if it.valid() and k < self.endKey:
                if k < self.endKey:
                    yield k[len(self.startKey):], v
                else:
                    break
        finally:
            it.close() # type: ignore

    def get(self, k : bytes) -> bytes | None:
        return self.db.get(self.startKey + k)

# There are two types of tables in the chainweb database:
#
# 1. Data tables that are indexes by block height and content hashes and
# 2. tables that map content hashes to block heights.
#
# All content hashes are SHA512/256 hashes. Block heights are 64-bit unsigned.
#
# Values use a custom binary encoding. Only legacy payload tables contain JSON
# objects.

H = TypeVar("H", bound=Sha512t256) # , covariant=True)

# def cast_to_hash[H:Hash](h: bytes) -> H:
def cast_to_hash(h: bytes) -> H:
    return cast(H, h)

# def cast_from_hash[H:Hash](h: H) -> bytes:
def cast_from_hash(h: H) -> bytes:
    return cast(bytes, h)

# class HeightIndex[H:Sha512t256](ChainwebDbTable):
class HeightIndex(ChainwebDbTable, Generic[H]):
    def __iter__(self) -> Iterator[tuple[H, BlockHeight]]:
        for k, v in super().__iter__():
            yield cast_to_hash(k), decode_block_height(v, byteorder="little")
    def get(self, k: H) -> BlockHeight | None:
        v = super().get(cast_from_hash(k))
        return v if v is None else decode_block_height(v, byteorder='little')

KeyByteOrder = Literal["little"] | Literal["big"]

# Work around unsupported Higher Order Types for Generics
ChainwebDbContentH = ChainwebDbContent[H]
T = TypeVar("T", bound=ChainwebDbContentH)

# class ChainwebDbContentTable[T: ChainwebDbContentH](ChainwebDbTable):
class ChainwebDbContentTable(ChainwebDbTable, Generic[T]):
    @property
    @abstractmethod
    def content_cls(self) -> Type[T]:
        """The class of the content."""
        raise NotImplementedError

    @property
    def key_byte_order(self) -> KeyByteOrder:
        return "big"

    def __iter__(self) -> Iterator[tuple[BlockHeight, T]]:
        for h, v in super().__iter__():
            height = h[:8] # first 8 key bytes are the height
            yield decode_block_height(height, byteorder=self.key_byte_order), self.content_cls.decode(v)

    def get(self, h: BlockHeight, k: H) -> T | None:
        # In the key (and only in the key) big endian byteorder is used
        v = super().get(encode_block_height(h, byteorder=self.key_byte_order) + cast_from_hash(k))
        return v if v is None else self.content_cls.decode(v)

# Legacy tables are index by content hash and contain JSON objects.
# Values contain JSON objects with base64 encoded binary values
#
class ChainwebDbJsonTable(ChainwebDbTable, Generic[T]):
    @property
    @abstractmethod
    def content_cls(self) -> Type[T]:
        """The class of the content."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        for _k, v in super().__iter__():
            yield self.content_cls.decode_json(v)

    def get(self, k: H) -> T | None:
        v = super().get(cast_from_hash(k))
        return v if v is None else self.content_cls.decode_json(v)

# ############################################################################ #
# BlockHeader Tables

class BlockHeightTable(HeightIndex[BlockHash]):
    """Chainweb chain database height index for headers"""
    def __init__(self, db :RocksDB, chain : ChainId):
        super().__init__(db, f'BlockHeader/{chain}/rank'.encode())

class BlockHeaderTable(ChainwebDbContentTable[Header]):
    """Chainweb Chain Database BlockHeader Table"""
    @property
    def content_cls(self) -> Type[Header]:
        return Header
    def __init__(self, db : RocksDB, chain : ChainId):
        super().__init__(db, f'BlockHeader/{chain}/header'.encode())

# ############################################################################ #
# Payload Tables

# TODO should be add an artificial chain index?
# or maybe provide a second set of tables that filters for the chain?

class BlockPayloadHeightTable(HeightIndex[BlockHash]):
    """Chainweb chain database height index for payloads"""
    def __init__(self, db :RocksDB):
        super().__init__(db, b'BlockPayloadIndex')

class BlockPayloadTable(ChainwebDbContentTable[BlockPayload]):
    """Chainweb Chain Database BlockPayload Table"""
    @property
    def content_cls(self) -> Type[BlockPayload]:
        return BlockPayload
    @property
    def key_byte_order(self) -> KeyByteOrder:
        return "little"
    def __init__(self, db: RocksDB):
        super().__init__(db, b'BlockPayload2')

class BlockTransactionsTable(ChainwebDbContentTable[BlockTransactions]):
    """Chainweb Chain Database BlockTransactions Table"""
    @property
    def content_cls(self) -> Type[BlockTransactions]:
        return BlockTransactions
    @property
    def key_byte_order(self) -> KeyByteOrder:
        return "little"
    def __init__(self, db: RocksDB):
        super().__init__(db, b'BlockTransactions2')

class BlockOutputsTable(ChainwebDbContentTable[BlockOutputs]):
    """Chainweb Chain Database BlockOutputs Table"""
    @property
    def content_cls(self) -> Type[BlockOutputs]:
        return BlockOutputs
    @property
    def key_byte_order(self) -> KeyByteOrder:
        return "little"
    def __init__(self, db: RocksDB):
        super().__init__(db, b'BlockOutputs2')

# Legacy JSON tables

class BlockPayloadTableLegacy(ChainwebDbJsonTable[BlockPayload]):
    """Chainweb Chain Database BlockPayload Table"""
    @property
    def content_cls(self) -> Type[BlockPayload]:
        return BlockPayload
    def __init__(self, db: RocksDB):
        super().__init__(db, b'BlockPayload')

class BlockTransactionsTableLegacy(ChainwebDbJsonTable[BlockTransactions]):
    """Chainweb Chain Database BlockTransactions Table"""
    @property
    def content_cls(self) -> Type[BlockTransactions]:
        return BlockTransactions
    def __init__(self, db: RocksDB):
        super().__init__(db, b'BlockTransactions')

class BlockOutputsTableLegacy(ChainwebDbJsonTable[BlockOutputs]):
    """Chainweb Chain Database BlockOutputs Table"""
    @property
    def content_cls(self) -> Type[BlockOutputs]:
        return BlockOutputs
    def __init__(self, db: RocksDB):
        super().__init__(db, b'BlockOutputs')

# ############################################################################ #
# Views
#

class BlockHeaderHashTable:
    """BlockHeader view that is indexed only by BlockHash"""
    def __init__(self, db, chain : ChainId):
        self.db = db
        self.chain = chain

    def _getBlockHeader(self, height : BlockHeight, hash: BlockHash) -> Header:
        return self.db.headers[self.chain].get(height, hash)

    def get(self, k : BlockHash) -> Header | None:
        v = self.db.headerHeights[self.chain].get(k)
        return v if v is None else self._getBlockHeader(v, k)

    # This iterates over block headers sorted by block hash. This is slow and
    # should barely be needed # If there's a need for it, it could be done more
    # efficient.
    #
    def __iter__(self) -> Iterator[Header]:
        for k, v in self.db.headerHeights[self.chain]:
            yield self._getBlockHeader(k, v)

class BlockPayloadDataTable:
    """Chainweb Chain Database BlockPayloadData"""

    def __init__(self, db):
        self.db = db

    def _getPayloadData(self, height: BlockHeight, payload : BlockPayload) -> BlockPayloadData:
        txs = self.db.transactions.get(height, payload.transactions_hash)
        return BlockPayloadData.create(payload,txs)

    def get(self, h: BlockHeight, k : PayloadHash) -> BlockPayloadData | None:
        # TODO fall back to old tables if needed
        v = self.db.payloads.get(h, k)
        return v if v is None else self._getPayloadData(h, v)

    def __iter__(self) -> Iterator[tuple[BlockHeight, BlockPayloadData]]:
        # This can be implemented more efficiently when we can assume that
        # payload iterators are ordered by height.
        for h, v in self.db.payloads:
            yield h, self._getPayloadData(h, v)

class BlockPayloadDataWithOutputsTable:
    """Chainweb Chain Database BlockPayloadData With Outputs Table"""

    def __init__(self, db):
        self.db = db

    def _getPayloadWithOutputs(self, height: BlockHeight, payload: BlockPayload) -> BlockPayloadDataWithOutputs:
        txs = self.db.transactions.get(height, payload.transactions_hash)
        outputs = self.db.outputs.get(height, payload.outputs_hash)
        return BlockPayloadDataWithOutputs.create(payload, txs, outputs)

    def get(self, h: BlockHeight, k : PayloadHash) -> BlockPayloadDataWithOutputs | None:
        # TODO fall back to old tables if needed
        v = self.db.payloads.get(h,k)
        return v if v is None else self._getPayloadWithOutputs(h, v)

    def __iter__(self) -> Iterator[tuple[BlockHeight, BlockPayloadDataWithOutputs]]:
        # This can be implemented more efficiently when we can assume that
        # payload iterators are ordered by height.
        for h, v in self.db.payloads:
            yield h, self._getPayloadWithOutputs(h, v)

class BlocksTable:
    """Chainweb Chain Database Blocks Table"""

    def __init__(self, cwdb, chain: ChainId):
        self.db = cwdb
        self.chain = chain

    def _getPayloadWithOutputs(self, height: BlockHeight, payload: BlockPayload) -> BlockPayloadDataWithOutputs:
        txs = self.db.transactions.get(height, payload.transactions_hash)
        outputs = self.db.outputs.get(height, payload.outputs_hash)
        return BlockPayloadDataWithOutputs.create(payload, txs, outputs)

    def get(self, h: BlockHeight, k: BlockHash) -> Block | None:
        # TODO fall back to old tables if needed
        hdr = self.db.headers[self.chain].get(h, k)
        v = self.db.payloads.get(h,hdr.payload_hash)
        if v is None:
            return None
        p = self._getPayloadWithOutputs(h, v)
        return Block.create(hdr, p)

    def __iter__(self) -> Iterator[tuple[BlockHeight, Block]]:
        # This can be implemented more efficiently when we can assume that
        # payload iterators are ordered by height.
        for h, v in self.db.headers[self.chain]:
            hdr = self.db.headers[self.chain].get(h, k)
            p =  self._getPayloadWithOutputs(h, v)
            yield h, Block.create(hdr, p)

# ############################################################################ #
# Chainweb Db
# ############################################################################ #

class ChainwebDb:
    """Chainweb Chain Database"""

    # Constants
    CHAIN_IDS : range = range(ChainId(0),ChainId(19))

    # Internal Methods

    def __init__(self, path : str):
        self.db = open_default(path)
        try:
            self.headers = {}
            self.header_heights = {}
            self.headers_by_hash = {}
            self.blocks = {}
            for i in self.CHAIN_IDS:
                self.headers[i] = BlockHeaderTable(self.db, ChainId(i))
                self.header_heights[i] = BlockHeightTable(self.db, ChainId(i))
                self.headers_by_hash[i] = BlockHeaderHashTable(self, ChainId(i))
                self.blocks[i] = BlocksTable(self, ChainId(i))

            self.payload_heights = BlockPayloadHeightTable(self.db)
            self.payloads = BlockPayloadTable(self.db)
            self.transactions = BlockTransactionsTable(self.db)
            self.outputs = BlockOutputsTable(self.db)
            self.payload_data = BlockPayloadDataTable(self)
            self.payload_data_with_outputs = BlockPayloadDataWithOutputsTable(self)

            # Legacy
            self.legacy_tables = lambda: None
            self.legacy_tables.payloads = BlockPayloadTableLegacy(self.db)
            self.legacy_tables.transactions = BlockTransactionsTableLegacy(self.db)
            self.legacy_tables.outputs = BlockOutputsTableLegacy(self.db)

        except:
            self.close()
            raise

    def __del__(self):
        self.close()

    def close(self):
        self.db.close()

class ProvideChainwebDb:
    """Resource manager for Chainweb Chain Database"""
    def __init__(self, path : str):
        self.path = path
        self.chainweb_db = None
    def __enter__(self):
        self.chainweb_db = ChainwebDb(self.path)
        return self.chainweb_db
    def __exit__(self, *args):
        if self.chainweb_db is not None:
            self.chainweb_db.close()

