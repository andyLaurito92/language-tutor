#!/usr/bin/env python3
"""
Test module to verify Catalan language support has been added correctly.

This module tests that Catalan language support is properly configured
throughout the language tutor system.
"""

# Standard library imports
import os
import sys
import unittest

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class TestCatalanSupport(unittest.TestCase):
    """Test cases for Catalan language support."""

    def test_catalan_in_supported_languages(self) -> None:
        """Test that Catalan is in the supported languages list."""
        try:
            from src.utils.config import Config
            
            # Check if Catalan is in supported languages
            self.assertIn('Catalan', Config.SUPPORTED_LANGUAGES, 
                         "Catalan not found in SUPPORTED_LANGUAGES")
            
            # Check if the language code is correct
            expected_code = 'ca'
            actual_code = Config.SUPPORTED_LANGUAGES['Catalan']
            self.assertEqual(actual_code, expected_code, 
                           f"Expected '{expected_code}' for Catalan, got '{actual_code}'")
            
        except ImportError:
            self.skipTest("Config module not available - dependencies not installed")

    def test_language_list_completeness(self) -> None:
        """Test that all expected languages are present."""
        try:
            from src.utils.config import Config
            
            expected_languages = [
                'Spanish', 'French', 'German', 'Italian', 'Portuguese',
                'Russian', 'Japanese', 'Korean', 'Chinese', 'Catalan', 'English'
            ]
            
            supported_languages = list(Config.SUPPORTED_LANGUAGES.keys())
            
            # Check that all expected languages are present
            for lang in expected_languages:
                self.assertIn(lang, supported_languages, 
                            f"Language '{lang}' should be in supported languages")
            
            # Ensure we have a reasonable number of languages
            self.assertGreaterEqual(len(supported_languages), 10, 
                                  "Should support at least 10 languages")
            
            # Verify Catalan specifically
            self.assertIn('Catalan', supported_languages, 
                         "Catalan should be in supported languages")
            
        except ImportError:
            self.skipTest("Config module not available - dependencies not installed")

    def test_language_codes_format(self) -> None:
        """Test that all language codes follow ISO 639-1 format."""
        try:
            from src.utils.config import Config
            
            for language, code in Config.SUPPORTED_LANGUAGES.items():
                # Test code format
                self.assertEqual(len(code), 2, 
                               f"Language code for {language} should be 2 characters, got '{code}'")
                self.assertTrue(code.islower(), 
                              f"Language code for {language} should be lowercase, got '{code}'")
                self.assertTrue(code.isalpha(), 
                              f"Language code for {language} should be alphabetic, got '{code}'")
            
            # Test Catalan specifically
            catalan_code = Config.SUPPORTED_LANGUAGES.get('Catalan')
            self.assertEqual(catalan_code, 'ca', 
                           f"Catalan code should be 'ca', got '{catalan_code}'")
            
        except ImportError:
            self.skipTest("Config module not available - dependencies not installed")

    def tearDown(self) -> None:
        """Clean up after each test method."""
        pass


if __name__ == '__main__':
    unittest.main()