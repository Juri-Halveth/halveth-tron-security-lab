# HALVETH · XOF-1296 research experiment

An **opt-in, read-only integrity label** for a single file. The companion tool, `halveth_xof1296.py`, computes:

- Ordinary SHA-256, for cross-checking and compatibility.
- A **1296-bit SHAKE256 digest** (162 bytes, 324 hex characters), with the domain `HALVETH\0CONTENT-XOF1296\0v1\0`.

The number 1296 was inspired by an audiovisual frequency visualization at 1296 Hz.
**Hz measures cycles per second; bits measure information length.**
A tone or video animation does not modify Windows, Git, TRON or nearby devices.
SHAKE256 supports nominal security strength **up to 256 bits**, not 1296 bits.

## Run

From repository root, with Python 3.8+:

```bash
python halveth/tools/halveth_xof1296.py ./halveth/README.md
python -m unittest discover -s halveth/tools -p 'test_halveth_xof1296.py' -v
```

For offline comparison, store the JSON stdout securely and later use
`python halveth/tools/halveth_xof1296.py PATH --expected 324_HEX_CHARS`
to compare against a previously trusted reference.

This does **not** replace Git object IDs, Windows Authenticode, TRON block hashing/consensus or digital signatures.
It never modifies files, does not search your disk automatically and does not contact external computers.
Do not publish fingerprints/filenames of confidential files without considering metadata sensitivity.

A future HALVETH/RACHEL content-addressed index could assign extra labels to events
and files using explicit canonical serialization, signatures and versioned algorithms
while preserving existing protocol identifiers.

References:
- [NIST FIPS 202 (SHAKE256)](https://csrc.nist.gov/pubs/fips/202/final)
- [Git hash transition](https://git-scm.com/docs/hash-function-transition)
- [Microsoft Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash)
