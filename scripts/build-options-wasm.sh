#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd -P)"
manifest="$root/rust/market-compass-core/Cargo.toml"
cargo test --manifest-path "$manifest"
cargo build --release --target wasm32-unknown-unknown --manifest-path "$manifest"
cp "$root/rust/market-compass-core/target/wasm32-unknown-unknown/release/market_compass_core.wasm" "$root/src/market_compass/web/options_engine.wasm"
chmod 644 "$root/src/market_compass/web/options_engine.wasm"
shasum -a 256 "$root/src/market_compass/web/options_engine.wasm"
