#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
xray = root / "xray"
xray.mkdir(exist_ok=True)

message = """\
build-geodata.py is currently a scaffold.

Expected inputs:
- domains/whitelist-hxehex.txt
- domains/custom.txt
- ip/whitelist-ip.txt
- ip/whitelist-cidr.txt
- ip/custom-cidr.txt

Expected outputs:
- xray/geosite.dat
- xray/geoip.dat

The actual geodata compilation step must be implemented and validated
before this repository is used in production.
"""

print(message)

# Create placeholders so repository structure is complete.
(xray / "geosite.dat").write_text(
    "placeholder: geosite.dat is not built yet\\n",
    encoding="utf-8"
)
(xray / "geoip.dat").write_text(
    "placeholder: geoip.dat is not built yet\\n",
    encoding="utf-8"
)

print("Created placeholder files in xray/.")
sys.exit(0)
