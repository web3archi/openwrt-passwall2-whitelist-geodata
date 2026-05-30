#!/usr/bin/env python3
from pathlib import Path
import ipaddress
import sys

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "geoip-lab"))

import geoip_pb2

DAT = REPO / "output" / "geoip.dat"

def main():
    if not DAT.exists():
        raise SystemExit(f"[ERR] missing file: {DAT}")

    data = geoip_pb2.GeoIPList()
    data.ParseFromString(DAT.read_bytes())

    print(f"[OK] entries: {len(data.entry)}")
    for entry in data.entry:
        print(f"TAG {entry.country_code} reverse_lookup={entry.reverse_lookup} cidrs={len(entry.cidr)}")
        for item in entry.cidr[:20]:
            if len(item.ip) == 4:
                addr = ipaddress.IPv4Address(item.ip)
            elif len(item.ip) == 16:
                addr = ipaddress.IPv6Address(item.ip)
            else:
                raise SystemExit(f"[ERR] unexpected IP length: {len(item.ip)}")
            print(f"  - {addr}/{item.prefix}")

if __name__ == "__main__":
    main()
