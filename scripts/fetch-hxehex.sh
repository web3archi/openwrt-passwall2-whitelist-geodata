#!/bin/sh
set -eu

BASE_URL="https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main"

mkdir -p domains ip

echo "[fetch] downloading whitelist.txt"
curl -fsSL "${BASE_URL}/whitelist.txt" -o domains/whitelist-hxehex.txt

echo "[fetch] downloading ipwhitelist.txt"
curl -fsSL "${BASE_URL}/ipwhitelist.txt" -o ip/whitelist-ip.txt

echo "[fetch] downloading cidrwhitelist.txt"
curl -fsSL "${BASE_URL}/cidrwhitelist.txt" -o ip/whitelist-cidr.txt

echo "[fetch] done"
wc -l domains/whitelist-hxehex.txt ip/whitelist-ip.txt ip/whitelist-cidr.txt
