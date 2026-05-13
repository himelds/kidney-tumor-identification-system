# Contributing to Kidney Tumor Identification System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

Please be respectful and constructive in all interactions. This is a research-oriented project — contributions that improve accuracy, explainability, or usability are especially welcome.

---

## How to Contribute

### Types of contributions welcome

- 🐛 Bug fixes
- 📈 Model improvements (better architecture, preprocessing, augmentation)
- 🔍 Explainability improvements (new XAI methods)
- 📖 Documentation improvements
- 🧪 New tests
- 🌐 New API endpoints
- 🎨 UI/UX improvements

### Types of contributions NOT accepted

- Adding clinical claims without peer-reviewed evidence
- Removing the medical disclaimer
- Breaking changes without discussion

---

## Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/kidney-tumor-identification-system.git
cd kidney-tumor-identification-system

# 2. Create a conda environment
conda create -n kidney-tumor python=3.11 -y
conda activate kidney-tumor

# 3. Install all dependencies
make install

# 4. Copy environment variables
cp .env.example .env
# Fill in your credentials in .env

# 5. Run the data pipeline
python main.py

# 6. Run tests to verify setup
make test
```

---

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. **Make your changes** following the coding standards below
4. **Run tests** before submitting:
   ```bash
   make test
   make lint
   ```
5. **Commit** with a descriptive message following [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: add LIME explainability support
   fix: correct preprocessing for DICOM images
   docs: update API reference
   test: add unit tests for drift detector
   ```
6. **Push** to your fork and open a Pull Request
7. Fill in the PR template and wait for review

---

## Coding Standards

This project uses automated code quality tools. They run automatically on every commit via pre-commit hooks.

**After cloning, install hooks:**
```bash
pre-commit install
```

### Style guidelines

- **Formatter:** `black` with line length 100
- **Import sorter:** `isort` with black profile
- **Linter:** `flake8` (extend-ignore: E203)
- **Python version:** 3.11+ syntax

### Component conventions

All components in `src/components/` must follow this pattern:

```python
class MyComponent:
    def __init__(self, config: MyConfig):
        self.config = config

    def run(self):
        # Main execution
        pass
```

### Pipeline stage conventions

All pipeline stages in `src/pipeline/` must follow this pattern:

```python
STAGE_NAME = "My Stage"

class MyPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        # ... use components

if __name__ == "__main__":
    pipeline = MyPipeline()
    pipeline.main()
```

### No hardcoded values

All paths, hyperparameters, and configuration must come from `config/config.yaml` or `params.yaml` — never hardcoded in Python files.

---

## Reporting Bugs

Open a GitHub Issue with:

- **Title:** Clear, descriptive summary
- **Environment:** OS, Python version, dependency versions
- **Steps to reproduce:** Exact commands or code
- **Expected behavior:** What should happen
- **Actual behavior:** What actually happens
- **Logs:** Relevant output from `logs/` directory

---

## Suggesting Features

Open a GitHub Issue with the `enhancement` label and describe:

- The problem you are trying to solve
- Your proposed solution
- Any alternatives you considered
- Whether you are willing to implement it

---

## Questions?

Feel free to reach out:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-dashimel-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/dashimel/)
[![Email](https://img.shields.io/badge/Email-himeldas077@gmail.com-red?style=flat-square&logo=gmail)](mailto:himeldas077@gmail.com)
