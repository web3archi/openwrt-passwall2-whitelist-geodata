#!/usr/bin/env python3
"""
Собирает output/geoip.dat с тегом RU-WHITELIST
из data/generated/cidrs.txt (после normalize_sources.py).

Формат: GeoIPList / GeoIP / CIDR
(совместим с v2fly/xray geoip.dat).
"""
from pathlib import Path
import ipaddress
import sys

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "geoip-lab"))

import geoip_pb2  # из geoip-lab

SRC = REPO / "data" / "generated" / "cidrs.txt"
OUT = REPO / "output" / "geoip.dat"
TAG = "RU-WHITELIST"

def parse_lines(path: Path):
    cidrs = []
    seen = set()

    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
        except ValueError as e:
            raise SystemExit(f"[ERR] {path}:{n}: bad CIDR '{line}': {e}")
        key = str(net)
        if key in seen:
            continue
        seen.add(key)
        cidrs.append(net)
    return cidrs

def main():
    if not SRC.exists():
        raise SystemExit(f"[ERR] missing source file: {SRC}")

    nets = parse_lines(SRC)

    entry = geoip_pb2.GeoIP()
    entry.country_code = TAG
    entry.reverse_lookup = False

    for net in nets:
        item = entry.cidr.add()
        item.ip = net.network_address.packed
        item.prefix = net.prefixlen

    geo_list = geoip_pb2.GeoIPList()
    geo_list.entry.append(entry)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(geo_list.SerializeToString())

    print(f"[OK] built: {OUT}")
    print(f"[OK] tag: {TAG}")
    print(f"[OK] cidr_count: {len(nets)}")

if __name__ == "__main__":
    main()
