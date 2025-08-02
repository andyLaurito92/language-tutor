# Standard library imports
import os
from typing import Any, Dict

# Third-party imports
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for the AI Tutor application."""
    
    # Model Provider Configuration
    MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'ollama')  # 'openai' or 'ollama'
    
    # OpenAI Configuration (optional)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    WHISPER_MODEL = "whisper-1"
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1')  # Default Ollama model
    
    # Speech-to-text options (when not using OpenAI Whisper)
    STT_PROVIDER = os.getenv('STT_PROVIDER', 'google')  # 'google', 'offline', 'openai'
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it', 
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Chinese': 'zh',
        'Catalan': 'ca',
        'English': 'en'
    }
    
    # Lesson types
    LESSON_TYPES = [
        'Conversation Practice',
        'Grammar Lessons',
        'Vocabulary Building',
        'Pronunciation Practice',
        'Reading Comprehension',
        'Writing Practice'
    ]
    
    # Difficulty levels
    DIFFICULTY_LEVELS = [
        'Beginner',
        'Intermediate',
        'Advanced'
    ]
    
    # Available Ollama models for language learning
    RECOMMENDED_OLLAMA_MODELS = [
        'llama3.2',      # Meta's Llama 3.1 (recommended)
        'llama3.1:70b',  # Larger version (if you have resources)
        'llama3',        # Meta's Llama 3
        'mistral',       # Mistral AI model
        'codellama',     # Code-focused but good for structured responses
        'gemma',         # Google's Gemma model
        'qwen2',         # Alibaba's Qwen2 model (good for multilingual)
    ]
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing or invalid
        """
        if cls.MODEL_PROVIDER == 'openai':
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY environment variable is required when using OpenAI")
        elif cls.MODEL_PROVIDER == 'ollama':
            # For Ollama, we just need to verify the base URL format
            if not cls.OLLAMA_BASE_URL.startswith('http'):
                raise ValueError("OLLAMA_BASE_URL must be a valid HTTP URL")
        else:
            raise ValueError(f"Invalid MODEL_PROVIDER: {cls.MODEL_PROVIDER}. Must be 'openai' or 'ollama'")
        return True
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """
        Get the appropriate model configuration based on provider.
        
        Returns:
            Dictionary containing model configuration with keys:
            - provider: The model provider ('openai' or 'ollama')
            - model: The model name to use
            - Additional provider-specific keys (api_key, base_url)
            
        Raises:
            ValueError: If the model provider is not supported
        """
        if cls.MODEL_PROVIDER == 'openai':
            return {
                'provider': 'openai',
                'model': cls.OPENAI_MODEL,
                'api_key': cls.OPENAI_API_KEY
            }
        elif cls.MODEL_PROVIDER == 'ollama':
            return {
                'provider': 'ollama',
                'model': cls.OLLAMA_MODEL,
                'base_url': cls.OLLAMA_BASE_URL
            }
        else:
            raise ValueError(f"Unsupported model provider: {cls.MODEL_PROVIDER}")
