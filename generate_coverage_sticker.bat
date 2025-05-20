pip install -r dev-requirements.txt 
pip install -e .
python -m coverage run -m pytest -v .
set coverage_output=coverage report -m
coverage-badge -o test_coverage.svg -f