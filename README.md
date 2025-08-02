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

## macOS Application

You can also run the AI Language Tutor as a native macOS application:

### Download Pre-built App

1. Go to the [Releases](../../releases) page
2. Download the latest `.dmg` file
3. Open the DMG and drag the app to your Applications folder
4. Launch "AI Language Tutor" from Applications

### Build Your Own

See [BUILD_MACOS.md](BUILD_MACOS.md) for detailed instructions on building the macOS application yourself.

```bash
# Quick build
./build_macos.sh
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
├── launcher.py           # macOS app launcher script
├── build_macos.sh        # macOS app build script
├── ai-language-tutor.spec # PyInstaller configuration
├── BUILD_MACOS.md        # macOS build instructions
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
├── .github/workflows/    # CI/CD workflows
│   └── build-macos.yml   # macOS app build automation
├── requirements.txt
├── requirements_build.txt # Dependencies for building
└── README.md
```

## License

MIT License
