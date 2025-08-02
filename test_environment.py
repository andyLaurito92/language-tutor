#!/usr/bin/env python3
"""
AI Language Tutor - Environment Verification Script
This script tests that all dependencies are properly installed and accessible.
"""

import sys
import platform
from pathlib import Path

def test_imports():
    """Test all required imports"""
    tests = []
    
    # Core Python libraries
    try:
        import os
        tests.append(("✅", "os", "Built-in"))
    except ImportError as e:
        tests.append(("❌", "os", str(e)))
    
    # OpenAI
    try:
        import openai
        tests.append(("✅", "openai", openai.__version__))
    except ImportError as e:
        tests.append(("❌", "openai", str(e)))
    
    # LangChain
    try:
        import langchain
        tests.append(("✅", "langchain", langchain.__version__))
    except ImportError as e:
        tests.append(("❌", "langchain", str(e)))
    
    try:
        import langchain_openai
        tests.append(("✅", "langchain_openai", "Available"))
    except ImportError as e:
        tests.append(("❌", "langchain_openai", str(e)))
    
    try:
        import langchain_community
        tests.append(("✅", "langchain_community", "Available"))
    except ImportError as e:
        tests.append(("❌", "langchain_community", str(e)))
    
    # Streamlit
    try:
        import streamlit
        tests.append(("✅", "streamlit", streamlit.__version__))
    except ImportError as e:
        tests.append(("❌", "streamlit", str(e)))
    
    # Audio libraries
    try:
        import speech_recognition
        tests.append(("✅", "speech_recognition", speech_recognition.__version__))
    except ImportError as e:
        tests.append(("❌", "speech_recognition", str(e)))
    
    try:
        import pyaudio
        tests.append(("✅", "pyaudio", "Available"))
    except ImportError as e:
        tests.append(("❌", "pyaudio", str(e)))
    
    try:
        import pydub
        tests.append(("✅", "pydub", "Available"))
    except ImportError as e:
        tests.append(("❌", "pydub", str(e)))
    
    # Data libraries
    try:
        import numpy
        tests.append(("✅", "numpy", numpy.__version__))
    except ImportError as e:
        tests.append(("❌", "numpy", str(e)))
    
    try:
        import pandas
        tests.append(("✅", "pandas", pandas.__version__))
    except ImportError as e:
        tests.append(("❌", "pandas", str(e)))
    
    try:
        import matplotlib
        tests.append(("✅", "matplotlib", matplotlib.__version__))
    except ImportError as e:
        tests.append(("❌", "matplotlib", str(e)))
    
    # Environment
    try:
        from dotenv import load_dotenv
        tests.append(("✅", "python-dotenv", "Available"))
    except ImportError as e:
        tests.append(("❌", "python-dotenv", str(e)))
    
    # Jupyter
    try:
        import IPython
        tests.append(("✅", "IPython", IPython.__version__))
    except ImportError as e:
        tests.append(("❌", "IPython", str(e)))
    
    return tests

def check_environment_files():
    """Check if required files exist"""
    files = [
        "requirements.txt",
        ".env.example", 
        "app.py",
        "cli_tutor.py",
        "example_usage.ipynb",
        "src/tutor/ai_tutor.py",
        "src/tutor/lessons.py",
        "src/tutor/speech.py",
        "src/utils/config.py",
        "src/utils/database.py",
        "data/lessons/conversation_lessons.json",
        "data/lessons/grammar_lessons.json"
    ]
    
    results = []
    for file in files:
        path = Path(file)
        if path.exists():
            results.append(("✅", file, "Found"))
        else:
            results.append(("❌", file, "Missing"))
    
    return results

def main():
    print("🚀 AI Language Tutor - Environment Verification")
    print("=" * 50)
    
    # System information
    print(f"🖥️  Platform: {platform.platform()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {Path.cwd()}")
    print(f"📍 Python Executable: {sys.executable}")
    
    # Check if we're in a conda environment
    if 'CONDA_DEFAULT_ENV' in os.environ:
        print(f"🔧 Conda Environment: {os.environ['CONDA_DEFAULT_ENV']}")
    else:
        print("⚠️  No active conda environment detected")
    
    print("\n📦 Testing Dependencies:")
    print("-" * 30)
    
    # Test imports
    import_tests = test_imports()
    for status, name, version in import_tests:
        print(f"{status} {name:<20} {version}")
    
    print("\n📁 Checking Project Files:")
    print("-" * 30)
    
    # Check files
    file_tests = check_environment_files()
    for status, name, result in file_tests:
        print(f"{status} {name:<35} {result}")
    
    # Summary
    failed_imports = [t for t in import_tests if t[0] == "❌"]
    missing_files = [t for t in file_tests if t[0] == "❌"]
    
    print("\n📊 Summary:")
    print("-" * 20)
    
    if not failed_imports and not missing_files:
        print("🎉 All checks passed! Your environment is ready.")
        print("🎯 You can now run:")
        print("   • streamlit run app.py")
        print("   • python cli_tutor.py")
        print("   • Open example_usage.ipynb in VS Code")
    else:
        if failed_imports:
            print(f"❌ {len(failed_imports)} dependency issues found")
        if missing_files:
            print(f"❌ {len(missing_files)} missing files found")
        print("📝 Please check the installation guide in CONDA_SETUP.md")

if __name__ == "__main__":
    import os
    main()
