#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v ansible-playbook >/dev/null; then
  echo 'Install Ansible first: apt-get update && apt-get install -y ansible-core' >&2
  exit 1
fi
if [[ $# -lt 2 ]]; then
  echo "Usage: bash $0 INVENTORY_FILE CERTBOT_EMAIL [extra ansible arguments...]" >&2
  exit 2
fi
inventory_file=$1
acme_email=$2
shift 2
exec ansible-playbook -i "$inventory_file" ansible/olamidepanel.yml --extra-vars "certbot_email=$acme_email" "$@"
