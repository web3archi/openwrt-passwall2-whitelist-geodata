#!/usr/bin/env python3
"""
Собирает output/geosite.dat с тегом RU-WHITELIST
из data/generated/domains.txt (после normalize_sources.py).

Формат: GeoSiteList / GeoSite / Domain
(совместим с v2fly/xray geosite.dat).
"""
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "geosite-lab"))

import common_pb2  # из geosite-lab

SRC = REPO / "data" / "generated" / "domains.txt"
OUT = REPO / "output" / "geosite.dat"
TAG = "RU-WHITELIST"

def normalize_domain(line: str) -> str:
    return line.strip().lower().rstrip(".")

def main():
    if not SRC.exists():
        raise SystemExit(f"[ERR] missing source file: {SRC}")

    domains = []
    seen = set()
    for n, raw in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        domain = normalize_domain(line)
        if not domain:
            continue
        if domain in seen:
            continue
        seen.add(domain)
        domains.append(domain)

    site = common_pb2.GeoSite()
    site.country_code = TAG

    for domain in domains:
        item = site.domain.add()
        # Тип домена: Plain (как и раньше)
        item.type = common_pb2.Domain.Plain
        item.value = domain

    site_list = common_pb2.GeoSiteList()
    site_list.entry.append(site)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(site_list.SerializeToString())

    print(f"[OK] built: {OUT}")
    print(f"[OK] tag: {TAG}")
    print(f"[OK] domain_count: {len(domains)}")
    if "2ip.io" in domains:
        print("[OK] smoke-test domain present: 2ip.io")
    else:
        raise SystemExit("[ERR] smoke-test domain missing: 2ip.io")

if __name__ == "__main__":
    main()
