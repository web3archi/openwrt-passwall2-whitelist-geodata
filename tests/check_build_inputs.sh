#!/bin/sh
set -eu

BUILD_DIR="work/build"

echo "== build files =="
ls -lh "${BUILD_DIR}"

echo
echo "== manifest =="
cat "${BUILD_DIR}/manifest.json"

echo
echo "== sample geosite =="
head -n 20 "${BUILD_DIR}/geosite-ru_whitelist.txt" || true

echo
echo "== sample geoip =="
head -n 20 "${BUILD_DIR}/geoip-ru_whitelist.txt" || true

echo
echo "== counts =="
wc -l \
  "${BUILD_DIR}/geosite-ru_whitelist.txt" \
  "${BUILD_DIR}/geoip-ru_whitelist.txt"

echo
echo "== sanity checks =="
grep -n '://' "${BUILD_DIR}/geosite-ru_whitelist.txt" && echo "BAD: URL found in geosite input" && exit 1 || true
grep -n '[A-Z]' "${BUILD_DIR}/geosite-ru_whitelist.txt" && echo "BAD: uppercase domain found" && exit 1 || true

echo "build-input sanity checks passed"
