#!/bin/bash

# Conda Environment Setup Script for AI Language Tutor
# This script sets up and activates the conda environment

echo "🚀 Setting up AI Language Tutor environment..."

# Add conda to PATH
export PATH="/opt/homebrew/anaconda3/bin:$PATH"

# Load conda configuration
source /opt/homebrew/anaconda3/etc/profile.d/conda.sh

# Activate the environment
conda activate language-tutor

# Check if activation was successful
if [[ "$CONDA_DEFAULT_ENV" == "language-tutor" ]]; then
    echo "✅ Successfully activated 'language-tutor' conda environment"
    echo "🐍 Python version: $(python --version)"
    echo "📦 Environment location: $CONDA_PREFIX"
    echo ""
    echo "🎯 You can now run:"
    echo "   • streamlit run app.py           (Web interface)"
    echo "   • python cli_tutor.py           (Command line interface)"
    echo "   • jupyter notebook               (Open the example notebook)"
    echo "   • code example_usage.ipynb       (Open notebook in VS Code)"
    echo ""
    echo "📝 Don't forget to set your OPENAI_API_KEY in .env file!"
    
    # Start a new shell with the environment activated
    exec bash
else
    echo "❌ Failed to activate conda environment"
    echo "Please check your conda installation and try again"
    exit 1
fi
