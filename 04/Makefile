install:
    pip install -r requirements.txt

test:
    python -m unittest discover -s . -p "test_*.py"

coverage:
    coverage run -m unittest discover -s . -p "test_*.py"
    coverage report -m
    coverage html

lint:
    flake8 .
    pylint *.py

format:
    black .

check: lint test coverage

all: install check

