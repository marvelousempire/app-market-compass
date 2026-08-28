PYTHON ?= python
ASSET ?= HYPE-USD
HORIZON ?= 20

.PHONY: setup test lint analyze node backtest app api

setup:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests

analyze:
	$(PYTHON) -m market_compass analyze $(ASSET) --horizon $(HORIZON)

node:
	$(PYTHON) -m market_compass node $(NODE) $(ASSET) --horizon $(HORIZON)

backtest:
	$(PYTHON) -m market_compass backtest $(ASSET) --horizon $(HORIZON)

app:
	$(PYTHON) -m uvicorn market_compass.api:app --reload --port 8000

api: app
