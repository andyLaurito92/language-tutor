# Copilot Instructions for Language Tutor

This document provides comprehensive guidelines for developing, contributing to, and maintaining the AI Language Tutor project. Please read this document carefully before making any contributions.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Development Workflow](#development-workflow)
3. [Branch Naming Conventions](#branch-naming-conventions)
4. [Code Style and Standards](#code-style-and-standards)
5. [File Organization](#file-organization)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Standards](#documentation-standards)
8. [Pull Request Guidelines](#pull-request-guidelines)
9. [Issue Management](#issue-management)
10. [Security Considerations](#security-considerations)
11. [Build and Deployment](#build-and-deployment)
12. [Troubleshooting](#troubleshooting)

## Project Overview

The AI Language Tutor is a Python-based application that combines LangChain, OpenAI's GPT-4, and Whisper to provide interactive language learning experiences. The project supports multiple interfaces (web, CLI, and programmatic) and focuses on conversational AI tutoring.

### Key Technologies
- **Python 3.8+**: Core programming language
- **Streamlit**: Web interface framework
- **LangChain**: AI orchestration and conversation management
- **OpenAI API**: GPT-4 for tutoring, Whisper for speech recognition
- **SQLite**: Progress tracking and data persistence
- **pytest/unittest**: Testing frameworks

## Development Workflow

### Initial Setup

1. **Fork and Clone**
   ```bash
   git fork https://github.com/andyLaurito92/language-tutor
   git clone https://github.com/YOUR_USERNAME/language-tutor
   cd language-tutor
   ```

2. **Environment Setup**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Verify Installation**
   ```bash
   # Run setup validation
   python scripts/validate_setup.py
   
   # Test basic functionality
   python cli_tutor.py --help
   
   # Run existing tests
   python -m unittest discover -s . -p "test_*.py"
   ```

### Development Process

1. **Before Starting Work**
   - Check existing issues and discussions
   - Create or assign yourself to an issue
   - Understand the scope and requirements
   - Plan your approach and identify affected components

2. **During Development**
   - Make frequent, small commits with descriptive messages
   - Run tests regularly to catch regressions early
   - Update documentation as you make changes
   - Follow the established code style and patterns

3. **Before Submitting**
   - Run full test suite
   - Check code style with linting tools
   - Update relevant documentation
   - Test the application manually
   - Ensure no sensitive data is committed

## Branch Naming Conventions

**❌ Avoid Generic Names:**
- `fix-1`, `fix-2`, `patch`
- `copilot/fix-8`, `temp-branch`
- `test`, `dev`, `new-feature`

**✅ Use Descriptive Names:**

### Format: `<type>/<descriptive-name>`

#### Types:
- **`feature/`** - New functionality
- **`bugfix/`** - Bug fixes
- **`docs/`** - Documentation updates
- **`refactor/`** - Code refactoring
- **`test/`** - Adding or improving tests
- **`chore/`** - Maintenance tasks
- **`hotfix/`** - Critical production fixes

#### Examples:
```bash
# Feature development
feature/add-voice-recognition-support
feature/implement-progress-analytics
feature/catalan-language-support

# Bug fixes
bugfix/audio-playback-stuttering
bugfix/memory-leak-in-conversation-handler
bugfix/api-rate-limit-handling

# Documentation
docs/update-installation-guide
docs/add-api-reference
docs/improve-contributing-guidelines

# Refactoring
refactor/ai-tutor-class-structure
refactor/database-connection-pooling
refactor/streamlit-component-organization

# Testing
test/add-integration-tests-for-speech
test/improve-ai-tutor-unit-coverage

# Chores
chore/update-dependencies
chore/cleanup-unused-imports
chore/add-pre-commit-hooks
```

### Branch Naming Best Practices:
- Use lowercase letters and hyphens (kebab-case)
- Be specific about what the branch does
- Include the component or area if relevant
- Keep names under 50 characters when possible
- Use present tense verbs (`add`, `fix`, `update`, `implement`)

## Code Style and Standards

### Python Code Style

Follow **PEP 8** guidelines with these specific requirements:

```python
# Use type hints for function parameters and return values
def process_audio_input(audio_data: bytes, language: str = "en") -> dict[str, Any]:
    """Process audio input and return transcription result."""
    pass

# Use descriptive variable names
user_input_text = "Hello, how are you?"
ai_response_data = tutor.generate_response(user_input_text)

# Use docstrings for all public functions and classes
class AITutor:
    """
    Main AI tutoring class that handles student interactions.
    
    This class manages conversation flow, generates responses,
    and tracks learning progress using OpenAI's GPT-4.
    """
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate AI tutor response to student input.
        
        Args:
            user_input: The student's input text or transcribed speech
            
        Returns:
            AI-generated response text
            
        Raises:
            OpenAIError: If API call fails
            ValueError: If input is empty or invalid
        """
        pass
```

### Code Organization Principles

1. **Single Responsibility**: Each function/class should have one clear purpose
2. **DRY (Don't Repeat Yourself)**: Extract common functionality into reusable components
3. **Dependency Injection**: Pass dependencies as parameters rather than hardcoding
4. **Error Handling**: Use proper exception handling with specific error types
5. **Logging**: Use Python's logging module for debugging and monitoring

### Import Organization

```python
# Standard library imports
import os
import sys
from typing import Dict, List, Optional, Any

# Third-party imports
import streamlit as st
from langchain.llms import OpenAI
from openai import OpenAI as OpenAIClient

# Local imports
from src.tutor.ai_tutor import AITutor
from src.utils.config import Config
from src.utils.database import ProgressTracker
```

## File Organization

### Directory Structure
```
language-tutor/
├── app.py                      # Main Streamlit application
├── cli_tutor.py               # Command-line interface
├── copilot-instructions.md    # This file
├── src/
│   ├── tutor/                 # Core tutoring logic
│   │   ├── __init__.py
│   │   ├── ai_tutor.py        # Main AI tutor class
│   │   ├── speech.py          # Speech recognition/synthesis
│   │   └── lessons.py         # Lesson management
│   ├── utils/                 # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   └── database.py        # Data persistence
│   └── __init__.py
├── data/                      # Data files and storage
│   ├── lessons/              # Lesson content
│   └── progress.db           # SQLite database
├── docs/                     # Documentation
│   ├── TECHNICAL_DOCS.md
│   ├── CONDA_SETUP.md
│   └── OLLAMA_SETUP.md
├── features/                 # Feature-specific code
│   └── 3d-tutor/            # 3D tutor feature
├── scripts/                  # Setup and utility scripts
│   ├── setup.sh
│   ├── setup.bat
│   ├── validate_setup.py
│   └── test_environment.py
├── test_*.py                 # Test files (root level)
├── requirements.txt          # Dependencies
├── requirements_no_audio.txt # Audio-free dependencies
├── .env.example             # Environment template
└── README.md                # Main documentation
```

### File Naming Conventions

- **Python modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase` (e.g., `AITutor`, `SpeechHandler`)
- **Functions/variables**: `snake_case` (e.g., `process_user_input`, `current_language`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_LANGUAGE`, `MAX_CONVERSATION_LENGTH`)
- **Test files**: `test_<module_name>.py` (e.g., `test_ai_tutor.py`)

### Where to Put New Code

| Type of Code | Location | Example |
|--------------|----------|---------|
| New AI features | `src/tutor/` | Speech emotion detection |
| Utility functions | `src/utils/` | Text preprocessing, file handlers |
| UI components | Root level or `src/ui/` | New Streamlit components |
| Data models | `src/models/` | Student profile, lesson structure |
| Tests | Root level | `test_new_feature.py` |
| Documentation | `docs/` | Feature-specific docs |
| Scripts | `scripts/` | Setup, deployment, maintenance |

## Testing Guidelines

### Test Structure

```python
#!/usr/bin/env python3
"""
Test module for AI tutor functionality.

This module tests the core AI tutoring features including
response generation, conversation memory, and error handling.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.tutor.ai_tutor import AITutor

class TestAITutor(unittest.TestCase):
    """Test cases for AITutor class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tutor = AITutor(language="English", difficulty="Beginner")
    
    def test_response_generation(self):
        """Test that AI tutor generates appropriate responses."""
        with patch('openai.OpenAI') as mock_openai:
            # Configure mock
            mock_response = Mock()
            mock_response.choices[0].message.content = "Hello! How can I help you learn today?"
            mock_openai.return_value.chat.completions.create.return_value = mock_response
            
            # Test
            response = self.tutor.generate_response("Hello")
            
            # Assertions
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            self.assertIn("help", response.lower())
    
    def tearDown(self):
        """Clean up after each test method."""
        pass

if __name__ == '__main__':
    unittest.main()
```

### Testing Best Practices

1. **Test Organization**
   - Group related tests in the same test class
   - Use descriptive test method names
   - Include docstrings explaining what each test validates

2. **Test Coverage**
   - Test happy path (normal functionality)
   - Test edge cases (empty inputs, boundary values)
   - Test error conditions (invalid inputs, API failures)
   - Test integration points between components

3. **Mocking External Dependencies**
   - Mock OpenAI API calls to avoid costs and rate limits
   - Mock file system operations for consistent testing
   - Mock database operations for faster tests

4. **Test Data**
   - Use representative but minimal test data
   - Store test data in separate files if needed
   - Clean up test data after tests complete

### Running Tests

```bash
# Run all tests
python -m unittest discover -s . -p "test_*.py" -v

# Run specific test file
python test_ai_tutor.py

# Run with coverage (if installed)
python -m coverage run -m unittest discover
python -m coverage report
```

## Documentation Standards

### Code Documentation

1. **Docstrings**: Use Google-style docstrings
```python
def generate_lesson_content(language: str, difficulty: str, topic: str) -> dict:
    """
    Generate dynamic lesson content for specified parameters.
    
    This function creates personalized lesson content based on the student's
    language choice, difficulty level, and preferred topic area.
    
    Args:
        language: Target language for learning (e.g., "Spanish", "French")
        difficulty: Student's proficiency level ("Beginner", "Intermediate", "Advanced")
        topic: Lesson topic area (e.g., "Travel", "Business", "Conversation")
    
    Returns:
        Dictionary containing lesson structure with keys:
        - title: Lesson title
        - content: Main lesson content
        - exercises: List of practice exercises
        - vocabulary: Key vocabulary items
    
    Raises:
        ValueError: If language is not supported
        LessonGenerationError: If content generation fails
    
    Example:
        >>> lesson = generate_lesson_content("Spanish", "Beginner", "Travel")
        >>> print(lesson["title"])
        "Basic Travel Phrases in Spanish"
    """
```

2. **Inline Comments**: Use sparingly for complex logic
```python
# Calculate confidence score based on response time and accuracy
# Using weighted average: 70% accuracy, 30% response time
confidence = (accuracy_score * 0.7) + (time_score * 0.3)
```

### README Updates

When adding new features, update the main README.md:
- Add feature to the feature list
- Update setup instructions if needed
- Include usage examples
- Update project structure if files are added

### Feature Documentation

For significant features, create dedicated documentation:
- `docs/FEATURE_NAME.md` for detailed feature docs
- Include architecture diagrams if helpful
- Provide API reference for programmatic usage
- Include troubleshooting section

## Pull Request Guidelines

### Before Creating a PR

1. **Self-Review Checklist**
   - [ ] Code follows style guidelines
   - [ ] All tests pass
   - [ ] New functionality has tests
   - [ ] Documentation is updated
   - [ ] No sensitive data committed
   - [ ] Changes are minimal and focused
   
2. **Testing Checklist**
   - [ ] Manual testing of affected features
   - [ ] Cross-platform compatibility (if applicable)
   - [ ] Performance impact considered
   - [ ] Error handling tested

### PR Description Template

```markdown
## Description
Brief description of changes and why they were made.

## Changes Made
- [ ] Added feature X to component Y
- [ ] Fixed bug in Z functionality  
- [ ] Updated documentation for ABC
- [ ] Added tests for new functionality

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for changes
- [ ] Manually tested affected functionality
- [ ] Verified no regressions introduced

## Screenshots/Demo
(Include screenshots for UI changes or demo output for CLI changes)

## Related Issue
Fixes #123

## Additional Notes
Any additional context, considerations, or follow-up items.
```

### PR Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one approving review required
3. **Testing**: Reviewer should test functionality when possible
4. **Documentation**: Ensure docs are updated and accurate

## Issue Management

### Creating Issues

Use these issue templates based on the type:

#### Bug Report
```markdown
## Bug Description
Clear description of the bug and its impact.

## Steps to Reproduce
1. Go to...
2. Click on...
3. See error...

## Expected Behavior
What should happen instead.

## Environment
- OS: [e.g., macOS, Windows, Linux]
- Python version: [e.g., 3.9.2]
- App version/commit: [e.g., main branch, v1.2.3]

## Error Messages
```
Paste any error messages or logs here
```

## Additional Context
Screenshots, videos, or other relevant information.
```

#### Feature Request
```markdown
## Feature Summary
Brief description of the proposed feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
Detailed description of how the feature should work.

## Alternatives Considered
Other approaches that were considered.

## Additional Context
Mockups, examples, or related issues.
```

### Working on Issues

1. **Assign Yourself**: Comment on the issue to claim it
2. **Ask Questions**: Clarify requirements before starting
3. **Break Down Large Issues**: Create sub-tasks if needed
4. **Update Progress**: Comment on progress and blockers
5. **Link PRs**: Reference the issue in your PR

## Security Considerations

### API Key Management

1. **Never Commit API Keys**
   ```bash
   # ❌ WRONG - Never do this
   OPENAI_API_KEY="sk-abcd1234..."
   
   # ✅ CORRECT - Use environment variables
   OPENAI_API_KEY=your_key_here  # in .env file (git-ignored)
   ```

2. **Environment Variables**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   if not api_key:
       raise ValueError("OPENAI_API_KEY environment variable is required")
   ```

3. **Key Rotation**: Regularly rotate API keys and update documentation

### Input Validation

```python
def validate_user_input(user_input: str) -> str:
    """Validate and sanitize user input."""
    if not user_input or not user_input.strip():
        raise ValueError("Input cannot be empty")
    
    # Remove potentially harmful characters
    sanitized = user_input.strip()[:1000]  # Limit length
    
    # Add additional validation as needed
    return sanitized
```

### Data Privacy

1. **User Data**: Don't log or store sensitive user conversations
2. **API Calls**: Be mindful of data sent to external APIs
3. **Local Storage**: Encrypt sensitive data in local database
4. **Audit Trail**: Log access to sensitive operations

## Build and Deployment

### Local Development

```bash
# Development server with hot reloading
streamlit run app.py --server.fileWatcherType poll

# CLI development
python cli_tutor.py --debug --language Spanish
```

### Environment Setup

1. **Development Environment**
   - Use virtual environments for isolation
   - Install all dependencies including dev tools
   - Enable debug logging and verbose output

2. **Production Environment**
   - Use production-grade WSGI server
   - Set appropriate logging levels
   - Configure proper error handling
   - Set resource limits and timeouts

### Dependencies

```bash
# Add new dependencies
pip install new-package
pip freeze > requirements.txt

# Or for audio-free installations
pip freeze > requirements_no_audio.txt
```

### Configuration Management

```python
# config.py
class Config:
    """Centralized configuration management."""
    
    # Development settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    
    # Application settings
    SUPPORTED_LANGUAGES = ["English", "Spanish", "French", "German", "Italian"]
    DEFAULT_LANGUAGE = "English"
    
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
```

## Troubleshooting

### Common Development Issues

1. **Import Errors**
   ```bash
   # Fix Python path issues
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   
   # Or add to your script
   sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
   ```

2. **OpenAI API Issues**
   ```python
   # Test API connectivity
   python -c "
   import openai
   client = openai.OpenAI()
   try:
       response = client.chat.completions.create(
           model='gpt-3.5-turbo',
           messages=[{'role': 'user', 'content': 'test'}],
           max_tokens=5
       )
       print('API working!')
   except Exception as e:
       print(f'API error: {e}')
   "
   ```

3. **Audio Issues**
   ```bash
   # Test microphone
   python -c "
   import speech_recognition as sr
   r = sr.Recognizer()
   with sr.Microphone() as source:
       print('Say something!')
       audio = r.listen(source, timeout=5)
   print('Audio captured successfully!')
   "
   ```

### Getting Help

1. **Check Documentation**: README, technical docs, and this file
2. **Search Issues**: Look for similar problems in GitHub issues
3. **Create Detailed Issues**: Include environment info and error messages
4. **Community Discussion**: Use GitHub Discussions for questions

### Debug Mode

Enable comprehensive debugging:
```bash
export DEBUG=1
export LOG_LEVEL=DEBUG
python app.py
```

## Contributing Workflow Summary

1. **Setup**: Fork → Clone → Install dependencies → Verify setup
2. **Plan**: Create/claim issue → Choose descriptive branch name → Plan approach
3. **Develop**: Code → Test → Document → Review → Commit
4. **Submit**: Create PR → Address feedback → Merge
5. **Cleanup**: Delete branch → Update local repo

## Questions or Suggestions?

If you have questions about these guidelines or suggestions for improvements, please:
- Open a GitHub issue with the label `documentation`
- Start a discussion in GitHub Discussions
- Reach out to the maintainers

Thank you for contributing to the AI Language Tutor project! 🎓🤖