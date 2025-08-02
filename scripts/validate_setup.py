#!/usr/bin/env python3
"""
Setup validation script for AI Language Tutor
Tests both OpenAI and Ollama configurations
"""

import os
import sys
from pathlib import Path

# Add src to path
script_path = Path(__file__).parent.parent
sys.path.insert(0, str(script_path / 'src'))
# Also add the parent directory to help with relative imports
sys.path.insert(0, str(script_path))

def test_imports():
    """Test that all required packages can be imported."""
    print("🔍 Testing package imports...")
    
    try:
        import langchain
        print(f"✅ LangChain: {langchain.__version__}")
    except ImportError as e:
        print(f"❌ LangChain import error: {e}")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError:
        print("⚠️ OpenAI package not available (optional)")
    
    try:
        import ollama
        print(f"✅ Ollama client available")
    except ImportError:
        print("⚠️ Ollama package not available (optional)")
    
    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import error: {e}")
        return False
    
    try:
        import speech_recognition
        print(f"✅ SpeechRecognition available")
    except ImportError:
        print("⚠️ SpeechRecognition not available (optional for voice features)")
    
    return True

def test_environment():
    """Test environment configuration."""
    print("\n🔍 Testing environment configuration...")
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Load .env if python-dotenv is available
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ .env file loaded")
        except ImportError:
            print("⚠️ python-dotenv not available, using system environment")
    else:
        print("⚠️ .env file not found, using system environment")
    
    # Check provider configuration
    provider = os.getenv('MODEL_PROVIDER', 'openai')
    print(f"🤖 Model Provider: {provider}")
    
    return True

def test_openai():
    """Test OpenAI configuration."""
    print("\n🔍 Testing OpenAI configuration...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️ OPENAI_API_KEY not found in environment")
        return False
    
    if api_key.startswith('sk-'):
        print("✅ OpenAI API key format looks correct")
    else:
        print("⚠️ OpenAI API key format might be incorrect")
    
    try:
        from src.utils.config import Config
        os.environ['MODEL_PROVIDER'] = 'openai'
        
        config = Config()
        config.validate_config()
        print("✅ OpenAI configuration valid")
        
        # Test AI Tutor initialization
        from src.tutor.ai_tutor import AITutor
        tutor = AITutor.from_config(config)
        print("✅ OpenAI AITutor initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI configuration error: {e}")
        return False

def test_ollama():
    """Test Ollama configuration."""
    print("\n🔍 Testing Ollama configuration...")
    
    try:
        import requests
        
        # Check if Ollama is running
        ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            print("✅ Ollama server is running")
            
            # List available models
            models = response.json().get('models', [])
            if models:
                print(f"✅ Available models: {[m['name'] for m in models]}")
                
                # Test configuration
                os.environ['MODEL_PROVIDER'] = 'ollama'
                os.environ['OLLAMA_MODEL'] = models[0]['name']
                
                from src.utils.config import Config
                from src.tutor.ai_tutor import AITutor
                
                config = Config()
                config.validate_config()
                print("✅ Ollama configuration valid")
                
                # Test AI Tutor initialization
                tutor = AITutor.from_config(config)
                print("✅ Ollama AITutor initialized successfully")
                
                return True
            else:
                print("⚠️ No Ollama models found. Try: ollama pull llama3.1")
                return False
        else:
            print(f"❌ Ollama server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server")
        print("💡 Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Ollama test error: {e}")
        return False

def test_database():
    """Test database functionality."""
    print("\n🔍 Testing database functionality...")
    
    try:
        from src.utils.database import ProgressTracker
        
        tracker = ProgressTracker()
        print("✅ Database connection established")
        
        # Test basic operations
        session_id = tracker.start_session("test_user", "Spanish", "conversation", "beginner")
        print(f"✅ Session created: {session_id}")
        
        tracker.log_interaction(session_id, "Hello", "Hola", 90)
        print("✅ Interaction logged")
        
        progress = tracker.get_user_progress("test_user")
        print(f"✅ Progress retrieved: {len(progress)} sessions")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def test_speech():
    """Test speech functionality."""
    print("\n🔍 Testing speech functionality...")
    
    try:
        from src.tutor.speech import SpeechHandler
        
        # Test with API key if available
        # Test the new configuration format
        api_key = os.getenv('OPENAI_API_KEY')
        speech_config = {
            'openai_api_key': api_key,
            'stt_provider': 'openai' if api_key else 'google',
            'tts_provider': 'openai' if api_key else None
        }
        
        handler = SpeechHandler(speech_config)
        print("✅ Speech handler initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Speech test error: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🎓 AI Language Tutor - Setup Validation")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment", test_environment),
        ("OpenAI", test_openai),
        ("Ollama", test_ollama),
        ("Database", test_database),
        ("Speech", test_speech),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All tests passed! Your setup is ready to go!")
    elif results.get("Package Imports") and (results.get("OpenAI") or results.get("Ollama")):
        print("✅ Basic functionality available. Some optional features may not work.")
    else:
        print("⚠️ Some critical tests failed. Check the errors above.")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
