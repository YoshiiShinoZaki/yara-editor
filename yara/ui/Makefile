
PYTHON ?= python
PYUIC4 = pyuic4

export PYTHONPATH = $(shell echo "$$PYTHONPATH"):$(shell python -c 'import os; print ":".join(os.path.abspath(line.strip()) for line in file("PYTHONPATH"))' 2>/dev/null)

.PHONY: all check clean clean-pyc

all: clean-pyc check build

check:
#	@$(PYTHON) scripts/detect_missing_analyse_text.py || true


clean: clean-pyc
	-rm -rf build

build:
	$(PYUIC4) yaraeditor.ui > yaraeditor.py


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs: docs/build

docs/build: docs/src/*.txt
	$(PYTHON) docs/generate.py html docs/build $?
	touch docs/build
