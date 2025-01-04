.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest -v --cov=app tests/

test-report:
	pytest -v --cov=app --cov-report=html tests/

run:
	flask run

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
