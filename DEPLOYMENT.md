# Deploy the development preview

No deployment to the requested custom domain has been performed by creating this repository. DNS/server access is required.

1. Point `vitabridge.olamidemedical.health` to the chosen server's public address. Do not assume an address from another project.
2. Clone this repository to your administration computer, install Ansible, and create an inventory:

```ini
[vitabridge]
your-server-address ansible_user=root
```

3. Inspect the existing web-server configuration for a conflicting exact or wildcard hostname. Review the dedicated nginx config in the playbook.
4. Run:

```bash
ansible-playbook -i inventory.ini ansible/deploy.yml
ansible-playbook -i inventory.ini ansible/deploy.yml -e enable_tls=true -e certbot_email=YOUR_EMAIL
```

5. Confirm the custom HTTPS domain serves VitaBridge, certificate renewal is enabled, and routing works externally. The static deployment remains a labeled demonstration. The playbook does not provision clinical storage or live communications.

The private Sites deployment is a separate review environment. Its .openai/hosting.json is Sites metadata, not configuration for the custom-domain server.

## Pull and deploy on Olamidepanel

The new `ansible/olamidepanel.yml` pulls the repository **on the target server**, stages a versioned release and configures a dedicated nginx host. It retains an existing certificate on repeat deployments, obtains HTTPS through ACME webroot, checks application routing, and restores the previous release/vhost on deployment failure. Existing releases are retained for recovery. It does not modify Olamidepanel's internal database or other domain configurations.

On your administration computer:

```bash
git clone https://github.com/olamidebello/Vitabridge.git
cd Vitabridge
cp ansible/inventory.example.ini inventory.ini
# Edit inventory.ini with your Olamidepanel SSH address/user.
bash scripts/deploy-olamidepanel.sh inventory.ini YOUR_EMAIL
```

On the Olamidepanel server itself, after cloning:

```bash
apt-get update && apt-get install -y git ansible-core
cd /opt/Vitabridge
ansible-playbook -i localhost, -c local ansible/olamidepanel.yml -e deploy_hosts=localhost -e certbot_email=YOUR_EMAIL
```

Before running, point the domain's A record to this server and ensure any AAAA record routes correctly. Allow inbound TCP 80/443. Private repositories require an SSH deploy key and a `repository_url` override using the SSH URL; configure GitHub's verified host key separately. Do not put access tokens in command lines or the repository. Git refuses to discard target checkout modifications. Override `repository_version` with a reviewed commit SHA for pinned releases. Initial TLS failure rolls back the site; correct DNS/ACME errors before retrying.

This deploys the current development preview. No server execution or DNS change is performed merely by adding this playbook.

## ACME 404 on Olamidepanel

Panel hosts may listen on a specific IPv4 address. Nginx chooses that address group before matching a hostname on a wildcard listener. The VitaBridge host now binds both wildcard and the server's default IPv4 address, plus IPv6 wildcard. Set `vitabridge_bind_ipv4` to a list of relevant local addresses when the server uses another panel listener address. No other virtual hosts are removed.

Before contacting Let's Encrypt, the playbook creates a unique challenge file and checks its exact contents over the local IP/Host header and the domain URL without redirects. If either check fails, it rolls back and saves the active Nginx configuration to `/var/log/vitabridge-nginx-deploy.log` (root-only). A server-origin domain check is a useful preflight; successful ACME authorization remains the external reachability test. Check all A/AAAA records and upstream proxies if failures persist.
