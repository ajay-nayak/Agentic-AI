# Contributing to Agentic AI Projects

Thank you for your interest in contributing to this repository! We welcome contributions that add new Agentic AI patterns, improve existing architectures, fix bugs, or expand documentation.

---

## Repository Philosophy

1. **Modular & Self-Contained**: Each project under `projects/` should be self-contained with its own dependencies, `src/`, `tests/`, and `README.md`.
2. **Deterministic & Testable**: Code should have unit tests with mocks to ensure test suites can run offline without external API keys.
3. **Well-Documented**: Code must adhere to clean code principles with descriptive docstrings, type annotations, and clear README explanations.

---

## Adding a New Project

To add a new project:
1. Copy the template from `config/templates/project-template/` into `projects/<new-project-name>`.
2. Update `pyproject.toml` with project-specific metadata and dependencies.
3. Implement your agentic logic in `src/` and write corresponding tests in `tests/`.
4. Create a comprehensive `README.md` following the project template structure.
5. Update the root `README.md` catalog table and learning path to include your new project.

---

## Code Quality Standards

Before submitting a pull request or pushing code, ensure standards are met:

```bash
# Format code
black .
isort .

# Run validation and test suite
python scripts/validation/validate_repo.py
python scripts/development/run_all_tests.py
```
