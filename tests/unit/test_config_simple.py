"""
Simple unit tests for the configuration module that work without dependencies.
"""
import pytest
import os
import sys
from unittest.mock import patch, MagicMock


def mock_load_dotenv():
    """Mock function for load_dotenv."""
    pass


class TestConfigSimple:
    """Simple test cases for the Config class."""
    
    def test_config_import_and_basic_structure(self):
        """Test that we can import config and it has expected structure."""
        # Mock the dotenv import
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load_dotenv)}):
            from utils.config import Config
            
            # Test that basic attributes exist
            assert hasattr(Config, 'SUPPORTED_LANGUAGES')
            assert hasattr(Config, 'LESSON_TYPES')
            assert hasattr(Config, 'DIFFICULTY_LEVELS')
            assert hasattr(Config, 'MODEL_PROVIDER')
    
    def test_catalan_support(self):
        """Test that Catalan is properly supported."""
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load_dotenv)}):
            from utils.config import Config
            
            # Test Catalan is in supported languages
            assert 'Catalan' in Config.SUPPORTED_LANGUAGES
            assert Config.SUPPORTED_LANGUAGES['Catalan'] == 'ca'
    
    def test_supported_languages_structure(self):
        """Test the structure of supported languages."""
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load_dotenv)}):
            from utils.config import Config
            
            # Test that we have expected languages
            expected_languages = ['Spanish', 'French', 'German', 'Italian', 'English', 'Catalan']
            
            for lang in expected_languages:
                assert lang in Config.SUPPORTED_LANGUAGES
                assert isinstance(Config.SUPPORTED_LANGUAGES[lang], str)
                assert len(Config.SUPPORTED_LANGUAGES[lang]) == 2  # Language codes are 2 chars
    
    def test_lesson_types_structure(self):
        """Test the structure of lesson types."""
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load_dotenv)}):
            from utils.config import Config
            
            assert isinstance(Config.LESSON_TYPES, list)
            assert len(Config.LESSON_TYPES) > 0
            
            # Test some expected lesson types
            expected_types = ['Conversation Practice', 'Grammar Lessons', 'Vocabulary Building']
            for lesson_type in expected_types:
                assert lesson_type in Config.LESSON_TYPES
    
    def test_difficulty_levels_structure(self):
        """Test the structure of difficulty levels."""
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load_dotenv)}):
            from utils.config import Config
            
            assert isinstance(Config.DIFFICULTY_LEVELS, list)
            expected_levels = ['Beginner', 'Intermediate', 'Advanced']
            assert Config.DIFFICULTY_LEVELS == expected_levels
    
    def test_config_methods_exist(self):
        """Test that expected methods exist on Config class."""
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load_dotenv)}):
            from utils.config import Config
            
            # Test that methods exist
            assert hasattr(Config, 'validate_config')
            assert hasattr(Config, 'get_model_config')
            assert callable(Config.validate_config)
            assert callable(Config.get_model_config)