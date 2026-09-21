#!/usr/bin/env python3
from pathlib import Path
import sys

BLOCKLIST_DIR = Path("./blocklists")

def get_target_file(domain: str) -> Path:
    first = domain[0].lower()
    if first.isalpha():
        return BLOCKLIST_DIR / f"{first}.txt"
    if first.isdigit():
        return BLOCKLIST_DIR / "0-9.txt"
    return BLOCKLIST_DIR / "other.txt"

def add_domains(domains: list[str]):
    if not BLOCKLIST_DIR.exists():
        print(f"Error: {BLOCKLIST_DIR} does not exists")
        sys.exit(1)

    for domain in domains:
        domain = domain.strip().lower()
        if not domain or "." not in domain:
            print(f"Invalid: {domain}")
            continue

        target = get_target_file(domain)

        existing = set()
        if target.exists():
            with target.open("r", encoding="utf-8") as f:
                existing = {line.strip().lower() for line in f if line.strip()}

        if domain in existing:
            print(f"Duplicated: {domain}")
            continue

        with target.open("a", encoding="utf-8") as f:
            f.write(domain + "\n")
        print(f"Added -> {target.name}: {domain}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 add_domain.py domain1.com domain2.com ...")
        sys.exit(1)

    add_domains(sys.argv[1:])
