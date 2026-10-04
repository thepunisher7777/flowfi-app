from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "index.html",
    "manifest.webmanifest",
    "sw.js",
    "posthog-bridge.js",
    "README.md",
    "metrics.html",
    "icon-192.png",
    "icon-512.png",
    "apple-touch-icon.png",
]


def fail(msg: str) -> None:
    raise SystemExit(f"[FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        fail(f"{path.name} is not a valid PNG")
    return struct.unpack(">II", data[16:24])


for name in REQUIRED:
    p = ROOT / name
    if not p.exists() or p.stat().st_size == 0:
        fail(f"Missing or empty required file: {name}")
ok("Required release files are present")

manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
expected = {
    "name": "Ledger",
    "short_name": "Ledger",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
}
for key, value in expected.items():
    if manifest.get(key) != value:
        fail(f"manifest {key!r} must be {value!r}; got {manifest.get(key)!r}")
ok("Manifest identity and GitHub Pages scope are stable")

index = (ROOT / "index.html").read_text(encoding="utf-8")
for marker in [
    "<title>Ledger</title>",
    'application-name\" content=\"Ledger',
    'apple-mobile-web-app-title\" content=\"Ledger',
    "const STORAGE_KEY = 'flowfi.public.v27';",
    "ANALYTICS_CONSENT_KEY",
    "navigator.serviceWorker.register('sw.js')",
]:
    if marker not in index:
        fail(f"index.html is missing release invariant: {marker}")
ok("Brand, storage compatibility, consent and service-worker invariants are present")

sw = (ROOT / "sw.js").read_text(encoding="utf-8")
if "ledger-beta-1-1-posthog" not in sw:
    fail("Service worker cache version is not the expected PostHog-enabled cache")
for asset in ["./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png", "./posthog-bridge.js"]:
    if asset not in sw:
        fail(f"Service worker core cache is missing {asset}")
if "posthog-bridge.js" not in sw or "injectPostHogBridge" not in sw:
    fail("Service worker does not inject the PostHog bridge")
ok("Service worker cache and analytics bridge injection are present")

bridge = (ROOT / "posthog-bridge.js").read_text(encoding="utf-8")
for marker in [
    "https://eu.i.posthog.com",
    "autocapture: false",
    "capture_pageview: false",
    "capture_pageleave: false",
    "disable_session_recording: true",
    "person_profiles: 'never'",
    "opt_out_capturing_by_default: true",
    "ledger.analytics.consent.v1",
]:
    if marker not in bridge:
        fail(f"PostHog bridge is missing privacy invariant: {marker}")
for forbidden in ["state.transactions", "state.liabilities", "flowfi.public.v27"]:
    if forbidden in bridge:
        fail(f"PostHog bridge must not access finance state: {forbidden}")
ok("PostHog bridge privacy invariants are present")

sizes = {
    "icon-192.png": (192, 192),
    "icon-512.png": (512, 512),
    "apple-touch-icon.png": (180, 180),
}
for name, expected_size in sizes.items():
    actual = png_size(ROOT / name)
    if actual != expected_size:
        fail(f"{name} must be {expected_size[0]}x{expected_size[1]}, got {actual[0]}x{actual[1]}")
ok("PWA icon dimensions are correct")

metrics = (ROOT / "metrics.html").read_text(encoding="utf-8")
for forbidden in ["localStorage.getItem('flowfi.public.v27')", "state.transactions", "state.liabilities", "counterapi.com"]:
    if forbidden in metrics:
        fail(f"metrics.html must not access finance state or the retired counter backend: {forbidden}")
ok("Public metrics status page is separated from local finance state")

print("\nLedger smoke checks passed.")
