# Code Quality and Development Workflow

This document explains the code quality tools and development workflow implemented for the Language Tutor project. These tools enforce the standards defined in `copilot-instructions.md`.

## Quick Start

```bash
# Setup development environment
make setup-dev

# Run all quality checks
make quality-check

# Format code before committing
make format

# Run tests
make test
```

## Code Quality Tools

### 1. Black - Code Formatting
**Purpose**: Automatic Python code formatting for consistency
**Configuration**: `pyproject.toml` (tool.black section)

```bash
# Format all code
black .

# Check formatting without changes
black --check --diff .
```

**Key Features**:
- 88 character line length (slightly longer than PEP 8's 79)
- Automatic string formatting and import organization
- Consistent indentation and spacing

### 2. isort - Import Organization
**Purpose**: Sorts and organizes imports according to PEP 8 and our guidelines
**Configuration**: `pyproject.toml` (tool.isort section)

```bash
# Sort imports
isort .

# Check import order
isort --check-only --diff .
```

**Import Order**:
1. Standard library imports
2. Third-party imports (langchain, openai, streamlit, etc.)
3. Local imports (src modules)

### 3. flake8 - Style and Error Checking
**Purpose**: Checks for PEP 8 compliance and common Python errors
**Configuration**: `.flake8`

```bash
# Run flake8
flake8 .
```

**Checks**:
- PEP 8 style violations
- Syntax errors
- Unused imports and variables
- Code complexity (max 10)
- Line length (88 characters)

### 4. pylint - Advanced Code Analysis
**Purpose**: Advanced static analysis for code quality and best practices
**Configuration**: `.pylintrc`

```bash
# Run pylint
pylint src/ app.py cli_tutor.py --fail-under=8.0
```

**Analysis**:
- Code smells and design issues
- Naming conventions
- Documentation compliance
- Refactoring suggestions
- Minimum score: 8.0/10

### 5. mypy - Static Type Checking
**Purpose**: Validates type hints and catches type-related errors
**Configuration**: `pyproject.toml` (tool.mypy section)

```bash
# Run type checking
mypy src/ --ignore-missing-imports
```

**Features**:
- Type hint validation
- Function signature checking
- Return type verification
- Optional type enforcement

### 6. bandit - Security Analysis
**Purpose**: Scans Python code for common security issues
**Configuration**: `.pre-commit-config.yaml`

```bash
# Run security scan
bandit -r src/ -f json -o bandit-report.json
```

**Security Checks**:
- Hard-coded passwords
- SQL injection vulnerabilities
- Shell injection risks
- Insecure random generators

### 7. safety - Dependency Vulnerability Scanning
**Purpose**: Checks dependencies for known security vulnerabilities

```bash
# Check dependencies
safety check -r requirements.txt
safety check -r requirements_no_audio.txt
```

## Pre-commit Hooks

Pre-commit hooks run quality checks automatically before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Skip hooks for emergency commits
git commit --no-verify -m "Emergency fix"
```

**Enabled Hooks**:
- Black formatting
- isort import organization
- flake8 linting
- File cleanup (trailing whitespace, EOF, etc.)
- Security scanning with bandit
- Dependency vulnerability checks

## GitHub Actions CI/CD

### CI Workflow (`.github/workflows/ci.yml`)
Runs on every pull request and push to main/develop:

1. **Code Quality Checks**:
   - Black formatting validation
   - isort import order validation
   - flake8 linting
   - pylint analysis (warning only)
   - mypy type checking (warning only)

2. **Testing**:
   - pytest with coverage reporting
   - Coverage reports in XML format for SonarQube

3. **Security**:
   - Dependency vulnerability scanning
   - Bandit security analysis

4. **SonarQube Analysis** (if configured):
   - Code quality metrics
   - Security hotspots
   - Technical debt analysis
   - Duplication detection

### PR Protection Workflow (`.github/workflows/pr-protection.yml`)
Validates pull request requirements:

1. **PR Title Format**: Must follow conventional commit format
   - `feature(scope): description`
   - `bugfix(scope): description`
   - `docs: description`

2. **Branch Naming**: Must follow convention
   - `feature/description`
   - `bugfix/description`
   - `docs/description`

3. **PR Description**: Must be provided and explain changes

4. **Issue Linking**: Must reference an issue with "Fixes #123"

## SonarQube Integration

### Configuration
- **Project file**: `sonar-project.properties`
- **Quality gate**: Configured to enforce minimum standards
- **Coverage**: Requires test coverage reporting
- **Security**: Scans for vulnerabilities and hotspots

### Setup (Optional)
1. Create SonarQube/SonarCloud account
2. Add repository secrets:
   - `SONAR_TOKEN`: Your SonarQube token
   - `SONAR_HOST_URL`: SonarQube server URL

### Quality Metrics
- **Maintainability**: Code smells, technical debt
- **Reliability**: Bugs, error-prone code
- **Security**: Vulnerabilities, security hotspots
- **Coverage**: Test coverage percentage
- **Duplication**: Code duplication detection

## Development Workflow

### 1. Setting Up
```bash
# Clone repository
git clone <repository-url>
cd language-tutor

# Setup development environment
make setup-dev
```

### 2. Making Changes
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Format code
make format

# Run quality checks
make quality-check

# Commit changes (pre-commit hooks will run)
git add .
git commit -m "feature: add your feature description"
```

### 3. Before Submitting PR
```bash
# Run CI checks locally
make ci-check

# Push branch
git push origin feature/your-feature-name

# Create pull request following the template
```

### 4. PR Review Process
1. Automated CI checks must pass
2. Code review by maintainer required
3. All conversations must be resolved
4. Branch must be up-to-date with main

## Configuration Files

| File | Purpose |
|------|---------|
| `.flake8` | flake8 linting configuration |
| `.pylintrc` | pylint analysis configuration |
| `pyproject.toml` | Black, isort, mypy, pytest configuration |
| `.pre-commit-config.yaml` | Pre-commit hooks configuration |
| `sonar-project.properties` | SonarQube analysis configuration |
| `requirements-dev.txt` | Development dependencies |
| `Makefile` | Development commands |

## Troubleshooting

### Common Issues

**Black formatting conflicts with other tools**:
- Solution: isort and flake8 are configured to work with Black's 88-character line length

**Pre-commit hooks failing**:
```bash
# Update hooks
pre-commit autoupdate

# Run specific hook
pre-commit run black --all-files
```

**Pylint score too low**:
- Focus on fixing errors and warnings first
- Refactor complex functions (reduce complexity)
- Add missing docstrings
- Follow naming conventions

**Type checking errors**:
- Add type hints to function parameters and return values
- Use `# type: ignore` comments sparingly for external libraries
- Install type stubs: `pip install types-requests`

**Test coverage too low**:
- Add unit tests for new functions
- Use pytest fixtures for common test data
- Mock external dependencies (OpenAI API, etc.)

### Getting Help

1. Check this documentation first
2. Review `copilot-instructions.md` for coding standards
3. Look at existing code for examples
4. Create an issue for questions or problems

### Network Connectivity Issues

If you encounter network timeouts when installing packages:

```bash
# Try with increased timeout
pip install --timeout 1000 -r requirements-dev.txt

# Or install packages individually
pip install black isort flake8 pylint mypy pytest

# Use offline mode if packages are cached
pip install --no-index --find-links ~/.cache/pip black

# Alternative: Use conda/mamba for faster installation
conda install black isort flake8 pylint mypy pytest -c conda-forge
```

### Manual Quality Checks (Without Tool Installation)

If you cannot install the quality tools, you can still follow the standards:

1. **Formatting**: Follow PEP 8 guidelines manually
2. **Imports**: Organize as: stdlib, third-party, local
3. **Line length**: Keep lines under 88 characters
4. **Type hints**: Add type annotations to functions
5. **Docstrings**: Use Google-style docstrings
6. **Testing**: Write tests for new functionality

## Continuous Improvement

The quality tools and standards will evolve with the project:

- **Metrics tracking**: Monitor code quality trends
- **Tool updates**: Regular updates to latest versions
- **Standards refinement**: Adjust based on team feedback
- **Coverage goals**: Gradually increase test coverage requirements

Remember: These tools are meant to help maintain code quality and consistency, not to be barriers to development. If you encounter issues or have suggestions for improvements, please create an issue or discuss with the team.