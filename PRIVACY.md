# Privacy — LEDGER by ARX

Ledger is local-first. Financial data is stored in the user's browser/device unless the user explicitly exports it.

## Financial data

Ledger does **not** send the following to analytics:

- transactions or transaction amounts
- categories or notes
- account names or balances
- budgets
- loans, debts or repayment amounts
- imported/exported finance files

The current local storage key remains `flowfi.public.v27` for compatibility with existing installs.

## Optional beta analytics

Beta analytics are opt-in. A user must explicitly allow anonymous analytics before events are sent, and can disable them later from Settings.

Allowed telemetry is limited to technical/product events such as:

- app/session opens
- active-user counters
- app version
- broad platform class
- screen names
- feature-use counters
- PWA installation events
- sanitized technical error counters

No analytics event should include free-form user text or financial values.

## Current analytics status

Beta 1.1 uses a lightweight counter-based analytics layer for early testing. This is considered provisional infrastructure and should be replaced by ARX Metrics / PostHog before broad public distribution.

## Backups and exports

Backups, CSV exports and Excel exports are created on-device and only leave the device when the user chooses where to save/share them.

## Security reports

Do not publish sensitive user data in a public issue. For a security problem, provide a minimal reproduction without real financial information.
