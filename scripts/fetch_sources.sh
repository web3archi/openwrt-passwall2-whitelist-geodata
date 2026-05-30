#!/bin/sh
set -eu

BASE_URL="https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main"
UPSTREAM_DIR="data/upstream"

mkdir -p "${UPSTREAM_DIR}"

echo "[fetch] downloading cidrwhitelist.txt"
curl -fsSL "${BASE_URL}/cidrwhitelist.txt" -o "${UPSTREAM_DIR}/cidrwhitelist.txt"

echo "[fetch] downloading ipwhitelist.txt"
curl -fsSL "${BASE_URL}/ipwhitelist.txt" -o "${UPSTREAM_DIR}/ipwhitelist.txt"

echo "[fetch] downloading whitelist.txt"
curl -fsSL "${BASE_URL}/whitelist.txt" -o "${UPSTREAM_DIR}/whitelist.txt"

echo "[fetch] done"
wc -l "${UPSTREAM_DIR}/whitelist.txt" \
      "${UPSTREAM_DIR}/ipwhitelist.txt" \
      "${UPSTREAM_DIR}/cidrwhitelist.txt"
