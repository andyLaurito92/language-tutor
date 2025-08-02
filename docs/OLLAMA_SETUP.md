# Ollama Setup Guide for AI Language Tutor

## What is Ollama?

Ollama allows you to run large language models locally on your machine, providing:
- **Privacy**: Your conversations stay completely local
- **No API costs**: Free to use once set up
- **Offline capability**: Works without internet connection
- **Control**: Choose from many open-source models

## Installation

### 1. Install Ollama

**macOS:**
```bash
# Download and install from https://ollama.ai
# Or use Homebrew:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai

### 2. Start Ollama Service

```bash
# Start the Ollama service
ollama serve
```

### 3. Download a Language Model

```bash
# Recommended models for language learning:
ollama pull llama3.2          # Latest version (4.7GB) - RECOMMENDED
ollama pull llama3.1          # Previous version (4.7GB) 
ollama pull llama3.2:70b      # Larger, better quality (39GB)
ollama pull mistral           # Fast and good (4.1GB)
ollama pull gemma             # Google's model (5.0GB)

# Multilingual models:
ollama pull qwen2             # Excellent for multiple languages
ollama pull llama3.2:chinese  # Specialized for Chinese
```

### 4. Test Ollama

```bash
# Test that Ollama is working
ollama run llama3.1
# Type a message and press Enter
# Type /bye to exit
```

## Configuration

### Environment Variables

Update your `.env` file:

```env
# Use Ollama as the model provider
MODEL_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Speech recognition (doesn't require OpenAI)
STT_PROVIDER=google
```

### Model Recommendations

**For Language Learning:**

1. **llama3.1** (Recommended)
   - Size: ~4.7GB
   - Best balance of quality and speed
   - Excellent multilingual capabilities

2. **qwen2**
   - Size: ~4.4GB
   - Exceptional multilingual performance
   - Great for non-English languages

3. **mistral**
   - Size: ~4.1GB
   - Fast responses
   - Good for conversation practice

4. **gemma**
   - Size: ~5.0GB
   - Google's model, good instruction following

## Usage

### Starting the Application

1. **Start Ollama service:**
   ```bash
   ollama serve
   ```

2. **Activate your conda environment:**
   ```bash
   ./activate_env.sh
   ```

3. **Run the application:**
   ```bash
   # Web interface
   streamlit run app.py
   
   # Command line
   python cli_tutor.py
   
   # Jupyter notebook
   jupyter notebook example_usage.ipynb
   ```

## Model Management

### List Available Models
```bash
ollama list
```

### Remove Models
```bash
ollama rm model_name
```

### Update Models
```bash
ollama pull model_name
```

## Performance Tips

1. **Model Size vs Quality:**
   - Smaller models (4GB): Faster, good for basic conversations
   - Larger models (70GB+): Better quality, slower responses

2. **Hardware Requirements:**
   - Minimum: 8GB RAM for 7B models
   - Recommended: 16GB+ RAM for better performance
   - GPU: Optional but significantly faster with NVIDIA GPU

3. **Memory Management:**
   - Ollama keeps models in memory after first use
   - Use `ollama stop model_name` to free memory

## Troubleshooting

### Common Issues

**"Connection refused" errors:**
- Make sure `ollama serve` is running
- Check that port 11434 is available
- Verify OLLAMA_BASE_URL in .env

**Model not found:**
- Run `ollama pull model_name` first
- Check available models with `ollama list`
- Verify model name in .env file

**Slow responses:**
- Try a smaller model (e.g., mistral instead of llama3.1:70b)
- Ensure sufficient RAM available
- Consider using GPU acceleration

**Out of memory:**
- Use smaller models
- Close other applications
- Restart Ollama service

### Performance Comparison

| Model | Size | Speed | Quality | Multilingual |
|-------|------|-------|---------|-------------|
| llama3.1 | 4.7GB | Good | Excellent | Excellent |
| mistral | 4.1GB | Fast | Good | Good |
| qwen2 | 4.4GB | Good | Excellent | Outstanding |
| gemma | 5.0GB | Good | Good | Good |

## Advanced Configuration

### Custom Model Parameters

You can customize model behavior by setting environment variables:

```env
# Model parameters (optional)
OLLAMA_TEMPERATURE=0.7    # Creativity (0.0-1.0)
OLLAMA_TOP_P=0.9         # Nucleus sampling
OLLAMA_TOP_K=40          # Top-k sampling
```

### Multiple Models

You can switch between models by changing the `OLLAMA_MODEL` in your `.env` file:

```env
# For conversation practice
OLLAMA_MODEL=llama3.1

# For grammar correction
OLLAMA_MODEL=qwen2

# For fast responses
OLLAMA_MODEL=mistral
```

## Benefits of Local Models

✅ **Privacy**: All data stays on your device
✅ **Cost**: No API fees after initial setup
✅ **Availability**: Works offline
✅ **Customization**: Fine-tune models for specific needs
✅ **Speed**: No network latency
✅ **Control**: Choose your preferred model

## Getting Help

- **Ollama Documentation**: https://ollama.ai/docs
- **Model Library**: https://ollama.ai/library
- **Community**: https://github.com/ollama/ollama

---

**Ready to start?** Follow the installation steps above, then run the AI Language Tutor with local models!
