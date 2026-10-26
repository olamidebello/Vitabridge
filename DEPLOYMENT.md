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
