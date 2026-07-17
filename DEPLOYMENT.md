# Docker deployment

From the project root, build and start DocFlex:

```bash
docker compose up -d --build
```

Nginx is the only public container. Open `http://<server-ip>/` (or your
domain after its DNS points at the server). The Flask/LibreOffice container is
available only on Docker's private network.

Useful commands:

```bash
docker compose ps
docker compose logs -f
docker compose down
```

To use a non-default host port, create `.env` from `.env.example` and set
`DOCFLEX_PORT`, then use `http://<server-ip>:<port>/`.

For a domain, update `server_name _;` in `nginx/default.conf` to the domain.
TLS is intentionally not configured yet; put a certificate-aware reverse
proxy in front of this stack or add Certbot when the domain is ready.
