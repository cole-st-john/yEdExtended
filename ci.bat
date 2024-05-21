@echo off

:: Install dependencies
python -m pip install --upgrade pip
python -m pip install flake8 pytest coverage coverage-badge setuptools
python -m pip install -e .
if exist requirements.dev.txt (
    python -m pip install -r requirements.dev.txt
)

:: Lint with flake8
:: Stop the build if there are Python syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
:: Exit-zero treats all errors as warnings (you may want to adjust this)
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

:: Run tests with pytest and coverage information
coverage run -m pytest .

:: Generate and commit coverage report (if Python version is 3.12)
for /f "tokens=2 delims==" %%i in ('python --version') do set PYTHON_VERSION=%%i
if "%PYTHON_VERSION%" == "3.12" (
    set coverage_output=coverage report -m
    coverage-badge -o test_coverage.svg -f

    :: Configure Git with the author information
    git config --global user.email "info@colestjohn.com"
    git config --global user.name "cole-st-john"

    :: Add the test_coverage.svg file to the repository
    git add test_coverage.svg

    :: Commit the file with a message that includes the coverage output
    git commit -m "Updated test coverage badge

    Test Coverage Results:

    %coverage_output%"

    :: Push the changes to the correct branch
    git push origin master
)

:: Set GitHub token environment variable (needs to be set beforehand in the system or CI/CD environment)
set GH_TOKEN=%GH_TOKEN%


pause