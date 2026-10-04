# Changelog

All notable Ledger changes should be documented here from Beta 1.1 onward.

## Beta 1.1 — 2026-10-05

### Added
- Optional anonymous beta analytics with explicit consent.
- PWA manifest metadata and install improvements.
- Repository smoke checks and GitHub Actions CI.
- Privacy/telemetry documentation.
- Privacy-first PostHog EU analytics bridge for product telemetry.

### Changed
- Retired the public CounterAPI metrics reader.
- Product telemetry now routes through PostHog while preserving the existing in-app consent flow.
- Service worker now injects and caches the analytics bridge without changing the finance data model.

### Preserved
- Existing local data key `flowfi.public.v27` to prevent data loss during the FlowFi → Ledger rebrand.
- No financial values or free-form finance data are included in analytics events.

## Earlier builds

Earlier releases were developed under FlowFi / Ledger V31.x naming. Their existing user data remains compatible with the current Ledger build.
