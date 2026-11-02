# PBFT Quorum Lab

An offline, dependency-free visual model of equal-sized Byzantine quorum sets.
Open `pbft-quorum-lab.html` in a browser. The calculator and visualization run
locally and make no network requests.

## What the model computes

For `n` fixed members, at most `f` Byzantine members, and quorum size `q`:

- the smallest possible overlap between two size-`q` sets is `max(0, 2q - n)`;
- a guaranteed correct member in that overlap requires the overlap to exceed
  `f`;
- a quorum can still be collected when up to `f` members are unavailable if
  `q <= n - f`.

The displayed safe-and-live interval is therefore
`ceil((n + f + 1) / 2) <= q <= n - f`. The familiar `n = 3f + 1`,
`q = 2f + 1` case is included as a preset. The visualization constructs one
pair of sets attaining the minimum overlap; it does not enumerate every pair.

## Model boundary

This is quorum arithmetic, not a full PBFT implementation or proof. It assumes
fixed membership, equal-size quorums, and a global upper bound of `f` Byzantine
members. It does not model signatures, views, message ordering, clocks,
network synchrony, implementation code, key control, or recovery.

The MIT-LCS-TR-817 source describes a particular BFT replicated-service
algorithm and its quorum assumptions. TRON's official documentation describes
DPoS block production and block solidification using active Super
Representatives' produced block heights. Those are distinct mechanisms; the
lab does not treat its quorum slider as a TRON network setting or infer a
production finding from the existence of PBFT-named message types in source.

## Local checks

Run the model tests with Node.js:

```powershell
node --test halveth/experiments/quorum-model.test.js
```

## Sources

- Castro, Miguel. *Practical Byzantine Fault Tolerance*, MIT-LCS-TR-817,
  January 2001: <https://dspace.mit.edu/entities/publication/0b00af4c-cc94-40a4-ac98-96f0d78216d1>
- TRON Developers, *Consensus and DPoS*:
  <https://developers.tron.network/docs/concensus>
- TRON java-tron protocol source, `Tron.proto`:
  <https://github.com/tronprotocol/java-tron/blob/develop/protocol/src/main/protos/core/Tron.proto>
