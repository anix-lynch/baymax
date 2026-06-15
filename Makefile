.PHONY: sync demo ui audit readiness test clean

# Baymax uses 3.10+ syntax (e.g. `int | None`). Default python3 must be >= 3.10.
# Override on macOS if system python3 is 3.9: make test PYTHON=/opt/homebrew/bin/python3
PYTHON ?= python3

sync:
	bash scripts/sync_sources.sh

audit:
	$(PYTHON) -m baymax.audit

readiness: audit
	$(PYTHON) deployment-readiness/verify.py

demo:
	$(PYTHON) -m baymax.demo

ui:
	$(PYTHON) -m http.server 8000

test:
	PYTHONPATH=. $(PYTHON) -m pytest tests -q

clean:
	rm -rf .pytest_cache baymax/__pycache__ tests/__pycache__
	rm -f outputs/*.db
