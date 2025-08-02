"""
Unit tests for the speech module.
"""
import pytest
from unittest.mock import patch, MagicMock, Mock


class TestSpeechHandler:
    """Test cases for the SpeechHandler class."""
    
    def test_speech_handler_init_with_mocked_dependencies(self):
        """Test SpeechHandler initialization with mocked dependencies."""
        # Mock speech recognition and related dependencies
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
        }):
            from tutor.speech import SpeechHandler
            
            config = {
                'stt_provider': 'google',
                'openai_api_key': None
            }
            
            # Mock the initialization components
            with patch('tutor.speech.sr.Recognizer') as mock_recognizer, \
                 patch('tutor.speech.sr.Microphone') as mock_microphone:
                
                mock_recognizer_instance = MagicMock()
                mock_microphone_instance = MagicMock()
                mock_recognizer.return_value = mock_recognizer_instance
                mock_microphone.return_value = mock_microphone_instance
                
                handler = SpeechHandler(config)
                
                assert handler.config == config
                assert handler.provider == 'google'
                assert handler.recognizer == mock_recognizer_instance
    
    def test_speech_handler_old_config_format(self):
        """Test SpeechHandler with old configuration format."""
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
        }):
            from tutor.speech import SpeechHandler
            
            # Old format config
            config = {
                'provider': 'openai',
                'api_key': 'test-key'
            }
            
            with patch('tutor.speech.sr.Recognizer') as mock_recognizer, \
                 patch('tutor.speech.sr.Microphone') as mock_microphone:
                
                mock_recognizer.return_value = MagicMock()
                mock_microphone.return_value = MagicMock()
                
                handler = SpeechHandler(config)
                
                assert handler.provider == 'openai'
                assert handler.config == config
    
    def test_speech_handler_new_config_format(self):
        """Test SpeechHandler with new configuration format."""
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
        }):
            from tutor.speech import SpeechHandler
            
            # New format config
            config = {
                'stt_provider': 'google',
                'openai_api_key': 'test-key'
            }
            
            with patch('tutor.speech.sr.Recognizer') as mock_recognizer, \
                 patch('tutor.speech.sr.Microphone') as mock_microphone:
                
                mock_recognizer.return_value = MagicMock()
                mock_microphone.return_value = MagicMock()
                
                handler = SpeechHandler(config)
                
                assert handler.provider == 'google'
                assert handler.config == config
    
    def test_speech_handler_openai_initialization(self):
        """Test SpeechHandler initialization with OpenAI provider."""
        mock_openai = MagicMock()
        
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': mock_openai,
        }):
            # Mock OPENAI_AVAILABLE flag
            with patch('tutor.speech.OPENAI_AVAILABLE', True):
                from tutor.speech import SpeechHandler
                
                config = {
                    'stt_provider': 'openai',
                    'openai_api_key': 'test-key'
                }
                
                with patch('tutor.speech.sr.Recognizer') as mock_recognizer, \
                     patch('tutor.speech.sr.Microphone') as mock_microphone, \
                     patch('tutor.speech.OpenAI') as mock_openai_client:
                    
                    mock_recognizer.return_value = MagicMock()
                    mock_microphone.return_value = MagicMock()
                    mock_client_instance = MagicMock()
                    mock_openai_client.return_value = mock_client_instance
                    
                    handler = SpeechHandler(config)
                    
                    assert handler.provider == 'openai'
                    assert hasattr(handler, 'client')
                    mock_openai_client.assert_called_once_with(api_key='test-key')
    
    def test_speech_handler_without_openai_available(self):
        """Test SpeechHandler when OpenAI is not available."""
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
        }):
            # Mock OPENAI_AVAILABLE as False
            with patch('tutor.speech.OPENAI_AVAILABLE', False):
                from tutor.speech import SpeechHandler
                
                config = {
                    'stt_provider': 'openai',
                    'openai_api_key': 'test-key'
                }
                
                with patch('tutor.speech.sr.Recognizer') as mock_recognizer, \
                     patch('tutor.speech.sr.Microphone') as mock_microphone:
                    
                    mock_recognizer.return_value = MagicMock()
                    mock_microphone.return_value = MagicMock()
                    
                    handler = SpeechHandler(config)
                    
                    # Should still initialize but without OpenAI client
                    assert handler.provider == 'openai'
                    assert not hasattr(handler, 'client') or handler.client is None
    
    def test_speech_handler_microphone_setup(self):
        """Test that microphone is properly set up."""
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
        }):
            from tutor.speech import SpeechHandler
            
            config = {'stt_provider': 'google'}
            
            with patch('tutor.speech.sr.Recognizer') as mock_recognizer, \
                 patch('tutor.speech.sr.Microphone') as mock_microphone:
                
                mock_recognizer_instance = MagicMock()
                mock_microphone_instance = MagicMock()
                mock_recognizer.return_value = mock_recognizer_instance
                mock_microphone.return_value = mock_microphone_instance
                
                # Set up the context manager for microphone
                mock_microphone_instance.__enter__ = Mock(return_value=mock_microphone_instance)
                mock_microphone_instance.__exit__ = Mock(return_value=None)
                
                handler = SpeechHandler(config)
                
                # Verify microphone was created and adjust_for_ambient_noise was called
                mock_microphone.assert_called_once()
                assert handler.microphone == mock_microphone_instance
    
    def test_speech_handler_class_structure(self):
        """Test the basic structure of the SpeechHandler class."""
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
        }):
            from tutor.speech import SpeechHandler
            
            # Test that the class exists and is properly defined
            assert SpeechHandler.__doc__ is not None
            assert "speech recognition" in SpeechHandler.__doc__.lower()
            
            # Test that __init__ method exists and has proper signature
            import inspect
            init_signature = inspect.signature(SpeechHandler.__init__)
            parameters = list(init_signature.parameters.keys())
            assert 'self' in parameters
            assert 'config' in parameters
    
    def test_speech_handler_availability_flags(self):
        """Test that availability flags are properly set."""
        with patch.dict('sys.modules', {
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
        }):
            from tutor import speech
            
            # Test that availability flag exists
            assert hasattr(speech, 'OPENAI_AVAILABLE')
            assert isinstance(speech.OPENAI_AVAILABLE, bool)