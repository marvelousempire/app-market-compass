PYTHON ?= python3
ASSET ?= HYPE-USD
HORIZON ?= 20

.PHONY: setup test lint analyze node backtest app api doctor

doctor:
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "Python interpreter '$(PYTHON)' not found. Install Python 3 or run make <target> PYTHON=/path/to/python3" && exit 1)
	@$(PYTHON) -c 'import sys; v=sys.version_info; assert v >= (3, 11), f"Python 3.11+ required, found {v.major}.{v.minor}"'
	@echo "Using $$($(PYTHON) --version) at $$(command -v $(PYTHON))"

setup: doctor
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e '.[dev]'

test: doctor
	$(PYTHON) -m pytest -q

lint: doctor
	$(PYTHON) -m ruff check src tests

analyze: doctor
	$(PYTHON) -m market_compass analyze $(ASSET) --horizon $(HORIZON)

node: doctor
	$(PYTHON) -m market_compass node $(NODE) $(ASSET) --horizon $(HORIZON)

backtest: doctor
	$(PYTHON) -m market_compass backtest $(ASSET) --horizon $(HORIZON)

app: doctor
	$(PYTHON) -m uvicorn market_compass.api:app --reload --port 8000

api: app
