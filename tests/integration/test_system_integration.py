"""
Integration tests for the language-tutor system.
"""
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock


class TestSystemIntegration:
    """Integration tests for system components working together."""
    
    def test_config_and_database_integration(self, temp_dir):
        """Test that Config and Database components work together."""
        # Mock dotenv to avoid dependency issues
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=MagicMock())}):
            from utils.config import Config
            from utils.database import ProgressTracker
            
            # Test that config languages can be used with database
            db_path = os.path.join(temp_dir, 'integration_test.db')
            tracker = ProgressTracker(db_path)
            
            # Test using a supported language from config
            supported_languages = list(Config.SUPPORTED_LANGUAGES.keys())
            test_language = supported_languages[0] if supported_languages else 'Spanish'
            
            session_id = tracker.start_session(
                user_id='integration_test_user',
                language=test_language,
                lesson_type=Config.LESSON_TYPES[0],
                difficulty=Config.DIFFICULTY_LEVELS[0]
            )
            
            assert session_id > 0
            tracker.end_session(session_id, score=85)
            
            progress = tracker.get_user_progress('integration_test_user')
            assert progress['total_sessions'] == 1
            assert progress['average_score'] == 85
    
    def test_config_and_lessons_integration(self, temp_dir):
        """Test that Config and LessonManager work together."""
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=MagicMock())}):
            from utils.config import Config
            from tutor.lessons import LessonManager
            
            # Test lesson manager with config-based paths
            lessons_path = os.path.join(temp_dir, 'lessons')
            manager = LessonManager(lessons_path)
            
            # Test that lesson types from config are available
            assert len(Config.LESSON_TYPES) > 0
            assert len(Config.DIFFICULTY_LEVELS) > 0
            assert len(Config.SUPPORTED_LANGUAGES) > 0
            
            # Test lesson manager initialization
            assert os.path.exists(lessons_path)
            assert manager.lessons_path == lessons_path
    
    def test_database_and_lessons_integration(self, temp_dir):
        """Test that Database and LessonManager work together."""
        from utils.database import ProgressTracker
        from tutor.lessons import LessonManager
        
        # Set up both components
        db_path = os.path.join(temp_dir, 'integration.db')
        lessons_path = os.path.join(temp_dir, 'lessons')
        
        tracker = ProgressTracker(db_path)
        manager = LessonManager(lessons_path)
        
        # Test that we can track progress for lessons
        session_id = tracker.start_session(
            user_id='lesson_test_user',
            language='Spanish',
            lesson_type='Conversation Practice',
            difficulty='Beginner'
        )
        
        # Log some interactions (simulating lesson activity)
        tracker.log_interaction(
            session_id,
            "Hola, ¿cómo estás?",
            "¡Muy bien! Your pronunciation is good.",
            feedback_score=4
        )
        
        tracker.end_session(session_id, score=78)
        
        # Verify the integration worked
        progress = tracker.get_user_progress('lesson_test_user')
        assert progress['total_sessions'] == 1
        assert len(progress['sessions']) == 1
        assert progress['sessions'][0]['lesson_type'] == 'Conversation Practice'
    
    @patch.dict('sys.modules', {
        'speech_recognition': MagicMock(),
        'streamlit': MagicMock(),
        'openai': MagicMock(),
        'langchain.memory': MagicMock(),
        'langchain_core.prompts': MagicMock(),
        'langchain.chains': MagicMock(),
        'langchain_core.messages': MagicMock(),
        'langchain_openai': MagicMock(),
        'langchain_ollama': MagicMock(),  
        'langchain_community.llms': MagicMock(),
        'langchain_community.chat_models': MagicMock(),
    })
    def test_ai_tutor_and_speech_integration(self):
        """Test that AITutor and SpeechHandler can work together."""
        from tutor.ai_tutor import AITutor
        from tutor.speech import SpeechHandler
        
        # Set up both components
        model_config = {
            'provider': 'ollama',
            'model': 'llama3.1',
            'base_url': 'http://localhost:11434'
        }
        
        speech_config = {
            'stt_provider': 'google'
        }
        
        with patch('tutor.ai_tutor.AITutor._initialize_llm', return_value=MagicMock()), \
             patch('tutor.speech.sr.Recognizer', return_value=MagicMock()), \
             patch('tutor.speech.sr.Microphone', return_value=MagicMock()):
            
            tutor = AITutor(model_config)
            speech_handler = SpeechHandler(speech_config)
            
            # Test that both components are properly initialized
            assert tutor.model_config == model_config
            assert speech_handler.config == speech_config
            
            # Test that they have compatible interfaces
            assert hasattr(tutor, 'current_language')
            assert hasattr(speech_handler, 'provider')
    
    def test_full_system_simulation(self, temp_dir):
        """Test a complete simulation of system components working together."""
        # Mock external dependencies
        with patch.dict('sys.modules', {
            'dotenv': MagicMock(load_dotenv=MagicMock()),
            'speech_recognition': MagicMock(),
            'streamlit': MagicMock(),
            'openai': MagicMock(),
            'langchain.memory': MagicMock(),
            'langchain_core.prompts': MagicMock(),
            'langchain.chains': MagicMock(),
            'langchain_core.messages': MagicMock(),
            'langchain_openai': MagicMock(),
            'langchain_ollama': MagicMock(),
            'langchain_community.llms': MagicMock(),
            'langchain_community.chat_models': MagicMock(),
        }):
            from utils.config import Config
            from utils.database import ProgressTracker
            from tutor.lessons import LessonManager
            from tutor.ai_tutor import AITutor
            from tutor.speech import SpeechHandler
            
            # Set up all components
            db_path = os.path.join(temp_dir, 'full_system.db')
            lessons_path = os.path.join(temp_dir, 'lessons')
            
            tracker = ProgressTracker(db_path)
            manager = LessonManager(lessons_path)
            
            model_config = Config.get_model_config()
            
            with patch('tutor.ai_tutor.AITutor._initialize_llm', return_value=MagicMock()), \
                 patch('tutor.speech.sr.Recognizer', return_value=MagicMock()), \
                 patch('tutor.speech.sr.Microphone', return_value=MagicMock()):
                
                tutor = AITutor(model_config)
                speech_handler = SpeechHandler({'stt_provider': 'google'})
                
                # Simulate a learning session
                session_id = tracker.start_session(
                    user_id='full_system_user',
                    language='Catalan',  # Test our Catalan support
                    lesson_type='Conversation Practice',
                    difficulty='Intermediate'
                )
                
                # Set tutor context
                tutor.current_language = 'Catalan'
                tutor.current_difficulty = 'Intermediate'
                tutor.current_lesson_type = 'Conversation Practice'
                
                # Simulate some interactions
                interactions = [
                    ("Bon dia!", "Bon dia! Com estàs avui?"),
                    ("Estic molt bé, gràcies.", "Perfecte! Your accent is improving."),
                ]
                
                for user_input, ai_response in interactions:
                    tracker.log_interaction(session_id, user_input, ai_response, feedback_score=4)
                
                tracker.end_session(session_id, score=88)
                
                # Verify the full system worked
                progress = tracker.get_user_progress('full_system_user')
                assert progress['total_sessions'] == 1
                assert progress['average_score'] == 88
                assert progress['sessions'][0]['language'] == 'Catalan'
                
                # Verify all components are properly set up
                assert 'Catalan' in Config.SUPPORTED_LANGUAGES
                assert tutor.current_language == 'Catalan'
                assert os.path.exists(lessons_path)
                assert os.path.exists(db_path)