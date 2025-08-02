"""
Unit tests for the AI tutor module.
"""
import pytest
from unittest.mock import patch, MagicMock, Mock


class TestAITutor:
    """Test cases for the AITutor class."""
    
    def test_ai_tutor_init_with_mock_dependencies(self):
        """Test AITutor initialization with mocked dependencies."""
        # Mock all the langchain dependencies
        mock_memory = MagicMock()
        mock_llm = MagicMock()
        
        with patch.dict('sys.modules', {
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from tutor.ai_tutor import AITutor
            
            # Test with Ollama config
            model_config = {
                'provider': 'ollama',
                'model': 'llama3.1',
                'base_url': 'http://localhost:11434'
            }
            
            # Mock the _initialize_llm method
            with patch.object(AITutor, '_initialize_llm', return_value=mock_llm):
                tutor = AITutor(model_config)
                
                assert tutor.model_config == model_config
                assert tutor.llm == mock_llm
                assert tutor.current_language is None
                assert tutor.current_difficulty is None
                assert tutor.current_lesson_type is None
                assert isinstance(tutor.lesson_context, dict)
    
    def test_ai_tutor_attributes_exist(self):
        """Test that AITutor has expected attributes."""
        mock_llm = MagicMock()
        
        with patch.dict('sys.modules', {
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from tutor.ai_tutor import AITutor
            
            model_config = {'provider': 'ollama', 'model': 'test'}
            
            with patch.object(AITutor, '_initialize_llm', return_value=mock_llm):
                tutor = AITutor(model_config)
                
                # Test that expected attributes exist
                assert hasattr(tutor, 'model_config')
                assert hasattr(tutor, 'llm')
                assert hasattr(tutor, 'memory')
                assert hasattr(tutor, 'current_language')
                assert hasattr(tutor, 'current_difficulty')
                assert hasattr(tutor, 'current_lesson_type')
                assert hasattr(tutor, 'lesson_context')
    
    def test_ai_tutor_openai_config(self):
        """Test AITutor with OpenAI configuration."""
        mock_llm = MagicMock()
        
        with patch.dict('sys.modules', {
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from tutor.ai_tutor import AITutor
            
            # Test with OpenAI config
            model_config = {
                'provider': 'openai',
                'model': 'gpt-4',
                'api_key': 'test-key'
            }
            
            with patch.object(AITutor, '_initialize_llm', return_value=mock_llm):
                tutor = AITutor(model_config)
                
                assert tutor.model_config['provider'] == 'openai'
                assert tutor.model_config['model'] == 'gpt-4'
                assert tutor.model_config['api_key'] == 'test-key'
    
    def test_ai_tutor_import_availability_flags(self):
        """Test that import availability flags are properly set."""
        with patch.dict('sys.modules', {
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from tutor import ai_tutor
            
            # Test that availability flags exist
            assert hasattr(ai_tutor, 'OPENAI_AVAILABLE')
            assert hasattr(ai_tutor, 'OLLAMA_AVAILABLE')
            assert isinstance(ai_tutor.OPENAI_AVAILABLE, bool)
            assert isinstance(ai_tutor.OLLAMA_AVAILABLE, bool)
    
    def test_ai_tutor_lesson_context_initialization(self):
        """Test that lesson context is properly initialized."""
        mock_llm = MagicMock()
        
        with patch.dict('sys.modules', {
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from tutor.ai_tutor import AITutor
            
            model_config = {'provider': 'ollama', 'model': 'test'}
            
            with patch.object(AITutor, '_initialize_llm', return_value=mock_llm):
                tutor = AITutor(model_config)
                
                # Test lesson context initialization
                assert tutor.lesson_context == {}
                assert tutor.current_language is None
                assert tutor.current_difficulty is None
                assert tutor.current_lesson_type is None
    
    def test_ai_tutor_class_structure(self):
        """Test the basic structure of the AITutor class."""
        with patch.dict('sys.modules', {
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from tutor.ai_tutor import AITutor
            
            # Test that the class exists and is properly defined
            assert AITutor.__doc__ is not None
            assert "Core AI tutor class" in AITutor.__doc__
            
            # Test that __init__ method exists and has proper signature
            import inspect
            init_signature = inspect.signature(AITutor.__init__)
            parameters = list(init_signature.parameters.keys())
            assert 'self' in parameters
            assert 'model_config' in parameters