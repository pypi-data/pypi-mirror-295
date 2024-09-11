.ONESHELL:

.DEFAULT_GOAL := setup

PYTHON=./venv/bin/python3
PYTEST=./venv/bin/pytest
FLAKE8=./venv/bin/flake8
MYPY=./venv/bin/mypy
COVERAGE=./venv/bin/coverage

venv/bin/activate:
	python3.12 -m venv venv
	. ./venv/bin/activate
	$(PYTHON) -m pip install --upgrade pip 
	$(PYTHON) -m pip install -r requirements/development.txt

venv: venv/bin/activate
	. ./venv/bin/activate

.PHONY: build
build: venv
	rm -f dist/*
	$(PYTHON) -m build
	$(PYTHON) -m pip install --upgrade -e .

.PHONY: setup
setup: clean venv build 

.PHONY: clean
clean:
	# Clean __pycache__ dirs - abuses list comprehension by using "side effect" of `rmtree`
	python3 -Bc "import pathlib; import shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	rm -rf venv

.PHONY: test
test: venv
	$(PYTEST)

.PHONY: test_fast
test_fast: venv
	$(PYTEST) -m "not slow"

.PHONY: coverage
coverage: venv
	$(COVERAGE) run -m pytest tests
	$(COVERAGE) report -m

.PHONY: coverage_html
coverage_html: venv
	$(COVERAGE) run -m pytest tests
	$(COVERAGE) html
# macOS
	open htmlcov/index.html

.PHONY: lint
lint: venv
	$(FLAKE8) src tests

.PHONY: mypy
mypy: venv
	$(MYPY) src tests

.PHONY: code
code: venv
	code .

.PHONY: all
all: setup
