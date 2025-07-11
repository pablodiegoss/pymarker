
lint:
	ruff format pymarker 
	ruff check --extend-select I --fix pymarker

check: 
	ruff check