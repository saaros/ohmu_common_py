PYTHON ?= python3
PYTEST_ARG ?= -vv
generated = ohmu_common_py/version.py

all: $(generated)

ohmu_common_py/version.py: version.py
	$(PYTHON) $^ $@

test: test-py2 test-py3

test-py2: $(generated)
	$(MAKE) PYTHON=python3 test-all

test-py3: $(generated)
	$(MAKE) PYTHON=python3 test-all

test-all: flake8 pylint unittest

unittest: $(generated)
	$(PYTHON) -m coverage run --source ohmu_common_py -m pytest $(PYTEST_ARG) test/
	$(PYTHON) -m coverage report --show-missing

pylint: $(generated)
	$(PYTHON) -m pylint.lint --rcfile .pylintrc ohmu_common_py test *.py

flake8: $(generated)
	$(PYTHON) -m flake8 --max-line-len=125 ohmu_common_py test *.py
