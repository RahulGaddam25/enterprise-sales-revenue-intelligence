.PHONY: install generate transform test

install:
	python -m pip install -e .

generate:
	PYTHONPATH=src python -m sales_intelligence.generate

transform:
	PYTHONPATH=src python -m sales_intelligence.pipeline

test:
	PYTHONPATH=src python -m unittest discover -s tests -v
