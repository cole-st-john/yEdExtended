uv run coverage run -m pytest -v .
set coverage_output=coverage report -m
coverage-badge -o test_coverage.svg -f