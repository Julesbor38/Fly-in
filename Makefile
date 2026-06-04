
PYTHON = python3
SCRIPT = fly-in.py
CONFIG = maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict build


run:
	 $(PYTHON) $(SCRIPT) $(CONFIG) || true

debug:
	@poetry run $(PYTHON) -m pdb $(SCRIPT) $(CONFIG) || true

clean:
	@rm -rf */__pycache__
	@rm -rf */.mypy_cache
	@rm -rf .mypy_cache
	@rm -rf __pycache__

lint:
	@python3 -m flake8 *.py && python3 -m flake8 mazegen/*.py
	@python3 -m mypy --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs .

build:
	@pip install poetry
	@poetry build 