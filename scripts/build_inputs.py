#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NORM = ROOT / "work" / "normalized"
BUILD = ROOT / "work" / "build"

TAG = "ru_whitelist"

def read_nonempty(path: Path):
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def main():
    BUILD.mkdir(parents=True, exist_ok=True)

    domains = sorted(set(read_nonempty(NORM / "domains.txt")))
    ips = sorted(set(read_nonempty(NORM / "ips.txt")))
    cidrs = sorted(set(read_nonempty(NORM / "cidrs.txt")))

    geosite_path = BUILD / f"geosite-{TAG}.txt"
    geoip_path = BUILD / f"geoip-{TAG}.txt"
    manifest_path = BUILD / "manifest.json"

    geosite_path.write_text(
        "\n".join(domains) + ("\n" if domains else ""),
        encoding="utf-8"
    )

    geoip_lines = ips + cidrs
    geoip_path.write_text(
        "\n".join(geoip_lines) + ("\n" if geoip_lines else ""),
        encoding="utf-8"
    )

    manifest = {
        "tag": TAG,
        "sources": {
            "domains": str((NORM / "domains.txt").relative_to(ROOT)),
            "ips": str((NORM / "ips.txt").relative_to(ROOT)),
            "cidrs": str((NORM / "cidrs.txt").relative_to(ROOT)),
        },
        "counts": {
            "domains": len(domains),
            "ips": len(ips),
            "cidrs": len(cidrs),
            "geoip_total_lines": len(geoip_lines),
        },
        "outputs": {
            "geosite_text": str(geosite_path.relative_to(ROOT)),
            "geoip_text": str(geoip_path.relative_to(ROOT)),
        },
    }

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print("[build-inputs] done")
    print(f"[build-inputs] tag: {TAG}")
    print(f"[build-inputs] domains: {len(domains)}")
    print(f"[build-inputs] ips: {len(ips)}")
    print(f"[build-inputs] cidrs: {len(cidrs)}")
    print(f"[build-inputs] geoip total lines: {len(geoip_lines)}")

if __name__ == "__main__":
    main()
