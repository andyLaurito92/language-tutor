#!/bin/bash

# AI Language Tutor Setup Script

echo "🎓 Setting up AI Language Tutor..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
echo "📁 Creating data directories..."
mkdir -p data/lessons
mkdir -p data

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file and add your OpenAI API key:"
    echo "   OPENAI_API_KEY=your_actual_api_key_here"
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Set your OpenAI API key in the .env file"
echo "  3. Run the app: streamlit run app.py"
echo ""
echo "🚀 Happy learning!"
