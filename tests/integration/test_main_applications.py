"""
Integration tests for main application modules.
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, Mock


class TestMainApplications:
    """Test the main application entry points."""
    
    def test_app_py_imports(self):
        """Test that app.py can be imported without errors."""
        # Mock all the heavy dependencies
        mock_modules = {
            'streamlit': MagicMock(),
            'dotenv': MagicMock(load_dotenv=MagicMock()),
            'speech_recognition': MagicMock(),
            'openai': MagicMock(),
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }
        
        with patch.dict('sys.modules', mock_modules):
            # Mock streamlit components
            mock_st = mock_modules['streamlit']
            mock_st.set_page_config = MagicMock()
            mock_st.title = MagicMock()
            mock_st.sidebar = MagicMock()
            mock_st.selectbox = MagicMock()
            mock_st.button = MagicMock()
            mock_st.write = MagicMock()
            mock_st.success = MagicMock()
            mock_st.error = MagicMock()
            mock_st.warning = MagicMock()
            mock_st.info = MagicMock()
            
            # Try importing app.py
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("app", "app.py")
                app_module = importlib.util.module_from_spec(spec)
                
                # Mock the AI tutor and speech initialization
                with patch('tutor.ai_tutor.AITutor') as mock_ai_tutor, \
                     patch('tutor.speech.SpeechHandler') as mock_speech, \
                     patch('utils.database.ProgressTracker') as mock_tracker:
                    
                    mock_ai_tutor.return_value = MagicMock()
                    mock_speech.return_value = MagicMock()
                    mock_tracker.return_value = MagicMock()
                    
                    spec.loader.exec_module(app_module)
                    
                    # Test that the app module was loaded successfully
                    assert app_module is not None
                    
            except Exception as e:
                pytest.fail(f"Failed to import app.py: {e}")
    
    def test_cli_tutor_imports(self):
        """Test that cli_tutor.py can be imported without errors."""
        mock_modules = {
            'dotenv': MagicMock(load_dotenv=MagicMock()),
            'speech_recognition': MagicMock(),
            'openai': MagicMock(),
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }
        
        with patch.dict('sys.modules', mock_modules):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("cli_tutor", "cli_tutor.py")
                cli_module = importlib.util.module_from_spec(spec)
                
                # Mock the dependencies
                with patch('tutor.ai_tutor.AITutor') as mock_ai_tutor, \
                     patch('tutor.speech.SpeechHandler') as mock_speech, \
                     patch('utils.database.ProgressTracker') as mock_tracker:
                    
                    mock_ai_tutor.return_value = MagicMock()
                    mock_speech.return_value = MagicMock()  
                    mock_tracker.return_value = MagicMock()
                    
                    # Mock input/output functions to avoid interactive issues
                    with patch('builtins.input', return_value='quit'), \
                         patch('builtins.print'):
                        
                        spec.loader.exec_module(cli_module)
                        
                        # Test that the CLI module was loaded successfully
                        assert cli_module is not None
                        
            except Exception as e:
                pytest.fail(f"Failed to import cli_tutor.py: {e}")
    
    def test_cli_tutor_has_main_function(self):
        """Test that cli_tutor.py has a main function."""
        mock_modules = {
            'dotenv': MagicMock(load_dotenv=MagicMock()),
            'speech_recognition': MagicMock(),
            'openai': MagicMock(),
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }
        
        with patch.dict('sys.modules', mock_modules):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("cli_tutor", "cli_tutor.py")
                cli_module = importlib.util.module_from_spec(spec)
                
                with patch('tutor.ai_tutor.AITutor'), \
                     patch('tutor.speech.SpeechHandler'), \
                     patch('utils.database.ProgressTracker'), \
                     patch('builtins.input', return_value='quit'), \
                     patch('builtins.print'):
                    
                    spec.loader.exec_module(cli_module)
                    
                    # Check if main function exists
                    assert hasattr(cli_module, 'main') or 'main' in dir(cli_module)
                    
            except Exception as e:
                pytest.fail(f"Failed to check main function in cli_tutor.py: {e}")
    
    def test_demo_catalan_support_imports(self):
        """Test that demo_catalan_support.py can be imported."""
        mock_modules = {
            'dotenv': MagicMock(load_dotenv=MagicMock()),
            'speech_recognition': MagicMock(),
            'openai': MagicMock(),
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }
        
        with patch.dict('sys.modules', mock_modules):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("demo", "demo_catalan_support.py")
                demo_module = importlib.util.module_from_spec(spec)
                
                with patch('tutor.ai_tutor.AITutor'), \
                     patch('tutor.speech.SpeechHandler'), \
                     patch('utils.database.ProgressTracker'), \
                     patch('builtins.input', return_value='quit'), \
                     patch('builtins.print'):
                    
                    spec.loader.exec_module(demo_module)
                    
                    # Test that the demo module was loaded successfully
                    assert demo_module is not None
                    
            except Exception as e:
                pytest.fail(f"Failed to import demo_catalan_support.py: {e}")
    
    def test_application_structure_validation(self):
        """Test that application files have the expected structure."""
        # Test that key files exist
        assert os.path.exists('app.py'), "app.py should exist"
        assert os.path.exists('cli_tutor.py'), "cli_tutor.py should exist"
        assert os.path.exists('demo_catalan_support.py'), "demo_catalan_support.py should exist"
        
        # Test that files are not empty
        with open('app.py', 'r') as f:
            app_content = f.read()
            assert len(app_content) > 100, "app.py should have substantial content"
            assert 'streamlit' in app_content.lower(), "app.py should use streamlit"
        
        with open('cli_tutor.py', 'r') as f:
            cli_content = f.read()
            assert len(cli_content) > 100, "cli_tutor.py should have substantial content"
            assert 'def main' in cli_content or 'if __name__' in cli_content, "cli_tutor.py should have main entry point"
    
    def test_configuration_files_exist(self):
        """Test that configuration files exist and are properly structured."""
        # Test requirements files
        assert os.path.exists('requirements.txt'), "requirements.txt should exist"
        assert os.path.exists('requirements_no_audio.txt'), "requirements_no_audio.txt should exist"
        
        # Test environment example
        assert os.path.exists('.env.example'), ".env.example should exist"
        
        # Test README
        assert os.path.exists('README.md'), "README.md should exist"
        
        # Test gitignore
        assert os.path.exists('.gitignore'), ".gitignore should exist"
    
    def test_data_directory_structure(self):
        """Test that data directory exists and has expected structure."""
        assert os.path.exists('data'), "data directory should exist"
        
        # Check if it's a directory
        assert os.path.isdir('data'), "data should be a directory"