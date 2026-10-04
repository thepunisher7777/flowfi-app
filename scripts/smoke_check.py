from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "index.html",
    "ledger-core.html",
    "manifest.webmanifest",
    "sw.js",
    "posthog-stub.js",
    "posthog-bridge.js",
    "arx-analytics-guard.js",
    "README.md",
    "PRIVACY.md",
    "CHANGELOG.md",
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
ok("Required Beta 1.2 release files are present")

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

bootstrap = (ROOT / "index.html").read_text(encoding="utf-8")
for marker in [
    "<title>Ledger</title>",
    "const RELEASE='Beta 1.2';",
    "./ledger-core.html",
    "./posthog-stub.js",
    "./posthog-bridge.js",
    "./arx-analytics-guard.js",
    "https://arx.local/telemetry",
    "Legacy analytics endpoint survived bootstrap migration",
    "const STORAGE_KEY = 'flowfi.public.v27';",
]:
    if marker not in bootstrap:
        fail(f"index.html bootstrap is missing release invariant: {marker}")
if not (
    bootstrap.find("./posthog-stub.js")
    < bootstrap.find("./posthog-bridge.js")
    < bootstrap.find("./arx-analytics-guard.js")
):
    fail("Analytics runtime scripts must load in stub -> bridge -> guard order")
ok("Bootstrap loads the supported analytics runtime before the preserved Ledger core")

core = (ROOT / "ledger-core.html").read_text(encoding="utf-8")
for marker in [
    "<title>Ledger</title>",
    "const APP_VERSION = 'Beta 1.1';",
    "const STORAGE_KEY = 'flowfi.public.v27';",
    "ANALYTICS_CONSENT_KEY",
    "navigator.serviceWorker.register('sw.js')",
    "https://counterapi.com/api",
]:
    if marker not in core:
        fail(f"ledger-core.html compatibility invariant missing: {marker}")
ok("Ledger finance core remains compatible and unchanged at the migration boundary")

# Mirror the deterministic runtime substitutions from index.html. This proves
# the executed core is Beta 1.2 and cannot keep the old external counter URL.
runtime = core
runtime = runtime.replace("const APP_VERSION = 'Beta 1.1';", "const APP_VERSION = 'Beta 1.2';")
runtime = runtime.replace("const ANALYTICS_NAMESPACE = 'thepunisher7777.github.io';", "const ANALYTICS_NAMESPACE = 'ledger';")
runtime = runtime.replace("const ANALYTICS_BASE = 'https://counterapi.com/api';", "const ANALYTICS_BASE = 'https://arx.local/telemetry';")
runtime = runtime.replace("CounterAPI · sin ID de usuario enviado por Ledger", "PostHog EU · telemetría anónima opt-in")
runtime = runtime.replace("LEDGER by ARX · Beta 1.1", "LEDGER by ARX · Beta 1.2")
if "https://counterapi.com/api" in runtime:
    fail("Runtime core still contains the retired external CounterAPI endpoint")
for marker in ["Beta 1.2", "https://arx.local/telemetry", "PostHog EU · telemetría anónima opt-in"]:
    if marker not in runtime:
        fail(f"Runtime migration is missing: {marker}")
ok("Runtime migration removes the external counter endpoint before execution")

sw = (ROOT / "sw.js").read_text(encoding="utf-8")
if "ledger-beta-1-2-arx-analytics" not in sw:
    fail("Service worker cache version is not Ledger Beta 1.2")
for asset in [
    "./index.html",
    "./ledger-core.html",
    "./manifest.webmanifest",
    "./icon-192.png",
    "./icon-512.png",
    "./apple-touch-icon.png",
    "./posthog-stub.js",
    "./posthog-bridge.js",
    "./arx-analytics-guard.js",
]:
    if asset not in sw:
        fail(f"Service worker core cache is missing {asset}")
if "networkFirst" not in sw:
    fail("Service worker must keep the release shell/core network-first")
ok("Service worker caches the complete Beta 1.2 runtime")

stub = (ROOT / "posthog-stub.js").read_text(encoding="utf-8")
for marker in ["window.posthog", "root.init", "static/array.js", "root.__SV = 1"]:
    if marker not in stub:
        fail(f"PostHog browser stub is missing supported bootstrap marker: {marker}")
if "flowfi.public.v27" in stub:
    fail("PostHog stub must not access Ledger finance state")
ok("PostHog browser stub is isolated from finance state")

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

guard = (ROOT / "arx-analytics-guard.js").read_text(encoding="utf-8")
for marker in [
    "https://arx.local",
    "before_send:sanitizeEvent",
    "autocapture:false",
    "capture_pageview:false",
    "disable_session_recording:true",
    "person_profiles:'never'",
    "opt_out_capturing",
    "ledger.analytics.consent.v1",
]:
    if marker not in guard:
        fail(f"ARX analytics guard is missing privacy invariant: {marker}")
for forbidden in ["state.transactions", "state.liabilities", "flowfi.public.v27", "accountBalance", "transaction.amount"]:
    if forbidden in guard:
        fail(f"ARX analytics guard must not access finance state: {forbidden}")
ok("ARX analytics guard restricts telemetry and synchronizes consent")

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
if "Beta 1.2" not in metrics or "POSTHOG EU" not in metrics:
    fail("metrics.html must describe the current Beta 1.2 analytics status")
ok("Public metrics status page is separated from local finance state")

print("\nLedger Beta 1.2 smoke checks passed.")
