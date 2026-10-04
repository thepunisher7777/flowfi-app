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

The local storage key remains `flowfi.public.v27` for compatibility with existing installs.

## Optional beta analytics

Beta analytics are **opt-in**. A user must explicitly allow anonymous analytics before Ledger forwards product telemetry, and can disable it later from Settings.

Allowed telemetry is limited to technical/product events such as:

- app/session opens
- active-user activity
- app version
- broad platform class
- screen names
- feature-use counters
- PWA installation events
- sanitized technical error counters

No analytics event should include free-form user text or financial values.

## Analytics provider and controls

Approved telemetry is routed to **PostHog EU Cloud** through the ARX analytics layer.

The PostHog project is configured with privacy-first defaults:
- IP anonymization enabled
- autocapture disabled
- automatic page views disabled by the client
- session recording disabled
- heatmaps disabled
- console capture disabled
- performance capture disabled

The client also disables automatic interaction capture, page-leave capture, exception capture, session recording and person profiles for this telemetry layer. The ARX analytics guard synchronizes opt-out state and applies an allowlist to Ledger event properties when the SDK is active.

Ledger does not intentionally identify testers by name or email through analytics.

## Compatibility transport

Beta 1.2 preserves the existing finance core byte-for-byte and upgrades its legacy analytics calls at the bootstrap boundary before the core executes. The old counter URL shape is used only as an internal compatibility transport between local scripts; CounterAPI is not used as the external analytics backend.

## Backups and exports

Backups, CSV exports and Excel exports are created on-device and only leave the device when the user chooses where to save/share them.

## Security reports

Do not publish sensitive user data in a public issue. For a security problem, provide a minimal reproduction without real financial information.
