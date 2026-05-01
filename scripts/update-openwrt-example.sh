#!/bin/sh
set -eu

BASE_URL="https://github.com/web3archi/openwrt-passwall2-whitelist-geodata/releases/latest/download"

wget -O /usr/share/v2ray/geoip.dat "${BASE_URL}/geoip.dat"
wget -O /usr/share/v2ray/geosite.dat "${BASE_URL}/geosite.dat"

service passwall2 restart
