#!/bin/bash

# Basic validation script for language-tutor project
# Can be run without installing quality tools
# Usage: ./validate-setup.sh

set -e

echo "🔍 Language Tutor - Basic Project Validation"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Python availability
echo ""
echo "🐍 Python Environment:"
echo "----------------------"
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    print_status 0 "Python 3 available: $python_version"
    
    # Check Python version is 3.8+
    python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null
    print_status $? "Python version >= 3.8"
else
    print_status 1 "Python 3 not found"
    exit 1
fi

# Check required files
echo ""
echo "📁 Project Structure:"
echo "--------------------"
required_files=(
    "README.md"
    "requirements.txt" 
    "requirements_no_audio.txt"
    "requirements-dev.txt"
    "app.py"
    "cli_tutor.py"
    "src/__init__.py"
    "copilot-instructions.md"
    ".flake8"
    ".pylintrc"
    "pyproject.toml"
    "sonar-project.properties"
    ".pre-commit-config.yaml"
    "Makefile"
    "docs/CODE_QUALITY.md"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        print_status 0 "$file exists"
    else
        print_status 1 "$file missing"
    fi
done

# Check directory structure
required_dirs=(
    "src/"
    "src/tutor/"
    "src/utils/"
    "docs/"
    ".github/"
    ".github/workflows/"
    ".github/ISSUE_TEMPLATE/"
)

for dir in "${required_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        print_status 0 "$dir directory exists"
    else
        print_status 1 "$dir directory missing"
    fi
done

# Check Python syntax
echo ""
echo "🔍 Python Syntax Check:"
echo "-----------------------"
python_files=("app.py" "cli_tutor.py")

for file in "${python_files[@]}"; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        print_status 0 "$file syntax OK"
    else
        print_status 1 "$file has syntax errors"
    fi
done

# Check src directory Python files
if find src -name "*.py" -exec python3 -m py_compile {} \; 2>/dev/null; then
    print_status 0 "src/ Python files syntax OK"
else
    print_status 1 "src/ has Python syntax errors"
fi

# Check YAML syntax (if PyYAML is available)
echo ""
echo "📋 Configuration Files:"
echo "-----------------------"
yaml_files=(
    ".github/workflows/ci.yml"
    ".github/workflows/pr-protection.yml"
    ".github/workflows/basic-validation.yml"
    ".pre-commit-config.yaml"
)

python3 -c "import yaml" 2>/dev/null
if [ $? -eq 0 ]; then
    for file in "${yaml_files[@]}"; do
        if [[ -f "$file" ]]; then
            if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
                print_status 0 "$file YAML syntax OK"
            else
                print_status 1 "$file has YAML syntax errors"
            fi
        else
            print_warning "$file not found"
        fi
    done
else
    print_warning "PyYAML not available - skipping YAML validation"
fi

# Check Git configuration
echo ""
echo "🌿 Git Configuration:"
echo "--------------------"
if git rev-parse --git-dir > /dev/null 2>&1; then
    print_status 0 "Git repository detected"
    
    # Check if there are any commits
    if git rev-parse HEAD > /dev/null 2>&1; then
        print_status 0 "Git history exists"
    else
        print_warning "No commits in repository yet"
    fi
    
    # Check for common branch names
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    print_status 0 "Current branch: $current_branch"
    
else
    print_status 1 "Not a Git repository"
fi

# Test basic imports
echo ""
echo "📦 Import Tests:"
echo "---------------"
import_test="
import sys
import os
sys.path.insert(0, 'src')

try:
    import src
    print('✅ src module importable')
except ImportError as e:
    print(f'❌ src module import failed: {e}')
    
try:
    from src.utils import config
    print('✅ src.utils.config importable')
except ImportError as e:
    print('⚠️  src.utils.config import failed (expected if dependencies missing)')

try:
    from src.tutor import ai_tutor
    print('✅ src.tutor.ai_tutor importable') 
except ImportError as e:
    print('⚠️  src.tutor.ai_tutor import failed (expected if dependencies missing)')
"

python3 -c "$import_test"

# Check for quality tool availability
echo ""
echo "🛠️  Quality Tools:"
echo "-----------------"
tools=("black" "isort" "flake8" "pylint" "mypy" "pytest")

for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        print_status 0 "$tool available"
    else
        print_warning "$tool not installed (run 'pip install $tool' or 'make install-dev')"
    fi
done

# Summary
echo ""
echo "📊 Summary:"
echo "----------"
echo "Project structure and basic validation completed."
echo ""
echo "Next steps:"
echo "1. Install development dependencies: make install-dev"
echo "2. Run quality checks: make quality-check"
echo "3. Read documentation: docs/CODE_QUALITY.md"
echo "4. Follow development workflow in README.md"
echo ""
echo "For issues with package installation, see docs/CODE_QUALITY.md"
echo "for troubleshooting and manual validation options."