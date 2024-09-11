.PHONY: test coverage clean test-coverage

# Run tests
test:
	PYTHONPATH=src python -m unittest discover src/test/

# Run a specific e2e test case
test-e2e-case:
	PYTHONPATH=src python -m unittest src.test.e2e.$(TEST_SUITE).$(TEST_CLASS).$(TEST_CASE)

# Run tests with coverage
coverage:
	rm -rf .coverage  # Clean old coverage data
	PYTHONPATH=src coverage run --source=src -m unittest discover src/test/
	coverage report -m --omit="src/test/*"

upload-module:
	rm -rf dist
	python -m build
	twine upload dist/*
