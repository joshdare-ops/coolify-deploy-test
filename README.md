# coolify-deploy-test

A throwaway Python standard-library app for JOS-706: prove one Coolify deploy
and one rollback. There are no third-party dependencies or required environment
variables.

## Local run

With Python 3.13:

```sh
python -u server.py
curl http://localhost:8080/
```

The server listens on all interfaces on port 8080. Set `PORT` to override it:

```sh
PORT=9090 python -u server.py
```

With Docker:

```sh
docker build -t coolify-deploy-test:v1 .
docker run --rm -p 8080:8080 coolify-deploy-test:v1
```

## Endpoints

- `GET /` (or `/index.html`): HTTP 200 with `VERSION=1`.
- `GET /health` (or `/health/`): HTTP 200 with `ok`.
- Other paths: HTTP 404.

## Tests

```sh
python -m unittest discover -s tests -v
```

These tests are the cheap check for version 1. They do not deploy anything.

## How Coolify deploys it

Create a Coolify project (for this test, `jos-706-test`) and add an application
from the public GitHub repository `joshdare-ops/coolify-deploy-test`. Use the
Dockerfile build pack and publish port 8080. No domain, volumes, or environment
variables are required. Deploy a commit from `main` after it is merged.

To test rollback later, a separate version 2 PR will change the served string to
`VERSION=2`. Deploy that, then use Coolify's rollback to this version 1
commit/image. The page should serve `VERSION=1` again.

Coolify rollback redeploys an already-built image for an earlier commit. It does
not undo environment variable, volume, or configuration changes.
