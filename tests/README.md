# Language Tutor Test Suite

This document describes the comprehensive test suite for the language-tutor project.

## Test Structure

The test suite is organized into two main categories:

### Unit Tests (`tests/unit/`)
- **test_config_simple.py**: Tests for configuration module (6 tests)
- **test_database.py**: Tests for database/progress tracking (12 tests)
- **test_ai_tutor.py**: Tests for AI tutor core functionality (6 tests)
- **test_lessons.py**: Tests for lesson management (6 tests)
- **test_speech.py**: Tests for speech recognition/TTS (8 tests)

### Integration Tests (`tests/integration/`)
- **test_system_integration.py**: Tests for component interaction (5 tests)
- **test_main_applications.py**: Tests for main application files (7 tests)

## Test Coverage

### Core Modules Tested
1. **Configuration Management** (`src/utils/config.py`)
   - Language support validation (including Catalan)
   - Lesson types and difficulty levels
   - Model provider configuration
   - Environment variable handling

2. **Database Operations** (`src/utils/database.py`)
   - Session management
   - Progress tracking
   - User interaction logging
   - Data persistence and retrieval

3. **AI Tutor Functionality** (`src/tutor/ai_tutor.py`)
   - Model initialization
   - Configuration handling
   - Context management
   - Provider compatibility

4. **Lesson Management** (`src/tutor/lessons.py`)
   - Lesson structure creation
   - Directory management
   - Content organization

5. **Speech Handling** (`src/tutor/speech.py`)
   - Speech recognition setup
   - Provider configuration
   - Audio input handling

### System Integration Testing
- Component interaction validation
- Configuration consistency across modules
- Database and lesson management integration
- Full system simulation with Catalan support

## Running Tests

### Prerequisites
```bash
pip install pytest pytest-mock
```

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests only
python -m pytest tests/integration/ -v

# Specific module tests
python -m pytest tests/unit/test_database.py -v
```

### Test Configuration
Tests are configured via `pytest.ini`:
- Verbose output enabled
- Short tracebacks for easier debugging
- Warning filters for cleaner output

## Test Results Summary

**Current Status**: 47 PASSED, 3 FAILED

### Passing Tests (47)
- ✅ All unit tests for core modules
- ✅ System integration tests
- ✅ Configuration validation
- ✅ Database operations
- ✅ Component interaction

### Known Issues (3)
- Import resolution issues in some integration tests for main applications
- These are non-critical and related to test environment setup

## Test Features

### Mocking Strategy
- Heavy dependencies (langchain, streamlit, speech_recognition) are mocked
- External services (OpenAI, Ollama) are mocked for reliable testing
- File system operations use temporary directories

### Fixtures
- `temp_dir`: Provides isolated temporary directories
- `mock_database_path`: Creates temporary database paths
- `sample_config`: Provides test configuration data
- `sample_user_data`: Provides test user information

### Validation Areas
1. **Data Integrity**: Database schema validation and data consistency
2. **Configuration**: Settings validation and provider compatibility  
3. **Language Support**: Catalan integration and multilingual features
4. **Component Integration**: Module interaction and data flow
5. **Error Handling**: Exception handling and edge cases

## Continuous Integration

The test suite is designed to run in CI/CD environments:
- No external dependencies required
- Comprehensive mocking of third-party services
- Fast execution time
- Clear pass/fail reporting

## Future Enhancements

1. **Coverage Reporting**: Add code coverage metrics
2. **Performance Tests**: Add benchmarking for database operations
3. **End-to-End Tests**: Browser automation for Streamlit UI
4. **Load Testing**: Test system under concurrent user load
5. **Security Tests**: Validate input sanitization and data protection

## Contributing to Tests

When adding new functionality:
1. Add corresponding unit tests in `tests/unit/`
2. Add integration tests if components interact
3. Mock external dependencies appropriately
4. Follow existing naming conventions
5. Ensure tests are isolated and reproducible