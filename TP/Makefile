.PHONY: test unit_test perf_test coverage lint doc

test:
	pytest tests/

unit_test:
	pytest -m "not perf" tests/

perf_test:
	pytest -m perf tests/performance/

coverage:
	coverage run -m pytest -m "not perf" tests/
	coverage report
	coverage html

lint:
	ruff check .

doc:
	pdoc3 --html --output-dir docs --force triangulator