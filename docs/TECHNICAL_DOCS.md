# AI Language Tutor - Technical Documentation

## Overview

The AI Language Tutor is a comprehensive language learning application that combines:
- **LangChain**: For conversation management and AI orchestration
- **OpenAI GPT-4**: For intelligent tutoring responses and feedback
- **OpenAI Whisper**: For speech-to-text transcription
- **Streamlit**: For the web interface
- **SQLite**: For progress tracking and data persistence

## Architecture

### Core Components

1. **AITutor** (`src/tutor/ai_tutor.py`)
   - Main AI tutoring logic using LangChain and GPT-4
   - Conversation management with memory
   - Student input analysis and feedback generation
   - Adaptive responses based on difficulty level

2. **SpeechHandler** (`src/tutor/speech.py`)
   - Speech recognition using OpenAI Whisper
   - Text-to-speech using OpenAI TTS
   - Audio processing and streaming

3. **LessonManager** (`src/tutor/lessons.py`)
   - Lesson content management
   - Dynamic lesson creation
   - Topic and difficulty organization

4. **ProgressTracker** (`src/utils/database.py`)
   - SQLite database for progress tracking
   - Session management
   - Performance analytics

5. **Configuration** (`src/utils/config.py`)
   - Centralized configuration management
   - Environment variable handling
   - Supported languages and settings

### User Interfaces

1. **Streamlit Web App** (`app.py`)
   - Full-featured web interface
   - Voice input/output support
   - Real-time conversation
   - Progress visualization

2. **Command Line Interface** (`cli_tutor.py`)
   - Simple text-based interface
   - Good for testing and development
   - All core features without audio

3. **Jupyter Notebook** (`example_usage.ipynb`)
   - Programmatic usage examples
   - Component testing
   - Educational demonstrations

## Features

### Language Learning
- **Multi-language Support**: Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, English
- **Difficulty Levels**: Beginner, Intermediate, Advanced
- **Lesson Types**: Conversation Practice, Grammar Lessons, Vocabulary Building, Pronunciation Practice, Reading Comprehension, Writing Practice

### AI Capabilities
- **Adaptive Responses**: Adjusts language complexity based on student level
- **Real-time Feedback**: Grammar, vocabulary, and pronunciation analysis
- **Personalized Learning**: Tracks progress and adapts to individual needs
- **Error Correction**: Gentle, constructive feedback with explanations

### Technical Features
- **Voice Recognition**: High-quality speech-to-text using Whisper
- **Speech Synthesis**: Natural text-to-speech responses
- **Conversation Memory**: Maintains context across interactions
- **Progress Analytics**: Detailed tracking and visualization
- **Exercise Generation**: Dynamic practice exercises

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Microphone (for voice features)

### Quick Setup

#### macOS/Linux
```bash
git clone <repository-url>
cd language-tutor
chmod +x scripts/setup.sh
./scripts/setup.sh
```

#### Windows
```cmd
git clone <repository-url>
cd language-tutor
scripts\setup.bat
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Web Interface
```bash
streamlit run app.py
```

### Command Line Interface
```bash
python cli_tutor.py
```

### Programmatic Usage
See `example_usage.ipynb` for detailed examples.

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization
- Add new languages in `Config.SUPPORTED_LANGUAGES`
- Create custom lessons in `data/lessons/`
- Modify AI prompts in `AITutor` class
- Adjust difficulty parameters

## Data Storage

### Database Schema
- **sessions**: Learning session records
- **interactions**: Individual conversation exchanges
- **progress_metrics**: Performance tracking data

### File Structure
```
data/
├── lessons/
│   ├── conversation_lessons.json
│   ├── grammar_lessons.json
│   └── vocabulary_lessons.json
└── progress.db
```

## Development

### Adding New Languages
1. Add language to `Config.SUPPORTED_LANGUAGES`
2. Create language-specific lesson content
3. Test with different difficulty levels

### Creating Custom Lessons
```python
lesson_manager = LessonManager()
lesson_data = {
    "id": "custom_lesson_1",
    "title": "Custom Lesson",
    "description": "Description here",
    "topics": ["topic1", "topic2"],
    "vocabulary": ["word1", "word2"]
}
lesson_manager.create_custom_lesson("conversation", "beginner", lesson_data)
```

### Extending AI Capabilities
- Modify system prompts in `AITutor.get_system_prompt()`
- Add new feedback metrics in `_analyze_student_input()`
- Create specialized exercise types

## Performance Considerations

### Optimization Tips
- Use conversation memory limits to control token usage
- Implement caching for repeated API calls
- Batch database operations for better performance
- Consider streaming responses for real-time feel

### Monitoring
- Track API usage and costs
- Monitor response times
- Log errors and performance metrics

## Security

### Best Practices
- Keep API keys secure and never commit them
- Validate user inputs before processing
- Implement rate limiting for API calls
- Use HTTPS in production deployments

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`

2. **OpenAI API Errors**
   - Check API key is set correctly
   - Verify API quota and billing
   - Test with simple API call

3. **Audio Issues**
   - Check microphone permissions
   - Install pyaudio dependencies
   - Test audio recording separately

4. **Database Errors**
   - Ensure data directory exists
   - Check file permissions
   - Verify SQLite installation

### Debug Mode
Enable verbose logging by setting environment variable:
```bash
export DEBUG=1
```

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install development dependencies
4. Run tests before submitting PR

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Document functions and classes
- Write unit tests for new features

## License

MIT License - see LICENSE file for details.

## Support

- Check documentation and examples first
- Search existing issues on GitHub
- Create detailed bug reports with reproduction steps
- Join community discussions

## Roadmap

### Planned Features
- [ ] Additional language support
- [ ] Mobile app version
- [ ] Advanced pronunciation analysis
- [ ] Gamification features
- [ ] Multi-user support
- [ ] Integration with external content
- [ ] Offline mode capabilities
- [ ] Performance analytics dashboard
