#!/bin/bash

# Test script to validate requirements.txt
# This script creates a temporary environment and tests if all requirements install correctly

echo "🧪 Testing requirements.txt installation..."

# Create temporary test environment
TEMP_ENV="temp-language-tutor-test"

# Add conda to PATH
export PATH="/opt/homebrew/anaconda3/bin:$PATH"
source /opt/homebrew/anaconda3/etc/profile.d/conda.sh

echo "📦 Creating temporary test environment..."
conda create -n $TEMP_ENV python=3.10 -y -q

echo "🔧 Activating test environment..."
conda activate $TEMP_ENV

echo "📥 Installing requirements from requirements.txt..."
if pip install -r requirements.txt -q; then
    echo "✅ All requirements installed successfully!"
    
    # Test critical imports
    echo "🧪 Testing critical imports..."
    python -c "
import openai
import langchain
import streamlit
import speech_recognition
import numpy
import pandas
import ipykernel
import IPython
print('✅ All imports successful!')
"
    
    if [ $? -eq 0 ]; then
        echo "🎉 Requirements.txt validation passed!"
        RESULT=0
    else
        echo "❌ Import test failed!"
        RESULT=1
    fi
else
    echo "❌ Requirements installation failed!"
    RESULT=1
fi

# Cleanup
echo "🧹 Cleaning up test environment..."
conda deactivate
conda env remove -n $TEMP_ENV -y -q

if [ $RESULT -eq 0 ]; then
    echo "✅ Requirements.txt is valid and complete!"
else
    echo "❌ Requirements.txt validation failed!"
fi

exit $RESULT
