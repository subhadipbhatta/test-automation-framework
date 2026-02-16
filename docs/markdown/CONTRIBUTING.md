# Contributing to Test Automation Framework

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/test-automation-framework.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Commit: `git commit -am 'Add feature'`
6. Push: `git push origin feature/your-feature`
7. Submit a Pull Request

## Code Style

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for all functions/classes

### Format Code

```bash
make format
```

### Run Linter

```bash
make lint
```

## Testing

- Write tests for new features
- Ensure all tests pass: `make test`
- Maintain or improve code coverage

## Documentation

- Update README.md for user-facing changes
- Update docs/ for architectural changes
- Add docstrings to functions/classes
- Update CHANGELOG.md

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Create PR with description of changes
6. Respond to code review feedback

## Reporting Issues

1. Search existing issues first
2. Provide clear description
3. Include steps to reproduce
4. Include expected vs actual behavior
5. Provide environment details (OS, Python version, etc.)

## Feature Requests

1. Check if already requested
2. Describe use case
3. Provide examples
4. Explain benefit to users

## Development Setup

```bash
make setup
pip install -e ".[dev]"
```

## Running Tests During Development

```bash
pytest -v -s               # Verbose, show output
pytest tests/web -m web   # Run web tests
pytest --lf               # Run last failed
pytest -x                 # Stop on first failure
```

## Code Review Process

All contributions go through:
1. Automated tests
2. Code review by maintainers
3. Approval and merge

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue for help
- Check documentation first
- Ask in discussions
