# LEDGER by ARX — Beta 1.2

Local-first personal finance PWA focused on fast expense tracking, configurable financial cycles, planning, debt visibility and useful statistics.

## Current release

**Beta 1.2** hardens the ARX analytics layer without changing Ledger's finance data model. Existing installs remain compatible through the preserved storage key `flowfi.public.v27`.

### Core
- transactions, transfers and categories
- configurable financial cycle
- accounts and balance reconciliation
- budgets and recurring movements
- financial calendar
- goals, debts and loan repayment tracking
- statistics and Excel / CSV / JSON export
- Monefy / generic CSV import
- PWA installation and offline cache
- local backup / recovery safeguards

## Runtime architecture

Ledger now uses a small bootstrap boundary:

- `index.html` — public bootstrap and release boundary
- `ledger-core.html` — existing Ledger application core, preserved byte-for-byte for data safety
- `posthog-bridge.js` — PostHog EU transport bridge
- `arx-analytics-guard.js` — consent synchronization and privacy hardening
- `sw.js` — offline cache and network-first release shell

The bootstrap upgrades the legacy telemetry endpoint to an internal virtual ARX endpoint before the application core executes. CounterAPI is no longer an external analytics backend. The compatibility transport remains internal only so Beta 1.2 can avoid a risky rewrite of the finance core during the analytics migration.

## Optional beta analytics

Analytics remain **opt-in**. Approved product telemetry is routed to PostHog EU Cloud.

Project and client protections include:
- anonymized IPs
- no autocapture
- no automatic page views
- no session recording
- no heatmaps
- no console capture
- no performance capture
- no user identification by name or email
- explicit event-property allowlisting once the SDK is active
- immediate opt-out synchronization when analytics are disabled

Financial records remain local to the device unless the user explicitly exports them. See [PRIVACY.md](PRIVACY.md).

## Metrics

`metrics.html` is only a public status page. Operational analytics are kept in the private **ARX Product Analytics** environment.

## Quality checks

Pull requests and pushes to `main` run release smoke checks for:
- PWA identity and GitHub Pages scope
- bootstrap/core integrity
- preservation of `flowfi.public.v27`
- ARX analytics privacy invariants
- service-worker release assets
- PWA icon dimensions
- separation between public metrics status and local finance state

```bash
python scripts/smoke_check.py
```

## Release files

- `index.html`
- `ledger-core.html`
- `manifest.webmanifest`
- `sw.js`
- `posthog-bridge.js`
- `arx-analytics-guard.js`
- `metrics.html`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`

See [CHANGELOG.md](CHANGELOG.md) for release history.
