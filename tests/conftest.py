"""
Test fixtures and configuration for the language-tutor test suite.
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add src to Python path so tests can import modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        'MODEL_PROVIDER': 'ollama',
        'OLLAMA_BASE_URL': 'http://localhost:11434',
        'OLLAMA_MODEL': 'llama3.1',
        'STT_PROVIDER': 'google'
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv('MODEL_PROVIDER', 'ollama')
    monkeypatch.setenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    monkeypatch.setenv('OLLAMA_MODEL', 'llama3.1')
    monkeypatch.setenv('STT_PROVIDER', 'google')


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'user_id': 'test_user_123',
        'language': 'Spanish',
        'difficulty': 'Intermediate',
        'lesson_type': 'Conversation Practice'
    }


@pytest.fixture
def mock_database_path(temp_dir):
    """Provide a temporary database path for testing."""
    return os.path.join(temp_dir, 'test_progress.db')