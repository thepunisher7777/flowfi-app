# LEDGER by ARX — Beta 1.1

Local-first personal finance PWA focused on fast expense tracking, configurable financial cycles, planning, debt visibility and useful statistics.

## Current release

Beta 1.1 preserves the existing local data model and storage key `flowfi.public.v27`.

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

### Optional beta analytics
Analytics are opt-in. Ledger routes approved product telemetry to PostHog EU Cloud through `posthog-bridge.js`.

Automatic interaction capture, automatic page views and session recording are disabled. Only the technical events allowed by the in-app consent flow are forwarded.

Financial records remain local to the device unless the user explicitly exports them. See [PRIVACY.md](PRIVACY.md) for the telemetry contract.

## Metrics

The old public counter reader has been retired. `metrics.html` is now a public status page; operational analytics are kept in the private ARX analytics environment.

## Quality checks

Pull requests and pushes to `main` run release smoke checks for PWA identity, storage compatibility, analytics privacy invariants, service-worker assets and icon dimensions.

```bash
python scripts/smoke_check.py
```

## Release files

- `index.html`
- `manifest.webmanifest`
- `sw.js`
- `posthog-bridge.js`
- `metrics.html`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`

See [CHANGELOG.md](CHANGELOG.md) for release history.
