# AI Language Tutor

An intelligent language tutoring application that combines LangChain, GPT-4, and Whisper to provide interactive language learning experiences.

## Features

- **Voice Recognition**: Use Whisper for speech-to-text conversion
- **AI Tutoring**: GPT-4 powered conversational tutor
- **Interactive Lessons**: Structured learning modules
- **Progress Tracking**: Monitor learning progress
- **Multiple Languages**: Support for various languages
- **Web Interface**: User-friendly Streamlit interface

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd language-tutor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

4. Run the application:
```bash
streamlit run app.py
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4 and Whisper access

## Usage

1. Launch the application
2. Select your target language
3. Choose a lesson type (conversation, grammar, vocabulary)
4. Interact with the AI tutor through text or voice
5. Track your progress over time

## Project Structure

```
language-tutor/
├── app.py                 # Main Streamlit application
├── cli_tutor.py          # Command-line interface
├── src/
│   ├── tutor/
│   │   ├── __init__.py
│   │   ├── ai_tutor.py    # Core AI tutor logic
│   │   ├── speech.py      # Speech recognition and synthesis
│   │   └── lessons.py     # Lesson management
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py      # Configuration management
│   │   └── database.py    # Progress tracking
│   └── __init__.py
├── data/
│   └── lessons/          # Lesson content
├── docs/                 # Documentation
│   ├── CONDA_SETUP.md    # Conda environment setup
│   ├── OLLAMA_SETUP.md   # Ollama model setup
│   └── TECHNICAL_DOCS.md # Technical documentation
├── scripts/              # Setup and utility scripts
│   ├── setup.sh          # Linux setup script
│   ├── setup.bat         # Windows setup script
│   ├── validate_setup.py # Setup validation
│   └── test_environment.py # Environment testing
├── requirements.txt
└── README.md
```

## Development

### Quick Development Setup

```bash
# Setup development environment with quality tools
make setup-dev

# Run all quality checks
make quality-check

# Format code before committing
make format
```

### Code Quality Standards

This project enforces high code quality standards using:

- **Black**: Automatic code formatting
- **isort**: Import organization
- **flake8**: PEP 8 compliance and error checking
- **pylint**: Advanced code analysis (minimum score: 8.0/10)
- **mypy**: Static type checking
- **bandit**: Security vulnerability scanning
- **safety**: Dependency vulnerability checking
- **SonarQube**: Comprehensive code quality analysis (optional)

### Development Workflow

1. **Setup**: `make setup-dev`
2. **Make changes**: Follow branch naming conventions (`feature/description`)
3. **Quality checks**: `make quality-check`
4. **Commit**: Pre-commit hooks run automatically
5. **Pull request**: Must pass all CI checks and code review

See [Code Quality Documentation](docs/CODE_QUALITY.md) for detailed information.

### Available Commands

```bash
make help           # Show all available commands
make install        # Install production dependencies
make install-dev    # Install development dependencies
make format         # Format code with Black and isort
make lint           # Run linting (flake8, pylint)
make type-check     # Run type checking (mypy)
make test          # Run tests with coverage
make security      # Run security checks
make clean         # Clean temporary files
```

## License

MIT License
