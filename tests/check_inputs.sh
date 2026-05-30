#!/bin/sh
set -eu

RAW_DIR="work/raw"
NORM_DIR="work/normalized"

echo "== raw files =="
ls -lh "${RAW_DIR}"

echo
echo "== normalized files =="
ls -lh "${NORM_DIR}"

echo
echo "== sample domains =="
head -n 20 "${NORM_DIR}/domains.txt" || true

echo
echo "== sample ips =="
head -n 20 "${NORM_DIR}/ips.txt" || true

echo
echo "== sample cidrs =="
head -n 20 "${NORM_DIR}/cidrs.txt" || true

echo
echo "== counts =="
wc -l "${NORM_DIR}/domains.txt" "${NORM_DIR}/ips.txt" "${NORM_DIR}/cidrs.txt"

echo
echo "== basic sanity checks =="
grep -n '://' "${NORM_DIR}/domains.txt" && echo "BAD: URL found in domains" && exit 1 || true
grep -n '/' "${NORM_DIR}/ips.txt" && echo "BAD: CIDR found in ips.txt" && exit 1 || true
grep -n '[A-Z]' "${NORM_DIR}/domains.txt" && echo "BAD: uppercase domain found" && exit 1 || true

echo "sanity checks passed"
