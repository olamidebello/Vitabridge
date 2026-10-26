# VitaBridge

Medical transport platform development preview for https://vitabridge.olamidemedical.health.

## Included
Responsive patient, dispatcher, crew, hospital and administrator workspaces; demo booking; optional GPS attachment; BLS/ALS eligible vehicle recommendation; manual assignment; trip state transitions; synthetic care-record capture; fleet readiness/fuel editing; hospital receiving status; consultation-provider URL; session audit view; installable web manifest and offline application shell. Logo, app icon and generated brand artwork are included.

## Run
Serve `dist/` with any static web server, for example `python3 -m http.server 8080 --directory dist`. Use HTTPS for geolocation and service workers. No package installation is required.

## Scope and safety
This is a functional **browser demonstration**, not a production emergency dispatch system. Data resides in browser memory and resets on reload. Role switching is not authorization. Do not enter real patient information. No SMS, emergency dispatch, live vehicle tracking, traffic ETA, AI model, insurance processing, telemedicine media transport, authentication, backend database, or clinical integration is connected. Vehicle matching is a deterministic capability/availability and straight-line-distance heuristic, not AI or medical triage. The illustrative map does not show real vehicles. Navigation links open standard Google Maps, not emergency routing. Hospital status is manually reported and requires verification.

Offline caching contains only the application shell. No PHI or emergency request is cached or automatically replayed. Requests do not reach any operator. No availability SLA or healthcare regulatory compliance is claimed.

## Deployment
`ansible/deploy.yml` publishes the static demonstration at the intended domain on an explicitly selected Debian/Ubuntu server. It uses a dedicated nginx vhost, verifies nginx before reload, and can optionally request a Let's Encrypt certificate. DNS, SSH credentials and server authorization must be supplied by the operator. It does not replace unrelated vhosts or remove existing wildcard configurations. See `DEPLOYMENT.md`.

## Production work remaining
1. Select jurisdiction, service areas, emergency numbers, licensed operator and private fleet/marketplace model.
2. Implement verified identity, MFA, tenant-scoped backend authorization, dispatch/crew assignments, consent and durable audit logs.
3. Add encrypted clinical storage with key management, retention/export controls, operator agreements and applicable privacy review.
4. Integrate fleet telemetry, traffic routing, dispatch acknowledgment, GPS freshness checks, escalation and clinical ePCR/hospital interfaces.
5. Connect consented SMS/push through a transactional outbox; implement delivery receipts, retries and dispatcher escalation. Configure approved telemedicine.
6. Provision redundant infrastructure, backups, restoration drills, load tests, monitoring, incident response and independently measured uptime targets. A single nginx server is not 99.99% high availability.
7. Validate safety-critical workflows with the ambulance operator before enabling real emergency intake.

## Brand
Forest teal #15564B, mint #DCEEE5, ivory #F5F7F3 and muted coral. Tagline: Care, connected. `dist/assets/logo.svg` and `icon.svg` are scalable code-native brand assets. `brand-art.jpg` was created with the built-in image generation tool using an ambulance/paramedic/home-to-hospital bridge concept. Prompt recorded in `BRAND.md`.

## Super admin, multi-tenant and marketplace preview

Select **Super admin** to create/edit/suspend organizations, manage tenant memberships and roles, toggle booking/marketplace features, edit products, review/cancel demo orders, adjust demo credits with a reason, and configure payment-provider references. The tenant selector switches between independent in-memory datasets for journeys, fleet, records, users, products, orders, gateway settings, features, profile and session audit history. Suspended tenants cannot create bookings or orders. Administrative pages remain demonstration controls, not server-enforced authorization.

The marketplace supports product publication/archive, currency amounts stored in integer minor units, and order snapshots that preserve the purchase amount after product edits. Stripe, PayPal, Paystack and Flutterwave settings are **test configuration interfaces only**. They accept environment-variable names, not secret values. Simulated orders remain explicitly unpaid. No checkout API, webhook verification, refund, payout, financial wallet, subscription renewal or provider SDK is implemented. Demo credits are session-only counters, not money.

Before production, implement authenticated server-side tenant membership checks on every resource; compound tenant keys and database policies; safe super-admin elevation; immutable platform and tenant audits; provider secret storage; server-priced checkout; idempotency; signed webhook verification; reconciliation; refund authorization; and currency/provider availability validation. Do not use this preview for production multi-tenant patient data or payments.

## Accounts and mobile preview
`server/auth.py` adds SQLite-backed signup/login/logout with scrypt hashes, hashed expiring sessions, Secure HttpOnly cookies, origin checks and aggregate request throttling. The deployment playbook installs its systemd service on loopback port 18872 and proxies /api/. Accounts do not convert the demo role switcher into backend clinical authorization. Email verification, password recovery and self-service deletion remain unfinished. Do not use for PHI.

`mobile/android` is an Android 8+ WebView development client. GitHub Actions builds and verifies a signed debug APK and publishes it to the android-preview prerelease. `/install.html` links the release and offers web-app instructions for iOS/desktop. APK availability depends on a successful build; signing-cache loss can require reinstalling. No native iOS binary, background tracking, emergency dispatch, or push notifications are implemented.
