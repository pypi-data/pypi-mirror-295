# Python Tools for [Chainweb](https://github.com/kadena-io/chainweb-node)

[Chainweb](https://www.kadena.io/chainweb) is the consensus protocol that is
used by the [Kadena blockchain](https://kadena.io). It is a highly scalable
version of Nakamoto consensus that is used by Bitcoin. Chainweb supports
parallel mining and sharded payload processing.

This package represents a growing selection of tools for working with data
structures from Chainweb.

New features are added on demand. If you miss something please file an
issue or submit a PR.

# Block Header Type

Python representation of Chainweb block headers.

# Block Payload Types

These types reflect the Chainweb view onto block payloads. The type captures
the structure that is represented in the on-chain Merkle tree. Semantics aspects
of the Pact smart contract language are mostly ignored as they are not relevant
for the consensus protocol.

For convenience, some Pact related JSON formatted content is parsed and
represented as `dict`.