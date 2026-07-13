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
validate-data:
	@python scripts/validate_data.py

migrate:
	@python scripts/migrate.py

ingest-db:
	@python scripts/ingest_master.py db

ingest-files:
	@python scripts/ingest_master.py files

ingest-api:
	@python scripts/ingest_master.py api

ingest:
	@python scripts/ingest_master.py all

profile:
	@python -m knowledge_prep.cli profile

clean-data:
	@python -m knowledge_prep.cli clean

enrich:
	@python -m knowledge_prep.cli enrich

export-golden:
	@python -m knowledge_prep.cli export

index:
	@python -m copilot.cli index

# Grab all arguments after "ask" and join them into a clean string
ask:
	@python -m copilot.cli ask "$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"

evaluate:
	@python -m copilot.cli evaluate

serve:
	@pip install -q uvicorn fastapi pydantic
	@python -m uvicorn copilot.api:app --host 127.0.0.1 --port 8000 --reload

# Prevents make from complaining about the query words being invalid targets
%:
	@: