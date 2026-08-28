PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python
RUN_PYTHON = $(if $(wildcard $(VENV_PYTHON)),$(VENV_PYTHON),$(PYTHON))
ASSET ?= HYPE-USD
HORIZON ?= 20

.PHONY: setup test lint analyze node backtest app api doctor clean

doctor:
	@$(RUN_PYTHON) -c 'import sys; v=sys.version_info; assert v >= (3, 11), f"Python 3.11+ required, found {v.major}.{v.minor}"'
	@echo "Using $$($(RUN_PYTHON) --version) at $$($(RUN_PYTHON) -c 'import sys; print(sys.executable)')"

setup:
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "Python interpreter '$(PYTHON)' not found. Install Python 3.11+ or run make setup PYTHON=/path/to/python3" && exit 1)
	@$(PYTHON) -c 'import sys; v=sys.version_info; assert v >= (3, 11), f"Python 3.11+ required, found {v.major}.{v.minor}"'
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -e '.[dev]'
	@echo "Market Compass is installed in $(VENV). Make targets use it automatically."

test: doctor
	$(RUN_PYTHON) -m pytest -q

lint: doctor
	$(RUN_PYTHON) -m ruff check src tests

analyze: doctor
	$(RUN_PYTHON) -m market_compass analyze $(ASSET) --horizon $(HORIZON)

node: doctor
	$(RUN_PYTHON) -m market_compass node $(NODE) $(ASSET) --horizon $(HORIZON)

backtest: doctor
	$(RUN_PYTHON) -m market_compass backtest $(ASSET) --horizon $(HORIZON)

app: doctor
	$(RUN_PYTHON) -m market_compass.launcher

api: doctor
	$(RUN_PYTHON) -m uvicorn market_compass.api:app --reload --port 8000

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache
