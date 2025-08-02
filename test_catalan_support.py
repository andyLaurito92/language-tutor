#!/usr/bin/env python3
"""
Test script to verify Catalan language support has been added correctly.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_catalan_in_supported_languages():
    """Test that Catalan is in the supported languages list."""
    try:
        from src.utils.config import Config
        
        # Check if Catalan is in supported languages
        assert 'Catalan' in Config.SUPPORTED_LANGUAGES, "Catalan not found in SUPPORTED_LANGUAGES"
        
        # Check if the language code is correct
        assert Config.SUPPORTED_LANGUAGES['Catalan'] == 'ca', f"Expected 'ca' for Catalan, got '{Config.SUPPORTED_LANGUAGES['Catalan']}'"
        
        print("✅ Catalan successfully added to supported languages")
        print(f"✅ Language code: {Config.SUPPORTED_LANGUAGES['Catalan']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Test failed: {e}")  
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_language_list():
    """Test that all expected languages are present."""
    try:
        from src.utils.config import Config
        
        expected_languages = [
            'Spanish', 'French', 'German', 'Italian', 'Portuguese',
            'Russian', 'Japanese', 'Korean', 'Chinese', 'Catalan', 'English'
        ]
        
        supported_languages = list(Config.SUPPORTED_LANGUAGES.keys())
        
        print(f"📋 Total supported languages: {len(supported_languages)}")
        print("📋 Supported languages:")
        for lang in supported_languages:
            code = Config.SUPPORTED_LANGUAGES[lang]
            print(f"   • {lang} ({code})")
        
        # Check that all expected languages are present
        missing_languages = set(expected_languages) - set(supported_languages)
        if missing_languages:
            print(f"❌ Missing languages: {missing_languages}")
            return False
            
        print("✅ All expected languages are supported")
        return True
        
    except Exception as e:
        print(f"❌ Error testing language list: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Catalan Language Support")
    print("=" * 40)
    
    tests = [
        ("Catalan in supported languages", test_catalan_in_supported_languages),
        ("Complete language list", test_language_list)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        print("-" * 25)
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
        print("🎉 All tests passed! Catalan support is working correctly.")
        return True
    else:
        print("💔 Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)