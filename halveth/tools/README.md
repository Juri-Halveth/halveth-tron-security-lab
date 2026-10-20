# HALVETH · XOF-1024 Integrity Lab

**Status:** opt-in, read-only, standard-library Python research tool. Does not alter Git, Windows, or TRON protocol hashes.

## Why 1024 bits?

SHAKE256 is an extendable-output function (XOF) standardized by **NIST FIPS 202**. With `digest(128)` it emits **128 bytes = 1024 bits = 256 hexadecimal characters**. Its nominal security strength is **up to 256 bits**, **not** 1024 bits. A longer digest is not equivalent to 1024-bit preimage/collision security.

Domain separation uses the literal byte prefix encoded in `DOMAIN` within the Python tool. Retaining SHA-256 alongside this extended digest preserves compatibility and enables independent cross-checking.

A manifest is **not a digital signature**: maintain a trusted copy, or sign it separately, to detect malicious replacement of the manifest itself.

## Windows / Git Bash / Linux / macOS

Python 3.8+ (no external dependencies):

```bash
python halveth/tools/halveth_hash1024.py snapshot path/to/your/project --out path/outside/project/manifest.json
python halveth/tools/halveth_hash1024.py verify path/to/your/project path/outside/project/manifest.json
python -m unittest discover -s halveth/tools -p 'test_halveth_hash1024.py' -v
```

The default output is **stdout** if `--out` is omitted. An existing output file is never overwritten. Common build repositories (`.git`, `build`, `database`, `node_modules`) and common key filenames are excluded. Choose a narrowly scoped directory containing files you intend to fingerprint; read-only hashing still opens those files.

The current implementation does not hash symlinks or follow symlinked directories. It is not a hardened adversarial filesystem monitor; concurrent mutations between hashing and verification are possible. Avoid putting sensitive names, file hashes, or confidential audit metadata into a public manifest.

## Boundaries

- **No** modifications to Windows system files, Authenticode signatures, Git commit IDs or remote history.
- **No** replacement of TRON block IDs or consensus cryptography. Nodes would become incompatible without a separately specified and adopted protocol upgrade.
- A frequency such as 432 Hz or 1024 Hz is not a cryptographic hash width.
- Future RACHEL OS integration is a design direction, not evidence of a running standalone operating system.

Research: [NIST FIPS 202](https://csrc.nist.gov/pubs/fips/202/final) · [Git hash transition](https://git-scm.com/docs/hash-function-transition) · [PowerShell Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash).
