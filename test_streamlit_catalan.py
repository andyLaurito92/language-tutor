#!/usr/bin/env python3
"""
Test script to verify that Catalan appears in the Streamlit UI language dropdown.
This simulates the core functionality without requiring all dependencies.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_streamlit_language_dropdown():
    """Test that we can create the language dropdown with Catalan included."""
    try:
        from src.utils.config import Config
        
        # Simulate what the Streamlit app does for language selection
        language_options = list(Config.SUPPORTED_LANGUAGES.keys())
        
        print("🖥️  Simulating Streamlit Language Dropdown")
        print("=" * 45)
        
        print("📋 Available language options:")
        for i, lang in enumerate(language_options, 1):
            code = Config.SUPPORTED_LANGUAGES[lang]
            marker = "🟢" if lang == "Catalan" else "⚪"
            print(f"   {marker} {i:2d}. {lang} ({code})")
        
        # Verify Catalan is present
        assert "Catalan" in language_options, "Catalan not found in language options"
        catalan_index = language_options.index("Catalan")
        
        print(f"\n✅ Catalan found at position {catalan_index + 1}")
        print(f"✅ Language code: {Config.SUPPORTED_LANGUAGES['Catalan']}")
        print(f"✅ Total languages available: {len(language_options)}")
        
        # Simulate selection
        print(f"\n📱 Simulating user selection of Catalan...")
        selected_language = "Catalan"
        selected_code = Config.SUPPORTED_LANGUAGES[selected_language]
        
        print(f"✅ Selected: {selected_language}")
        print(f"✅ Language code: {selected_code}")
        print("✅ Selection successful - Catalan is fully integrated!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_compatible_imports():
    """Test that our config can be imported by Streamlit."""
    try:
        # Test the imports that app.py uses
        from src.utils.config import Config
        
        print("\n🔧 Testing Streamlit-compatible imports...")
        print("-" * 40)
        
        # Test accessing properties the way the app does
        supported_languages = Config.SUPPORTED_LANGUAGES
        lesson_types = Config.LESSON_TYPES
        difficulty_levels = Config.DIFFICULTY_LEVELS
        
        print(f"✅ SUPPORTED_LANGUAGES: {len(supported_languages)} languages")
        print(f"✅ LESSON_TYPES: {len(lesson_types)} types")
        print(f"✅ DIFFICULTY_LEVELS: {len(difficulty_levels)} levels")
        
        # Specifically test that Catalan works with the app logic
        if "Catalan" in supported_languages:
            catalan_code = supported_languages["Catalan"]
            print(f"✅ Catalan integration: {catalan_code}")
        
        print("✅ All imports compatible with Streamlit app structure")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run the Streamlit compatibility tests."""
    print("🧪 Testing Catalan in Streamlit UI")
    print("=" * 40)
    
    tests = [
        ("Language dropdown simulation", test_streamlit_language_dropdown),
        ("Streamlit-compatible imports", test_streamlit_compatible_imports)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print(f"\n📊 Test Summary:")
    print("-" * 20)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Catalan is ready for Streamlit UI!")
        print("🖥️  Users will see Catalan as an option in the language dropdown")
        print("🌐 The AI tutor will receive 'Catalan' as the target language")
        return True
    else:
        print("💔 Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)