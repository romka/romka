#!/usr/bin/env bash

set -euo pipefail

HUGO_VERSION="${HUGO_VERSION:-0.163.3}"
HUGO_ARCHIVE="hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
HUGO_CHECKSUMS="hugo_${HUGO_VERSION}_checksums.txt"
BUILD_TEMP_DIR="$(mktemp -d)"
TOOLS_DIR="${HOME}/.local/render-tools"

cleanup() {
    rm -rf "$BUILD_TEMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TOOLS_DIR/hugo" "${PWD}/.cache/hugo"

echo "Installing Hugo Extended ${HUGO_VERSION}..."
curl -fsSLo "$BUILD_TEMP_DIR/$HUGO_ARCHIVE" "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/${HUGO_ARCHIVE}"
curl -fsSLo "$BUILD_TEMP_DIR/$HUGO_CHECKSUMS" "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/${HUGO_CHECKSUMS}"

(
    cd "$BUILD_TEMP_DIR"
    grep "  ${HUGO_ARCHIVE}$" "$HUGO_CHECKSUMS" > selected.sha256
    sha256sum -c selected.sha256
)

tar -C "$TOOLS_DIR/hugo" -xzf "$BUILD_TEMP_DIR/$HUGO_ARCHIVE" hugo
export PATH="$TOOLS_DIR/hugo:$PATH"
export HUGO_CACHEDIR="${PWD}/.cache/hugo"

echo "Using $(hugo version)"
echo "Building Render static site..."
hugo --gc --minify --environment=render
