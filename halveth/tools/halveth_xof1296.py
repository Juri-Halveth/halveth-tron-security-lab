#!/usr/bin/env python3
"""HALVETH opt-in 1296-bit file fingerprint. Reads, never alters source files.

Not a Windows signature, Git object ID, blockchain hash, or digital signature.
The output length is 1296 bits; SHAKE256 security is not 1296 bits.
"""
import argparse
import hashlib
import hmac
import json
from pathlib import Path
import sys

DOMAIN = b"HALVETH\x00CONTENT-XOF1296\x00v1\x00"
OUTPUT_BYTES = 162


def fingerprint(file_path):
    path = Path(file_path).expanduser()
    if path.is_symlink() or not path.is_file():
        raise ValueError("Provide an existing regular file, not a symlink")
    sha256 = hashlib.sha256()
    xof = hashlib.shake_256()
    xof.update(DOMAIN)
    length = 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            length += len(block)
            sha256.update(block)
            xof.update(block)
    return {"schema": "halveth.content-identity-1296.v1",
            "size_bytes": length,
            "sha256": sha256.hexdigest(),
            "shake256_1296": xof.hexdigest(OUTPUT_BYTES),
            "shake256_output_bits": OUTPUT_BYTES * 8,
            "shake256_domain_hex": DOMAIN.hex(),
            "security_note": "SHAKE256 supports up to 256-bit security, not 1296-bit security. Unsigned fingerprint requires a trusted reference."}


def cli(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="One explicitly selected file to fingerprint")
    parser.add_argument("--expected", help="Optional previously trusted 1296-bit hex fingerprint")
    ns = parser.parse_args(args)
    try:
        result = fingerprint(ns.file)
        if ns.expected is not None:
            candidate = ns.expected.lower().strip()
            result["matches_expected"] = (
                len(candidate) == 2 * OUTPUT_BYTES and
                hmac.compare_digest(candidate, result["shake256_1296"]))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if result.get("matches_expected") is False else 0
    except (OSError, ValueError) as e:
        print("HALVETH_ERROR:", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
