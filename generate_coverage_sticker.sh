uv run coverage run -m pytest -v .
coverage_output=$(coverage report -m)
coverage-badge -o test_coverage.svg -f
xdg-open test_coverage.svg