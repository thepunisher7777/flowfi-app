# Changelog

All notable Ledger changes are documented here from Beta 1.1 onward.

## Beta 1.2 — 2026-10-05

### Changed
- Added a lightweight bootstrap boundary so analytics loads before the finance core executes.
- Preserved the existing Ledger application core as `ledger-core.html` to minimize data-model risk during the infrastructure migration.
- Upgraded runtime telemetry to an internal ARX virtual endpoint before the core executes.
- Added `arx-analytics-guard.js` for consent synchronization and stricter PostHog property filtering.
- Simplified the service worker and moved to the `ledger-beta-1-2-arx-analytics` cache.
- Updated the visible beta label and telemetry provider copy to Beta 1.2 / PostHog EU at runtime.

### PostHog
- Renamed the analytics project to **ARX Product Analytics**.
- Set reporting timezone to `Europe/Madrid`.
- Kept IP anonymization enabled.
- Disabled project-level autocapture, session recording, heatmaps, console capture and performance capture.

### Preserved
- Existing local data key `flowfi.public.v27`.
- Existing transactions, accounts, balances, loans, budgets, imports, exports and backups.
- Explicit opt-in analytics consent.

## Beta 1.1 — 2026-10-05

### Added
- Optional anonymous beta analytics with explicit consent.
- PWA manifest metadata and install improvements.
- Repository smoke checks and GitHub Actions CI.
- Privacy/telemetry documentation.
- Privacy-first PostHog EU analytics bridge for product telemetry.

### Changed
- Retired the public CounterAPI metrics reader.
- Product telemetry routes through PostHog while preserving the existing in-app consent flow.

### Preserved
- Existing local data key `flowfi.public.v27` to prevent data loss during the FlowFi → Ledger rebrand.
- No financial values or free-form finance data are included in analytics events.

## Earlier builds

Earlier releases were developed under FlowFi / Ledger V31.x naming. Their existing user data remains compatible with the current Ledger build.
