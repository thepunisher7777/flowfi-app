# LEDGER by ARX — Beta 1.1

Local-first personal finance PWA focused on fast expense tracking, financial cycles, planning, debt visibility and useful statistics without turning personal finance into accounting software.

## Current release

**Beta 1.1** adds optional anonymous analytics for early testers while preserving the existing local data model and storage key `flowfi.public.v27`.

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

### Beta analytics
Analytics are **opt-in**. With consent, Ledger can count sessions, active users, installations, app version, broad platform, screens, feature usage and sanitized technical errors.

Ledger does **not** send transactions, amounts, categories, notes, account names, balances, budgets, loans/debts or imported/exported finance files.

See [PRIVACY.md](PRIVACY.md) for the telemetry contract.

## Beta metrics

The current provisional beta panel is available at:

https://thepunisher7777.github.io/flowfi-app/metrics.html

The counter-based analytics backend is intended only for early testing. Before broad public distribution it should be replaced by **ARX Metrics / PostHog**.

## Quality checks

Every pull request and push to `main` runs lightweight release smoke checks that verify:

- required release files
- Ledger PWA identity and GitHub Pages scope
- preservation of `flowfi.public.v27`
- service-worker core assets
- PWA icon dimensions
- separation between metrics and local financial state

Run locally with:

```bash
python scripts/smoke_check.py
```

## Release files

- `index.html`
- `manifest.webmanifest`
- `sw.js`
- `metrics.html`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`

See [CHANGELOG.md](CHANGELOG.md) for release history.
