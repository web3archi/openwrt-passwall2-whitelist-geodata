#!/usr/bin/env python3
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "geosite-lab"))

import common_pb2

DAT = REPO / "output" / "geosite.dat"

def main():
    if not DAT.exists():
        raise SystemExit(f"[ERR] missing file: {DAT}")

    data = common_pb2.GeoSiteList()
    data.ParseFromString(DAT.read_bytes())

    print(f"[OK] entries: {len(data.entry)}")
    found_2ip = False

    for entry in data.entry:
        print(f"TAG {entry.country_code} domains={len(entry.domain)}")
        for item in entry.domain[:20]:
            print(f"  - type={item.type} value={item.value}")
            if item.value == "2ip.io":
                found_2ip = True

    if not found_2ip:
        for entry in data.entry:
            for item in entry.domain:
                if item.value == "2ip.io":
                    found_2ip = True
                    break

    if found_2ip:
        print("[OK] smoke-test domain present in dat: 2ip.io")
    else:
        raise SystemExit("[ERR] smoke-test domain not found in dat: 2ip.io")

if __name__ == "__main__":
    main()
