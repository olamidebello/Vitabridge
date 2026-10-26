#!/usr/bin/env bash
set -euo pipefail
# Run on the Olamidepanel server, from a reviewed copy of this repository.
cd "$(dirname "$0")/.."
if [[ $(id -u) -ne 0 ]]; then
  echo 'Run this deployment as root on the Olamidepanel server.' >&2
  exit 1
fi
if [[ $# -lt 1 ]]; then
  echo "Usage: bash $0 CERTBOT_EMAIL [additional ansible arguments...]" >&2
  exit 2
fi
acme_email=$1
shift
if ! command -v ansible-playbook >/dev/null; then
  echo 'Install dependencies: apt-get update && apt-get install -y git ansible-core' >&2
  exit 1
fi
if [[ -n $(git status --porcelain --untracked-files=no) ]]; then
  echo 'Tracked checkout changes detected; commit or preserve them before deploying.' >&2
  exit 1
fi
git pull --ff-only origin main
exec ansible-playbook -i localhost, -c local ansible/pull-and-deploy.yml \
  -e deploy_hosts=localhost --extra-vars "certbot_email=$acme_email" "$@"
