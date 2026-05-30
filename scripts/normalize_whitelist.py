#!/usr/bin/env python3
from __future__ import annotations

import ipaddress
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "work" / "raw"
OUT = ROOT / "work" / "normalized"

DOMAIN_RE = re.compile(r"^[a-z0-9.-]+$")

def read_lines(path: Path):
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()

def strip_comment(line: str) -> str:
    line = line.strip()
    if not line or line.startswith("#"):
        return ""
    if "#" in line:
        line = line.split("#", 1)[0].strip()
    return line.strip()

def normalize_domain(line: str) -> str | None:
    line = strip_comment(line).lower().rstrip(".")
    if not line:
        return None

    if "://" in line:
        return None
    if "/" in line:
        return None
    if " " in line or "\t" in line:
        return None
    if line.startswith("*."):
        line = line[2:]
    if line.startswith("."):
        line = line[1:]

    if not DOMAIN_RE.match(line):
        return None
    if "." not in line:
        return None
    if ".." in line:
        return None

    return line

def normalize_ip(line: str) -> str | None:
    line = strip_comment(line)
    if not line:
        return None
    try:
        ip = ipaddress.ip_address(line)
        return str(ip)
    except ValueError:
        return None

def normalize_cidr(line: str) -> str | None:
    line = strip_comment(line)
    if not line:
        return None
    try:
        net = ipaddress.ip_network(line, strict=False)
        return str(net)
    except ValueError:
        return None

def write_sorted(path: Path, items):
    path.write_text(
        "\n".join(sorted(items)) + ("\n" if items else ""),
        encoding="utf-8"
    )

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    raw_domains = read_lines(RAW / "whitelist.txt")
    raw_ips = read_lines(RAW / "ipwhitelist.txt")
    raw_cidrs = read_lines(RAW / "cidrwhitelist.txt")

    domains = {d for line in raw_domains if (d := normalize_domain(line))}
    ips = {i for line in raw_ips if (i := normalize_ip(line))}
    cidrs = {c for line in raw_cidrs if (c := normalize_cidr(line))}

    write_sorted(OUT / "domains.txt", domains)
    write_sorted(OUT / "ips.txt", ips)
    write_sorted(OUT / "cidrs.txt", cidrs)

    print("[normalize] done")
    print(f"[normalize] domains: {len(domains)}")
    print(f"[normalize] ips: {len(ips)}")
    print(f"[normalize] cidrs: {len(cidrs)}")

if __name__ == "__main__":
    main()
