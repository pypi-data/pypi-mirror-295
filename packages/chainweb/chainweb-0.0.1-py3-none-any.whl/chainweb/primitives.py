from abc import abstractmethod
from typing import Generic, NewType, Literal, Protocol, TypeVar
from enum import Enum

from chainweb.utils import decode_base64, encode_base64_bytes

# ############################################################################ #
# Base Types

Hash = NewType("Hash", bytes)
Sha512t256 = NewType("Sha512t256", Hash)
PosixTime = NewType('PosixTime', int) # UInt64, POSIX timestamp with microsecond precision

# ############################################################################ #
# Exceptions

class ChainwebException(Exception):
    """Base class for all chainweb exceptions."""

# ############################################################################ #
# Chainweb Types

class ChainwebVersion(Enum):
    """Enumeration of the different chainweb versions."""
    DEVELOPMENT = 1
    MAINNET01 = 5
    TESTNET04 = 7

ChainId = NewType('ChainId', int) # UInt32
BlockHash = NewType('BlockHash', Sha512t256) # SHA512/256
PayloadHash = NewType('PayloadHash', Sha512t256) # SHA512/256
BlockHeight = NewType('BlockHeight', int) # Unit64
BlockTime = NewType('BlockTime', PosixTime) # UInt64, POSIX timestamp with microsecond precision
Target = NewType('Target', bytes) # 32 bytes
Weight = NewType('Weight', bytes) # 32 bytes
Nonce = NewType('Nonce', bytes) # 8 bytes

# ############################################################################ #
# Encoding of Hashes

def hash_from_b64(b : str) -> Hash:
    """Decode a base64 urlsafe (without padding) encoded string to a hash."""
    return Hash(decode_base64(b))

def sha512t256_from_b64(b : str) -> Sha512t256:
    """Decode a base64 urlsafe (without padding) encoded string to a sha512t256 hash."""
    return Sha512t256(hash_from_b64(b))

def hash_to_b64(h : Hash) -> bytes:
    """Encode a hash to a base64 urlsafe (without padding) encoded string."""
    return encode_base64_bytes(h)

def sha512t256_to_b64(h : Sha512t256) -> bytes:
    """Encode a sha512t256 hash to a base64 urlsafe (without padding) encoded string."""
    return encode_base64_bytes(h)

def read_hash(h : Hash | bytes | bytearray | str) -> Hash:
    """Decode a hash from a hash, bytes, bytearray, or str."""
    if isinstance(h, bytes) and len(h) == 32:
        return Hash(h)
    if isinstance(h, bytearray) and len(h) == 32:
        return Sha512t256(Hash(h))
    # base64 encoded str
    if isinstance(h, str) and len(h) == 43:
        return hash_from_b64(h)
    # hex encoded str
    if isinstance(h, str) and len(h) == 64:
        return Sha512t256(Hash(bytes.fromhex(h)))
    raise ChainwebException(f"unsupported format of hash {h}. Supported formats are 32 bytes, 44 base64 characters, and 64 hex characters.")

def read_sha512t256(h : Sha512t256 | Hash | bytes | bytearray | str) -> Sha512t256:
    """Decode a sha512t256 hash from a sha512t256, hash, bytes, bytearray, or str."""
    return Sha512t256(read_hash(h))

# ############################################################################ #
# Encoding of BlockHeight

# The default block height encoding is little endian (like everywhere in chainweb).
# An exception of this rule is the key of HeightIndex tables where big-endian is
# used to preserve the order of headers by height in the db.
#
# Unfortunately, the implementation of payload tables is buggy and uses
# little-endian encoding for the height in the key.
#

def decode_block_height(b: bytes, byteorder: Literal["little"] | Literal["big"] = "little") -> BlockHeight:
    """Decode a block height from a byte string."""
    return BlockHeight(int.from_bytes(b, byteorder=byteorder, signed=False))

def encode_block_height(b: BlockHeight, byteorder: Literal["little"] | Literal["big"] = "little") -> bytes:
    """Encode a block height to a byte string."""
    return b.to_bytes(length=8, byteorder=byteorder, signed=False)

# ############################################################################ #
# Encoding Protocol For Chainweb Data

H_co = TypeVar("H_co", bound=Sha512t256, covariant=True)

class ChainwebDbContent(Protocol, Generic[H_co]):
    """Base class for all chainweb database content."""

    @property
    @abstractmethod
    def cls(self) -> type["ChainwebDbContent"]:
        """Return the class of the content."""
        raise NotImplementedError

    @property
    @abstractmethod
    def content_hash(self) -> H_co:
        """Compute the hash of the content."""
        raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytes:
        """Encode the content to a byte string."""
        raise NotImplementedError

    @classmethod
    def decode(cls, b: bytes | bytearray) -> "ChainwebDbContent":
        """Decode the content from a byte string."""
        raise NotImplementedError

    @abstractmethod
    def encode_json(self) -> bytes:
        """Encode the content to a JSON encoded byte string."""
        raise NotImplementedError

    @classmethod
    def decode_json(cls, b: bytes | bytearray) -> "ChainwebDbContent":
        """Decode the content from a JSON encoded byte string."""
        raise NotImplementedError
