# openwrt-passwall2-whitelist-geodata

**Language:** [Русский](README.md) | English

Repository for converting whitelist data from [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist) into `geosite.dat` and `geoip.dat` files suitable for **PassWall2 on OpenWrt**.

The main use case is **PassWall2 + Xray** on low-resource routers where **whitelisted resources should go direct and everything else should go through proxy/VPN**.

## Why this project exists

This project is built specifically for **routers with limited memory and storage**, where large universal geodata sets are often unnecessary and inefficient.

Its architecture is intentionally focused on producing **small, targeted whitelist datasets** that solve a practical routing task and fit better into constrained OpenWrt systems.

## What this repository does

This repository:

- fetches whitelist source data from [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist);
- uses these upstream text files:
  - [`whitelist.txt`](https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/whitelist.txt)
  - [`ipwhitelist.txt`](https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/ipwhitelist.txt)
  - [`cidrwhitelist.txt`](https://github.com/hxehex/russia-mobile-internet-whitelist/blob/main/cidrwhitelist.txt)
- normalizes domains, IPs, and CIDRs;
- builds:
  - `geosite.dat`
  - `geoip.dat`
- publishes release assets for OpenWrt / PassWall2 use.

## Tested platform

This repository was developed and tested in the following environment:

- **Router:** Asus RT-AX53U / RT-AX1800U
- **SoC / target:** MediaTek MT7621, `ramips/mt7621`
- **Architecture:** `mipsel_24kc`
- **OpenWrt:** 23.05.5
- **PassWall2:** `luci-app-passwall2`
- **Backend:** Xray using `geosite.dat` and `geoip.dat` from `/usr/share/v2ray/`

Other routers and OpenWrt versions may work too, but should be treated as unverified unless tested separately.

## Repository layout

```text
openwrt-passwall2-whitelist-geodata/
├── README.md
├── README.en.md
├── LICENSE
├── .github/
├── data/
├── proto_src/
├── proto_out/
├── scripts/
└── tests/
```

## Data pipeline

1. `scripts/fetch_sources.sh` fetches upstream text lists from GitHub.
2. `scripts/normalize_sources.py` normalizes domains and converts individual IPs into host CIDRs.
3. `scripts/build_geosite_dat.py` builds `geosite.dat`.
4. `scripts/build_geoip_dat.py` builds `geoip.dat`.
5. GitHub Actions publishes release artifacts.

Both generated outputs use the `RU-WHITELIST` tag.

## Why `2ip.io` is included

The project intentionally adds `2ip.io` to the generated domain whitelist even if that domain is not present in upstream data.

It is used as a **smoke-test domain** for quick validation of routing behavior in OpenWrt + PassWall2 deployments. It is easy to remember, easy to test manually, and useful for checking whether whitelist traffic is actually going through the intended `direct` path.

At the same time, `2ip.ru` and `ifconfig.me` are intentionally **not** force-added by this project.

## Using with OpenWrt / PassWall2

In the reference setup, geodata are configured via the built-in update mechanism in PassWall2:

1. Open **PassWall2 → Rule Manage**.
2. In the GeoIP/Geosite update section, locate the **bottom Custom fields**:
   - **GeoIP Update URL (Custom)**
   - **Geosite Update URL (Custom)**
3. Set custom URLs pointing to this repository’s release in those Custom fields, for example:

   ```text
   GeoIP Update URL (Custom):   https://github.com/web3archi/openwrt-passwall2-whitelist-geodata/releases/download/geodata-latest/geoip.dat
   Geosite Update URL (Custom): https://github.com/web3archi/openwrt-passwall2-whitelist-geodata/releases/download/geodata-latest/geosite.dat
   ```
4. Press Enter in each field to confirm the value, then click **Save & Apply**.

After that, PassWall2 will download and update `geoip.dat` / `geosite.dat` from this repository using its own geodata update mechanism. No additional shell scripts on the router side are required in the basic scenario.

A typical routing idea when using these geodata:

- `geosite:RU-WHITELIST` → `direct`
- `geoip:RU-WHITELIST` → `direct`
- everything else → selected proxy/VPN profile

The exact rule order and implementation depend on the local PassWall2 configuration.
## License and software freedom

This project is intended to be **free and open-source software**.

- Scripts, workflow files, and glue code may be used, modified, and redistributed under the repository license.
- Upstream whitelist text data remains attributable to [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist).

## Note

This project is not affiliated with OpenWrt, PassWall2, Xray, or the upstream whitelist repository.
