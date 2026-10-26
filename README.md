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
