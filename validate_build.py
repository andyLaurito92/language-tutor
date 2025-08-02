#!/usr/bin/env python3
"""
Validation script for macOS app build.
This script tests that all necessary components are in place for building.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (missing)")
        return False

def check_python_module(module_name):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ Python module: {module_name}")
        return True
    except ImportError:
        print(f"❌ Python module: {module_name} (not available)")
        return False

def main():
    """Main validation function."""
    print("🔍 Validating macOS build setup...")
    print("=" * 40)
    
    # Check required files
    required_files = [
        ("launcher.py", "Launcher script"),
        ("ai-language-tutor.spec", "PyInstaller spec"),
        ("build_macos.sh", "Build script"),
        ("app.py", "Main application"),
        ("requirements_build.txt", "Build requirements"),
        ("BUILD_MACOS.md", "Build documentation"),
    ]
    
    files_ok = all(check_file_exists(file, desc) for file, desc in required_files)
    
    print("\n🐍 Python modules check...")
    print("-" * 30)
    
    # Check core modules
    core_modules = [
        "streamlit",
        "pathlib", 
        "subprocess",
        "webbrowser",
        "socket",
        "threading",
    ]
    
    modules_ok = all(check_python_module(module) for module in core_modules)
    
    print("\n🛠️ Optional build tools...")
    print("-" * 30)
    
    # Check build tools
    build_tools = [
        "pyinstaller",
    ]
    
    for tool in build_tools:
        check_python_module(tool)
    
    print("\n📋 macOS specific checks...")
    print("-" * 30)
    
    # Check if running on macOS
    if sys.platform == "darwin":
        print("✅ Running on macOS")
        
        # Check for Homebrew
        if os.system("which brew > /dev/null 2>&1") == 0:
            print("✅ Homebrew is installed")
            
            # Check for create-dmg
            if os.system("which create-dmg > /dev/null 2>&1") == 0:
                print("✅ create-dmg is available")
            else:
                print("⚠️  create-dmg not found (install with: brew install create-dmg)")
        else:
            print("⚠️  Homebrew not found (needed for create-dmg)")
    else:
        print(f"⚠️  Not running on macOS (current: {sys.platform})")
        print("   macOS apps can only be built on macOS systems")
    
    print("\n📊 Summary...")
    print("-" * 30)
    
    if files_ok and modules_ok:
        print("🎉 Build setup looks good!")
        print("\n📝 Next steps:")
        print("   1. Install missing optional dependencies if needed")
        print("   2. Run ./build_macos.sh to build the app")
        print("   3. Test the built app in the dist/ directory")
        return 0
    else:
        print("⚠️  Some issues found in build setup")
        print("\n🔧 To fix:")
        if not files_ok:
            print("   - Ensure all required files are present")
        if not modules_ok:
            print("   - Install missing Python modules: pip install -r requirements_build.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())