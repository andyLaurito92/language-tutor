# Conda Envir- ✅ **LangChain** suite (0.2.14) - AI orchestration framework
  - LangChain-Core (0.2.43) - Core functionality
  - LangChain-OpenAI (0.1.20) - OpenAI integration
  - LangChain-Community (0.2.12) - Community integrations
  - LangChain-Text-Splitters (0.2.4) - Text processing
- ✅ **Streamlit** (1.37.0) - Web interfacent Setup Guide

## Environment Successfully Created! ✅

Your AI Language Tutor conda environment has been successfully created with all dependencies installed.

### Environment Details
- **Environment Name**: `language-tutor`
- **Python Version**: 3.11.5
- **Location**: `/opt/homebrew/anaconda3/envs/language-tutor`

### Installed Packages
- ✅ **OpenAI** (1.40.0) - GPT-4 and Whisper API
- ✅ **LangChain** (0.2.14) - AI orchestration framework
- ✅ **LangChain-OpenAI** (0.1.20) - OpenAI integration
- ✅ **LangChain-Community** (0.2.12) - Community integrations
- ✅ **Streamlit** (1.37.0) - Web interface
- ✅ **PyAudio** (0.2.14) - Audio input/output
- ✅ **SpeechRecognition** (3.10.4) - Speech processing
- ✅ **PyDub** (0.25.1) - Audio processing
- ✅ **IPython & Jupyter Kernel** - For notebook support in VS Code
- ✅ **NumPy**, **Pandas**, **Matplotlib**, **Seaborn** - Data processing
- ✅ **python-dotenv** (1.0.1) - Environment variables

## Quick Start

### 1. Activate the Environment
```bash
# Option 1: Use the activation script (recommended)
./activate_env.sh

# Option 2: Manual activation
export PATH="/opt/homebrew/anaconda3/bin:$PATH"
source /opt/homebrew/anaconda3/etc/profile.d/conda.sh
conda activate language-tutor
```

### 2. Set up Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit with your OpenAI API key
nano .env  # or use your preferred editor
```

### 3. Run the Application
```bash
# Web interface (recommended)
streamlit run app.py

# Command line interface
python cli_tutor.py

# Jupyter notebook examples
jupyter notebook example_usage.ipynb
```

## VS Code Integration

### Method 1: Conda Integration (Recommended)
1. Open VS Code in your project folder
2. Press `Cmd+Shift+P` (macOS) to open command palette
3. Type "Python: Select Interpreter"
4. Choose the conda environment: `/opt/homebrew/anaconda3/envs/language-tutor/bin/python`

### Method 2: Jupyter Kernel Selection
1. Open the notebook `example_usage.ipynb` in VS Code
2. Click on the kernel selector in the top-right corner
3. Select "Language Tutor (Python 3.10.18)" from the list
4. The notebook should now use the correct conda environment

### Method 3: Terminal Integration
1. Open VS Code terminal
2. Run: `source activate_env.sh`
3. The environment will be activated in the terminal

### Method 4: Fix conda in VS Code terminal permanently
Add this to your VS Code settings.json:
```json
{
    "terminal.integrated.env.osx": {
        "PATH": "/opt/homebrew/anaconda3/bin:${env:PATH}"
    },
    "terminal.integrated.shellArgs.osx": [
        "-c",
        "source /opt/homebrew/anaconda3/etc/profile.d/conda.sh && exec zsh"
    ]
}
```

## Troubleshooting

### Conda not found in VS Code terminal
If you get "conda: command not found" in VS Code:

1. **Temporary fix** (current session only):
   ```bash
   export PATH="/opt/homebrew/anaconda3/bin:$PATH"
   source /opt/homebrew/anaconda3/etc/profile.d/conda.sh
   conda activate language-tutor
   ```

2. **Permanent fix** - Add to your `.zshrc`:
   ```bash
   echo 'export PATH="/opt/homebrew/anaconda3/bin:$PATH"' >> ~/.zshrc
   /opt/homebrew/anaconda3/bin/conda init zsh
   source ~/.zshrc
   ```

3. **VS Code specific fix** - Use the activation script:
   ```bash
   ./activate_env.sh
   ```

### PyAudio Issues
If you encounter PyAudio issues:
```bash
# Reinstall PortAudio
brew reinstall portaudio

# Reinstall PyAudio in the conda environment
conda activate language-tutor
pip uninstall pyaudio
pip install pyaudio
```

### OpenAI API Key Issues
1. Make sure your `.env` file exists and contains:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
2. Verify the key is loaded:
   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv()
   print(os.getenv('OPENAI_API_KEY'))  # Should not be None
   ```

## Environment Management

### Deactivate Environment
```bash
conda deactivate
```

### Update Packages
```bash
conda activate language-tutor
pip install --upgrade -r requirements.txt
```

### Remove Environment (if needed)
```bash
conda env remove -n language-tutor
```

### List All Environments
```bash
conda env list
```

## Next Steps

1. ✅ **Environment Created**
2. 🔑 **Set up your OpenAI API key in `.env`**
3. 🚀 **Run the application using one of the methods above**
4. 📚 **Explore the example notebook for usage examples**
5. 🎯 **Start learning languages with your AI tutor!**

## Support

If you encounter any issues:
1. Check this troubleshooting guide first
2. Ensure your OpenAI API key is valid and has credits
3. Verify microphone permissions for voice features
4. Check the technical documentation for detailed usage

Happy learning! 🎓📚
