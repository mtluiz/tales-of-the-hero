P3 ?= $(shell which python3)
P ?= $(shell which python)
PYTHON ?= $(if $(P3), $(P3), $(P) )

setup:
	@$(PYTHON) -m pip install -r requirements.txt

run:
	@$(PYTHON) src/main.py