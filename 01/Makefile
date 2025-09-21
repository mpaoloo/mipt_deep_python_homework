.PHONY: test lint format type-check coverage clean

install:
	pip3 install coverage flake8 pylint black isort mypy

test:
	python3 -m unittest discover -v

coverage:
	python3 -m coverage run -m unittest discover
	python3 -m coverage report -m
	python3 -m coverage html

lint:
	python3 -m flake8 .
	python3 -m pylint *.py

format:
	python3 -m black --line-length 79 *.py

type-check:
	python3 -m mypy *.py --ignore-missing-imports

all: install format lint type-check coverage
