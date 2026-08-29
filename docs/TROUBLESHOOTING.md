# Market Compass Troubleshooting

This guide covers the failures most likely to appear during local setup and the failures already observed on macOS.

The first debugging rule is simple:

> Verify the directory, verify the interpreter, verify the environment, then blame the market data provider.

Humans tend to reverse that order and lose twenty minutes.

---

# 1. `fatal: not a git repository`

Example:

```text
fatal: not a git repository (or any of the parent directories): .git
make: *** No rule to make target `setup'. Stop.
```

Cause:

You are not inside the cloned repository directory.

Check:

```bash
pwd
ls -la
```

A repository root should contain at least:

```text
.git/
Makefile
pyproject.toml
README.md
src/
tests/
docs/
```

If the repository was accidentally cloned inside another folder with the same name, locate it:

```bash
find ~/Developer -maxdepth 5 -name .git -type d -print
```

Then `cd` to the parent of the `.git` directory.

---

# 2. `make: python: No such file or directory`

Old versions of the Makefile defaulted to `python`. Modern macOS commonly exposes `python3` instead.

Current repository behavior:

```make
PYTHON ?= python3
```

Fix:

```bash
git pull
make setup
```

Or specify an interpreter explicitly:

```bash
make setup PYTHON=/usr/local/bin/python3
```

Market Compass requires Python 3.11+.

---

# 3. Verify the active environment

The project uses a local `.venv`.

Run:

```bash
make doctor
```

Expected shape:

```text
Using Python 3.x.x at /path/to/app-market-compass/.venv/bin/python
```

Make targets automatically prefer `.venv/bin/python` when it exists.

You do not need to activate the environment for Make targets.

For direct CLI commands, either use:

```bash
.venv/bin/market-compass analyze HYPE --horizon 20
```

or activate it:

```bash
source .venv/bin/activate
market-compass analyze HYPE --horizon 20
```

---

# 4. `CERTIFICATE_VERIFY_FAILED`

Example:

```text
SSLCertVerificationError: certificate verify failed: unable to get local issuer certificate
```

This occurred on a Python.org macOS installation when the standard library attempted to reach the live Yahoo endpoint.

Current Market Compass uses the `certifi` CA bundle explicitly.

Update and reinstall dependencies:

```bash
git pull
make setup
```

Then retry:

```bash
make analyze ASSET=HYPE HORIZON=20
```

Do **not** solve this by disabling TLS certificate verification. A research application that fixes trust errors by choosing not to trust anything has misunderstood the assignment.

---

# 5. `market-compass` command not found

If you installed into system Python, pip may warn that its scripts directory is not on `PATH`.

The recommended solution is the project `.venv`:

```bash
make setup
```

Then use:

```bash
.venv/bin/market-compass registry
```

or Make targets:

```bash
make analyze ASSET=HYPE HORIZON=20
```

No global PATH changes are required.

---

# 6. Browser does not open

Current behavior:

```bash
make app
```

runs the Market Compass launcher, starts the local server, waits briefly for readiness, and attempts to open the default browser.

The application address is:

```text
http://127.0.0.1:8000
```

If the browser does not open automatically but the server is running, open that address manually.

For a server/API process that should **not** open a browser:

```bash
make api
```

---

# 7. Port 8000 is already in use

Symptom:

Uvicorn reports that the address is already in use.

Check which process owns the port:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

Stop the old local Market Compass/Uvicorn process and rerun:

```bash
make app
```

---

# 8. Live symbol cannot be found

Market Compass first searches the requested symbol because providers sometimes use internal names for crypto instruments.

For example, a user may request:

```text
HYPE
```

while the provider may expose an internal symbol with an additional suffix.

The report metadata should preserve both:

- `requested_symbol`
- `resolved_symbol`

If a symbol still cannot be resolved, verify the provider supports it or use CSV input.

---

# 9. Live provider is down or unreliable

The current live provider is a public research source, not an SLA-backed institutional feed.

If live acquisition fails, CSV mode isolates the engine from the provider.

Required CSV shape:

```text
date,open,high,low,close,volume
```

Run:

```bash
.venv/bin/market-compass analyze TEST --csv ./prices.csv --horizon 20
```

If CSV works while live mode fails, the analytic engine is healthy and the failure is in acquisition/provider access.

Provider abstraction, caching, and failover are Phase 1 roadmap priorities.

---

# 10. Tests pass but analysis fails

This is possible.

Unit tests primarily validate deterministic calculations and internal contracts. Live analysis additionally depends on:

- network connectivity;
- TLS;
- provider availability;
- provider symbol resolution;
- provider response shape.

So:

```text
8/10/20 tests passed
```

means the software contracts tested locally passed. It does not mean every external service is reachable.

Debug sequence:

```bash
make doctor
make test
make analyze ASSET=HYPE HORIZON=20
```

If the last command fails, inspect the bottom of the traceback for the first Market Compass/provider-specific error.

---

# 11. Reset the local environment

If dependencies become inconsistent:

```bash
make clean
make setup
make test
```

`make clean` removes the project virtual environment and local test caches. It does not delete source code.

---

# 12. Verify repository version

Check your current commit:

```bash
git rev-parse --short HEAD
```

Check whether local `main` is behind:

```bash
git status
git fetch origin
git log --oneline --decorate -5
```

Update:

```bash
git pull
```

If you have local edits, Git may require you to commit/stash them before pulling.

---

# 13. What to include in a useful bug report

Include:

```bash
pwd
git rev-parse --short HEAD
make doctor
```

Then include:

- the command that failed;
- the last 30-50 lines of the traceback;
- requested symbol;
- whether CSV mode works;
- operating system and architecture.

Do not paste API keys or credentials. Market Compass does not require broker credentials in v0.1.

---

# 14. Expected healthy local sequence

```bash
git pull
make setup
make test
make analyze ASSET=HYPE HORIZON=20
make app
```

Healthy expectations:

1. `.venv` is created/updated;
2. tests complete successfully;
3. analysis prints a Market Compass report;
4. `make app` starts the local server;
5. the default browser opens to `http://127.0.0.1:8000` or the URL works manually.

If those five things happen, the local v0.1 application is operating as intended.
