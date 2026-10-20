#!/usr/bin/env python3
"""HALVETH additive file-integrity research tool (SHA-256 + SHAKE256/1024).

Does not change files, Windows security policy, Git object IDs, or TRON consensus.
An unsigned manifest detects unintentional differences only when the expected
manifest itself is kept trustworthy.
"""
import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import sys

SCHEMA = "halveth.integrity.v1"
DOMAIN = b"HALVETH\x00SHAKE256\x00FILE\x001024\x00v1\x00"
EXCLUDE_DIRS = {".git", ".gradle", ".idea", ".venv", "venv", "node_modules",
                "build", "dist", "database", "output-directory", "logs", "__pycache__"}
EXCLUDE_FILES = {".env", ".env.local", "id_rsa", "id_ed25519", "credentials.json",
                 "localwitnesskeystore.json"}
EXCLUDE_SUFFIXES = (".pem", ".p12", ".pfx", ".key", ".keystore")


def excluded_file(name):
    lower = name.lower()
    return lower in EXCLUDE_FILES or lower.endswith(EXCLUDE_SUFFIXES)


def source_files(root):
    """Enumerate explicit root without following symlinks or common secret dirs."""
    root = Path(root).expanduser()
    if root.is_symlink() or not root.exists():
        raise ValueError("Root must exist and must not be a symlink")
    if root.is_file():
        if excluded_file(root.name):
            raise ValueError("Explicit root points to a secret/key-like file")
        yield root.name, root
        return
    if not root.is_dir():
        raise ValueError("Root must be a regular file or directory")
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs
                         if d not in EXCLUDE_DIRS and not (Path(parent) / d).is_symlink())
        for name in sorted(files):
            p = Path(parent) / name
            if excluded_file(name) or p.is_symlink() or not p.is_file():
                continue
            yield p.relative_to(root).as_posix(), p


def digests(path):
    standard = hashlib.sha256()
    extended = hashlib.shake_256()
    extended.update(DOMAIN)
    size = 0
    with open(path, "rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            standard.update(chunk)
            extended.update(chunk)
            size += len(chunk)
    return {"bytes": size, "sha256": standard.hexdigest(),
            "shake256_1024": extended.hexdigest(128)}


def snapshot(root):
    records = []
    for rel, p in source_files(root):
        item = {"path": rel}
        item.update(digests(p))
        records.append(item)
    records.sort(key=lambda item: item["path"])
    return {
        "schema": SCHEMA,
        "algorithms": {"sha256_bits": 256,
                       "shake256_output_bits": 1024,
                       "shake256_max_claimed_security_bits": 256,
                       "shake256_domain_hex": DOMAIN.hex()},
        "notes": "Unsigned, read-only research manifest; not a digital signature or protocol migration.",
        "files": records,
    }


def verify(root, expected):
    if expected.get("schema") != SCHEMA or expected.get("algorithms", {}).get("shake256_domain_hex") != DOMAIN.hex():
        raise ValueError("Unsupported manifest schema or hash domain")
    old = {item["path"]: item for item in expected.get("files", [])}
    new = {item["path"]: item for item in snapshot(root)["files"]}
    if len(old) != len(expected.get("files", [])):
        raise ValueError("Duplicate manifest file paths")
    missing = sorted(old.keys() - new.keys())
    extra = sorted(new.keys() - old.keys())
    changed = sorted(path for path in old.keys() & new.keys()
                     if old[path].get("bytes") != new[path]["bytes"]
                     or not hmac.compare_digest(str(old[path].get("sha256", "")), new[path]["sha256"])
                     or not hmac.compare_digest(str(old[path].get("shake256_1024", "")), new[path]["shake256_1024"]))
    return {"ok": not (missing or extra or changed), "missing": missing,
            "extra": extra, "changed": changed, "checked": len(new)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot", help="Create additive manifest without changing source files")
    snap.add_argument("root")
    snap.add_argument("--out", help="Output JSON file OUTSIDE root; default stdout")
    check = commands.add_parser("verify", help="Compare source tree with saved manifest")
    check.add_argument("root")
    check.add_argument("manifest")
    args = parser.parse_args(argv)
    try:
        if args.command == "snapshot":
            root = Path(args.root).expanduser().resolve()
            if args.out:
                dest = Path(args.out).expanduser().resolve()
                if root.is_dir() and (root == dest or root in dest.parents):
                    raise ValueError("Manifest destination must be outside the scanned directory")
                payload = json.dumps(snapshot(args.root), indent=2, ensure_ascii=False) + "\n"
                with open(dest, "x", encoding="utf-8") as stream:
                    stream.write(payload)
                print("CREATED:", dest)
            else:
                print(json.dumps(snapshot(args.root), indent=2, ensure_ascii=False))
            return 0
        with open(args.manifest, "r", encoding="utf-8") as stream:
            expected = json.load(stream)
        result = verify(args.root, expected)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("HALVETH_ERROR:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
