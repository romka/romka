#!/usr/bin/env bash

set -euo pipefail

HUGO_VERSION="${HUGO_VERSION:-0.163.3}"
HUGO_ARCHIVE="hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
HUGO_CHECKSUMS="hugo_${HUGO_VERSION}_checksums.txt"
BUILD_TEMP_DIR="$(mktemp -d)"
TOOLS_DIR="$BUILD_TEMP_DIR/tools"
IS_RENDER_BUILD=false

if [[ -n "${RENDER_GIT_COMMIT:-}" || "${RENDER_SERVICE_TYPE:-}" == "static" ]]; then
    IS_RENDER_BUILD=true
fi

if [[ "$IS_RENDER_BUILD" == "true" ]]; then
    HUGO_DESTINATION="${HUGO_DESTINATION:-public}"
    export HUGO_CACHEDIR="${HUGO_CACHEDIR:-${PWD}/.cache/hugo}"
    export HUGO_RESOURCEDIR="${HUGO_RESOURCEDIR:-${PWD}/resources}"
else
    HUGO_DESTINATION="${HUGO_DESTINATION:-public}"
    export HUGO_CACHEDIR="${HUGO_CACHEDIR:-${PWD}/.cache/hugo}"
fi

cleanup() {
    rm -rf "$BUILD_TEMP_DIR"
}
trap cleanup EXIT

safe_rm() {
    local path=$1

    if [[ -n "$path" && "$path" != "/" ]]; then
        rm -rf "$path"
    fi
}

print_disk_usage() {
    echo "Disk usage snapshot:"
    df -h . /tmp 2>/dev/null || true
    du -sh .git content public resources .cache "$HUGO_CACHEDIR" "${HUGO_RESOURCEDIR:-}" "$HUGO_DESTINATION" 2>/dev/null || true
}

mkdir -p "$TOOLS_DIR/hugo" "$HUGO_CACHEDIR"
if [[ -n "${HUGO_RESOURCEDIR:-}" ]]; then
    mkdir -p "$HUGO_RESOURCEDIR"
fi

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

echo "Using $(hugo version)"
print_disk_usage

if [[ "$IS_RENDER_BUILD" == "true" ]]; then
    echo "Removing Git metadata from Render build workspace to reduce peak disk usage..."
    safe_rm .git
    safe_rm public
    safe_rm resources
    safe_rm .cache
    safe_rm "$HUGO_DESTINATION"
    safe_rm "$HUGO_CACHEDIR"
    safe_rm "${HUGO_RESOURCEDIR:-}"
    mkdir -p "$HUGO_CACHEDIR"
    if [[ -n "${HUGO_RESOURCEDIR:-}" ]]; then
        mkdir -p "$HUGO_RESOURCEDIR"
    fi
    print_disk_usage
fi

echo "Building Render static site..."
hugo --gc --minify --environment=render --destination "$HUGO_DESTINATION"

if [[ "$IS_RENDER_BUILD" == "true" ]]; then
    echo "Removing build-only files from Render workspace..."
    if [[ "$HUGO_DESTINATION" != "public" ]]; then
        safe_rm public
        mv "$HUGO_DESTINATION" public
    fi
    safe_rm "$HUGO_CACHEDIR"
    safe_rm "${HUGO_RESOURCEDIR:-}"
    safe_rm content
    safe_rm .venv
    print_disk_usage
fi
