# Market Compass Documentation

This directory separates **product vision**, **current implementation**, **current truth**, **engineering architecture**, and **future roadmap** so they do not get mixed into one heroic Markdown file.

## Read in this order

### 0. [`PRODUCT-INTENTION.md`](PRODUCT-INTENTION.md)

**Canonical founder intention and feature-purpose registry.**

This controls why Market Compass exists, what every named feature is meant to accomplish, what
the user must receive, and what each feature must never be allowed to become.

### 1. [`../README.md`](../README.md)

Start here.

Explains:

- what Market Compass is;
- what problem it is trying to solve;
- what works today;
- what does not work yet;
- how to install and run it;
- how evidence scores should be interpreted.

### 2. [`STATUS.md`](STATUS.md)

**Current implementation truth table.**

Use this document whenever you need to know whether a capability is:

- implemented;
- partial;
- research;
- planned;
- not in current scope.

If the long-term PRD and STATUS appear to disagree about whether something exists today, **STATUS wins**.

### 3. [`IMPLEMENTATION.md`](IMPLEMENTATION.md)

Explains the current v0.1 code:

- runtime flow;
- module responsibilities;
- local environment;
- technical logic;
- current data sources;
- scoring;
- current extension seams.

### 4. [`ARCHITECTURE.md`](ARCHITECTURE.md)

Explains the engineering design:

- why 115 nodes do not require 115 physical scripts;
- trust boundaries;
- canonical contracts;
- provider/model replacement strategy;
- evidence aggregation philosophy;
- future provenance/data architecture;
- failure behavior;
- testing strategy.

### 5. [`ROADMAP.md`](ROADMAP.md)

Explains the staged path from v0.1 research software toward a production research platform.

Major stages include:

- data trust and reproducibility;
- multi-timeframe analysis;
- asset/fundamental intelligence;
- event intelligence;
- verified relationship graph;
- stronger historical analogs;
- champion/challenger forecasting;
- narratives;
- options;
- persistent product workflows;
- execution only after separate safety/legal/security review.

### 6. [`PRODUCT-REQUIREMENTS.md`](PRODUCT-REQUIREMENTS.md)

The long-form product requirements document.

This is the broadest product vision and includes capabilities that are **not yet implemented**.

Read it as the design destination, not as a release checklist claiming everything exists today.

### 7. [`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md)

The conceptual 115-node IP/product inventory.

The stable node IDs represent independently addressable product capabilities. The runtime implementation intentionally maps related node IDs to shared code where that reduces duplication.

The live runtime mapping is:

```text
src/market_compass/registry.py
```

### 8. [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)

Use when local setup or live analysis fails.

Covers:

- wrong directory / not a git repository;
- `python` vs `python3`;
- `.venv` verification;
- SSL certificate failures;
- PATH warnings;
- browser auto-open;
- port conflicts;
- provider/symbol failures;
- CSV fallback;
- environment reset.

### 9. [`../CHANGELOG.md`](../CHANGELOG.md) and [`FEATURE-JOURNAL.md`](FEATURE-JOURNAL.md)

The change log records what shipped. The separate feature journal records founder direction,
product interpretation, preservation decisions, evidence, and unresolved work.

---

# Source-of-truth hierarchy

For **what exists today**:

```text
STATUS.md
  -> IMPLEMENTATION.md
  -> runtime code + tests
```

For **how it is engineered**:

```text
ARCHITECTURE.md
  -> runtime code
```

For **what should be built next**:

```text
ROADMAP.md
```

For **long-term product intent**:

```text
PRODUCT-INTENTION.md
  -> PRODUCT-REQUIREMENTS.md
  -> IP-NODE-REGISTRY.md
```

For **history and reasoning**:

```text
CHANGELOG.md (what changed)
FEATURE-JOURNAL.md (why it changed)
```

The README is the product front door and should summarize all of the above without pretending that planned features are already implemented.

---

# Documentation rules

When updating the project:

1. If founder intention or a feature's purpose changes, update `PRODUCT-INTENTION.md` and append `FEATURE-JOURNAL.md`.
2. If shipped code changes, update `CHANGELOG.md` and `STATUS.md`.
3. If module/data/control-flow design changes, update `ARCHITECTURE.md` and/or `IMPLEMENTATION.md`.
4. If priorities change, update `ROADMAP.md`.
5. If a new long-term product requirement appears, update `PRODUCT-REQUIREMENTS.md` and the node registry when appropriate.
6. If installation/runtime failure behavior changes, update `TROUBLESHOOTING.md`.
7. A later projection must explicitly map and preserve earlier named features.
8. Keep the root README readable by someone who did not participate in the original design conversation.

The goal is boring consistency. Boring documentation is underrated because the alternative is six files confidently describing six different products.
