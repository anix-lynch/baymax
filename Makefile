.PHONY: sync demo audit test clean

sync:
	bash scripts/sync_sources.sh

audit:
	python -m baymax.audit

demo:
	python -m baymax.demo

test:
	PYTHONPATH=. pytest tests -q

clean:
	rm -rf .pytest_cache baymax/__pycache__ tests/__pycache__
	rm -f outputs/*.db
