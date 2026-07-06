.PHONY: \
	install \
	format \
	lint \
	test \
	validate-data \
	migrate \
	ingest-db \
	ingest-files \
	ingest-api \
	ingest \
	profile \
	clean-data \
	enrich \
	export-golden \
	index \
	ask \
	evaluate \
	serve
install:
	pip install -e ".[dev,readers,llm]"

format:
	py -3.11 -m ruff format .

lint:
	py -3.11 -m ruff check .

test:
	py -3.11 -m pytest