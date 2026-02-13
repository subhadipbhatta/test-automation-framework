# Makefile for Test Automation Framework

.PHONY: help install setup test test-web test-api test-salesforce test-smoke coverage report clean docs lint format

help:
	@echo "Test Automation Framework - Available Commands"
	@echo "=============================================="
	@echo "make install       - Install dependencies"
	@echo "make setup         - Setup environment (install + init)"
	@echo "make test          - Run all tests"
	@echo "make test-web      - Run web tests only"
	@echo "make test-api      - Run API tests only"
	@echo "make test-salesforce - Run Salesforce tests only"
	@echo "make test-smoke    - Run smoke tests only"
	@echo "make coverage      - Run tests with coverage report"
	@echo "make report        - Generate HTML test report"
	@echo "make clean         - Clean up generated files"
	@echo "make lint          - Run linters"
	@echo "make format        - Format code"
	@echo "make docs          - Generate documentation"

install:
	pip install -r requirements.txt
	playwright install

setup: install
	cp .env.example .env
	mkdir -p reports logs
	@echo "Setup complete! Edit .env with your configuration."

test:
	pytest tests/ -v --tb=short

test-web:
	pytest tests/web -v -m web --tb=short

test-api:
	pytest tests/api -v -m api --tb=short

test-salesforce:
	pytest tests/salesforce -v -m salesforce --tb=short

test-smoke:
	pytest tests/ -v -m smoke --tb=short

coverage:
	pytest --cov=src --cov-report=html --cov-report=term

report:
	pytest --html=reports/report.html --self-contained-html -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf reports/*.html
	rm -rf .tox/

lint:
	flake8 src tests --max-line-length=100
	mypy src --ignore-missing-imports

format:
	black src tests --line-length=100
	isort src tests --profile=black --line-length=100

docs:
	@echo "Documentation is available in docs/ directory"
	@echo "Quick Start: docs/QUICKSTART.md"
	@echo "Architecture: docs/ARCHITECTURE.md"
	@echo "API Guide: docs/API_GUIDE.md"
	@echo "Salesforce Guide: docs/SALESFORCE_GUIDE.md"
